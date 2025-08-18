"""
OWASP ZAP Web Uygulama Güvenlik Tarayıcısı
Web uygulama güvenlik açıklarını tespit eder
"""

import asyncio
import aiohttp
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class ZAPScanner(BaseScanner):
    """OWASP ZAP kullanarak web uygulama güvenlik taraması yapan tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ZAP Scanner", config)
        
        # ZAP API konfigürasyonu
        self.zap_host = config.get("zap_host", "localhost") if config else "localhost"
        self.zap_port = config.get("zap_port", 8080) if config else 8080
        self.zap_api_key = config.get("zap_api_key", "") if config else ""
        
        # ZAP API endpoint'leri
        self.base_url = f"http://{self.zap_host}:{self.zap_port}"
        self.api_url = f"{self.base_url}/JSON"
        
        # Tarama seçenekleri
        self.scan_types = {
            "spider": "spider",
            "active": "active",
            "passive": "passive",
            "full": "full"
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
        """ZAP taraması gerçekleştirir"""
        options = options or {}
        scan_type = options.get("scan_type", "active")
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"ZAP taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # ZAP bağlantısını kontrol et
            if not await self._check_zap_connection():
                result.status = "failed"
                result.error_message = "ZAP bağlantısı kurulamadı"
                return result
            
            # Hedef URL'yi ZAP'a ekle
            context_id = await self._add_target_to_zap(target_url)
            if not context_id:
                result.status = "failed"
                result.error_message = "Hedef URL ZAP'a eklenemedi"
                return result
            
            self.add_scan_log(result, f"Hedef URL ZAP'a eklendi. Context ID: {context_id}")
            
            # Spider taraması (URL keşfi)
            if scan_type in ["spider", "active", "full"]:
                await self._run_spider_scan(result, target_url, context_id)
            
            # Active tarama (güvenlik açığı tespiti)
            if scan_type in ["active", "full"]:
                await self._run_active_scan(result, target_url, context_id)
            
            # Passive tarama (mevcut trafik analizi)
            if scan_type in ["passive", "full"]:
                await self._run_passive_scan(result, target_url, context_id)
            
            # Güvenlik açıklarını topla
            await self._collect_vulnerabilities(result, target_url, context_id)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"ZAP taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            self.add_scan_log(result, f"Tarama hatası: {e}", "error")
        
        finally:
            await self.post_scan_cleanup()
        
        return result
    
    async def _check_zap_connection(self) -> bool:
        """ZAP bağlantısını kontrol eder"""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/core/view/version"
                params = {"apikey": self.zap_api_key} if self.zap_api_key else {}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        version = data.get("version", "Unknown")
                        self.add_scan_log(ScanResult(), f"ZAP versiyonu: {version}")
                        return True
                    else:
                        return False
        except Exception as e:
            self.logger.error(f"ZAP bağlantı hatası: {e}")
            return False
    
    async def _add_target_to_zap(self, target_url: str) -> Optional[str]:
        """Hedef URL'yi ZAP'a ekler"""
        try:
            async with aiohttp.ClientSession() as session:
                # Context oluştur
                url = f"{self.api_url}/context/action/newContext"
                params = {"apikey": self.zap_api_key} if self.zap_api_key else {}
                data = {"contextName": f"scan_{int(time.time())}"}
                
                async with session.post(url, params=params, json=data) as response:
                    if response.status == 200:
                        context_data = await response.json()
                        context_id = context_data.get("contextId")
                        
                        if context_id:
                            # Hedef URL'yi context'e ekle
                            include_url = f"{self.api_url}/context/action/includeInContext"
                            include_data = {
                                "contextName": data["contextName"],
                                "regex": f".*{target_url}.*"
                            }
                            
                            async with session.post(include_url, params=params, json=include_data) as inc_response:
                                if inc_response.status == 200:
                                    return context_id
                
                return None
                
        except Exception as e:
            self.logger.error(f"Hedef URL ekleme hatası: {e}")
            return None
    
    async def _run_spider_scan(self, result: ScanResult, target_url: str, context_id: str):
        """Spider taraması çalıştırır"""
        try:
            self.add_scan_log(result, "Spider taraması başlatılıyor...")
            
            async with aiohttp.ClientSession() as session:
                # Spider taramasını başlat
                url = f"{self.api_url}/spider/action/scan"
                params = {"apikey": self.zap_api_key} if self.zap_api_key else {}
                data = {
                    "url": target_url,
                    "contextName": context_id,
                    "maxChildren": 10
                }
                
                async with session.post(url, params=params, json=data) as response:
                    if response.status == 200:
                        scan_data = await response.json()
                        scan_id = scan_data.get("scan")
                        
                        if scan_id:
                            # Spider taramasının tamamlanmasını bekle
                            await self._wait_for_spider_completion(result, scan_id)
                        else:
                            self.add_scan_log(result, "Spider taraması başlatılamadı", "warning")
                    else:
                        self.add_scan_log(result, "Spider taraması başlatılamadı", "warning")
                        
        except Exception as e:
            self.add_scan_log(result, f"Spider tarama hatası: {e}", "error")
    
    async def _wait_for_spider_completion(self, result: ScanResult, scan_id: str):
        """Spider taramasının tamamlanmasını bekler"""
        try:
            max_wait = 300  # 5 dakika
            wait_time = 0
            
            while wait_time < max_wait:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.api_url}/spider/view/status"
                    params = {"apikey": self.zap_api_key, "scanId": scan_id} if self.zap_api_key else {"scanId": scan_id}
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            status_data = await response.json()
                            status = status_data.get("status", "")
                            
                            if status == "100":
                                self.add_scan_log(result, "Spider taraması tamamlandı")
                                break
                            elif "error" in status.lower():
                                self.add_scan_log(result, f"Spider tarama hatası: {status}", "error")
                                break
                
                await asyncio.sleep(5)
                wait_time += 5
                
                if wait_time % 30 == 0:
                    self.add_scan_log(result, f"Spider taraması devam ediyor... ({wait_time}s)")
            
            if wait_time >= max_wait:
                self.add_scan_log(result, "Spider tarama zaman aşımı", "warning")
                
        except Exception as e:
            self.add_scan_log(result, f"Spider tamamlanma bekleme hatası: {e}", "error")
    
    async def _run_active_scan(self, result: ScanResult, target_url: str, context_id: str):
        """Active tarama çalıştırır"""
        try:
            self.add_scan_log(result, "Active tarama başlatılıyor...")
            
            async with aiohttp.ClientSession() as session:
                # Active taramayı başlat
                url = f"{self.api_url}/ascan/action/scan"
                params = {"apikey": self.zap_api_key} if self.zap_api_key else {}
                data = {
                    "url": target_url,
                    "contextName": context_id,
                    "scanPolicyName": "Default Policy"
                }
                
                async with session.post(url, params=params, json=data) as response:
                    if response.status == 200:
                        scan_data = await response.json()
                        scan_id = scan_data.get("scan")
                        
                        if scan_id:
                            # Active taramanın tamamlanmasını bekle
                            await self._wait_for_active_completion(result, scan_id)
                        else:
                            self.add_scan_log(result, "Active tarama başlatılamadı", "warning")
                    else:
                        self.add_scan_log(result, "Active tarama başlatılamadı", "warning")
                        
        except Exception as e:
            self.add_scan_log(result, f"Active tarama hatası: {e}", "error")
    
    async def _wait_for_active_completion(self, result: ScanResult, scan_id: str):
        """Active taramanın tamamlanmasını bekler"""
        try:
            max_wait = 600  # 10 dakika
            wait_time = 0
            
            while wait_time < max_wait:
                async with aiohttp.ClientSession() as session:
                    url = f"{self.api_url}/ascan/view/status"
                    params = {"apikey": self.zap_api_key, "scanId": scan_id} if self.zap_api_key else {"scanId": scan_id}
                    
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            status_data = await response.json()
                            status = status_data.get("status", "")
                            
                            if status == "100":
                                self.add_scan_log(result, "Active tarama tamamlandı")
                                break
                            elif "error" in status.lower():
                                self.add_scan_log(result, f"Active tarama hatası: {status}", "error")
                                break
                
                await asyncio.sleep(10)
                wait_time += 10
                
                if wait_time % 60 == 0:
                    self.add_scan_log(result, f"Active tarama devam ediyor... ({wait_time}s)")
            
            if wait_time >= max_wait:
                self.add_scan_log(result, "Active tarama zaman aşımı", "warning")
                
        except Exception as e:
            self.add_scan_log(result, f"Active tamamlanma bekleme hatası: {e}", "error")
    
    async def _run_passive_scan(self, result: ScanResult, target_url: str, context_id: str):
        """Passive tarama çalıştırır"""
        try:
            self.add_scan_log(result, "Passive tarama çalıştırılıyor...")
            
            # Passive tarama otomatik olarak çalışır
            # Sadece log ekle
            self.add_scan_log(result, "Passive tarama tamamlandı")
            
        except Exception as e:
            self.add_scan_log(result, f"Passive tarama hatası: {e}", "error")
    
    async def _collect_vulnerabilities(self, result: ScanResult, target_url: str, context_id: str):
        """Tespit edilen güvenlik açıklarını toplar"""
        try:
            async with aiohttp.ClientSession() as session:
                # Güvenlik açıklarını al
                url = f"{self.api_url}/core/view/alerts"
                params = {"apikey": self.zap_api_key, "baseurl": target_url} if self.zap_api_key else {"baseurl": target_url}
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        alerts_data = await response.json()
                        alerts = alerts_data.get("alerts", [])
                        
                        for alert in alerts:
                            await self._process_zap_alert(result, alert, target_url)
                    else:
                        self.add_scan_log(result, "Güvenlik açıkları alınamadı", "warning")
                        
        except Exception as e:
            self.add_scan_log(result, f"Güvenlik açığı toplama hatası: {e}", "error")
    
    async def _process_zap_alert(self, result: ScanResult, alert: Dict[str, Any], target_url: str):
        """ZAP alert'ini işler ve güvenlik açığına dönüştürür"""
        try:
            # Alert bilgilerini çıkar
            title = alert.get("name", "Unknown Vulnerability")
            description = alert.get("description", "")
            risk = alert.get("risk", "Medium").lower()
            confidence = alert.get("confidence", "Medium").lower()
            url = alert.get("url", target_url)
            evidence = alert.get("evidence", "")
            solution = alert.get("solution", "")
            
            # Risk seviyesini belirle
            severity_map = {
                "high": "high",
                "medium": "medium", 
                "low": "low",
                "informational": "low"
            }
            severity = severity_map.get(risk, "medium")
            
            # CVE bilgisi
            cve_id = None
            if "cve" in alert:
                cve_id = alert["cve"]
            
            # Güvenlik açığı oluştur
            vuln = Vulnerability(
                title=title,
                description=description,
                severity=severity,
                cve_id=cve_id,
                location=url,
                evidence=evidence or f"Risk: {risk}, Confidence: {confidence}",
                payload=solution if solution else None
            )
            
            self.add_vulnerability(result, vuln)
            
            # Log ekle
            self.add_scan_log(
                result, 
                f"Güvenlik açığı tespit edildi: {title} ({severity}) - {risk} risk, {confidence} confidence"
            )
            
        except Exception as e:
            self.add_scan_log(result, f"Alert işleme hatası: {e}", "warning")
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
        risk_counts = {
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for vuln in result.vulnerabilities:
            risk_counts[vuln.severity] += 1
        
        return {
            "total_vulnerabilities": len(result.vulnerabilities),
            "risk_distribution": risk_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
