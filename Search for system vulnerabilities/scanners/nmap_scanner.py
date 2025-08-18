"""
Nmap Port ve Servis Tarayıcısı
Port taraması ve servis tespiti
"""

import asyncio
import subprocess
import re
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class NmapScanner(BaseScanner):
    """Nmap kullanarak port ve servis taraması yapan tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("Nmap Scanner", config)
        self.nmap_path = config.get("nmap_path", "nmap") if config else "nmap"
        
        # Port tarama seçenekleri
        self.scan_types = {
            "quick": "-F -T4",  # Hızlı tarama
            "standard": "-sS -sV -O",  # Standart tarama
            "full": "-p- -sS -sV -O -A",  # Tam tarama
            "stealth": "-sS -sV -T2"  # Gizli tarama
        }
    
    async def validate_target(self, target_url: str) -> bool:
        """Hedef URL'nin geçerli olup olmadığını kontrol eder"""
        try:
            # URL'den hostname'i çıkar
            from urllib.parse import urlparse
            parsed = urlparse(target_url)
            hostname = parsed.netloc or parsed.path
            
            # Basit hostname validasyonu
            return bool(hostname and len(hostname) > 0)
        except Exception:
            return False
    
    async def scan(self, target_url: str, options: Dict[str, Any] = None) -> ScanResult:
        """Nmap taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "quick")
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"Nmap taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # Hostname'i çıkar
            hostname = self._extract_hostname(target_url)
            self.add_scan_log(result, f"Hedef hostname: {hostname}")
            
            # Nmap komutunu oluştur
            nmap_args = self._build_nmap_command(hostname, scan_type, options)
            self.add_scan_log(result, f"Nmap komutu: {' '.join(nmap_args)}")
            
            # Nmap taramasını çalıştır
            scan_output = await self._run_nmap_scan(nmap_args)
            
            # Sonuçları parse et
            await self._parse_nmap_results(result, scan_output, hostname)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"Nmap taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
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
    
    def _build_nmap_command(self, hostname: str, scan_type: str, options: Dict[str, Any]) -> List[str]:
        """Nmap komutunu oluşturur"""
        base_args = [self.nmap_path]
        
        # Scan type seçenekleri
        if scan_type in self.scan_types:
            base_args.extend(self.scan_types[scan_type].split())
        
        # Ek seçenekler
        if options.get("output_xml"):
            base_args.extend(["-oX", "-"])
        
        # Hostname ekle
        base_args.append(hostname)
        
        return base_args
    
    async def _run_nmap_scan(self, nmap_args: List[str]) -> str:
        """Nmap taramasını çalıştırır"""
        try:
            process = await asyncio.create_subprocess_exec(
                *nmap_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Nmap hatası: {stderr.decode()}")
            
            return stdout.decode()
            
        except Exception as e:
            raise Exception(f"Nmap çalıştırma hatası: {e}")
    
    async def _parse_nmap_results(self, result: ScanResult, scan_output: str, hostname: str):
        """Nmap çıktısını parse eder ve güvenlik açıklarını tespit eder"""
        try:
            # XML çıktısını parse et
            if scan_output.strip().startswith("<?xml"):
                await self._parse_xml_output(result, scan_output, hostname)
            else:
                await self._parse_text_output(result, scan_output, hostname)
                
        except Exception as e:
            self.add_scan_log(result, f"Sonuç parse hatası: {e}", "error")
    
    async def _parse_xml_output(self, result: ScanResult, xml_output: str, hostname: str):
        """XML çıktısını parse eder"""
        try:
            root = ET.fromstring(xml_output)
            
            # Host bilgilerini bul
            for host in root.findall(".//host"):
                # Port bilgilerini işle
                for port in host.findall(".//port"):
                    await self._analyze_port(result, port, hostname)
                
                # OS bilgilerini işle
                os_info = host.find(".//os")
                if os_info is not None:
                    await self._analyze_os_info(result, os_info, hostname)
                    
        except Exception as e:
            self.add_scan_log(result, f"XML parse hatası: {e}", "error")
    
    async def _parse_text_output(self, result: ScanResult, text_output: str, hostname: str):
        """Text çıktısını parse eder"""
        try:
            lines = text_output.split('\n')
            
            for line in lines:
                # Port bilgilerini ara
                port_match = re.search(r'(\d+)/(\w+)\s+(\w+)\s+(.+)', line)
                if port_match:
                    port_num, protocol, state, service = port_match.groups()
                    await self._analyze_text_port(result, port_num, protocol, state, service, hostname)
                    
        except Exception as e:
            self.add_scan_log(result, f"Text parse hatası: {e}", "error")
    
    async def _analyze_port(self, result: ScanResult, port_elem, hostname: str):
        """Port bilgisini analiz eder ve güvenlik açıklarını tespit eder"""
        try:
            port_id = port_elem.get("portid")
            protocol = port_elem.get("protocol")
            state = port_elem.find("state")
            service = port_elem.find("service")
            
            if state is not None and state.get("state") == "open":
                # Açık port tespit edildi
                port_info = f"{port_id}/{protocol}"
                
                # Servis bilgisi
                service_name = "unknown"
                service_version = ""
                if service is not None:
                    service_name = service.get("name", "unknown")
                    service_version = service.get("version", "")
                
                # Güvenlik açığı tespiti
                await self._check_port_vulnerabilities(
                    result, hostname, port_info, service_name, service_version
                )
                
        except Exception as e:
            self.add_scan_log(result, f"Port analiz hatası: {e}", "warning")
    
    async def _analyze_text_port(self, result: ScanResult, port_num: str, protocol: str, state: str, service: str, hostname: str):
        """Text çıktısından port bilgisini analiz eder"""
        if state.lower() == "open":
            port_info = f"{port_num}/{protocol}"
            
            # Servis adını çıkar
            service_name = service.split()[0] if service else "unknown"
            
            await self._check_port_vulnerabilities(
                result, hostname, port_info, service_name, ""
            )
    
    async def _analyze_os_info(self, result: ScanResult, os_elem, hostname: str):
        """OS bilgisini analiz eder"""
        try:
            os_name = os_elem.find(".//osname")
            os_version = os_elem.find(".//osversion")
            
            if os_name is not None:
                os_info = f"{os_name.text}"
                if os_version is not None:
                    os_info += f" {os_version.text}"
                
                # OS tabanlı güvenlik açıkları
                await self._check_os_vulnerabilities(result, hostname, os_info)
                
        except Exception as e:
            self.add_scan_log(result, f"OS analiz hatası: {e}", "warning")
    
    async def _check_port_vulnerabilities(self, result: ScanResult, hostname: str, port_info: str, service_name: str, service_version: str):
        """Port tabanlı güvenlik açıklarını kontrol eder"""
        # Bilinen güvenlik açıkları
        known_vulns = {
            "21": {"service": "ftp", "severity": "medium", "description": "FTP servisi açık - anonymous login kontrol edilmeli"},
            "22": {"service": "ssh", "severity": "low", "description": "SSH servisi açık - güçlü şifreleme kontrol edilmeli"},
            "23": {"service": "telnet", "severity": "high", "description": "Telnet servisi açık - şifrelenmemiş trafik"},
            "25": {"service": "smtp", "severity": "medium", "description": "SMTP servisi açık - spam koruması kontrol edilmeli"},
            "53": {"service": "dns", "severity": "low", "description": "DNS servisi açık - zone transfer kontrol edilmeli"},
            "80": {"service": "http", "severity": "low", "description": "HTTP servisi açık - HTTPS'e yönlendirme önerilir"},
            "110": {"service": "pop3", "severity": "medium", "description": "POP3 servisi açık - şifrelenmemiş trafik"},
            "143": {"service": "imap", "severity": "medium", "description": "IMAP servisi açık - şifrelenmemiş trafik"},
            "443": {"service": "https", "severity": "low", "description": "HTTPS servisi açık - sertifika kontrol edilmeli"},
            "1433": {"service": "mssql", "severity": "high", "description": "MSSQL servisi açık - güçlü kimlik doğrulama gerekli"},
            "3306": {"service": "mysql", "severity": "high", "description": "MySQL servisi açık - güçlü kimlik doğrulama gerekli"},
            "3389": {"service": "rdp", "severity": "high", "description": "RDP servisi açık - güçlü kimlik doğrulama gerekli"},
            "5432": {"service": "postgresql", "severity": "high", "description": "PostgreSQL servisi açık - güçlü kimlik doğrulama gerekli"},
            "5900": {"service": "vnc", "severity": "high", "description": "VNC servisi açık - güçlü kimlik doğrulama gerekli"},
            "6379": {"service": "redis", "severity": "high", "description": "Redis servisi açık - kimlik doğrulama kontrol edilmeli"},
            "27017": {"service": "mongodb", "severity": "high", "description": "MongoDB servisi açık - kimlik doğrulama kontrol edilmeli"}
        }
        
        port_num = port_info.split('/')[0]
        
        if port_num in known_vulns:
            vuln_info = known_vulns[port_num]
            
            vuln = Vulnerability(
                title=f"Açık Port: {port_info} - {vuln_info['service'].upper()}",
                description=vuln_info['description'],
                severity=vuln_info['severity'],
                location=f"{hostname}:{port_info}",
                evidence=f"Port {port_info} açık, Servis: {service_name} {service_version}".strip()
            )
            self.add_vulnerability(result, vuln)
        
        # Genel güvenlik kontrolleri
        if service_name.lower() in ["http", "https"]:
            await self._check_web_service_security(result, hostname, port_info, service_name)
    
    async def _check_web_service_security(self, result: ScanResult, hostname: str, port_info: str, service_name: str):
        """Web servisi güvenlik kontrollerini yapar"""
        # HTTP servisi için ek kontroller
        if service_name.lower() == "http":
            vuln = Vulnerability(
                title="HTTP Servisi - Şifrelenmemiş Trafik",
                description="HTTP servisi şifrelenmemiş trafik kullanıyor. HTTPS'e yönlendirme önerilir.",
                severity="medium",
                location=f"{hostname}:{port_info}",
                evidence=f"HTTP servisi {port_info} portunda çalışıyor"
            )
            self.add_vulnerability(result, vuln)
    
    async def _check_os_vulnerabilities(self, result: ScanResult, hostname: str, os_info: str):
        """OS tabanlı güvenlik açıklarını kontrol eder"""
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
                break
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        open_ports = []
        services = set()
        
        for vuln in result.vulnerabilities:
            if "Port:" in vuln.title:
                port_match = re.search(r'Port: (\d+/\w+)', vuln.title)
                if port_match:
                    open_ports.append(port_match.group(1))
            
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
            "open_ports": len(set(open_ports)),
            "services_detected": len(services),
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
