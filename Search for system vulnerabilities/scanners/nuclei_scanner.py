"""
Nuclei Template Tabanlı Zafiyet Tarayıcısı
Template tabanlı güvenlik açığı tespiti
"""

import asyncio
import subprocess
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class NucleiScanner(BaseScanner):
    """Nuclei kullanarak template tabanlı güvenlik açığı taraması yapan tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("Nuclei Scanner", config)
        self.nuclei_path = config.get("nuclei_path", "nuclei") if config else "nuclei"
        
        # Nuclei tarama seçenekleri
        self.scan_types = {
            "quick": ["-severity", "critical,high"],
            "standard": ["-severity", "critical,high,medium"],
            "full": ["-severity", "critical,high,medium,low"],
            "custom": []
        }
        
        # Template kategorileri
        self.template_categories = [
            "cves", "vulnerabilities", "misconfiguration", "exposures"
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
        """Nuclei taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "standard")
        templates = options.get("templates", self.template_categories)
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"Nuclei taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # Nuclei komutunu oluştur
            nuclei_args = self._build_nuclei_command(target_url, scan_type, templates, options)
            self.add_scan_log(result, f"Nuclei komutu: {' '.join(nuclei_args)}")
            
            # Nuclei taramasını çalıştır
            scan_output = await self._run_nuclei_scan(nuclei_args)
            
            # Sonuçları parse et
            await self._parse_nuclei_results(result, scan_output, target_url)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"Nuclei taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            self.add_scan_log(result, f"Tarama hatası: {e}", "error")
        
        finally:
            await self.post_scan_cleanup()
        
        return result
    
    def _build_nuclei_command(self, target_url: str, scan_type: str, templates: List[str], options: Dict[str, Any]) -> List[str]:
        """Nuclei komutunu oluşturur"""
        base_args = [self.nuclei_path]
        
        # JSON output
        base_args.extend(["-json"])
        
        # Scan type seçenekleri
        if scan_type in self.scan_types:
            base_args.extend(self.scan_types[scan_type])
        
        # Template kategorileri
        for template in templates:
            base_args.extend(["-t", template])
        
        # Rate limiting
        if options.get("rate_limit"):
            base_args.extend(["-rate-limit", str(options["rate_limit"])])
        
        # Timeout
        if options.get("timeout"):
            base_args.extend(["-timeout", str(options["timeout"])])
        
        # Concurrency
        if options.get("concurrency"):
            base_args.extend(["-c", str(options["concurrency"])])
        
        # Target ekle
        base_args.append(target_url)
        
        return base_args
    
    async def _run_nuclei_scan(self, nuclei_args: List[str]) -> str:
        """Nuclei taramasını çalıştırır"""
        try:
            process = await asyncio.create_subprocess_exec(
                *nuclei_args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0 and process.returncode != 1:  # Nuclei başarısız taramalarda 1 döner
                raise Exception(f"Nuclei hatası: {stderr.decode()}")
            
            return stdout.decode()
            
        except Exception as e:
            raise Exception(f"Nuclei çalıştırma hatası: {e}")
    
    async def _parse_nuclei_results(self, result: ScanResult, scan_output: str, target_url: str):
        """Nuclei JSON çıktısını parse eder ve güvenlik açıklarını tespit eder"""
        try:
            lines = scan_output.strip().split('\n')
            
            for line in lines:
                if line.strip():
                    try:
                        vuln_data = json.loads(line)
                        await self._process_vulnerability(result, vuln_data, target_url)
                    except json.JSONDecodeError:
                        # JSON olmayan satırları log'la
                        if "error" in line.lower() or "warning" in line.lower():
                            self.add_scan_log(result, line, "warning")
                        continue
                        
        except Exception as e:
            self.add_scan_log(result, f"Sonuç parse hatası: {e}", "error")
    
    async def _process_vulnerability(self, result: ScanResult, vuln_data: Dict[str, Any], target_url: str):
        """Tek bir güvenlik açığını işler"""
        try:
            # Nuclei çıktısından güvenlik açığı bilgilerini çıkar
            title = vuln_data.get("info", {}).get("name", "Unknown Vulnerability")
            description = vuln_data.get("info", {}).get("description", "")
            severity = vuln_data.get("info", {}).get("severity", "medium").lower()
            cve_id = vuln_data.get("info", {}).get("cve", "")
            cvss_score = vuln_data.get("info", {}).get("cvss", {}).get("score", 0)
            
            # Location bilgisi
            location = vuln_data.get("matched-at", target_url)
            
            # Evidence ve payload
            evidence = vuln_data.get("extracted-results", "")
            payload = vuln_data.get("request", "")
            
            # Template bilgisi
            template_id = vuln_data.get("template-id", "")
            template_path = vuln_data.get("template-path", "")
            
            # Güvenlik açığı oluştur
            vuln = Vulnerability(
                title=title,
                description=description or f"Template: {template_id}",
                severity=severity,
                cve_id=cve_id if cve_id else None,
                cvss_score=float(cvss_score) if cvss_score else None,
                location=location,
                evidence=evidence or f"Template: {template_path}",
                payload=payload if payload else None
            )
            
            self.add_vulnerability(result, vuln)
            
            # Log ekle
            self.add_scan_log(
                result, 
                f"Güvenlik açığı tespit edildi: {title} ({severity}) - {template_id}"
            )
            
        except Exception as e:
            self.add_scan_log(result, f"Güvenlik açığı işleme hatası: {e}", "warning")
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        template_counts = {}
        cve_counts = 0
        
        for vuln in result.vulnerabilities:
            # Template sayılarını hesapla
            if vuln.evidence and "Template:" in vuln.evidence:
                template_name = vuln.evidence.split("Template:")[-1].strip()
                template_counts[template_name] = template_counts.get(template_name, 0) + 1
            
            # CVE sayısını hesapla
            if vuln.cve_id:
                cve_counts += 1
        
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
            "templates_used": len(template_counts),
            "cve_vulnerabilities": cve_counts,
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
