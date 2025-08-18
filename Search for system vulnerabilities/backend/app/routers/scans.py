"""
Tarama API Router
Güvenlik taraması endpoint'leri
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from app.database import get_db
from app.models.scan_models import ScanCreate, ScanResponse, ScanStatus
from app.services.scan_service import ScanService
from app.core.auth import get_current_user
from app.models.user_models import User

router = APIRouter()

@router.post("/", response_model=ScanResponse, status_code=status.HTTP_201_CREATED)
async def create_scan(
    scan_data: ScanCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Yeni tarama oluşturur"""
    try:
        scan_service = ScanService(db, current_user)
        
        # Kullanıcının tarama limitini kontrol et
        if not await scan_service.check_scan_limit():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Aylık tarama limitiniz doldu. Premium üyeliğe geçin."
            )
        
        # Taramayı oluştur
        scan = await scan_service.create_scan(scan_data)
        
        # Background task olarak taramayı başlat
        background_tasks.add_task(scan_service.run_scan, scan.id)
        
        return ScanResponse(
            id=scan.id,
            target_url=scan.target_url,
            scan_type=scan.scan_type,
            status=scan.status,
            priority=scan.priority,
            created_at=scan.created_at,
            message="Tarama başlatıldı"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama oluşturulamadı: {str(e)}"
        )

@router.get("/", response_model=List[ScanResponse])
async def get_scans(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının taramalarını listeler"""
    try:
        scan_service = ScanService(db, current_user)
        scans = await scan_service.get_user_scans(skip, limit, status_filter)
        
        return [
            ScanResponse(
                id=scan.id,
                target_url=scan.target_url,
                scan_type=scan.scan_type,
                status=scan.status,
                priority=scan.priority,
                created_at=scan.created_at,
                started_at=scan.started_at,
                completed_at=scan.completed_at
            )
            for scan in scans
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Taramalar alınamadı: {str(e)}"
        )

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Belirli bir taramayı getirir"""
    try:
        scan_service = ScanService(db, current_user)
        scan = await scan_service.get_scan(scan_id)
        
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarama bulunamadı"
            )
        
        return ScanResponse(
            id=scan.id,
            target_url=scan.target_url,
            scan_type=scan.scan_type,
            status=scan.status,
            priority=scan.priority,
            created_at=scan.created_at,
            started_at=scan.started_at,
            completed_at=scan.completed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama alınamadı: {str(e)}"
        )

@router.get("/{scan_id}/vulnerabilities")
async def get_scan_vulnerabilities(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tarama sonucundaki güvenlik açıklarını getirir"""
    try:
        scan_service = ScanService(db, current_user)
        vulnerabilities = await scan_service.get_scan_vulnerabilities(scan_id)
        
        return {
            "scan_id": scan_id,
            "total_vulnerabilities": len(vulnerabilities),
            "vulnerabilities": [
                {
                    "id": vuln.id,
                    "title": vuln.title,
                    "description": vuln.description,
                    "severity": vuln.severity,
                    "cve_id": vuln.cve_id,
                    "cvss_score": vuln.cvss_score,
                    "scanner_name": vuln.scanner_name,
                    "location": vuln.location,
                    "evidence": vuln.evidence,
                    "created_at": vuln.created_at
                }
                for vuln in vulnerabilities
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Güvenlik açıkları alınamadı: {str(e)}"
        )

@router.get("/{scan_id}/logs")
async def get_scan_logs(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tarama log'larını getirir"""
    try:
        scan_service = ScanService(db, current_user)
        logs = await scan_service.get_scan_logs(scan_id)
        
        return {
            "scan_id": scan_id,
            "total_logs": len(logs),
            "logs": [
                {
                    "id": log.id,
                    "message": log.message,
                    "level": log.level,
                    "timestamp": log.timestamp
                }
                for log in logs
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Log'lar alınamadı: {str(e)}"
        )

@router.get("/{scan_id}/summary")
async def get_scan_summary(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Tarama özetini getirir"""
    try:
        scan_service = ScanService(db, current_user)
        summary = await scan_service.get_scan_summary(scan_id)
        
        return summary
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama özeti alınamadı: {str(e)}"
        )

@router.delete("/{scan_id}")
async def delete_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Taramayı siler"""
    try:
        scan_service = ScanService(db, current_user)
        success = await scan_service.delete_scan(scan_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarama bulunamadı"
            )
        
        return {"message": "Tarama başarıyla silindi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama silinemedi: {str(e)}"
        )

@router.post("/{scan_id}/cancel")
async def cancel_scan(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Çalışan taramayı iptal eder"""
    try:
        scan_service = ScanService(db, current_user)
        success = await scan_service.cancel_scan(scan_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tarama iptal edilemedi"
            )
        
        return {"message": "Tarama iptal edildi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama iptal edilemedi: {str(e)}"
        )

@router.post("/{scan_id}/retry")
async def retry_scan(
    scan_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Başarısız taramayı tekrar dener"""
    try:
        scan_service = ScanService(db, current_user)
        scan = await scan_service.retry_scan(scan_id)
        
        if not scan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tarama tekrar denenemedi"
            )
        
        # Background task olarak taramayı başlat
        background_tasks.add_task(scan_service.run_scan, scan.id)
        
        return {"message": "Tarama tekrar başlatıldı"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tarama tekrar denenemedi: {str(e)}"
        )
