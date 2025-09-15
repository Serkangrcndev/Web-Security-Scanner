# GuardMesh - Premium Web Güvenlik Tarayıcısı

Bu proje, web sitelerindeki güvenlik açıklarını otomatik olarak tespit etmek için tasarlanmış kapsamlı bir güvenlik tarayıcısıdır. Modern web teknolojileri kullanılarak geliştiri4. **PostgreSQL bağlantı hatası**: PostgreSQL şifresini kontrol edinmiş olup, hem frontend hem de backend bileşenlerinden oluşmaktadır.

## 🚀 Özellikler

### Güvenlik Tarayıcıları

- **XSS Tarayıcısı**: Cross-Site Scripting güvenlik açıklarını tespit eder
- **Nmap Tarayıcısı**: Port tarama ve servis tespiti
- **Nuclei Tarayıcısı**: Şablon tabanlı güvenlik açığı taraması
- **OWASP ZAP Tarayıcısı**: Otomatik web uygulama güvenliği taraması
- **SQLMap Tarayıcısı**: SQL injection güvenlik açıklarını tespit eder
- **Nikto Tarayıcısı**: Web sunucu güvenlik açıkları taraması
- **Shodan Tarayıcısı**: İnternet cihazları arama ve analiz

### Kullanıcı Arayüzü

- Modern ve responsive tasarım (Next.js + TypeScript)
- Gerçek zamanlı tarama ilerleme takibi
- Güvenlik açıklarının detaylı raporlaması
- Dashboard ve analitik görünümler
- Çoklu tarama türü desteği (Hızlı, Standart, Tam)

### Backend Altyapısı

- Python tabanlı mikro servis mimarisi
- MSSQL veritabanı desteği
- Redis ile önbellekleme ve kuyruk yönetimi
- Asenkron tarama işlemleri
- RESTful API endpoints

## 🛠️ Teknoloji Stack

### Frontend

- **Next.js 14** - React framework
- **TypeScript** - Tip güvenliği
- **Tailwind CSS** - Stil sistemi
- **Framer Motion** - Animasyonlar
- **Zustand** - State yönetimi
- **React Query** - Veri fetching
- **Recharts** - Grafikler ve analitikler

### Backend

- **Python 3.11** - Ana programlama dili
- **FastAPI** - REST API framework
- **SQLAlchemy** - ORM ve veritabanı işlemleri
- **PostgreSQL** - Veritabanı
- **Celery** - Asenkron görev kuyruğu
- **Redis** - Önbellekleme ve mesaj kuyruğu

### DevOps

- **Docker & Docker Compose** - Konteynerleştirme
- **Nginx** - Reverse proxy (opsiyonel)

## 📋 Gereksinimler

### Sistem Gereksinimleri

- Docker ve Docker Compose
- En az 4GB RAM
- 2GB boş disk alanı
- İnternet bağlantısı (scanner araçları için)

### Backend Gereksinimleri

Aşağıdaki güvenlik tarama araçlarının sistemde kurulu olması gerekir:

#### Gerekli Araçlar

- **Nmap** - Port tarama aracı
- **Nuclei** - Şablon tabanlı tarayıcı
- **OWASP ZAP** - Web uygulama güvenlik tarayıcısı
- **SQLMap** - SQL injection testi
- **Nikto** - Web sunucu tarayıcısı
- **Shodan CLI** - İnternet cihazları arama

#### Python Kütüphaneleri

```
aiohttp>=3.8.0
beautifulsoup4>=4.11.0
sqlalchemy>=1.4.0
fastapi>=0.100.0
uvicorn>=0.20.0
celery>=5.3.0
redis>=4.5.0
psycopg2-binary==2.9.9
pydantic>=2.0.0
python-multipart>=0.0.6
```

## 🚀 Kurulum ve Çalıştırma

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/Serkangrcndev/Web-Security-Scanner.git
cd Web-Security-Scanner
```

### 2. Gerekli Araçları Kurun

```bash
# Ubuntu/Debian için
sudo apt update
sudo apt install nmap nikto sqlmap

# Nuclei kurulumu
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# OWASP ZAP kurulumu
wget https://github.com/zaproxy/zaproxy/releases/download/v2.12.0/ZAP_2.12.0_Linux.tar.gz
tar -xzf ZAP_2.12.0_Linux.tar.gz

# Shodan CLI kurulumu
pip install shodan
```

### 3. Docker ile Çalıştırma

```bash
# Tüm servisleri başlat
docker-compose up -d

# Logları takip et
docker-compose logs -f
```

### 4. Servislerin Durumunu Kontrol Et

```bash
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### 5. Veritabanı Yapılandırması

İlk çalıştırmada PostgreSQL tabloları otomatik olarak oluşturulacaktır. Varsayılan PostgreSQL bilgileri:

- **Database**: guardmesh_db
- **User**: guardmesh_user
- **Password**: secure_password_2024
- **Port**: 5432

## 📖 Kullanım

### Temel Tarama İşlemi

1. Web tarayıcıda `http://localhost:3000` adresine gidin
2. Ana sayfada hedef URL'yi girin
3. Tarama türünü seçin:
   - **Hızlı Tarama**: Temel kontroller (5-10 dakika)
   - **Standart Tarama**: Kapsamlı analiz (15-30 dakika)
   - **Tam Tarama**: Tüm testler (30-60 dakika)
4. "Taramayı Başlat" butonuna tıklayın
5. Gerçek zamanlı ilerlemeyi takip edin
6. Tarama tamamlandığında sonuçları görüntüleyin

### API Kullanımı

```bash
# Tarama başlatma
curl -X POST http://localhost:8000/scan/start \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "scan_type": "quick"}'

# Tarama durumunu kontrol etme
curl http://localhost:8000/scan/status/{scan_id}

# Tarama sonuçlarını alma
curl http://localhost:8000/scan/results/{scan_id}
```

## 🔧 Yapılandırma

### Environment Variables

```bash
# Backend için (.env dosyası)
DATABASE_URL=postgresql://guardmesh_user:secure_password_2024@guardmesh-postgres:5432/guardmesh_db
REDIS_URL=redis://guardmesh-redis:6379
SECRET_KEY=guardmesh-secret-key-2024
DEBUG=True

# Frontend için (.env.local dosyası)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Scanner Yapılandırması

`scanners/` klasöründeki her scanner için yapılandırma dosyaları oluşturabilirsiniz:

```python
# Örnek: xss_scanner_config.py
XSS_CONFIG = {
    "timeout": 30,
    "max_payloads": 100,
    "custom_payloads": ["<script>alert('test')</script>"]
}
```

## 📊 Raporlama ve Analitik

- Güvenlik açıklarının severity seviyesine göre sınıflandırılması
- CVSS skorlaması
- Tarama loglarının detaylı kayıt edilmesi
- Dashboard üzerinden istatistikler ve grafikler
- PDF/JSON formatında rapor dışa aktarımı

## 🔒 Güvenlik Notları

- Bu araç sadece yetkili sistemlerde kullanılmalıdır
- Tarama işlemleri hedef sistem üzerinde etki yaratabilir
- Üretim ortamlarında dikkatli kullanılmalıdır
- Tarama sonuçları gizli tutulmalıdır

## 🐛 Sorun Giderme

### Yaygın Problemler

1. **Docker servisleri başlamıyor**: Docker ve Docker Compose sürümlerini kontrol edin
2. **Scanner araçları bulunamıyor**: Sistem PATH'inde olduğundan emin olun
3. **Veritabanı bağlantı hatası**: MSSQL şifresini kontrol edin
4. **Frontend yüklenmiyor**: Node.js sürümünü kontrol edin (18.0.0+)

### Log Dosyaları

```bash
# Backend logları
docker-compose logs guardmesh-backend

# Frontend logları
docker-compose logs guardmesh-frontend

# Tüm loglar
docker-compose logs
```

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 📞 İletişim

- Proje Sahibi: Serkangrcndev
- GitHub: https://github.com/Serkangrcndev/Web-Security-Scanner
- E-posta: [E-posta adresinizi buraya ekleyin]

---

**Uyarı**: Bu araç güvenlik araştırması ve penetration testing için tasarlanmıştır. Yasal olmayan kullanımlar sorumluluğunuzdadır.</content>
<parameter name="filePath">c:\Users\Alperen\Desktop\Web-Security-Scanner\Search for system vulnerabilities\README.md
