from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import logging
import os

from app.database import Report, Scan, User
from app.models.report_models import ReportCreate, ReportUpdate, ReportResponse, ReportListResponse
from app.core.config import settings
from app.core.celery_app import celery_app

logger = logging.getLogger(__name__)

class ReportService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    async def create_report(self, report_data: ReportCreate) -> Report:
        """Yeni rapor oluştur"""
        try:
            # Tarama sahibi kontrolü
            scan = self.db.query(Scan).filter(
                Scan.id == report_data.scan_id,
                Scan.user_id == self.current_user.id
            ).first()
            
            if not scan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarama bulunamadı"
                )
            
            # Premium özellik kontrolü
            if report_data.report_type in ["pdf", "excel"] and not self.current_user.is_premium:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bu rapor formatı sadece premium kullanıcılar için mevcuttur"
                )
            
            # Yeni rapor oluştur
            db_report = Report(
                user_id=self.current_user.id,
                scan_id=report_data.scan_id,
                report_type=report_data.report_type,
                status="generating",
                created_at=datetime.utcnow()
            )
            
            self.db.add(db_report)
            self.db.commit()
            self.db.refresh(db_report)
            
            logger.info(f"Report {db_report.id} created for scan {report_data.scan_id}")
            return db_report
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Report creation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor oluşturulamadı: {str(e)}"
            )

    async def generate_report(self, report_id: int) -> bool:
        """Rapor oluştur (Celery task ile)"""
        try:
            report = await self.get_report(report_id)
            
            # Celery task'ı başlat
            task = celery_app.send_task(
                "app.tasks.report_tasks.generate_report",
                args=[report_id],
                queue="reports"
            )
            
            logger.info(f"Report generation {report_id} started with task {task.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start report generation: {e}")
            return False

    async def get_report(self, report_id: int) -> Report:
        """Rapor detayını getir"""
        report = self.db.query(Report).filter(
            Report.id == report_id,
            Report.user_id == self.current_user.id
        ).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
        return report

    async def get_user_reports(
        self, 
        page: int = 1, 
        size: int = 20,
        report_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> ReportListResponse:
        """Kullanıcının raporlarını getir"""
        query = self.db.query(Report).filter(Report.user_id == self.current_user.id)
        
        # Filtreler
        if report_type:
            query = query.filter(Report.report_type == report_type)
        if status:
            query = query.filter(Report.status == status)
        
        # Toplam sayı
        total = query.count()
        
        # Sayfalama
        reports = query.order_by(desc(Report.created_at)).offset((page - 1) * size).limit(size).all()
        
        # Toplam sayfa sayısı
        pages = (total + size - 1) // size
        
        return ReportListResponse(
            reports=reports,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def download_report(self, report_id: int) -> str:
        """Rapor indir"""
        try:
            report = await self.get_report(report_id)
            
            if report.status != "completed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rapor henüz hazır değil"
                )
            
            if not report.file_path or not os.path.exists(report.file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Rapor dosyası bulunamadı"
                )
            
            # İndirme sayısını artır
            report.download_count += 1
            self.db.commit()
            
            return report.file_path
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Report download failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor indirilemedi: {str(e)}"
            )

    async def delete_report(self, report_id: int) -> bool:
        """Rapor sil"""
        try:
            report = await self.get_report(report_id)
            
            # Dosyayı sil
            if report.file_path and os.path.exists(report.file_path):
                os.remove(report.file_path)
            
            # Veritabanından sil
            self.db.delete(report)
            self.db.commit()
            
            logger.info(f"Report {report_id} deleted successfully")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Report deletion failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor silinemedi: {str(e)}"
            )

    async def regenerate_report(self, report_id: int) -> bool:
        """Rapor yeniden oluştur"""
        try:
            report = await self.get_report(report_id)
            
            if report.status == "generating":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rapor zaten oluşturuluyor"
                )
            
            # Eski dosyayı sil
            if report.file_path and os.path.exists(report.file_path):
                os.remove(report.file_path)
            
            # Durumu sıfırla
            report.status = "generating"
            report.file_path = None
            report.error_message = None
            report.completed_at = None
            self.db.commit()
            
            # Yeni rapor oluştur
            await self.generate_report(report_id)
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Report regeneration failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor yeniden oluşturulamadı: {str(e)}"
            )

    async def get_report_status(self, report_id: int) -> Dict[str, Any]:
        """Rapor durumunu getir"""
        try:
            report = await self.get_report(report_id)
            
            return {
                "id": report.id,
                "status": report.status,
                "created_at": report.created_at,
                "completed_at": report.completed_at,
                "error_message": report.error_message,
                "download_count": report.download_count,
                "file_size": os.path.getsize(report.file_path) if report.file_path and os.path.exists(report.file_path) else None
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get report status: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor durumu alınamadı: {str(e)}"
            )

    async def get_available_formats(self) -> List[Dict[str, Any]]:
        """Kullanılabilir rapor formatlarını getir"""
        formats = [
            {
                "format": "json",
                "name": "JSON",
                "description": "Yapılandırılmış veri formatı",
                "is_premium": False,
                "file_extension": ".json"
            },
            {
                "format": "pdf",
                "name": "PDF",
                "description": "Profesyonel PDF raporu",
                "is_premium": True,
                "file_extension": ".pdf"
            },
            {
                "format": "excel",
                "name": "Excel",
                "description": "Excel tablosu formatında",
                "is_premium": True,
                "file_extension": ".xlsx"
            }
        ]
        
        return formats

    async def create_bulk_report(self, scan_ids: List[int], report_type: str) -> Dict[str, Any]:
        """Toplu rapor oluştur"""
        try:
            # Premium kontrolü
            if report_type in ["pdf", "excel"] and not self.current_user.is_premium:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bu rapor formatı sadece premium kullanıcılar için mevcuttur"
                )
            
            # Tarama sahibi kontrolü
            scans = self.db.query(Scan).filter(
                Scan.id.in_(scan_ids),
                Scan.user_id == self.current_user.id
            ).all()
            
            if len(scans) != len(scan_ids):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bazı taramalar bulunamadı veya erişim izniniz yok"
                )
            
            # Celery task'ı başlat
            task = celery_app.send_task(
                "app.tasks.report_tasks.generate_bulk_report",
                args=[scan_ids, report_type, self.current_user.id],
                queue="reports"
            )
            
            logger.info(f"Bulk report generation started with task {task.id} for {len(scan_ids)} scans")
            
            return {
                "task_id": task.id,
                "scan_count": len(scan_ids),
                "report_type": report_type,
                "status": "generating"
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Bulk report creation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Toplu rapor oluşturulamadı: {str(e)}"
            )

    async def get_report_templates(self) -> List[Dict[str, Any]]:
        """Kullanılabilir rapor şablonlarını getir"""
        templates = [
            {
                "id": 1,
                "name": "Standart Güvenlik Raporu",
                "description": "Temel güvenlik açığı bilgileri ve öneriler",
                "report_type": "pdf",
                "sections": ["summary", "vulnerabilities", "recommendations"],
                "is_default": True,
                "is_premium": False
            },
            {
                "id": 2,
                "name": "Detaylı Teknik Rapor",
                "description": "Teknik detaylar, CVE bilgileri ve çözüm önerileri",
                "report_type": "pdf",
                "sections": ["summary", "vulnerabilities", "technical_details", "cve_info", "recommendations"],
                "is_default": False,
                "is_premium": True
            },
            {
                "id": 3,
                "name": "Yönetici Özeti",
                "description": "Yöneticiler için özet bilgiler ve risk değerlendirmesi",
                "report_type": "pdf",
                "sections": ["executive_summary", "risk_assessment", "key_findings", "action_items"],
                "is_default": False,
                "is_premium": True
            }
        ]
        
        return templates

    async def schedule_report(self, scan_id: int, report_type: str, schedule_config: Dict[str, Any]) -> Dict[str, Any]:
        """Rapor zamanlaması oluştur"""
        try:
            # Premium kontrolü
            if report_type in ["pdf", "excel"] and not self.current_user.is_premium:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bu rapor formatı sadece premium kullanıcılar için mevcuttur"
                )
            
            # Tarama sahibi kontrolü
            scan = self.db.query(Scan).filter(
                Scan.id == scan_id,
                Scan.user_id == self.current_user.id
            ).first()
            
            if not scan:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarama bulunamadı"
                )
            
            # Zamanlama oluştur (bu kısım daha sonra implement edilebilir)
            schedule_info = {
                "scan_id": scan_id,
                "report_type": report_type,
                "schedule_config": schedule_config,
                "status": "active",
                "created_at": datetime.utcnow()
            }
            
            logger.info(f"Report schedule created for scan {scan_id}")
            return schedule_info
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Report scheduling failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor zamanlaması oluşturulamadı: {str(e)}"
            )

    async def get_report_analytics(self, report_id: int) -> Dict[str, Any]:
        """Rapor analitiklerini getir"""
        try:
            report = await self.get_report(report_id)
            
            # Bu kısım daha sonra implement edilebilir
            analytics = {
                "report_id": report.id,
                "generation_time": None,  # Rapor oluşturma süresi
                "file_size": os.path.getsize(report.file_path) if report.file_path and os.path.exists(report.file_path) else None,
                "download_count": report.download_count,
                "unique_downloads": report.download_count,  # Şimdilik aynı
                "average_view_time": None,
                "user_feedback": None,
                "created_at": report.created_at
            }
            
            return analytics
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to get report analytics: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Rapor analitikleri alınamadı: {str(e)}"
            )

    async def cleanup_expired_reports(self, days_old: int = 7) -> int:
        """Süresi dolmuş raporları temizle"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Eski raporları bul
            old_reports = self.db.query(Report).filter(
                Report.created_at < cutoff_date,
                Report.user_id == self.current_user.id
            ).all()
            
            deleted_count = 0
            for report in old_reports:
                try:
                    # Dosyayı sil
                    if report.file_path and os.path.exists(report.file_path):
                        os.remove(report.file_path)
                    
                    # Veritabanından sil
                    self.db.delete(report)
                    deleted_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to cleanup report {report.id}: {e}")
                    continue
            
            self.db.commit()
            logger.info(f"Report cleanup completed: {deleted_count} old reports removed")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Report cleanup failed: {e}")
            return 0
