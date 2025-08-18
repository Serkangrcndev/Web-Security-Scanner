"""
Rapor API Router
Tarama raporları ve export işlemleri
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os

from app.database import get_db
from app.models.report_models import ReportCreate, ReportResponse
from app.services.report_service import ReportService
from app.core.auth import get_current_user
from app.models.user_models import User

router = APIRouter()

@router.post("/", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    report_data: ReportCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Yeni rapor oluşturur"""
    try:
        report_service = ReportService(db, current_user)
        
        # Premium özellik kontrolü
        if report_data.report_type in ["pdf", "excel"] and not current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu rapor formatı sadece premium kullanıcılar için mevcuttur"
            )
        
        # Rapor oluştur
        report = await report_service.create_report(report_data)
        
        # Background task olarak raporu oluştur
        background_tasks.add_task(report_service.generate_report, report.id)
        
        return ReportResponse(
            id=report.id,
            scan_id=report.scan_id,
            report_type=report.report_type,
            status="generating",
            created_at=report.created_at,
            message="Rapor oluşturuluyor"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor oluşturulamadı: {str(e)}"
        )

@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Kullanıcının raporlarını listeler"""
    try:
        report_service = ReportService(db, current_user)
        reports = await report_service.get_user_reports(skip, limit, report_type)
        
        return [
            ReportResponse(
                id=report.id,
                scan_id=report.scan_id,
                report_type=report.report_type,
                status=report.status,
                file_path=report.file_path,
                download_count=report.download_count,
                created_at=report.created_at
            )
            for report in reports
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Raporlar alınamadı: {str(e)}"
        )

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Belirli bir raporu getirir"""
    try:
        report_service = ReportService(db, current_user)
        report = await report_service.get_report(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
        return ReportResponse(
            id=report.id,
            scan_id=report.scan_id,
            report_type=report.report_type,
            status=report.status,
            file_path=report.file_path,
            download_count=report.download_count,
            created_at=report.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor alınamadı: {str(e)}"
        )

@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Raporu indirir"""
    try:
        report_service = ReportService(db, current_user)
        report = await report_service.get_report(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
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
        
        # Download sayısını artır
        await report_service.increment_download_count(report_id)
        
        # Dosya türüne göre content type belirle
        content_type_map = {
            "pdf": "application/pdf",
            "excel": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "json": "application/json"
        }
        
        content_type = content_type_map.get(report.report_type, "application/octet-stream")
        
        # Dosya adını belirle
        filename = f"security_scan_report_{report.scan_id}.{report.report_type}"
        
        return FileResponse(
            path=report.file_path,
            media_type=content_type,
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor indirilemedi: {str(e)}"
        )

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Raporu siler"""
    try:
        report_service = ReportService(db, current_user)
        success = await report_service.delete_report(report_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
        return {"message": "Rapor başarıyla silindi"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor silinemedi: {str(e)}"
        )

@router.post("/{report_id}/regenerate")
async def regenerate_report(
    report_id: int,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Raporu yeniden oluşturur"""
    try:
        report_service = ReportService(db, current_user)
        report = await report_service.get_report(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
        # Raporu yeniden oluştur
        success = await report_service.regenerate_report(report_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rapor yeniden oluşturulamadı"
            )
        
        # Background task olarak raporu oluştur
        background_tasks.add_task(report_service.generate_report, report_id)
        
        return {"message": "Rapor yeniden oluşturuluyor"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor yeniden oluşturulamadı: {str(e)}"
        )

@router.get("/{report_id}/status")
async def get_report_status(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Rapor durumunu getirir"""
    try:
        report_service = ReportService(db, current_user)
        report = await report_service.get_report(report_id)
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rapor bulunamadı"
            )
        
        return {
            "report_id": report.id,
            "status": report.status,
            "created_at": report.created_at,
            "download_count": report.download_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rapor durumu alınamadı: {str(e)}"
        )

@router.get("/export-formats")
async def get_export_formats(
    current_user: User = Depends(get_current_user)
):
    """Kullanılabilir export formatlarını listeler"""
    try:
        formats = {
            "json": {
                "name": "JSON",
                "description": "Structured data format",
                "available": True,
                "file_extension": "json"
            },
            "pdf": {
                "name": "PDF",
                "description": "Portable Document Format - Premium özellik",
                "available": current_user.is_premium,
                "file_extension": "pdf"
            },
            "excel": {
                "name": "Excel",
                "description": "Microsoft Excel format - Premium özellik",
                "available": current_user.is_premium,
                "file_extension": "xlsx"
            }
        }
        
        return {
            "formats": formats,
            "is_premium": current_user.is_premium
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Export formatları alınamadı: {str(e)}"
        )

@router.post("/bulk-export")
async def bulk_export_reports(
    scan_ids: List[int],
    report_type: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Birden fazla tarama için toplu rapor oluşturur"""
    try:
        if not current_user.is_premium:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu özellik sadece premium kullanıcılar için mevcuttur"
            )
        
        report_service = ReportService(db, current_user)
        
        # Toplu rapor oluştur
        reports = await report_service.create_bulk_reports(scan_ids, report_type)
        
        # Background task olarak raporları oluştur
        for report in reports:
            background_tasks.add_task(report_service.generate_report, report.id)
        
        return {
            "message": f"{len(reports)} rapor oluşturuluyor",
            "report_ids": [report.id for report in reports]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Toplu rapor oluşturulamadı: {str(e)}"
        )
