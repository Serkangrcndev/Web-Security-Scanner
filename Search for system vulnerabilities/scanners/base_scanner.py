from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import asyncio
import logging

@dataclass
class Vulnerability:
    """Güvenlik açığı veri yapısı"""
    title: str
    description: str
    severity: str  # low, medium, high, critical
    cve_id: Optional[str] = None
    cvss_score: Optional[float] = None
    scanner_name: str = ""
    payload: Optional[str] = None
    location: Optional[str] = None
    evidence: Optional[str] = None
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

@dataclass
class ScanResult:
    """Tarama sonucu veri yapısı"""
    scanner_name: str
    target_url: str
    start_time: datetime
    end_time: Optional[datetime] = None
    vulnerabilities: List[Vulnerability] = None
    status: str = "running"  # running, completed, failed
    error_message: Optional[str] = None
    scan_logs: List[str] = None
    
    def __post_init__(self):
        if self.vulnerabilities is None:
            self.vulnerabilities = []
        if self.scan_logs is None:
            self.scan_logs = []

class BaseScanner(ABC):
    """Temel tarayıcı sınıfı - tüm tarayıcılar bu sınıftan türetilir"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"scanner.{name}")
        self.is_running = False
        
    @abstractmethod
    async def scan(self, target_url: str, options: Dict[str, Any] = None) -> ScanResult:
        """Ana tarama metodu - alt sınıflar tarafından implement edilmeli"""
        pass
    
    @abstractmethod
    async def validate_target(self, target_url: str) -> bool:
        """Hedef URL'nin geçerli olup olmadığını kontrol eder"""
        pass
    
    async def pre_scan_checks(self, target_url: str) -> bool:
        """Tarama öncesi kontroller"""
        try:
            if not await self.validate_target(target_url):
                self.logger.error(f"Invalid target URL: {target_url}")
                return False
            return True
        except Exception as e:
            self.logger.error(f"Pre-scan check failed: {e}")
            return False
    
    async def post_scan_cleanup(self):
        """Tarama sonrası temizlik işlemleri"""
        self.is_running = False
        self.logger.info(f"Scanner {self.name} cleanup completed")
    
    def add_vulnerability(self, result: ScanResult, vuln: Vulnerability):
        """Tarama sonucuna güvenlik açığı ekler"""
        vuln.scanner_name = self.name
        result.vulnerabilities.append(vuln)
        self.logger.info(f"Vulnerability found: {vuln.title} ({vuln.severity})")
    
    def add_scan_log(self, result: ScanResult, message: str, level: str = "info"):
        """Tarama logu ekler"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        result.scan_logs.append(log_entry)
        
        if level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        else:
            self.logger.info(message)
    
    async def run_with_timeout(self, coro, timeout: int = 300):
        """Zaman aşımı ile coroutine çalıştırır"""
        try:
            return await asyncio.wait_for(coro, timeout=timeout)
        except asyncio.TimeoutError:
            self.logger.error(f"Scan timeout after {timeout} seconds")
            raise
    
    def get_severity_score(self, severity: str) -> int:
        """Severity string'ini sayısal skora çevirir"""
        severity_map = {
            "low": 1,
            "medium": 2, 
            "high": 3,
            "critical": 4
        }
        return severity_map.get(severity.lower(), 0)
    
    def sort_vulnerabilities(self, vulnerabilities: List[Vulnerability]) -> List[Vulnerability]:
        """Güvenlik açıklarını severity'ye göre sıralar"""
        return sorted(
            vulnerabilities,
            key=lambda x: self.get_severity_score(x.severity),
            reverse=True
        )
