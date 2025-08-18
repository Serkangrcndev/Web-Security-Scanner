from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

class UserUpdate(BaseModel):
    """Kullanıcı güncelleme modeli"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Kullanıcı adı")
    email: Optional[EmailStr] = Field(None, description="Email adresi")
    is_premium: Optional[bool] = Field(None, description="Premium üyelik durumu")
    is_active: Optional[bool] = Field(None, description="Hesap aktif durumu")

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

class UserListResponse(BaseModel):
    """Kullanıcı listesi yanıt modeli"""
    users: List[UserResponse] = Field(..., description="Kullanıcı listesi")
    total: int = Field(..., description="Toplam kullanıcı sayısı")
    page: int = Field(..., description="Mevcut sayfa")
    size: int = Field(..., description="Sayfa boyutu")
    pages: int = Field(..., description="Toplam sayfa sayısı")

class UserStats(BaseModel):
    """Kullanıcı istatistikleri modeli"""
    total_scans: int = Field(..., description="Toplam tarama sayısı")
    completed_scans: int = Field(..., description="Tamamlanan tarama sayısı")
    failed_scans: int = Field(..., description="Başarısız tarama sayısı")
    total_vulnerabilities: int = Field(..., description="Toplam bulunan zafiyet sayısı")
    critical_vulnerabilities: int = Field(..., description="Kritik zafiyet sayısı")
    high_vulnerabilities: int = Field(..., description="Yüksek zafiyet sayısı")
    medium_vulnerabilities: int = Field(..., description="Orta zafiyet sayısı")
    low_vulnerabilities: int = Field(..., description="Düşük zafiyet sayısı")
    monthly_scan_count: int = Field(..., description="Bu ay yapılan tarama sayısı")
    monthly_scan_limit: int = Field(..., description="Aylık tarama limiti")
    premium_features_used: List[str] = Field(..., description="Kullanılan premium özellikler")
    last_scan_date: Optional[datetime] = Field(None, description="Son tarama tarihi")
    average_scan_duration: Optional[float] = Field(None, description="Ortalama tarama süresi (saniye)")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PremiumUpgrade(BaseModel):
    """Premium üyelik yükseltme modeli"""
    plan_type: str = Field(..., description="Plan tipi (monthly, yearly)")
    payment_method: str = Field(..., description="Ödeme yöntemi")
    auto_renew: bool = Field(True, description="Otomatik yenileme")

class PremiumFeatures(BaseModel):
    """Premium özellikler modeli"""
    feature_name: str = Field(..., description="Özellik adı")
    description: str = Field(..., description="Özellik açıklaması")
    is_available: bool = Field(..., description="Özellik mevcut mu?")
    usage_count: Optional[int] = Field(None, description="Kullanım sayısı")
    usage_limit: Optional[int] = Field(None, description="Kullanım limiti")

class UserPreferences(BaseModel):
    """Kullanıcı tercihleri modeli"""
    email_notifications: bool = Field(True, description="Email bildirimleri")
    scan_notifications: bool = Field(True, description="Tarama bildirimleri")
    vulnerability_alerts: bool = Field(True, description="Zafiyet uyarıları")
    report_format: str = Field("pdf", description="Tercih edilen rapor formatı")
    language: str = Field("tr", description="Dil tercihi")
    timezone: str = Field("Europe/Istanbul", description="Zaman dilimi")
    scan_timeout: int = Field(300, description="Varsayılan tarama zaman aşımı (saniye)")
    max_concurrent_scans: int = Field(3, description="Maksimum eş zamanlı tarama sayısı")

class UserActivity(BaseModel):
    """Kullanıcı aktivite modeli"""
    id: int = Field(..., description="Aktivite ID")
    user_id: int = Field(..., description="Kullanıcı ID")
    activity_type: str = Field(..., description="Aktivite tipi")
    description: str = Field(..., description="Aktivite açıklaması")
    ip_address: Optional[str] = Field(None, description="IP adresi")
    user_agent: Optional[str] = Field(None, description="Kullanıcı ajanı")
    timestamp: datetime = Field(..., description="Aktivite zamanı")
    metadata: Optional[dict] = Field(None, description="Ek bilgiler")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserActivityResponse(BaseModel):
    """Kullanıcı aktivite yanıt modeli"""
    activities: List[UserActivity] = Field(..., description="Aktivite listesi")
    total: int = Field(..., description="Toplam aktivite sayısı")
    page: int = Field(..., description="Mevcut sayfa")
    size: int = Field(..., description="Sayfa boyutu")
    pages: int = Field(..., description="Toplam sayfa sayısı")

class ContactSupport(BaseModel):
    """Destek iletişim modeli"""
    subject: str = Field(..., min_length=5, max_length=200, description="Konu")
    message: str = Field(..., min_length=10, max_length=2000, description="Mesaj")
    priority: str = Field("normal", description="Öncelik (low, normal, high, urgent)")
    category: str = Field(..., description="Kategori (technical, billing, feature_request, bug_report)")
    attachments: Optional[List[str]] = Field(None, description="Ek dosyalar")

class SupportTicket(BaseModel):
    """Destek bileti modeli"""
    id: int = Field(..., description="Bilet ID")
    subject: str = Field(..., description="Konu")
    status: str = Field(..., description="Durum")
    priority: str = Field(..., description="Öncelik")
    category: str = Field(..., description="Kategori")
    created_at: datetime = Field(..., description="Oluşturulma tarihi")
    updated_at: Optional[datetime] = Field(None, description="Son güncelleme tarihi")
    assigned_to: Optional[str] = Field(None, description="Atanan destek personeli")
    response_time: Optional[int] = Field(None, description="Yanıt süresi (saat)")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
