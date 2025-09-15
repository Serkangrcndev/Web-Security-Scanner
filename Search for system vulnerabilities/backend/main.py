
# GuardMesh Güvenlik Tarayıcı Backend
# FastAPI tabanlı web güvenlik tarama uygulaması


import os
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv


from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


from scanners.base_scanner import BaseScanner
from scanners.xss_scanner import XSSScanner
from scanners.nmap_scanner import NmapScanner
from scanners.nuclei_scanner import NucleiScanner
from scanners.zap_scanner import ZAPScanner
from scanners.sqlmap_scanner import SQLMapScanner
from scanners.nikto_scanner import NiktoScanner
from scanners.shodan_scanner import ShodanScanner


# Ortam değişkenlerini yükle
load_dotenv()

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("guardmesh-backend")


# Uygulama başlatma/durdurma için lifecycle yönetimi
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("GuardMesh Backend başlatılıyor...")
    yield
    logger.info("GuardMesh Backend kapatılıyor...")


# FastAPI uygulaması oluştur
app = FastAPI(
    title="GuardMesh Güvenlik Tarayıcı API",
    description="Premium Web Security Scanner Backend API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic modelleri
class ScanRequest(BaseModel):
    url: str
    scan_type: str = "quick"  # quick, standard, full
    options: Optional[dict] = None

class ScanStatus(BaseModel):
    scan_id: str
    status: str
    progress: int
    message: str

class VulnerabilityResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    cve_id: Optional[str] = None
    cvss_score: Optional[float] = None
    scanner_name: str
    location: Optional[str] = None
    timestamp: datetime

class ScanResultResponse(BaseModel):
    scan_id: str
    url: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    vulnerabilities: List[VulnerabilityResponse]
    scan_logs: List[str]


# Geçici bellek (ileride veritabanı ile değiştirilebilir)
scan_results = {}
active_scans = {}


# Tarayıcı eşlemesi
SCANNERS = {
    "xss": XSSScanner,
    "nmap": NmapScanner,
    "nuclei": NucleiScanner,
    "zap": ZAPScanner,
    "sqlmap": SQLMapScanner,
    "nikto": NiktoScanner,
    "shodan": ShodanScanner
}


# Uygun tarayıcıyı döndür
def get_scanner(scan_type: str, scanner_name: str):
    scanner_class = SCANNERS.get(scanner_name.lower())
    if not scanner_class:
        raise ValueError(f"Bilinmeyen tarayıcı: {scanner_name}")

    config = {}
    if scan_type == "quick":
        config["timeout"] = 300  # 5 dakika
    elif scan_type == "standard":
        config["timeout"] = 900  # 15 dakika
    elif scan_type == "full":
        config["timeout"] = 3600  # 1 saat

    return scanner_class(config=config)


# Arka planda güvenlik taraması başlat
async def run_scan(scan_id: str, url: str, scan_type: str, scanner_names: List[str]):
    try:
        active_scans[scan_id] = {"status": "running", "progress": 0}

        all_vulnerabilities = []
        all_logs = []

        total_scanners = len(scanner_names)
        for i, scanner_name in enumerate(scanner_names):
            try:
                scanner = get_scanner(scan_type, scanner_name)
                result = await scanner.scan(url)

                # Güvenlik açıklarını uygun formata çevir
                for vuln in result.vulnerabilities:
                    vuln_dict = {
                        "id": len(all_vulnerabilities) + 1,
                        "title": vuln.title,
                        "description": vuln.description,
                        "severity": vuln.severity,
                        "cve_id": vuln.cve_id,
                        "cvss_score": vuln.cvss_score,
                        "scanner_name": vuln.scanner_name,
                        "location": vuln.location,
                        "timestamp": vuln.timestamp
                    }
                    all_vulnerabilities.append(vuln_dict)

                all_logs.extend(result.scan_logs)

                # İlerleme güncelle
                progress = int((i + 1) / total_scanners * 100)
                active_scans[scan_id] = {"status": "running", "progress": progress}

            except Exception as e:
                logger.error(f"{scanner_name} tarayıcısı başarısız: {e}")
                all_logs.append(f"HATA: {scanner_name} tarayıcısı başarısız: {str(e)}")

        # Sonuçları kaydet
        scan_results[scan_id] = {
            "scan_id": scan_id,
            "url": url,
            "status": "completed",
            "start_time": datetime.now(),
            "end_time": datetime.now(),
            "vulnerabilities": all_vulnerabilities,
            "scan_logs": all_logs
        }

        active_scans[scan_id] = {"status": "completed", "progress": 100}

    except Exception as e:
        logger.error(f"Tarama {scan_id} başarısız: {e}")
        active_scans[scan_id] = {"status": "failed", "progress": 0, "error": str(e)}


# Ana endpoint
@app.get("/")
async def root():
    return {"message": "GuardMesh Güvenlik Tarayıcı API", "version": "1.0.0"}


# Sağlık kontrolü
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}


# Tarama başlatma endpoint'i
@app.post("/scan/start", response_model=dict)
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Yeni bir güvenlik taraması başlat"""
    scan_id = f"scan_{int(datetime.now().timestamp())}"

    # Tarama türüne göre tarayıcıları belirle
    scanner_mapping = {
        "quick": ["nmap", "xss"],
        "standard": ["nmap", "xss", "nuclei", "nikto"],
        "full": ["nmap", "xss", "nuclei", "zap", "sqlmap", "nikto", "shodan"]
    }

    scanner_names = scanner_mapping.get(request.scan_type, ["nmap", "xss"])

    # Arka planda taramayı başlat
    background_tasks.add_task(run_scan, scan_id, request.url, request.scan_type, scanner_names)

    return {
        "scan_id": scan_id,
        "message": f"{request.url} için tarama başlatıldı",
        "scanners": scanner_names
    }


# Tarama durumu sorgulama
@app.get("/scan/status/{scan_id}", response_model=ScanStatus)
async def get_scan_status(scan_id: str):
    if scan_id not in active_scans:
        raise HTTPException(status_code=404, detail="Tarama bulunamadı")

    scan_info = active_scans[scan_id]
    return ScanStatus(
        scan_id=scan_id,
        status=scan_info["status"],
        progress=scan_info.get("progress", 0),
        message=scan_info.get("error", "Tarama devam ediyor")
    )


# Tarama sonuçlarını getir
@app.get("/scan/results/{scan_id}", response_model=ScanResultResponse)
async def get_scan_results(scan_id: str):
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Tarama sonucu bulunamadı")

    result = scan_results[scan_id]
    return ScanResultResponse(**result)


# Desteklenen tarayıcıları listele
@app.get("/scanners")
async def list_scanners():
    return {
        "scanners": list(SCANNERS.keys()),
        "descriptions": {
            "xss": "Cross-Site Scripting Tarayıcı",
            "nmap": "Port ve Servis Tarayıcı",
            "nuclei": "Şablon tabanlı Açık Tarayıcı",
            "zap": "OWASP ZAP Web Tarayıcı",
            "sqlmap": "SQL Injection Tarayıcı",
            "nikto": "Web Sunucu Tarayıcı",
            "shodan": "İnternet Cihazı Tarayıcı"
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
