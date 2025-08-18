"""
Kullanıcı Yönetimi API Router
Kullanıcı profil ve premium özellik yönetimi
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user_models import UserUpdate, UserResponse, UserStats
from app.services.user_service import UserService
from app.core.auth import get_current_user
from app.models.user_models import User

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı profil bilgilerini getirir"""
    try:
        user_service = UserService(db)
        user = await user_service.get_user_by_id(current_user.id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_premium=user.is_premium,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profil bilgileri alınamadı: {str(e)}"
        )

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı profil bilgilerini günceller"""
    try:
        user_service = UserService(db)
        
        # Email değişikliği varsa benzersizlik kontrolü
        if user_data.email and user_data.email != current_user.email:
            if await user_service.email_exists(user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bu email adresi zaten kullanılıyor"
                )
        
        # Profili güncelle
        updated_user = await user_service.update_user_profile(current_user.id, user_data)
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Kullanıcı bulunamadı"
            )
        
        return UserResponse(
            id=updated_user.id,
            email=updated_user.email,
            username=updated_user.username,
            is_premium=updated_user.is_premium,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profil güncellenemedi: {str(e)}"
        )

@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı istatistiklerini getirir"""
    try:
        user_service = UserService(db)
        stats = await user_service.get_user_stats(current_user.id)
        
        return stats
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"İstatistikler alınamadı: {str(e)}"
        )

@router.get("/scan-limit")
async def get_scan_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının tarama limitini getirir"""
    try:
        user_service = UserService(db)
        limit_info = await user_service.get_scan_limit_info(current_user.id)
        
        return limit_info
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama limiti bilgisi alınamadı: {str(e)}"
        )

@router.post("/upgrade-premium")
async def upgrade_to_premium(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcıyı premium üyeliğe yükseltir"""
    try:
        user_service = UserService(db)
        
        # Premium üyeliğe yükselt
        success = await user_service.upgrade_to_premium(current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Premium üyeliğe yükseltilemedi"
            )
        
        return {"message": "Premium üyeliğe başarıyla yükseltildiniz"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Premium üyeliğe yükseltilemedi: {str(e)}"
        )

@router.post("/downgrade-free")
async def downgrade_to_free(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcıyı ücretsiz üyeliğe düşürür"""
    try:
        user_service = UserService(db)
        
        # Ücretsiz üyeliğe düşür
        success = await user_service.downgrade_to_free(current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ücretsiz üyeliğe düşürülemedi"
            )
        
        return {"message": "Ücretsiz üyeliğe düşürüldünüz"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ücretsiz üyeliğe düşürülemedi: {str(e)}"
        )

@router.delete("/account")
async def delete_user_account(
    password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcı hesabını siler"""
    try:
        user_service = UserService(db)
        
        # Şifreyi doğrula
        if not await user_service.verify_password(password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Şifre yanlış"
            )
        
        # Hesabı sil
        success = await user_service.delete_user_account(current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Hesap silinemedi"
            )
        
        return {"message": "Hesabınız başarıyla silindi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Hesap silinemedi: {str(e)}"
        )

@router.get("/premium-features")
async def get_premium_features(
    current_user: User = Depends(get_current_user)
):
    """Premium özellikleri listeler"""
    try:
        features = {
            "scan_priority": {
                "name": "Öncelikli Tarama",
                "description": "Taramalarınız premium kullanıcılar için öncelikli olarak işlenir",
                "available": current_user.is_premium
            },
            "detailed_reports": {
                "name": "Detaylı Raporlar",
                "description": "CVE referansları, çözüm önerileri ve detaylı analiz",
                "available": current_user.is_premium
            },
            "monthly_scan_limit": {
                "name": "Aylık Tarama Limiti",
                "description": "100 URL tarama hakkı (ücretsiz: 10 URL)",
                "available": current_user.is_premium,
                "limit": 100 if current_user.is_premium else 10
            },
            "export_formats": {
                "name": "Çoklu Export Formatı",
                "description": "PDF, Excel, JSON formatlarında rapor export",
                "available": current_user.is_premium
            },
            "api_access": {
                "name": "API Erişimi",
                "description": "Programatik erişim için API anahtarları",
                "available": current_user.is_premium
            }
        }
        
        return {
            "is_premium": current_user.is_premium,
            "features": features
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Premium özellikler alınamadı: {str(e)}"
        )

@router.get("/billing-info")
async def get_billing_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının fatura bilgilerini getirir"""
    try:
        if not current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu özellik sadece premium kullanıcılar için mevcuttur"
            )
        
        user_service = UserService(db)
        billing_info = await user_service.get_billing_info(current_user.id)
        
        return billing_info
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fatura bilgileri alınamadı: {str(e)}"
        )

@router.post("/contact-support")
async def contact_support(
    subject: str,
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Destek ekibi ile iletişim kurar"""
    try:
        user_service = UserService(db)
        
        # Destek talebi oluştur
        success = await user_service.create_support_ticket(
            current_user.id, subject, message
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Destek talebi oluşturulamadı"
            )
        
        return {"message": "Destek talebiniz başarıyla oluşturuldu"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Destek talebi oluşturulamadı: {str(e)}"
        )
