"""
SQLMap SQL Injection Tarayıcısı
SQL Injection güvenlik açıklarını tespit eder
"""

import asyncio
import subprocess
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class SQLMapScanner(BaseScanner):
    """SQLMap kullanarak SQL Injection güvenlik açıklarını tespit eden tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("SQLMap Scanner", config)
        self.sqlmap_path = config.get("sqlmap_path", "sqlmap") if config else "sqlmap"
        
        # SQLMap tarama seçenekleri
        self.scan_types = {
            "quick": ["--batch", "--random-agent", "--level", "1"],
            "standard": ["--batch", "--random-agent", "--level", "3"],
            "full": ["--batch", "--random-agent", "--level", "5", "--risk", "3"],
            "custom": []
        }
        
        # SQL Injection teknikleri
        self.techniques = [
            "B",  # Boolean-based blind
            "E",  # Error-based
            "U",  # Union query-based
            "S",  # Stacked queries
            "T",  # Time-based blind
            "Q"   # Inline queries
        ]
    
    async def validate_target(self, target_url: str) -> bool:
        """Hedef URL'nin geçerli olup olmadığını kontrol eder"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(target_url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    async def scan(self, target_url: str, options: Dict[str, Any] = None) -> ScanResult:
        """SQLMap taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "standard")
        techniques = options.get("techniques", self.techniques)
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"SQLMap taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # SQLMap komutunu oluştur
            sqlmap_args = self._build_sqlmap_command(target_url, scan_type, techniques, options)
            self.add_scan_log(result, f"SQLMap komutu: {' '.join(sqlmap_args)}")
            
            # SQLMap taramasını çalıştır
            scan_output = await self._run_sqlmap_scan(sqlmap_args)
            
            # Sonuçları parse et
            await self._parse_sqlmap_results(result, scan_output, target_url)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"SQLMap taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            self.add_scan_log(result, f"Tarama hatası: {e}", "error")
        
        finally:
            await self.post_scan_cleanup()
        
        return result
    
    def _build_sqlmap_command(self, target_url: str, scan_type: str, techniques: List[str], options: Dict[str, Any]) -> List[str]:
        """SQLMap komutunu oluşturur"""
        base_args = [self.sqlmap_path]
        
        # Target URL
        base_args.extend(["-u", target_url])
        
        # Scan type seçenekleri
        if scan_type in self.scan_types:
            base_args.extend(self.scan_types[scan_type])
        
        # Teknikler
        if techniques:
            base_args.extend(["--technique", "".join(techniques)])
        
        # Form alanları
        if options.get("forms"):
            base_args.append("--forms")
        
        # Crawl
        if options.get("crawl"):
            base_args.extend(["--crawl", str(options["crawl"])])
        
        # Database
        if options.get("dbms"):
            base_args.extend(["--dbms", options["dbms"]])
        
        # Output format
        base_args.extend(["--output-dir", "/tmp/sqlmap_output"])
        
        # Verbose
        base_args.append("--verbose")
        
        return base_args
    
    async def _run_sqlmap_scan(self, sqlmap_args: List[str]) -> str:
        """SQLMap taramasını çalıştırır"""
        try:
            process = await asyncio.create_subprocess_exec(
                *sqlmap_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0 and process.returncode != 1:  # SQLMap başarısız taramalarda 1 döner
                raise Exception(f"SQLMap hatası: {stderr.decode()}")
            
            return stdout.decode()
            
        except Exception as e:
            raise Exception(f"SQLMap çalıştırma hatası: {e}")
    
    async def _parse_sqlmap_results(self, result: ScanResult, scan_output: str, target_url: str):
        """SQLMap çıktısını parse eder ve güvenlik açıklarını tespit eder"""
        try:
            # SQLMap çıktısında güvenlik açığı belirtilerini ara
            await self._check_for_sql_injection(result, scan_output, target_url)
            
            # Log dosyalarını kontrol et
            await self._check_sqlmap_logs(result, target_url)
            
        except Exception as e:
            self.add_scan_log(result, f"Sonuç parse hatası: {e}", "error")
    
    async def _check_for_sql_injection(self, result: ScanResult, scan_output: str, target_url: str):
        """SQLMap çıktısında SQL Injection belirtilerini arar"""
        try:
            # SQL Injection tespit edildi mi?
            if "sqlmap identified the following injection point" in scan_output.lower():
                await self._process_sql_injection_detection(result, scan_output, target_url)
            
            # Hata mesajları
            if "sql syntax" in scan_output.lower() or "mysql" in scan_output.lower():
                await self._process_sql_error_detection(result, scan_output, target_url)
            
            # Database bilgileri
            if "database:" in scan_output.lower():
                await self._process_database_info(result, scan_output, target_url)
                
        except Exception as e:
            self.add_scan_log(result, f"SQL Injection kontrol hatası: {e}", "error")
    
    async def _process_sql_injection_detection(self, result: ScanResult, scan_output: str, target_url: str):
        """SQL Injection tespitini işler"""
        try:
            # Injection point bilgilerini çıkar
            injection_match = re.search(
                r"sqlmap identified the following injection point\(s\):(.*?)parameter:",
                scan_output,
                re.DOTALL | re.IGNORECASE
            )
            
            if injection_match:
                injection_info = injection_match.group(1)
                
                # Parameter bilgisini çıkar
                param_match = re.search(r"parameter: ([^\s]+)", scan_output, re.IGNORECASE)
                parameter = param_match.group(1) if param_match else "Unknown"
                
                # Type bilgisini çıkar
                type_match = re.search(r"type: ([^\s]+)", scan_output, re.IGNORECASE)
                injection_type = type_match.group(1) if type_match else "Unknown"
                
                # Title bilgisini çıkar
                title_match = re.search(r"title: ([^\n]+)", scan_output, re.IGNORECASE)
                title = title_match.group(1) if title_match else "SQL Injection Detected"
                
                # Güvenlik açığı oluştur
                vuln = Vulnerability(
                    title=f"SQL Injection - {title}",
                    description=f"SQL Injection tespit edildi. Parameter: {parameter}, Type: {injection_type}",
                    severity="critical",
                    location=f"{target_url} (Parameter: {parameter})",
                    evidence=injection_info[:200] + "..." if len(injection_info) > 200 else injection_info,
                    payload=f"Parameter: {parameter}, Type: {injection_type}"
                )
                
                self.add_vulnerability(result, vuln)
                
                # Log ekle
                self.add_scan_log(
                    result, 
                    f"SQL Injection tespit edildi: {title} - Parameter: {parameter}, Type: {injection_type}"
                )
                
        except Exception as e:
            self.add_scan_log(result, f"SQL Injection işleme hatası: {e}", "warning")
    
    async def _process_sql_error_detection(self, result: ScanResult, scan_output: str, target_url: str):
        """SQL hata mesajlarını işler"""
        try:
            # SQL hata mesajlarını ara
            error_patterns = [
                r"sql syntax.*mysql",
                r"mysql.*error",
                r"oracle.*error",
                r"sql server.*error",
                r"postgresql.*error"
            ]
            
            for pattern in error_patterns:
                matches = re.findall(pattern, scan_output, re.IGNORECASE)
                for match in matches:
                    vuln = Vulnerability(
                        title="SQL Error Information Disclosure",
                        description="SQL hata mesajları tespit edildi. Bu durum güvenlik açığına işaret edebilir.",
                        severity="medium",
                        location=target_url,
                        evidence=match[:100] + "..." if len(match) > 100 else match,
                        payload="SQL Error Detection"
                    )
                    
                    self.add_vulnerability(result, vuln)
                    
                    # Log ekle
                    self.add_scan_log(
                        result, 
                        f"SQL hata mesajı tespit edildi: {match[:50]}..."
                    )
                    
        except Exception as e:
            self.add_scan_log(result, f"SQL hata işleme hatası: {e}", "warning")
    
    async def _process_database_info(self, result: ScanResult, scan_output: str, target_url: str):
        """Database bilgilerini işler"""
        try:
            # Database bilgilerini ara
            db_patterns = [
                r"database: ([^\n]+)",
                r"dbms: ([^\n]+)",
                r"back-end dbms: ([^\n]+)"
            ]
            
            for pattern in db_patterns:
                matches = re.findall(pattern, scan_output, re.IGNORECASE)
                for match in matches:
                    vuln = Vulnerability(
                        title="Database Information Disclosure",
                        description=f"Database bilgileri tespit edildi: {match}",
                        severity="low",
                        location=target_url,
                        evidence=f"Database: {match}",
                        payload="Database Enumeration"
                    )
                    
                    self.add_vulnerability(result, vuln)
                    
                    # Log ekle
                    self.add_scan_log(
                        result, 
                        f"Database bilgisi tespit edildi: {match}"
                    )
                    
        except Exception as e:
            self.add_scan_log(result, f"Database bilgi işleme hatası: {e}", "warning")
    
    async def _check_sqlmap_logs(self, result: ScanResult, target_url: str):
        """SQLMap log dosyalarını kontrol eder"""
        try:
            # Log dosyası yolu
            log_file = "/tmp/sqlmap_output/log"
            
            # Log dosyasını oku
            try:
                with open(log_file, 'r') as f:
                    log_content = f.read()
                    
                    # Log içeriğinde güvenlik açığı belirtilerini ara
                    if "injection point" in log_content.lower():
                        await self._process_log_injection_detection(result, log_content, target_url)
                        
            except FileNotFoundError:
                self.add_scan_log(result, "SQLMap log dosyası bulunamadı", "info")
                
        except Exception as e:
            self.add_scan_log(result, f"Log kontrol hatası: {e}", "warning")
    
    async def _process_log_injection_detection(self, result: ScanResult, log_content: str, target_url: str):
        """Log dosyasından injection tespitini işler"""
        try:
            # Log içeriğinde injection bilgilerini ara
            injection_lines = [line for line in log_content.split('\n') if 'injection' in line.lower()]
            
            for line in injection_lines:
                vuln = Vulnerability(
                    title="SQL Injection - Log Detection",
                    description="SQLMap log dosyasında SQL Injection tespit edildi",
                    severity="critical",
                    location=target_url,
                    evidence=line[:200] + "..." if len(line) > 200 else line,
                    payload="Log Analysis"
                )
                
                self.add_vulnerability(result, vuln)
                
                # Log ekle
                self.add_scan_log(
                    result, 
                    f"Log dosyasında SQL Injection tespit edildi: {line[:50]}..."
                )
                
        except Exception as e:
            self.add_scan_log(result, f"Log injection işleme hatası: {e}", "warning")
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        injection_types = set()
        parameters = set()
        
        for vuln in result.vulnerabilities:
            if "SQL Injection" in vuln.title:
                injection_types.add("SQL Injection")
                
                # Parameter bilgisini çıkar
                if vuln.payload and "Parameter:" in vuln.payload:
                    param_match = re.search(r"Parameter: ([^,]+)", vuln.payload)
                    if param_match:
                        parameters.add(param_match.group(1))
        
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
            "injection_types": len(injection_types),
            "affected_parameters": len(parameters),
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
