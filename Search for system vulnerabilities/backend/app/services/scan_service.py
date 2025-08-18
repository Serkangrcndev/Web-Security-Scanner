from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import asyncio
import logging

from app.database import Scan, Vulnerability, ScanLog, User
from app.models.scan_models import ScanCreate, ScanUpdate, ScanResponse, ScanListResponse
from app.core.config import settings
from app.core.celery_app import celery_app
from scanners import XSSScanner, NmapScanner, NucleiScanner, ZAPScanner, SQLMapScanner, NiktoScanner, ShodanScanner

logger = logging.getLogger(__name__)

class ScanService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user
        self.scanners = {
            'xss': XSSScanner(),
            'nmap': NmapScanner(),
            'nuclei': NucleiScanner(),
            'zap': ZAPScanner(),
            'sqlmap': SQLMapScanner(),
            'nikto': NiktoScanner(),
            'shodan': ShodanScanner()
        }

    async def check_scan_limit(self) -> bool:
        """Kullanıcının aylık tarama limitini kontrol et"""
        if self.current_user.is_premium:
            limit = settings.PREMIUM_SCAN_LIMIT
        else:
            limit = settings.FREE_SCAN_LIMIT
        
        # Bu ay yapılan tarama sayısını hesapla
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_scans = self.db.query(Scan).filter(
            Scan.user_id == self.current_user.id,
            Scan.created_at >= start_of_month
        ).count()
        
        return monthly_scans < limit

    async def create_scan(self, scan_data: ScanCreate) -> Scan:
        """Yeni tarama oluştur"""
        try:
            # Tarama limiti kontrolü
            if not await self.check_scan_limit():
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Aylık tarama limitiniz doldu. Premium üyeliğe geçin."
                )
            
            # Yeni tarama oluştur
            db_scan = Scan(
                user_id=self.current_user.id,
                target_url=str(scan_data.target_url),
                scan_type=scan_data.scan_type,
                status="pending",
                priority=scan_data.priority or 1,
                created_at=datetime.utcnow()
            )
            
            self.db.add(db_scan)
            self.db.commit()
            self.db.refresh(db_scan)
            
            # Log ekle
            await self.add_scan_log(db_scan.id, "Tarama oluşturuldu", "info")
            
            return db_scan
            
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"Scan creation failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Tarama oluşturulamadı: {str(e)}"
            )

    async def run_scan(self, scan_id: int) -> bool:
        """Tarama çalıştır"""
        try:
            scan = self.db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                logger.error(f"Scan {scan_id} not found")
                return False
            
            # Tarama durumunu güncelle
            scan.status = "running"
            scan.started_at = datetime.utcnow()
            self.db.commit()
            
            await self.add_scan_log(scan_id, "Tarama başlatıldı", "info")
            
            # Celery task'ı başlat
            task = celery_app.send_task(
                "app.tasks.scan_tasks.run_security_scan",
                args=[scan_id, str(scan.target_url), scan.scan_type],
                queue="premium" if self.current_user.is_premium else "default"
            )
            
            logger.info(f"Scan {scan_id} started with task {task.id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start scan {scan_id}: {e}")
            await self.update_scan_status(scan_id, "failed", str(e))
            return False

    async def get_scan(self, scan_id: int) -> Optional[Scan]:
        """Tarama detayını getir"""
        scan = self.db.query(Scan).filter(
            Scan.id == scan_id,
            Scan.user_id == self.current_user.id
        ).first()
        
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarama bulunamadı"
            )
        
        return scan

    async def get_user_scans(
        self, 
        page: int = 1, 
        size: int = 20,
        status: Optional[str] = None,
        scan_type: Optional[str] = None
    ) -> ScanListResponse:
        """Kullanıcının taramalarını getir"""
        query = self.db.query(Scan).filter(Scan.user_id == self.current_user.id)
        
        # Filtreler
        if status:
            query = query.filter(Scan.status == status)
        if scan_type:
            query = query.filter(Scan.scan_type == scan_type)
        
        # Toplam sayı
        total = query.count()
        
        # Sayfalama
        scans = query.order_by(desc(Scan.created_at)).offset((page - 1) * size).limit(size).all()
        
        # Toplam sayfa sayısı
        pages = (total + size - 1) // size
        
        return ScanListResponse(
            scans=scans,
            total=total,
            page=page,
            size=size,
            pages=pages
        )

    async def update_scan_status(self, scan_id: int, status: str, error_message: Optional[str] = None) -> bool:
        """Tarama durumunu güncelle"""
        try:
            scan = self.db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                return False
            
            scan.status = status
            if status == "completed":
                scan.completed_at = datetime.utcnow()
            elif status == "failed":
                scan.error_message = error_message
            
            self.db.commit()
            
            await self.add_scan_log(scan_id, f"Durum güncellendi: {status}", "info")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update scan status: {e}")
            return False

    async def update_scan_progress(self, scan_id: int, progress: float) -> bool:
        """Tarama ilerlemesini güncelle"""
        try:
            scan = self.db.query(Scan).filter(Scan.id == scan_id).first()
            if not scan:
                return False
            
            # Progress field'ı database'de yoksa eklenebilir
            # Şimdilik sadece log ekliyoruz
            await self.add_scan_log(scan_id, f"İlerleme: %{progress:.1f}", "info")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update scan progress: {e}")
            return False

    async def add_vulnerability(self, scan_id: int, vuln_data: Dict[str, Any]) -> Vulnerability:
        """Güvenlik açığı ekle"""
        try:
            vuln = Vulnerability(
                scan_id=scan_id,
                title=vuln_data.get("title", ""),
                description=vuln_data.get("description", ""),
                severity=vuln_data.get("severity", "low"),
                cve_id=vuln_data.get("cve_id"),
                cvss_score=vuln_data.get("cvss_score"),
                scanner_name=vuln_data.get("scanner_name", ""),
                payload=vuln_data.get("payload"),
                location=vuln_data.get("location"),
                evidence=vuln_data.get("evidence"),
                created_at=datetime.utcnow()
            )
            
            self.db.add(vuln)
            self.db.commit()
            self.db.refresh(vuln)
            
            await self.add_scan_log(scan_id, f"Güvenlik açığı bulundu: {vuln.title}", "warning")
            return vuln
            
        except Exception as e:
            logger.error(f"Failed to add vulnerability: {e}")
            self.db.rollback()
            raise

    async def get_scan_vulnerabilities(self, scan_id: int) -> List[Vulnerability]:
        """Tarama güvenlik açıklarını getir"""
        # Önce tarama sahibi kontrolü
        await self.get_scan(scan_id)
        
        vulnerabilities = self.db.query(Vulnerability).filter(
            Vulnerability.scan_id == scan_id
        ).order_by(desc(Vulnerability.created_at)).all()
        
        return vulnerabilities

    async def get_scan_logs(self, scan_id: int) -> List[ScanLog]:
        """Tarama loglarını getir"""
        # Önce tarama sahibi kontrolü
        await self.get_scan(scan_id)
        
        logs = self.db.query(ScanLog).filter(
            ScanLog.scan_id == scan_id
        ).order_by(ScanLog.timestamp).all()
        
        return logs

    async def add_scan_log(self, scan_id: int, message: str, level: str = "info") -> bool:
        """Tarama logu ekle"""
        try:
            log = ScanLog(
                scan_id=scan_id,
                message=message,
                level=level,
                timestamp=datetime.utcnow()
            )
            
            self.db.add(log)
            self.db.commit()
            return True
            
        except Exception as e:
            logger.error(f"Failed to add scan log: {e}")
            return False

    async def cancel_scan(self, scan_id: int) -> bool:
        """Tarama iptal et"""
        try:
            scan = await self.get_scan(scan_id)
            
            if scan.status not in ["pending", "running"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sadece bekleyen veya çalışan taramalar iptal edilebilir"
                )
            
            scan.status = "cancelled"
            scan.completed_at = datetime.utcnow()
            self.db.commit()
            
            await self.add_scan_log(scan_id, "Tarama iptal edildi", "warning")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to cancel scan: {e}")
            return False

    async def retry_scan(self, scan_id: int) -> bool:
        """Tarama yeniden dene"""
        try:
            scan = await self.get_scan(scan_id)
            
            if scan.status != "failed":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sadece başarısız taramalar yeniden denenebilir"
                )
            
            # Yeni tarama oluştur
            new_scan = Scan(
                user_id=self.current_user.id,
                target_url=scan.target_url,
                scan_type=scan.scan_type,
                status="pending",
                priority=scan.priority,
                created_at=datetime.utcnow()
            )
            
            self.db.add(new_scan)
            self.db.commit()
            self.db.refresh(new_scan)
            
            # Yeni taramayı başlat
            await self.run_scan(new_scan.id)
            
            await self.add_scan_log(new_scan.id, "Tarama yeniden denendi", "info")
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to retry scan: {e}")
            return False

    async def delete_scan(self, scan_id: int) -> bool:
        """Tarama sil"""
        try:
            scan = await self.get_scan(scan_id)
            
            if scan.status in ["running", "pending"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Çalışan veya bekleyen taramalar silinemez"
                )
            
            # İlişkili verileri sil
            self.db.query(Vulnerability).filter(Vulnerability.scan_id == scan_id).delete()
            self.db.query(ScanLog).filter(ScanLog.scan_id == scan_id).delete()
            
            # Taramayı sil
            self.db.delete(scan)
            self.db.commit()
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to delete scan: {e}")
            return False

    async def get_scan_summary(self, scan_id: int) -> Dict[str, Any]:
        """Tarama özeti getir"""
        try:
            scan = await self.get_scan(scan_id)
            vulnerabilities = await self.get_scan_vulnerabilities(scan_id)
            
            # Severity sayılarını hesapla
            severity_counts = {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            }
            
            for vuln in vulnerabilities:
                severity_counts[vuln.severity] += 1
            
            # Risk skoru hesapla
            risk_score = (
                severity_counts["critical"] * 10 +
                severity_counts["high"] * 7 +
                severity_counts["medium"] * 4 +
                severity_counts["low"] * 1
            )
            
            return {
                "scan_id": scan_id,
                "target_url": scan.target_url,
                "scan_type": scan.scan_type,
                "status": scan.status,
                "total_vulnerabilities": len(vulnerabilities),
                "severity_counts": severity_counts,
                "risk_score": risk_score,
                "started_at": scan.started_at,
                "completed_at": scan.completed_at,
                "created_at": scan.created_at
            }
            
        except Exception as e:
            logger.error(f"Failed to get scan summary: {e}")
            raise

    async def get_user_scan_stats(self) -> Dict[str, Any]:
        """Kullanıcı tarama istatistikleri"""
        try:
            # Toplam tarama sayısı
            total_scans = self.db.query(Scan).filter(Scan.user_id == self.current_user.id).count()
            
            # Durum bazında sayılar
            completed_scans = self.db.query(Scan).filter(
                Scan.user_id == self.current_user.id,
                Scan.status == "completed"
            ).count()
            
            failed_scans = self.db.query(Scan).filter(
                Scan.user_id == self.current_user.id,
                Scan.status == "failed"
            ).count()
            
            running_scans = self.db.query(Scan).filter(
                Scan.user_id == self.current_user.id,
                Scan.status == "running"
            ).count()
            
            # Toplam güvenlik açığı sayısı
            total_vulnerabilities = self.db.query(Vulnerability).join(Scan).filter(
                Scan.user_id == self.current_user.id
            ).count()
            
            # Severity bazında güvenlik açığı sayıları
            severity_counts = self.db.query(
                Vulnerability.severity,
                func.count(Vulnerability.id)
            ).join(Scan).filter(
                Scan.user_id == self.current_user.id
            ).group_by(Vulnerability.severity).all()
            
            severity_dict = {severity: count for severity, count in severity_counts}
            
            # Bu ay yapılan tarama sayısı
            start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            monthly_scan_count = self.db.query(Scan).filter(
                Scan.user_id == self.current_user.id,
                Scan.created_at >= start_of_month
            ).count()
            
            return {
                "total_scans": total_scans,
                "completed_scans": completed_scans,
                "failed_scans": failed_scans,
                "running_scans": running_scans,
                "total_vulnerabilities": total_vulnerabilities,
                "severity_counts": severity_dict,
                "monthly_scan_count": monthly_scan_count,
                "monthly_scan_limit": settings.PREMIUM_SCAN_LIMIT if self.current_user.is_premium else settings.FREE_SCAN_LIMIT
            }
            
        except Exception as e:
            logger.error(f"Failed to get user scan stats: {e}")
            raise
