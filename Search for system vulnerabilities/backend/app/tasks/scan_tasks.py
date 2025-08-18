from celery import shared_task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import logging
import asyncio
import time

from app.database import SessionLocal, Scan, Vulnerability, ScanLog
from app.core.config import settings
from scanners import XSSScanner, NmapScanner, NucleiScanner, ZAPScanner, SQLMapScanner, NiktoScanner, ShodanScanner

logger = logging.getLogger(__name__)

# Database connection for Celery tasks
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@shared_task(bind=True, name="app.tasks.scan_tasks.run_security_scan")
def run_security_scan(self, scan_id: int, target_url: str, scan_type: str):
    """
    Güvenlik taraması çalıştır
    Bu task Celery worker tarafından asenkron olarak çalıştırılır
    """
    db = SessionLocal()
    try:
        logger.info(f"Starting security scan {scan_id} for {target_url}")
        
        # Tarama durumunu güncelle
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            logger.error(f"Scan {scan_id} not found")
            return False
        
        scan.status = "running"
        scan.started_at = datetime.utcnow()
        db.commit()
        
        # Log ekle
        add_scan_log(db, scan_id, "Tarama başlatıldı", "info")
        
        # Tarama tipine göre scanner'ları seç
        scanners_to_run = select_scanners_for_scan_type(scan_type)
        
        # Her scanner'ı çalıştır
        total_scanners = len(scanners_to_run)
        completed_scanners = 0
        
        for scanner_name, scanner in scanners_to_run.items():
            try:
                logger.info(f"Running {scanner_name} scanner for scan {scan_id}")
                
                # Scanner'ı çalıştır
                result = run_scanner(scanner, target_url, scan_type)
                
                # Sonuçları işle
                if result and result.vulnerabilities:
                    for vuln in result.vulnerabilities:
                        add_vulnerability_to_db(db, scan_id, vuln, scanner_name)
                
                # İlerleme güncelle
                completed_scanners += 1
                progress = (completed_scanners / total_scanners) * 100
                update_scan_progress(db, scan_id, progress)
                
                # Log ekle
                add_scan_log(db, scan_id, f"{scanner_name} taraması tamamlandı", "info")
                
            except Exception as e:
                logger.error(f"Scanner {scanner_name} failed: {e}")
                add_scan_log(db, scan_id, f"{scanner_name} taraması başarısız: {str(e)}", "error")
                continue
        
        # Tarama tamamlandı
        scan.status = "completed"
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        add_scan_log(db, scan_id, "Tarama tamamlandı", "info")
        logger.info(f"Security scan {scan_id} completed successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Security scan {scan_id} failed: {e}")
        
        # Hata durumunu güncelle
        if scan:
            scan.status = "failed"
            scan.completed_at = datetime.utcnow()
            db.commit()
        
        add_scan_log(db, scan_id, f"Tarama başarısız: {str(e)}", "error")
        return False
        
    finally:
        db.close()

def select_scanners_for_scan_type(scan_type: str) -> dict:
    """Tarama tipine göre scanner'ları seç"""
    scanners = {}
    
    if scan_type == "quick":
        # Hızlı tarama: sadece temel scanner'lar
        scanners['xss'] = XSSScanner()
        scanners['nuclei'] = NucleiScanner()
        
    elif scan_type == "standard":
        # Standart tarama: orta seviye kapsamlılık
        scanners['xss'] = XSSScanner()
        scanners['nuclei'] = NucleiScanner()
        scanners['nmap'] = NmapScanner()
        scanners['nikto'] = NiktoScanner()
        
    elif scan_type == "full":
        # Tam tarama: tüm scanner'lar
        scanners['xss'] = XSSScanner()
        scanners['nuclei'] = NucleiScanner()
        scanners['nmap'] = NmapScanner()
        scanners['zap'] = ZAPScanner()
        scanners['sqlmap'] = SQLMapScanner()
        scanners['nikto'] = NiktoScanner()
        scanners['shodan'] = ShodanScanner()
        
    elif scan_type == "custom":
        # Özel tarama: kullanıcı seçimi (varsayılan olarak standart)
        scanners['xss'] = XSSScanner()
        scanners['nuclei'] = NucleiScanner()
        scanners['nmap'] = NmapScanner()
        scanners['nikto'] = NiktoScanner()
    
    return scanners

def run_scanner(scanner, target_url: str, scan_type: str):
    """Scanner'ı çalıştır"""
    try:
        # Asenkron scanner'ı senkron olarak çalıştır
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(scanner.scan(target_url, {"scan_type": scan_type}))
            return result
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Scanner execution failed: {e}")
        return None

def add_vulnerability_to_db(db, scan_id: int, vuln, scanner_name: str):
    """Güvenlik açığını veritabanına ekle"""
    try:
        db_vuln = Vulnerability(
            scan_id=scan_id,
            title=vuln.title,
            description=vuln.description,
            severity=vuln.severity,
            cve_id=vuln.cve_id,
            cvss_score=vuln.cvss_score,
            scanner_name=scanner_name,
            payload=vuln.payload,
            location=vuln.location,
            evidence=vuln.evidence,
            created_at=datetime.utcnow()
        )
        
        db.add(db_vuln)
        db.commit()
        
        logger.info(f"Added vulnerability: {vuln.title} for scan {scan_id}")
        
    except Exception as e:
        logger.error(f"Failed to add vulnerability to database: {e}")
        db.rollback()

def add_scan_log(db, scan_id: int, message: str, level: str = "info"):
    """Tarama logu ekle"""
    try:
        log = ScanLog(
            scan_id=scan_id,
            message=message,
            level=level,
            timestamp=datetime.utcnow()
        )
        
        db.add(log)
        db.commit()
        
    except Exception as e:
        logger.error(f"Failed to add scan log: {e}")
        db.rollback()

def update_scan_progress(db, scan_id: int, progress: float):
    """Tarama ilerlemesini güncelle"""
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            # Progress field'ı database'de yoksa eklenebilir
            # Şimdilik sadece log ekliyoruz
            add_scan_log(db, scan_id, f"İlerleme: %{progress:.1f}", "info")
            
    except Exception as e:
        logger.error(f"Failed to update scan progress: {e}")

@shared_task(bind=True, name="app.tasks.scan_tasks.cancel_scan")
def cancel_scan(self, scan_id: int):
    """Tarama iptal et"""
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            logger.error(f"Scan {scan_id} not found for cancellation")
            return False
        
        if scan.status not in ["pending", "running"]:
            logger.warning(f"Scan {scan_id} cannot be cancelled (status: {scan.status})")
            return False
        
        scan.status = "cancelled"
        scan.completed_at = datetime.utcnow()
        db.commit()
        
        add_scan_log(db, scan_id, "Tarama iptal edildi", "warning")
        logger.info(f"Scan {scan_id} cancelled successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to cancel scan {scan_id}: {e}")
        return False
        
    finally:
        db.close()

@shared_task(bind=True, name="app.tasks.scan_tasks.retry_scan")
def retry_scan(self, scan_id: int):
    """Tarama yeniden dene"""
    db = SessionLocal()
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            logger.error(f"Scan {scan_id} not found for retry")
            return False
        
        if scan.status != "failed":
            logger.warning(f"Scan {scan_id} cannot be retried (status: {scan.status})")
            return False
        
        # Yeni tarama oluştur
        new_scan = Scan(
            user_id=scan.user_id,
            target_url=scan.target_url,
            scan_type=scan.scan_type,
            status="pending",
            priority=scan.priority,
            created_at=datetime.utcnow()
        )
        
        db.add(new_scan)
        db.commit()
        db.refresh(new_scan)
        
        # Yeni taramayı başlat
        run_security_scan.delay(new_scan.id, scan.target_url, scan.scan_type)
        
        add_scan_log(db, new_scan.id, "Tarama yeniden denendi", "info")
        logger.info(f"Scan {scan_id} retry initiated as scan {new_scan.id}")
        
        return new_scan.id
        
    except Exception as e:
        logger.error(f"Failed to retry scan {scan_id}: {e}")
        return False
        
    finally:
        db.close()

@shared_task(bind=True, name="app.tasks.scan_tasks.cleanup_old_scans")
def cleanup_old_scans(self, days_old: int = 30):
    """Eski taramaları temizle"""
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # Eski tamamlanmış taramaları bul
        old_scans = db.query(Scan).filter(
            Scan.status.in_(["completed", "failed", "cancelled"]),
            Scan.created_at < cutoff_date
        ).all()
        
        deleted_count = 0
        for scan in old_scans:
            try:
                # İlişkili verileri sil
                db.query(Vulnerability).filter(Vulnerability.scan_id == scan.id).delete()
                db.query(ScanLog).filter(ScanLog.timestamp < cutoff_date).delete()
                
                # Taramayı sil
                db.delete(scan)
                deleted_count += 1
                
            except Exception as e:
                logger.error(f"Failed to cleanup scan {scan.id}: {e}")
                continue
        
        db.commit()
        logger.info(f"Cleanup completed: {deleted_count} old scans removed")
        
        return deleted_count
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")
        return 0
        
    finally:
        db.close()

@shared_task(bind=True, name="app.tasks.scan_tasks.update_scan_timeouts")
def update_scan_timeouts(self):
    """Zaman aşımına uğrayan taramaları güncelle"""
    db = SessionLocal()
    try:
        timeout_threshold = datetime.utcnow() - timedelta(minutes=settings.SCAN_TIMEOUT)
        
        # Zaman aşımına uğrayan taramaları bul
        timeout_scans = db.query(Scan).filter(
            Scan.status == "running",
            Scan.started_at < timeout_threshold
        ).all()
        
        updated_count = 0
        for scan in timeout_scans:
            try:
                scan.status = "failed"
                scan.completed_at = datetime.utcnow()
                scan.error_message = "Tarama zaman aşımına uğradı"
                updated_count += 1
                
                add_scan_log(db, scan.id, "Tarama zaman aşımına uğradı", "error")
                
            except Exception as e:
                logger.error(f"Failed to update timeout scan {scan.id}: {e}")
                continue
        
        db.commit()
        logger.info(f"Timeout update completed: {updated_count} scans marked as failed")
        
        return updated_count
        
    except Exception as e:
        logger.error(f"Timeout update failed: {e}")
        return 0
        
    finally:
        db.close()
