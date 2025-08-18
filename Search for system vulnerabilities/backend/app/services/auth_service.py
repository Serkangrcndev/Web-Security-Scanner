from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status

from app.database import User
from app.models.auth_models import UserCreate, UserLogin
from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Şifre doğrulama"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Şifre hash'leme"""
        return pwd_context.hash(password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Access token oluşturma"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, data: dict) -> str:
        """Refresh token oluşturma"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=30)  # 30 gün
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> dict:
        """Token doğrulama"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token süresi dolmuş"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz token"
            )

    async def user_exists(self, email: str) -> bool:
        """Kullanıcı var mı kontrol et"""
        user = self.db.query(User).filter(User.email == email).first()
        return user is not None

    async def username_exists(self, username: str) -> bool:
        """Kullanıcı adı var mı kontrol et"""
        user = self.db.query(User).filter(User.username == username).first()
        return user is not None

    async def create_user(self, user_data: UserCreate) -> User:
        """Yeni kullanıcı oluştur"""
        try:
            # Email ve username kontrolü
            if await self.user_exists(user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bu email adresi zaten kullanılıyor"
                )
            
            if await self.username_exists(user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bu kullanıcı adı zaten kullanılıyor"
                )

            # Yeni kullanıcı oluştur
            hashed_password = self.get_password_hash(user_data.password)
            db_user = User(
                email=user_data.email,
                username=user_data.username,
                hashed_password=hashed_password,
                is_premium=False,
                is_active=True
            )
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return db_user
            
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Kullanıcı oluşturulamadı"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Kullanıcı oluşturulamadı: {str(e)}"
            )

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Kullanıcı kimlik doğrulama"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hesap aktif değil"
            )
        
        return user

    async def login_user(self, user_credentials: UserLogin) -> dict:
        """Kullanıcı girişi"""
        user = await self.authenticate_user(user_credentials.email, user_credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz email veya şifre"
            )

        # Token oluştur
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id), "email": user.email, "username": user.username},
            expires_delta=access_token_expires
        )
        
        refresh_token = self.create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_premium": user.is_premium,
                "is_active": user.is_active,
                "created_at": user.created_at
            }
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """Access token yenileme"""
        try:
            payload = self.verify_token(refresh_token)
            
            # Refresh token tipini kontrol et
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Geçersiz refresh token"
                )
            
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Geçersiz token"
                )
            
            # Kullanıcıyı kontrol et
            user = self.db.query(User).filter(User.id == int(user_id)).first()
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Kullanıcı bulunamadı veya aktif değil"
                )
            
            # Yeni access token oluştur
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = self.create_access_token(
                data={"sub": str(user.id), "email": user.email, "username": user.username},
                expires_delta=access_token_expires
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token süresi dolmuş"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz refresh token"
            )

    async def get_current_user(self, token: str) -> User:
        """Mevcut kullanıcıyı getir"""
        payload = self.verify_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz token"
            )
        
        user = self.db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Kullanıcı bulunamadı"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hesap aktif değil"
            )
        
        return user

    async def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Şifre değiştirme"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        
        # Mevcut şifreyi kontrol et
        if not self.verify_password(current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mevcut şifre yanlış"
            )
        
        # Yeni şifreyi hash'le ve güncelle
        user.hashed_password = self.get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        self.db.commit()
        return True

    async def request_password_reset(self, email: str) -> bool:
        """Şifre sıfırlama isteği"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            # Güvenlik için email bulunamadı hatası verme
            return True
        
        # Burada email gönderme işlemi yapılır
        # Şimdilik sadece True döndürüyoruz
        return True

    async def reset_password(self, token: str, new_password: str) -> bool:
        """Şifre sıfırlama"""
        try:
            # Token'ı doğrula (şifre sıfırlama için özel secret key kullanılabilir)
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id = payload.get("sub")
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Geçersiz token"
                )
            
            user = self.db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # Yeni şifreyi hash'le ve güncelle
            user.hashed_password = self.get_password_hash(new_password)
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            return True
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token süresi dolmuş"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Geçersiz token"
            )

    async def logout_user(self, user_id: int) -> bool:
        """Kullanıcı çıkışı"""
        # Burada token blacklist'e eklenebilir
        # Şimdilik sadece True döndürüyoruz
        return True
