"""
Nikto Web Server Güvenlik Tarayıcısı
Web server güvenlik açıklarını tespit eder
"""

import asyncio
import subprocess
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class NiktoScanner(BaseScanner):
    """Nikto kullanarak web server güvenlik taraması yapan tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("Nikto Scanner", config)
        self.nikto_path = config.get("nikto_path", "nikto") if config else "nikto"
        
        # Nikto tarama seçenekleri
        self.scan_types = {
            "quick": ["-Tuning", "1,2,3,4,5,6,7,8,9,0,a,b,c"],
            "standard": ["-Tuning", "1,2,3,4,5,6,7,8,9,0,a,b,c,x"],
            "full": ["-Tuning", "1,2,3,4,5,6,7,8,9,0,a,b,c,x"],
            "custom": []
        }
        
        # Nikto tuning seçenekleri
        self.tuning_options = {
            "1": "File Upload",
            "2": "Misconfigurations / Default Files",
            "3": "Information Disclosure",
            "4": "Misc (attempted password brute force, etc.)",
            "5": "Remote File Retrieval - Inside Web Root",
            "6": "Denial of Service",
            "7": "WebService",
            "8": "Reverse Proxy",
            "9": "Multiple Index",
            "0": "Reverse Proxy",
            "a": "Authentication Bypass",
            "b": "Software Identification",
            "c": "Remote Source Inclusion",
            "x": "Remote File Retrieval - Outside Web Root"
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
        """Nikto taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "standard")
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"Nikto taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # Hostname'i çıkar
            hostname = self._extract_hostname(target_url)
            self.add_scan_log(result, f"Hedef hostname: {hostname}")
            
            # Nikto komutunu oluştur
            nikto_args = self._build_nikto_command(hostname, scan_type, options)
            self.add_scan_log(result, f"Nikto komutu: {' '.join(nikto_args)}")
            
            # Nikto taramasını çalıştır
            scan_output = await self._run_nikto_scan(nikto_args)
            
            # Sonuçları parse et
            await self._parse_nikto_results(result, scan_output, hostname)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"Nikto taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
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
    
    def _build_nikto_command(self, hostname: str, scan_type: str, options: Dict[str, Any]) -> List[str]:
        """Nikto komutunu oluşturur"""
        base_args = [self.nikto_path]
        
        # Host
        base_args.extend(["-h", hostname])
        
        # Scan type seçenekleri
        if scan_type in self.scan_types:
            base_args.extend(self.scan_types[scan_type])
        
        # Port
        if options.get("port"):
            base_args.extend(["-p", str(options["port"])])
        
        # SSL
        if options.get("ssl"):
            base_args.append("-ssl")
        
        # User agent
        if options.get("user_agent"):
            base_args.extend(["-useragent", options["user_agent"]])
        else:
            base_args.extend(["-useragent", "Mozilla/5.0 (Nikto Scanner)"])
        
        # Timeout
        if options.get("timeout"):
            base_args.extend(["-timeout", str(options["timeout"])])
        
        # Format
        base_args.extend(["-Format", "txt"])
        
        return base_args
    
    async def _run_nikto_scan(self, nikto_args: List[str]) -> str:
        """Nikto taramasını çalıştırır"""
        try:
            process = await asyncio.create_subprocess_exec(
                *nikto_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0 and process.returncode != 1:  # Nikto başarısız taramalarda 1 döner
                raise Exception(f"Nikto hatası: {stderr.decode()}")
            
            return stdout.decode()
            
        except Exception as e:
            raise Exception(f"Nikto çalıştırma hatası: {e}")
    
    async def _parse_nikto_results(self, result: ScanResult, scan_output: str, hostname: str):
        """Nikto çıktısını parse eder ve güvenlik açıklarını tespit eder"""
        try:
            lines = scan_output.split('\n')
            
            for line in lines:
                if line.strip():
                    await self._process_nikto_line(result, line, hostname)
                    
        except Exception as e:
            self.add_scan_log(result, f"Sonuç parse hatası: {e}", "error")
    
    async def _process_nikto_line(self, result: ScanResult, line: str, hostname: str):
        """Tek bir Nikto satırını işler"""
        try:
            # Nikto çıktı formatını parse et
            if line.startswith("+ "):
                await self._process_vulnerability_line(result, line, hostname)
            elif line.startswith("- "):
                await self._process_info_line(result, line, hostname)
            elif line.startswith("* "):
                await self._process_warning_line(result, line, hostname)
                
        except Exception as e:
            self.add_scan_log(result, f"Satır işleme hatası: {e}", "warning")
    
    async def _process_vulnerability_line(self, result: ScanResult, line: str, hostname: str):
        """Güvenlik açığı satırını işler"""
        try:
            # + işaretini kaldır
            vuln_line = line[2:].strip()
            
            # Güvenlik açığı bilgilerini çıkar
            if ":" in vuln_line:
                title, details = vuln_line.split(":", 1)
                title = title.strip()
                details = details.strip()
                
                # Severity belirle
                severity = self._determine_severity(title, details)
                
                # Güvenlik açığı oluştur
                vuln = Vulnerability(
                    title=title,
                    description=details,
                    severity=severity,
                    location=hostname,
                    evidence=line,
                    payload=details
                )
                
                self.add_vulnerability(result, vuln)
                
                # Log ekle
                self.add_scan_log(
                    result, 
                    f"Güvenlik açığı tespit edildi: {title} ({severity})"
                )
                
        except Exception as e:
            self.add_scan_log(result, f"Güvenlik açığı işleme hatası: {e}", "warning")
    
    async def _process_info_line(self, result: ScanResult, line: str, hostname: str):
        """Bilgi satırını işler"""
        try:
            # - işaretini kaldır
            info_line = line[2:].strip()
            
            # Bilgi mesajını log'la
            self.add_scan_log(result, f"Bilgi: {info_line}")
            
        except Exception as e:
            self.add_scan_log(result, f"Bilgi işleme hatası: {e}", "warning")
    
    async def _process_warning_line(self, result: ScanResult, line: str, hostname: str):
        """Uyarı satırını işler"""
        try:
            # * işaretini kaldır
            warning_line = line[2:].strip()
            
            # Uyarı mesajını log'la
            self.add_scan_log(result, f"Uyarı: {warning_line}", "warning")
            
        except Exception as e:
            self.add_scan_log(result, f"Uyarı işleme hatası: {e}", "warning")
    
    def _determine_severity(self, title: str, details: str) -> str:
        """Güvenlik açığı severity'sini belirler"""
        title_lower = title.lower()
        details_lower = details.lower()
        
        # Kritik güvenlik açıkları
        critical_keywords = [
            "remote code execution",
            "sql injection",
            "command injection",
            "file inclusion",
            "directory traversal",
            "buffer overflow",
            "privilege escalation"
        ]
        
        # Yüksek güvenlik açıkları
        high_keywords = [
            "cross-site scripting",
            "cross-site request forgery",
            "authentication bypass",
            "information disclosure",
            "session fixation",
            "weak encryption"
        ]
        
        # Orta güvenlik açıkları
        medium_keywords = [
            "directory listing",
            "default credentials",
            "missing security headers",
            "server information disclosure",
            "outdated software"
        ]
        
        # Kritik kontrol
        for keyword in critical_keywords:
            if keyword in title_lower or keyword in details_lower:
                return "critical"
        
        # Yüksek kontrol
        for keyword in high_keywords:
            if keyword in title_lower or keyword in details_lower:
                return "high"
        
        # Orta kontrol
        for keyword in medium_keywords:
            if keyword in title_lower or keyword in details_lower:
                return "medium"
        
        # Varsayılan olarak düşük
        return "low"
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        vulnerability_types = set()
        
        for vuln in result.vulnerabilities:
            # Güvenlik açığı türünü belirle
            vuln_type = self._categorize_vulnerability(vuln.title, vuln.description)
            vulnerability_types.add(vuln_type)
        
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
            "vulnerability_types": len(vulnerability_types),
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
    
    def _categorize_vulnerability(self, title: str, description: str) -> str:
        """Güvenlik açığını kategorize eder"""
        title_lower = title.lower()
        description_lower = description.lower()
        
        if any(keyword in title_lower or keyword in description_lower for keyword in ["sql", "injection"]):
            return "SQL Injection"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["xss", "cross-site scripting"]):
            return "Cross-Site Scripting"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["directory", "traversal"]):
            return "Directory Traversal"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["file", "inclusion"]):
            return "File Inclusion"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["authentication", "bypass"]):
            return "Authentication Bypass"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["information", "disclosure"]):
            return "Information Disclosure"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["default", "credentials"]):
            return "Default Credentials"
        elif any(keyword in title_lower or keyword in description_lower for keyword in ["outdated", "version"]):
            return "Outdated Software"
        else:
            return "Other"
