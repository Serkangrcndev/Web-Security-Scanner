from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ScanType(str, Enum):
    """Tarama tipi enum"""
    QUICK = "quick"
    STANDARD = "standard"
    FULL = "full"
    CUSTOM = "custom"

class ScanStatus(str, Enum):
    """Tarama durumu enum"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ScanPriority(int, Enum):
    """Tarama önceliği enum"""
    NORMAL = 1
    PREMIUM = 2
    URGENT = 3

class ScanCreate(BaseModel):
    """Yeni tarama oluşturma modeli"""
    target_url: HttpUrl = Field(..., description="Taranacak hedef URL")
    scan_type: ScanType = Field(..., description="Tarama tipi")
    options: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Tarama seçenekleri"
    )
    priority: Optional[ScanPriority] = Field(
        default=ScanPriority.NORMAL,
        description="Tarama önceliği"
    )

class ScanUpdate(BaseModel):
    """Tarama güncelleme modeli"""
    status: Optional[ScanStatus] = Field(None, description="Tarama durumu")
    priority: Optional[ScanPriority] = Field(None, description="Tarama önceliği")
    options: Optional[Dict[str, Any]] = Field(None, description="Tarama seçenekleri")

class ScanResponse(BaseModel):
    """Tarama yanıt modeli"""
    id: int = Field(..., description="Tarama ID")
    target_url: str = Field(..., description="Hedef URL")
    scan_type: str = Field(..., description="Tarama tipi")
    status: str = Field(..., description="Tarama durumu")
    priority: int = Field(..., description="Tarama önceliği")
    progress: Optional[float] = Field(None, description="Tarama ilerlemesi (%)")
    started_at: Optional[datetime] = Field(None, description="Başlama tarihi")
    completed_at: Optional[datetime] = Field(None, description="Tamamlanma tarihi")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    error_message: Optional[str] = Field(None, description="Hata mesajı")
    message: Optional[str] = Field(None, description="Bilgi mesajı")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ScanListResponse(BaseModel):
    """Tarama listesi yanıt modeli"""
    scans: List[ScanResponse] = Field(..., description="Tarama listesi")
    total: int = Field(..., description="Toplam tarama sayısı")
    page: int = Field(..., description="Mevcut sayfa")
    size: int = Field(..., description="Sayfa boyutu")
    pages: int = Field(..., description="Toplam sayfa sayısı")

class ScanOptions(BaseModel):
    """Tarama seçenekleri modeli"""
    xss: Optional[bool] = Field(False, description="XSS taraması yapılsın mı?")
    sql_injection: Optional[bool] = Field(False, description="SQL Injection taraması yapılsın mı?")
    csrf: Optional[bool] = Field(False, description="CSRF taraması yapılsın mı?")
    security_headers: Optional[bool] = Field(False, description="Güvenlik başlıkları kontrol edilsin mi?")
    port_scan: Optional[bool] = Field(False, description="Port taraması yapılsın mı?")
    service_detection: Optional[bool] = Field(False, description="Servis tespiti yapılsın mı?")
    vulnerability_scan: Optional[bool] = Field(False, description="Zafiyet taraması yapılsın mı?")
    custom_payloads: Optional[List[str]] = Field(
        default_factory=list,
        description="Özel test payload'ları"
    )
    timeout: Optional[int] = Field(300, description="Tarama zaman aşımı (saniye)")
    max_threads: Optional[int] = Field(10, description="Maksimum thread sayısı")

class ScanProgress(BaseModel):
    """Tarama ilerleme modeli"""
    scan_id: int = Field(..., description="Tarama ID")
    progress: float = Field(..., description="İlerleme yüzdesi")
    current_step: str = Field(..., description="Mevcut adım")
    total_steps: int = Field(..., description="Toplam adım sayısı")
    estimated_time: Optional[int] = Field(None, description="Tahmini kalan süre (saniye)")
    status: str = Field(..., description="Durum")
    message: Optional[str] = Field(None, description="Bilgi mesajı")

class ScanCancel(BaseModel):
    """Tarama iptal modeli"""
    scan_id: int = Field(..., description="İptal edilecek tarama ID")
    reason: Optional[str] = Field(None, description="İptal nedeni")

class ScanRetry(BaseModel):
    """Tarama yeniden deneme modeli"""
    scan_id: int = Field(..., description="Yeniden denenecek tarama ID")
    options: Optional[ScanOptions] = Field(None, description="Yeni tarama seçenekleri")

class ScanStats(BaseModel):
    """Tarama istatistikleri modeli"""
    total_scans: int = Field(..., description="Toplam tarama sayısı")
    completed_scans: int = Field(..., description="Tamamlanan tarama sayısı")
    failed_scans: int = Field(..., description="Başarısız tarama sayısı")
    running_scans: int = Field(..., description="Çalışan tarama sayısı")
    average_duration: Optional[float] = Field(None, description="Ortalama tarama süresi (saniye)")
    total_vulnerabilities: int = Field(..., description="Toplam bulunan zafiyet sayısı")
    critical_vulnerabilities: int = Field(..., description="Kritik zafiyet sayısı")
    high_vulnerabilities: int = Field(..., description="Yüksek zafiyet sayısı")
    medium_vulnerabilities: int = Field(..., description="Orta zafiyet sayısı")
    low_vulnerabilities: int = Field(..., description="Düşük zafiyet sayısı")

class ScanLogEntry(BaseModel):
    """Tarama log girişi modeli"""
    id: int = Field(..., description="Log ID")
    scan_id: int = Field(..., description="Tarama ID")
    message: str = Field(..., description="Log mesajı")
    level: str = Field(..., description="Log seviyesi (info, warning, error)")
    timestamp: datetime = Field(..., description="Log zamanı")
    scanner_name: Optional[str] = Field(None, description="Scanner adı")
    step_name: Optional[str] = Field(None, description="Adım adı")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ScanLogResponse(BaseModel):
    """Tarama log yanıt modeli"""
    logs: List[ScanLogEntry] = Field(..., description="Log listesi")
    total: int = Field(..., description="Toplam log sayısı")
