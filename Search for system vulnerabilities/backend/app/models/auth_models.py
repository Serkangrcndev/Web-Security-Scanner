from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """Kullanıcı kayıt modeli"""
    email: EmailStr = Field(..., description="Kullanıcı email adresi")
    username: str = Field(..., min_length=3, max_length=50, description="Kullanıcı adı")
    password: str = Field(..., min_length=8, description="Şifre (en az 8 karakter)")

class UserLogin(BaseModel):
    """Kullanıcı giriş modeli"""
    email: EmailStr = Field(..., description="Kullanıcı email adresi")
    password: str = Field(..., description="Şifre")

class Token(BaseModel):
    """JWT token modeli"""
    access_token: str = Field(..., description="Access token")
    refresh_token: str = Field(..., description="Refresh token")
    token_type: str = Field(default="bearer", description="Token tipi")
    expires_in: int = Field(..., description="Token geçerlilik süresi (saniye)")
    user: 'UserResponse' = Field(..., description="Kullanıcı bilgileri")

class TokenRefresh(BaseModel):
    """Token yenileme modeli"""
    refresh_token: str = Field(..., description="Refresh token")

class PasswordResetRequest(BaseModel):
    """Şifre sıfırlama isteği modeli"""
    email: EmailStr = Field(..., description="Şifre sıfırlanacak email adresi")

class PasswordReset(BaseModel):
    """Şifre sıfırlama modeli"""
    token: str = Field(..., description="Şifre sıfırlama token'ı")
    new_password: str = Field(..., min_length=8, description="Yeni şifre (en az 8 karakter)")

class PasswordChange(BaseModel):
    """Şifre değiştirme modeli"""
    current_password: str = Field(..., description="Mevcut şifre")
    new_password: str = Field(..., min_length=8, description="Yeni şifre (en az 8 karakter)")

class UserResponse(BaseModel):
    """Kullanıcı yanıt modeli"""
    id: int = Field(..., description="Kullanıcı ID")
    email: str = Field(..., description="Email adresi")
    username: str = Field(..., description="Kullanıcı adı")
    is_premium: bool = Field(..., description="Premium üyelik durumu")
    is_active: bool = Field(..., description="Hesap aktif durumu")
    created_at: datetime = Field(..., description="Hesap oluşturma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Son güncelleme tarihi")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Forward references için
Token.model_rebuild()
