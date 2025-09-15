"""
Shodan Internet Intelligence Tarayıcısı
Açık port ve cihaz bilgilerini toplar
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import re

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class ShodanScanner(BaseScanner):
    """Shodan API kullanarak internet intelligence taraması yapan tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("Shodan Scanner", config)
        
        # Shodan API konfigürasyonu
        self.api_key = config.get("shodan_api_key", "") if config else ""
        self.api_base_url = "https://api.shodan.io"
        
        # API endpoint'leri
        self.endpoints = {
            "host": "/shodan/host/{}",
            "search": "/shodan/host/search",
            "facets": "/shodan/host/search/facets",
            "filters": "/shodan/host/search/filters",
            "tokens": "/shodan/host/search/tokens"
        }
        
        # Tarama seçenekleri
        self.scan_types = {
            "basic": "basic",
            "detailed": "detailed",
            "comprehensive": "comprehensive"
        }
    
    async def validate_target(self, target_url: str) -> bool:
        """Hedef URL'nin geçerli olup olmadığını kontrol eder"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(target_url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    async def scan(self, target_url: str, options: Dict[str, Any] = None) -> ScanResult:
        """Shodan taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "basic")
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"Shodan taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # API key kontrolü
            if not self.api_key:
                result.status = "failed"
                result.error_message = "Shodan API key gerekli"
                return result
            
            # Hostname'i çıkar
            hostname = self._extract_hostname(target_url)
            self.add_scan_log(result, f"Hedef hostname: {hostname}")
            
            # Shodan host bilgilerini al
            await self._get_host_information(result, hostname)
            
            # Shodan search sonuçlarını al
            await self._search_host_information(result, hostname)
            
            # Güvenlik açıklarını analiz et
            await self._analyze_security_issues(result, hostname)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"Shodan taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            self.add_scan_log(result, f"Tarama hatası: {e}", "error")
        
        finally:
            await self.post_scan_cleanup()
        
        return result
    
    def _extract_hostname(self, target_url: str) -> str:
        """URL'den hostname'i çıkarır"""
        from urllib.parse import urlparse
        parsed = urlparse(target_url)
        return parsed.netloc or parsed.path
    
    async def _get_host_information(self, result: ScanResult, hostname: str):
        """Shodan'dan host bilgilerini alır"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_base_url}{self.endpoints['host'].format(hostname)}"
                params = {"key": self.api_key}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        host_data = await response.json()
                        await self._process_host_data(result, host_data, hostname)
                    else:
                        self.add_scan_log(result, f"Host bilgisi alınamadı: HTTP {response.status}", "warning")
                        
        except Exception as e:
            self.add_scan_log(result, f"Host bilgisi alma hatası: {e}", "error")
    
    async def _search_host_information(self, result: ScanResult, hostname: str):
        """Shodan'da host araması yapar"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_base_url}{self.endpoints['search']}"
                params = {
                    "key": self.api_key,
                    "query": f"hostname:{hostname}",
                    "facets": "port,product,os"
                }
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        search_data = await response.json()
                        await self._process_search_data(result, search_data, hostname)
                    else:
                        self.add_scan_log(result, f"Search sonucu alınamadı: HTTP {response.status}", "warning")
                        
        except Exception as e:
            self.add_scan_log(result, f"Search hatası: {e}", "error")
    
    async def _process_host_data(self, result: ScanResult, host_data: Dict[str, Any], hostname: str):
        """Host verilerini işler ve güvenlik açıklarını tespit eder"""
        try:
            # Port bilgileri
            ports = host_data.get("ports", [])
            for port in ports:
                await self._analyze_port_security(result, port, hostname, host_data)
            
            # OS bilgisi
            os_info = host_data.get("os", "")
            if os_info:
                await self._analyze_os_security(result, os_info, hostname)
            
            # Product bilgileri
            data = host_data.get("data", [])
            for item in data:
                product = item.get("product", "")
                if product:
                    await self._analyze_product_security(result, product, hostname, item)
                    
        except Exception as e:
            self.add_scan_log(result, f"Host veri işleme hatası: {e}", "error")
    
    async def _process_search_data(self, result: ScanResult, search_data: Dict[str, Any], hostname: str):
        """Search verilerini işler"""
        try:
            matches = search_data.get("matches", [])
            
            for match in matches:
                # Port bilgisi
                port = match.get("port", 0)
                if port:
                    await self._analyze_port_security(result, port, hostname, match)
                
                # Product bilgisi
                product = match.get("product", "")
                if product:
                    await self._analyze_product_security(result, product, hostname, match)
                    
        except Exception as e:
            self.add_scan_log(result, f"Search veri işleme hatası: {e}", "error")
    
    async def _analyze_port_security(self, result: ScanResult, port: int, hostname: str, data: Dict[str, Any]):
        """Port güvenlik analizi yapar"""
        try:
            # Bilinen güvenlik açıkları
            port_vulns = {
                21: {"service": "FTP", "severity": "medium", "description": "FTP servisi açık - anonymous login kontrol edilmeli"},
                22: {"service": "SSH", "severity": "low", "description": "SSH servisi açık - güçlü şifreleme kontrol edilmeli"},
                23: {"service": "Telnet", "severity": "high", "description": "Telnet servisi açık - şifrelenmemiş trafik"},
                25: {"service": "SMTP", "severity": "medium", "description": "SMTP servisi açık - spam koruması kontrol edilmeli"},
                53: {"service": "DNS", "severity": "low", "description": "DNS servisi açık - zone transfer kontrol edilmeli"},
                80: {"service": "HTTP", "severity": "low", "description": "HTTP servisi açık - HTTPS'e yönlendirme önerilir"},
                110: {"service": "POP3", "severity": "medium", "description": "POP3 servisi açık - şifrelenmemiş trafik"},
                143: {"service": "IMAP", "severity": "medium", "description": "IMAP servisi açık - şifrelenmemiş trafik"},
                443: {"service": "HTTPS", "severity": "low", "description": "HTTPS servisi açık - sertifika kontrol edilmeli"},
                1433: {"service": "MSSQL", "severity": "high", "description": "MSSQL servisi açık - güçlü kimlik doğrulama gerekli"},
                3306: {"service": "MySQL", "severity": "high", "description": "MySQL servisi açık - güçlü kimlik doğrulama gerekli"},
                3389: {"service": "RDP", "severity": "high", "description": "RDP servisi açık - güçlü kimlik doğrulama gerekli"},
                5432: {"service": "PostgreSQL", "severity": "high", "description": "PostgreSQL servisi açık - güçlü kimlik doğrulama gerekli"},
                5900: {"service": "VNC", "severity": "high", "description": "VNC servisi açık - güçlü kimlik doğrulama gerekli"},
                6379: {"service": "Redis", "severity": "high", "description": "Redis servisi açık - kimlik doğrulama kontrol edilmeli"},
                27017: {"service": "MongoDB", "severity": "high", "description": "MongoDB servisi açık - kimlik doğrulama kontrol edilmeli"}
            }
            
            if port in port_vulns:
                vuln_info = port_vulns[port]
                
                vuln = Vulnerability(
                    title=f"Açık Port: {port} - {vuln_info['service']}",
                    description=vuln_info['description'],
                    severity=vuln_info['severity'],
                    location=f"{hostname}:{port}",
                    evidence=f"Port {port} açık, Servis: {vuln_info['service']}"
                )
                
                self.add_vulnerability(result, vuln)
                
                # Log ekle
                self.add_scan_log(
                    result, 
                    f"Port güvenlik açığı tespit edildi: {port} - {vuln_info['service']} ({vuln_info['severity']})"
                )
                
        except Exception as e:
            self.add_scan_log(result, f"Port güvenlik analizi hatası: {e}", "warning")
    
    async def _analyze_os_security(self, result: ScanResult, os_info: str, hostname: str):
        """OS güvenlik analizi yapar"""
        try:
            # Eski OS versiyonları için güvenlik uyarıları
            old_os_patterns = [
                (r"Windows.*XP", "Windows XP - Desteklenmeyen OS, güvenlik güncellemeleri mevcut değil"),
                (r"Windows.*Vista", "Windows Vista - Desteklenmeyen OS, güvenlik güncellemeleri mevcut değil"),
                (r"Windows.*7", "Windows 7 - EOL, güvenlik güncellemeleri sınırlı"),
                (r"Ubuntu.*1[0-6]", "Eski Ubuntu versiyonu - güvenlik güncellemeleri kontrol edilmeli"),
                (r"CentOS.*6", "CentOS 6 - EOL, güvenlik güncellemeleri mevcut değil")
            ]
            
            for pattern, description in old_os_patterns:
                if re.search(pattern, os_info, re.IGNORECASE):
                    vuln = Vulnerability(
                        title=f"Eski OS Versiyonu: {os_info}",
                        description=description,
                        severity="high",
                        location=hostname,
                        evidence=f"OS: {os_info}"
                    )
                    
                    self.add_vulnerability(result, vuln)
                    
                    # Log ekle
                    self.add_scan_log(
                        result, 
                        f"OS güvenlik açığı tespit edildi: {os_info} - {description}"
                    )
                    break
                    
        except Exception as e:
            self.add_scan_log(result, f"OS güvenlik analizi hatası: {e}", "warning")
    
    async def _analyze_product_security(self, result: ScanResult, product: str, hostname: str, data: Dict[str, Any]):
        """Product güvenlik analizi yapar"""
        try:
            # Bilinen güvenlik açıkları olan ürünler
            vulnerable_products = {
                "apache": {"severity": "medium", "description": "Apache web server - güvenlik güncellemeleri kontrol edilmeli"},
                "nginx": {"severity": "medium", "description": "Nginx web server - güvenlik güncellemeleri kontrol edilmeli"},
                "iis": {"severity": "medium", "description": "IIS web server - güvenlik güncellemeleri kontrol edilmeli"},
                "tomcat": {"severity": "medium", "description": "Tomcat application server - güvenlik güncellemeleri kontrol edilmeli"},
                "jboss": {"severity": "medium", "description": "JBoss application server - güvenlik güncellemeleri kontrol edilmeli"},
                "weblogic": {"severity": "medium", "description": "WebLogic application server - güvenlik güncellemeleri kontrol edilmeli"},
                "websphere": {"severity": "medium", "description": "WebSphere application server - güvenlik güncellemeleri kontrol edilmeli"}
            }
            
            product_lower = product.lower()
            
            for vuln_product, vuln_info in vulnerable_products.items():
                if vuln_product in product_lower:
                    vuln = Vulnerability(
                        title=f"Web Server: {product}",
                        description=vuln_info['description'],
                        severity=vuln_info['severity'],
                        location=hostname,
                        evidence=f"Product: {product}"
                    )
                    
                    self.add_vulnerability(result, vuln)
                    
                    # Log ekle
                    self.add_scan_log(
                        result, 
                        f"Product güvenlik açığı tespit edildi: {product} ({vuln_info['severity']})"
                    )
                    break
                    
        except Exception as e:
            self.add_scan_log(result, f"Product güvenlik analizi hatası: {e}", "warning")
    
    async def _analyze_security_issues(self, result: ScanResult, hostname: str):
        """Genel güvenlik açıklarını analiz eder"""
        try:
            # Shodan'dan ek güvenlik bilgileri al
            await self._get_additional_security_info(result, hostname)
            
        except Exception as e:
            self.add_scan_log(result, f"Güvenlik analizi hatası: {e}", "error")
    
    async def _get_additional_security_info(self, result: ScanResult, hostname: str):
        """Ek güvenlik bilgilerini alır"""
        try:
            # Burada Shodan'dan ek güvenlik bilgileri alınabilir
            # Örneğin: SSL sertifika bilgileri, güvenlik açığı veritabanları, vb.
            pass
            
        except Exception as e:
            self.add_scan_log(result, f"Ek güvenlik bilgisi alma hatası: {e}", "warning")
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        open_ports = set()
        services = set()
        
        for vuln in result.vulnerabilities:
            if "Port:" in vuln.title:
                port_match = re.search(r'Port: (\d+)', vuln.title)
                if port_match:
                    open_ports.add(port_match.group(1))
            
            if vuln.evidence and "Servis:" in vuln.evidence:
                service_match = re.search(r'Servis: (\w+)', vuln.evidence)
                if service_match:
                    services.add(service_match.group(1))
        
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for vuln in result.vulnerabilities:
            severity_counts[vuln.severity] += 1
        
        return {
            "total_vulnerabilities": len(result.vulnerabilities),
            "open_ports": len(open_ports),
            "services_detected": len(services),
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
