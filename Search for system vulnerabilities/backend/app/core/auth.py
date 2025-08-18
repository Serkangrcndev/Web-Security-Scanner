from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.services.auth_service import AuthService
from app.database import User

# HTTP Bearer token security scheme
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    JWT token'dan mevcut kullanıcıyı getir
    Bu fonksiyon tüm korumalı endpoint'lerde kullanılır
    """
    try:
        auth_service = AuthService(db)
        user = await auth_service.get_current_user(credentials.credentials)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Geçersiz kimlik bilgileri",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Mevcut kullanıcının aktif olup olmadığını kontrol et
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hesap aktif değil"
        )
    return current_user

async def get_premium_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Premium kullanıcı kontrolü
    """
    if not current_user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu özellik sadece premium kullanıcılar için mevcuttur"
        )
    return current_user

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Opsiyonel kullanıcı doğrulama
    Token yoksa None döner, token varsa kullanıcıyı doğrular
    """
    if not credentials:
        return None
    
    try:
        auth_service = AuthService(db)
        user = await auth_service.get_current_user(credentials.credentials)
        return user
    except Exception:
        return None

def require_permissions(required_permissions: list):
    """
    Belirli izinleri gerektiren decorator
    """
    def permission_checker(current_user: User = Depends(get_current_active_user)):
        # Burada kullanıcının izinlerini kontrol edebilirsiniz
        # Şimdilik sadece premium kontrolü yapıyoruz
        if "premium" in required_permissions and not current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu işlem için premium üyelik gerekli"
            )
        return current_user
    
    return permission_checker

def require_scan_limit_check():
    """
    Tarama limiti kontrolü için decorator
    """
    def limit_checker(current_user: User = Depends(get_current_active_user)):
        # Burada aylık tarama limitini kontrol edebilirsiniz
        # Şimdilik sadece True döndürüyoruz
        return current_user
    
    return limit_checker

# Kullanım örnekleri:
# @router.get("/protected")
# async def protected_route(current_user: User = Depends(get_current_user)):
#     return {"message": f"Merhaba {current_user.username}"}

# @router.get("/premium-only")
# async def premium_route(current_user: User = Depends(get_premium_user)):
#     return {"message": "Premium özellik"}

# @router.get("/with-permissions")
# async def permission_route(current_user: User = Depends(require_permissions(["premium", "admin"]))):
#     return {"message": "İzinli erişim"}

# @router.get("/optional-auth")
# async def optional_auth_route(current_user: Optional[User] = Depends(get_optional_user)):
#     if current_user:
#         return {"message": f"Merhaba {current_user.username}"}
#     return {"message": "Anonim kullanıcı"}
