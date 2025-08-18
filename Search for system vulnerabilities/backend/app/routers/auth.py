"""
Kimlik Doğrulama API Router
Kullanıcı giriş, kayıt ve token yönetimi
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Optional

from app.database import get_db
from app.models.auth_models import UserCreate, UserLogin, Token, UserResponse
from app.services.auth_service import AuthService
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Yeni kullanıcı kaydı"""
    try:
        auth_service = AuthService(db)
        
        # Kullanıcı zaten var mı kontrol et
        if await auth_service.user_exists(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bu email adresi zaten kullanılıyor"
            )
        
        # Kullanıcı oluştur
        user = await auth_service.create_user(user_data)
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_premium=user.is_premium,
            is_active=user.is_active,
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kullanıcı kaydı oluşturulamadı: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Kullanıcı girişi"""
    try:
        auth_service = AuthService(db)
        
        # Kullanıcıyı doğrula
        user = await auth_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Geçersiz email veya şifre",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Hesap aktif değil"
            )
        
        # Access token oluştur
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            email=user.email,
            username=user.username,
            is_premium=user.is_premium
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Giriş yapılamadı: {str(e)}"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_token: str = Depends(auth_service.get_current_token),
    db: Session = Depends(get_db)
):
    """Access token yeniler"""
    try:
        auth_service = AuthService(db)
        
        # Token'ı yenile
        new_token = await auth_service.refresh_token(current_token)
        
        if not new_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token yenilenemedi"
            )
        
        return new_token
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Token yenilenemedi: {str(e)}"
        )

@router.post("/logout")
async def logout(
    current_token: str = Depends(auth_service.get_current_token),
    db: Session = Depends(get_db)
):
    """Kullanıcı çıkışı"""
    try:
        auth_service = AuthService(db)
        
        # Token'ı geçersiz kıl
        await auth_service.invalidate_token(current_token)
        
        return {"message": "Başarıyla çıkış yapıldı"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Çıkış yapılamadı: {str(e)}"
        )

@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """Şifre sıfırlama isteği"""
    try:
        auth_service = AuthService(db)
        
        # Şifre sıfırlama email'i gönder
        success = await auth_service.send_password_reset_email(email)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bu email adresi bulunamadı"
            )
        
        return {"message": "Şifre sıfırlama email'i gönderildi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Şifre sıfırlama email'i gönderilemedi: {str(e)}"
        )

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Şifre sıfırlama"""
    try:
        auth_service = AuthService(db)
        
        # Şifreyi sıfırla
        success = await auth_service.reset_password(token, new_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Şifre sıfırlanamadı"
            )
        
        return {"message": "Şifre başarıyla sıfırlandı"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Şifre sıfırlanamadı: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Mevcut kullanıcı bilgilerini getirir"""
    try:
        return UserResponse(
            id=current_user.id,
            email=current_user.email,
            username=current_user.username,
            is_premium=current_user.is_premium,
            is_active=current_user.is_active,
            created_at=current_user.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Kullanıcı bilgileri alınamadı: {str(e)}"
        )

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user = Depends(auth_service.get_current_user),
    db: Session = Depends(get_db)
):
    """Şifre değiştirme"""
    try:
        auth_service = AuthService(db)
        
        # Mevcut şifreyi doğrula
        if not await auth_service.verify_password(current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Mevcut şifre yanlış"
            )
        
        # Şifreyi değiştir
        success = await auth_service.change_password(current_user.id, new_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Şifre değiştirilemedi"
            )
        
        return {"message": "Şifre başarıyla değiştirildi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Şifre değiştirilemedi: {str(e)}"
        )
