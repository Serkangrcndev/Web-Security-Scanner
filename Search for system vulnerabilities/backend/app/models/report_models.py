from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ReportType(str, Enum):
    """Rapor tipi enum"""
    PDF = "pdf"
    EXCEL = "excel"
    JSON = "json"
    HTML = "html"

class ReportStatus(str, Enum):
    """Rapor durumu enum"""
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"

class ReportCreate(BaseModel):
    """Yeni rapor oluşturma modeli"""
    scan_id: int = Field(..., description="Rapor oluşturulacak tarama ID")
    report_type: ReportType = Field(..., description="Rapor tipi")
    include_recommendations: bool = Field(True, description="Çözüm önerileri dahil edilsin mi?")
    include_cve_details: bool = Field(True, description="CVE detayları dahil edilsin mi?")
    include_technical_details: bool = Field(False, description="Teknik detaylar dahil edilsin mi?")
    custom_sections: Optional[List[str]] = Field(None, description="Özel rapor bölümleri")
    language: str = Field("tr", description="Rapor dili")
    template: Optional[str] = Field(None, description="Rapor şablonu")

class ReportUpdate(BaseModel):
    """Rapor güncelleme modeli"""
    status: Optional[ReportStatus] = Field(None, description="Rapor durumu")
    file_path: Optional[str] = Field(None, description="Dosya yolu")
    error_message: Optional[str] = Field(None, description="Hata mesajı")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Ek bilgiler")

class ReportResponse(BaseModel):
    """Rapor yanıt modeli"""
    id: int = Field(..., description="Rapor ID")
    scan_id: int = Field(..., description="Tarama ID")
    report_type: str = Field(..., description="Rapor tipi")
    status: str = Field(..., description="Rapor durumu")
    file_path: Optional[str] = Field(None, description="Dosya yolu")
    file_size: Optional[int] = Field(None, description="Dosya boyutu (bytes)")
    download_count: int = Field(..., description="İndirme sayısı")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    completed_at: Optional[datetime] = Field(None, description="Tamamlanma tarihi")
    expires_at: Optional[datetime] = Field(None, description="Geçerlilik tarihi")
    error_message: Optional[str] = Field(None, description="Hata mesajı")
    message: Optional[str] = Field(None, description="Bilgi mesajı")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReportListResponse(BaseModel):
    """Rapor listesi yanıt modeli"""
    reports: List[ReportResponse] = Field(..., description="Rapor listesi")
    total: int = Field(..., description="Toplam rapor sayısı")
    page: int = Field(..., description="Mevcut sayfa")
    size: int = Field(..., description="Sayfa boyutu")
    pages: int = Field(..., description="Toplam sayfa sayısı")

class ReportTemplate(BaseModel):
    """Rapor şablonu modeli"""
    id: int = Field(..., description="Şablon ID")
    name: str = Field(..., description="Şablon adı")
    description: str = Field(..., description="Şablon açıklaması")
    report_type: ReportType = Field(..., description="Rapor tipi")
    sections: List[str] = Field(..., description="Şablon bölümleri")
    is_default: bool = Field(False, description="Varsayılan şablon mu?")
    is_premium: bool = Field(False, description="Premium şablon mu?")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Son güncelleme tarihi")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReportSection(BaseModel):
    """Rapor bölümü modeli"""
    name: str = Field(..., description="Bölüm adı")
    title: str = Field(..., description="Bölüm başlığı")
    content: str = Field(..., description="Bölüm içeriği")
    order: int = Field(..., description="Bölüm sırası")
    is_visible: bool = Field(True, description="Bölüm görünür mü?")
    data_source: Optional[str] = Field(None, description="Veri kaynağı")
    template_variables: Optional[Dict[str, Any]] = Field(None, description="Şablon değişkenleri")

class ReportContent(BaseModel):
    """Rapor içeriği modeli"""
    report_id: int = Field(..., description="Rapor ID")
    sections: List[ReportSection] = Field(..., description="Rapor bölümleri")
    summary: str = Field(..., description="Rapor özeti")
    recommendations: List[str] = Field(..., description="Öneriler")
    risk_score: float = Field(..., description="Risk skoru")
    risk_level: str = Field(..., description="Risk seviyesi")
    generated_at: datetime = Field(..., description="Oluşturulma zamanı")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReportExport(BaseModel):
    """Rapor export modeli"""
    report_id: int = Field(..., description="Export edilecek rapor ID")
    export_format: ReportType = Field(..., description="Export formatı")
    include_attachments: bool = Field(False, description="Ekler dahil edilsin mi?")
    compression: bool = Field(False, description="Sıkıştırma yapılsın mı?")
    password_protection: Optional[str] = Field(None, description="Şifre koruması")
    custom_filename: Optional[str] = Field(None, description="Özel dosya adı")

class ReportAnalytics(BaseModel):
    """Rapor analitik modeli"""
    report_id: int = Field(..., description="Rapor ID")
    generation_time: float = Field(..., description="Oluşturulma süresi (saniye)")
    file_size: int = Field(..., description="Dosya boyutu (bytes)")
    download_count: int = Field(..., description="İndirme sayısı")
    unique_downloads: int = Field(..., description="Benzersiz indirme sayısı")
    average_view_time: Optional[float] = Field(None, description="Ortalama görüntüleme süresi (saniye)")
    user_feedback: Optional[str] = Field(None, description="Kullanıcı geri bildirimi")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class BulkReportExport(BaseModel):
    """Toplu rapor export modeli"""
    scan_ids: List[int] = Field(..., description="Export edilecek tarama ID'leri")
    report_type: ReportType = Field(..., description="Rapor tipi")
    include_recommendations: bool = Field(True, description="Çözüm önerileri dahil edilsin mi?")
    include_cve_details: bool = Field(True, description="CVE detayları dahil edilsin mi?")
    export_format: ReportType = Field(..., description="Export formatı")
    compression: bool = Field(False, description="Sıkıştırma yapılsın mı?")
    custom_filename: Optional[str] = Field(None, description="Özel dosya adı")

class ReportSchedule(BaseModel):
    """Rapor zamanlama modeli"""
    id: int = Field(..., description="Zamanlama ID")
    scan_id: int = Field(..., description="Tarama ID")
    report_type: ReportType = Field(..., description="Rapor tipi")
    schedule_type: str = Field(..., description="Zamanlama tipi (daily, weekly, monthly, custom)")
    schedule_config: Dict[str, Any] = Field(..., description="Zamanlama konfigürasyonu")
    is_active: bool = Field(True, description="Zamanlama aktif mi?")
    last_generated: Optional[datetime] = Field(None, description="Son oluşturulma tarihi")
    next_generation: Optional[datetime] = Field(None, description="Sonraki oluşturulma tarihi")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ReportNotification(BaseModel):
    """Rapor bildirim modeli"""
    id: int = Field(..., description="Bildirim ID")
    report_id: int = Field(..., description="Rapor ID")
    user_id: int = Field(..., description="Kullanıcı ID")
    notification_type: str = Field(..., description="Bildirim tipi (email, push, sms)")
    status: str = Field(..., description="Bildirim durumu")
    sent_at: Optional[datetime] = Field(None, description="Gönderilme tarihi")
    read_at: Optional[datetime] = Field(None, description="Okunma tarihi")
    message: str = Field(..., description="Bildirim mesajı")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Ek bilgiler")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
