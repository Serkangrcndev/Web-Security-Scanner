from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import logging

from app.database import User, Scan, Vulnerability
from app.models.user_models import UserUpdate, UserResponse, UserStats
from app.core.config import settings

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """ID'ye göre kullanıcı getir"""
        return self.db.query(User).filter(User.id == user_id).first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Email'e göre kullanıcı getir"""
        return self.db.query(User).filter(User.email == email).first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Username'e göre kullanıcı getir"""
        return self.db.query(User).filter(User.username == username).first()

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        """Kullanıcı bilgilerini güncelle"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # Email değişikliği kontrolü
            if user_data.email and user_data.email != user.email:
                existing_user = await self.get_user_by_email(user_data.email)
                if existing_user and existing_user.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Bu email adresi zaten kullanılıyor"
                    )
                user.email = user_data.email
            
            # Username değişikliği kontrolü
            if user_data.username and user_data.username != user.username:
                existing_user = await self.get_user_by_username(user_data.username)
                if existing_user and existing_user.id != user_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Bu kullanıcı adı zaten kullanılıyor"
                    )
                user.username = user_data.username
            
            # Diğer alanları güncelle
            if user_data.is_premium is not None:
                user.is_premium = user_data.is_premium
            if user_data.is_active is not None:
                user.is_active = user_data.is_active
            
            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"User update failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Kullanıcı güncellenemedi: {str(e)}"
            )

    async def get_user_stats(self, user_id: int) -> UserStats:
        """Kullanıcı istatistiklerini getir"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # Tarama istatistikleri
            total_scans = self.db.query(Scan).filter(Scan.user_id == user_id).count()
            completed_scans = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.status == "completed"
            ).count()
            failed_scans = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.status == "failed"
            ).count()
            running_scans = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.status == "running"
            ).count()
            
            # Güvenlik açığı istatistikleri
            total_vulnerabilities = self.db.query(Vulnerability).join(Scan).filter(
                Scan.user_id == user_id
            ).count()
            
            # Severity bazında sayılar
            severity_counts = self.db.query(
                Vulnerability.severity,
                func.count(Vulnerability.id)
            ).join(Scan).filter(
                Scan.user_id == user_id
            ).group_by(Vulnerability.severity).all()
            
            severity_dict = {severity: count for severity, count in severity_counts}
            
            # Bu ay yapılan tarama sayısı
            start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_scan_count = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.created_at >= start_of_month
            ).count()
            
            # Ortalama tarama süresi
            completed_scans_with_duration = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.status == "completed",
                Scan.started_at.isnot(None),
                Scan.completed_at.isnot(None)
            ).all()
            
            total_duration = 0
            for scan in completed_scans_with_duration:
                duration = (scan.completed_at - scan.started_at).total_seconds()
                total_duration += duration
            
            average_duration = total_duration / len(completed_scans_with_duration) if completed_scans_with_duration else None
            
            # Son tarama tarihi
            last_scan = self.db.query(Scan).filter(
                Scan.user_id == user_id
            ).order_by(desc(Scan.created_at)).first()
            
            last_scan_date = last_scan.created_at if last_scan else None
            
            # Premium özellikler
            premium_features_used = []
            if user.is_premium:
                premium_features_used = [
                    "Detaylı PDF Raporlar",
                    "Excel Raporlar",
                    "Yüksek Tarama Limitleri",
                    "Öncelikli Tarama Kuyruğu"
                ]
            
            return UserStats(
                total_scans=total_scans,
                completed_scans=completed_scans,
                failed_scans=failed_scans,
                running_scans=running_scans,
                total_vulnerabilities=total_vulnerabilities,
                critical_vulnerabilities=severity_dict.get("critical", 0),
                high_vulnerabilities=severity_dict.get("high", 0),
                medium_vulnerabilities=severity_dict.get("medium", 0),
                low_vulnerabilities=severity_dict.get("low", 0),
                monthly_scan_count=monthly_scan_count,
                monthly_scan_limit=settings.PREMIUM_SCAN_LIMIT if user.is_premium else settings.FREE_SCAN_LIMIT,
                premium_features_used=premium_features_used,
                last_scan_date=last_scan_date,
                average_scan_duration=average_duration
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user stats: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Kullanıcı istatistikleri alınamadı: {str(e)}"
            )

    async def upgrade_to_premium(self, user_id: int, plan_type: str = "monthly") -> User:
        """Kullanıcıyı premium'a yükselt"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            if user.is_premium:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Kullanıcı zaten premium üye"
                )
            
            # Burada ödeme işlemi yapılır
            # Şimdilik sadece premium durumunu güncelliyoruz
            user.is_premium = True
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User {user_id} upgraded to premium")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Premium upgrade failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Premium yükseltme başarısız: {str(e)}"
            )

    async def downgrade_from_premium(self, user_id: int) -> User:
        """Kullanıcıyı premium'dan düşür"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            if not user.is_premium:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Kullanıcı zaten premium değil"
                )
            
            user.is_premium = False
            user.updated_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"User {user_id} downgraded from premium")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Premium downgrade failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Premium düşürme başarısız: {str(e)}"
            )

    async def delete_user(self, user_id: int) -> bool:
        """Kullanıcıyı sil"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # İlişkili verileri sil
            # Önce taramaları sil
            scans = self.db.query(Scan).filter(Scan.user_id == user_id).all()
            for scan in scans:
                # Güvenlik açıklarını sil
                self.db.query(Vulnerability).filter(Vulnerability.scan_id == scan.id).delete()
                # Taramayı sil
                self.db.delete(scan)
            
            # Raporları sil
            from app.database import Report
            self.db.query(Report).filter(Report.user_id == user_id).delete()
            
            # Kullanıcıyı sil
            self.db.delete(user)
            self.db.commit()
            
            logger.info(f"User {user_id} deleted successfully")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"User deletion failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Kullanıcı silinemedi: {str(e)}"
            )

    async def get_user_activity(self, user_id: int, page: int = 1, size: int = 20) -> Dict[str, Any]:
        """Kullanıcı aktivitelerini getir"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # Tarama aktiviteleri
            scans = self.db.query(Scan).filter(
                Scan.user_id == user_id
            ).order_by(desc(Scan.created_at)).offset((page - 1) * size).limit(size).all()
            
            total_scans = self.db.query(Scan).filter(Scan.user_id == user_id).count()
            
            # Aktivite listesi oluştur
            activities = []
            for scan in scans:
                activity = {
                    "id": scan.id,
                    "user_id": user_id,
                    "activity_type": "scan",
                    "description": f"Güvenlik taraması başlatıldı: {scan.target_url}",
                    "timestamp": scan.created_at,
                    "metadata": {
                        "scan_type": scan.scan_type,
                        "status": scan.status,
                        "target_url": scan.target_url
                    }
                }
                activities.append(activity)
            
            return {
                "activities": activities,
                "total": total_scans,
                "page": page,
                "size": size,
                "pages": (total_scans + size - 1) // size
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get user activity: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Kullanıcı aktiviteleri alınamadı: {str(e)}"
            )

    async def check_scan_limit(self, user_id: int) -> Dict[str, Any]:
        """Kullanıcının tarama limitini kontrol et"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            # Aylık limit
            if user.is_premium:
                monthly_limit = settings.PREMIUM_SCAN_LIMIT
            else:
                monthly_limit = settings.FREE_SCAN_LIMIT
            
            # Bu ay yapılan tarama sayısı
            start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_scan_count = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.created_at >= start_of_month
            ).count()
            
            # Eş zamanlı tarama limiti
            running_scans = self.db.query(Scan).filter(
                Scan.user_id == user_id,
                Scan.status == "running"
            ).count()
            
            max_concurrent = 5 if user.is_premium else 2
            
            return {
                "monthly_limit": monthly_limit,
                "monthly_used": monthly_scan_count,
                "monthly_remaining": monthly_limit - monthly_scan_count,
                "concurrent_limit": max_concurrent,
                "concurrent_used": running_scans,
                "concurrent_remaining": max_concurrent - running_scans,
                "can_scan": monthly_scan_count < monthly_limit and running_scans < max_concurrent
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to check scan limit: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Tarama limiti kontrol edilemedi: {str(e)}"
            )

    async def get_premium_features(self, user_id: int) -> List[Dict[str, Any]]:
        """Kullanıcının premium özelliklerini getir"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Kullanıcı bulunamadı"
                )
            
            features = [
                {
                    "feature_name": "Detaylı PDF Raporlar",
                    "description": "Profesyonel PDF raporları oluşturma",
                    "is_available": user.is_premium,
                    "usage_count": None,
                    "usage_limit": None
                },
                {
                    "feature_name": "Excel Raporlar",
                    "description": "Excel formatında rapor export",
                    "is_available": user.is_premium,
                    "usage_count": None,
                    "usage_limit": None
                },
                {
                    "feature_name": "Yüksek Tarama Limitleri",
                    "description": f"Aylık {settings.PREMIUM_SCAN_LIMIT} tarama hakkı",
                    "is_available": user.is_premium,
                    "usage_count": None,
                    "usage_limit": settings.PREMIUM_SCAN_LIMIT
                },
                {
                    "feature_name": "Öncelikli Tarama Kuyruğu",
                    "description": "Premium kullanıcılar için öncelikli tarama",
                    "is_available": user.is_premium,
                    "usage_count": None,
                    "usage_limit": None
                },
                {
                    "feature_name": "Gelişmiş Scanner'lar",
                    "description": "Tüm güvenlik scanner'larına erişim",
                    "is_available": user.is_premium,
                    "usage_count": None,
                    "usage_limit": None
                }
            ]
            
            return features
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get premium features: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Premium özellikler alınamadı: {str(e)}"
            )
