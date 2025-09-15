"""
XSS (Cross-Site Scripting) Tarayıcısı
Manuel payload testleri ve otomatik tespit
"""

import asyncio
import aiohttp
import re
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from bs4 import BeautifulSoup
import logging

from .base_scanner import BaseScanner, ScanResult, Vulnerability

class XSSScanner(BaseScanner):
    """XSS güvenlik açıklarını tespit eden tarayıcı"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("XSS Scanner", config)
        
        # XSS payload'ları
        self.xss_payloads = [
            # Basic XSS payloads
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')",
            
            # Encoded payloads
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            
            # Event handlers
            "' onmouseover='alert(\"XSS\")' '",
            "\" onfocus=\"alert('XSS')\" \"",
            
            # Filter bypass attempts
            "<ScRiPt>alert('XSS')</ScRiPt>",
            "<script>alert(String.fromCharCode(88,83,83))</script>",
            
            # DOM XSS
            "javascript:alert(document.cookie)",
            "data:text/html,<script>alert('XSS')</script>"
        ]
        
        # Form field patterns
        self.form_patterns = [
            r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>',
            r'<textarea[^>]*name=["\']([^"\']+)["\'][^>]*>',
            r'<select[^>]*name=["\']([^"\']+)["\'][^>]*>'
        ]
        
        # XSS detection patterns
        self.xss_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'<iframe[^>]*>',
            r'<object[^>]*>',
            r'<embed[^>]*>'
        ]
    
    async def validate_target(self, target_url: str) -> bool:
        """Hedef URL'nin geçerli olup olmadığını kontrol eder"""
        try:
            parsed = urlparse(target_url)
            return bool(parsed.scheme and parsed.netloc)
        except Exception:
            return False
    
    async def scan(self, target_url: str, options: Dict[str, Any] = None) -> ScanResult:
        """XSS taraması gerçekleştirir"""
        options = options or {}
        
        # Tarama başlat
        result = ScanResult(
            scanner_name=self.name,
            target_url=target_url,
            start_time=asyncio.get_event_loop().time()
        )
        
        try:
            self.is_running = True
            self.add_scan_log(result, f"XSS taraması başlatıldı: {target_url}")
            
            # Pre-scan kontrolleri
            if not await self.pre_scan_checks(target_url):
                result.status = "failed"
                result.error_message = "Pre-scan kontrolleri başarısız"
                return result
            
            # Ana sayfayı analiz et
            await self._analyze_main_page(result, target_url)
            
            # Form alanlarını bul ve test et
            await self._test_form_fields(result, target_url)
            
            # URL parametrelerini test et
            await self._test_url_parameters(result, target_url)
            
            # Reflected XSS testleri
            await self._test_reflected_xss(result, target_url)
            
            # DOM XSS testleri
            await self._test_dom_xss(result, target_url)
            
            # Sonuçları sırala
            result.vulnerabilities = self.sort_vulnerabilities(result.vulnerabilities)
            result.status = "completed"
            result.end_time = asyncio.get_event_loop().time()
            
            self.add_scan_log(result, f"XSS taraması tamamlandı. {len(result.vulnerabilities)} açık bulundu.")
            
        except Exception as e:
            result.status = "failed"
            result.error_message = str(e)
            self.add_scan_log(result, f"Tarama hatası: {e}", "error")
        
        finally:
            await self.post_scan_cleanup()
        
        return result
    
    async def _analyze_main_page(self, result: ScanResult, target_url: str):
        """Ana sayfayı analiz eder ve potansiyel XSS açıklarını arar"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(target_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        await self._check_content_for_xss(result, content, target_url)
                    else:
                        self.add_scan_log(result, f"Ana sayfa yüklenemedi: HTTP {response.status}", "warning")
        except Exception as e:
            self.add_scan_log(result, f"Ana sayfa analizi hatası: {e}", "error")
    
    async def _check_content_for_xss(self, result: ScanResult, content: str, url: str):
        """HTML içeriğinde XSS açıkları arar"""
        soup = BeautifulSoup(content, 'html.parser')
        
        # Script tag'leri kontrol et
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                for pattern in self.xss_patterns:
                    if re.search(pattern, script.string, re.IGNORECASE):
                        vuln = Vulnerability(
                            title="Potansiyel XSS - Script Tag",
                            description=f"Script tag içinde potansiyel XSS kodu tespit edildi",
                            severity="medium",
                            location=url,
                            evidence=script.string[:100] + "..." if len(script.string) > 100 else script.string
                        )
                        self.add_vulnerability(result, vuln)
        
        # Event handler'ları kontrol et
        for tag in soup.find_all(attrs=lambda x: any(attr.startswith('on') for attr in x.keys())):
            event_attrs = [attr for attr in tag.attrs.keys() if attr.startswith('on')]
            for attr in event_attrs:
                vuln = Vulnerability(
                    title="Potansiyel XSS - Event Handler",
                    description=f"HTML tag'inde event handler tespit edildi: {attr}",
                    severity="medium",
                    location=url,
                    evidence=f"<{tag.name} {attr}=\"{tag[attr]}\">"
                )
                self.add_vulnerability(result, vuln)
    
    async def _test_form_fields(self, result: ScanResult, target_url: str):
        """Form alanlarını bulur ve XSS payload'ları ile test eder"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(target_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        soup = BeautifulSoup(content, 'html.parser')
                        
                        forms = soup.find_all('form')
                        for form in forms:
                            action = form.get('action', '')
                            method = form.get('method', 'get').lower()
                            
                            # Form alanlarını bul
                            inputs = form.find_all(['input', 'textarea', 'select'])
                            for input_field in inputs:
                                field_name = input_field.get('name')
                                if field_name:
                                    await self._test_form_field_xss(
                                        result, target_url, action, method, field_name, input_field
                                    )
        except Exception as e:
            self.add_scan_log(result, f"Form test hatası: {e}", "error")
    
    async def _test_form_field_xss(self, result: ScanResult, base_url: str, action: str, method: str, field_name: str, input_field):
        """Belirli bir form alanını XSS payload'ları ile test eder"""
        try:
            # Form URL'ini oluştur
            form_url = urljoin(base_url, action) if action else base_url
            
            # Test payload'ları
            for payload in self.xss_payloads[:5]:  # İlk 5 payload ile test et
                if method == 'post':
                    # POST form test
                    data = {field_name: payload}
                    async with aiohttp.ClientSession() as session:
                        async with session.post(form_url, data=data) as response:
                            if response.status == 200:
                                content = await response.text()
                                if payload in content:
                                    vuln = Vulnerability(
                                        title="Reflected XSS - Form Field",
                                        description=f"Form alanında reflected XSS tespit edildi: {field_name}",
                                        severity="high",
                                        payload=payload,
                                        location=form_url,
                                        evidence=f"Field: {field_name}, Payload: {payload}"
                                    )
                                    self.add_vulnerability(result, vuln)
                else:
                    # GET form test
                    params = {field_name: payload}
                    test_url = f"{form_url}?{urlencode(params)}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(test_url) as response:
                            if response.status == 200:
                                content = await response.text()
                                if payload in content:
                                    vuln = Vulnerability(
                                        title="Reflected XSS - Form Field (GET)",
                                        description=f"GET form alanında reflected XSS tespit edildi: {field_name}",
                                        severity="high",
                                        payload=payload,
                                        location=test_url,
                                        evidence=f"Field: {field_name}, Payload: {payload}"
                                    )
                                    self.add_vulnerability(result, vuln)
                                    
        except Exception as e:
            self.add_scan_log(result, f"Form field XSS test hatası: {e}", "warning")
    
    async def _test_url_parameters(self, result: ScanResult, target_url: str):
        """URL parametrelerini XSS payload'ları ile test eder"""
        try:
            parsed = urlparse(target_url)
            if parsed.query:
                params = parse_qs(parsed.query)
                base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                
                for param_name, param_values in params.items():
                    for payload in self.xss_payloads[:3]:  # İlk 3 payload ile test et
                        test_params = params.copy()
                        test_params[param_name] = [payload]
                        test_url = f"{base_url}?{urlencode(test_params, doseq=True)}"
                        
                        async with aiohttp.ClientSession() as session:
                            async with session.get(test_url) as response:
                                if response.status == 200:
                                    content = await response.text()
                                    if payload in content:
                                        vuln = Vulnerability(
                                            title="Reflected XSS - URL Parameter",
                                            description=f"URL parametresinde reflected XSS tespit edildi: {param_name}",
                                            severity="high",
                                            payload=payload,
                                            location=test_url,
                                            evidence=f"Parameter: {param_name}, Payload: {payload}"
                                        )
                                        self.add_vulnerability(result, vuln)
                                        
        except Exception as e:
            self.add_scan_log(result, f"URL parameter test hatası: {e}", "warning")
    
    async def _test_reflected_xss(self, result: ScanResult, target_url: str):
        """Reflected XSS testleri gerçekleştirir"""
        try:
            # Basit reflected XSS testi
            test_payload = "<script>alert('XSS')</script>"
            test_url = f"{target_url}?test={test_payload}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(test_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        if test_payload in content:
                            vuln = Vulnerability(
                                title="Reflected XSS - URL Parameter",
                                description="URL parametresinde reflected XSS tespit edildi",
                                severity="high",
                                payload=test_payload,
                                location=test_url,
                                evidence=f"Payload reflected: {test_payload}"
                            )
                            self.add_vulnerability(result, vuln)
                            
        except Exception as e:
            self.add_scan_log(result, f"Reflected XSS test hatası: {e}", "warning")
    
    async def _test_dom_xss(self, result: ScanResult, target_url: str):
        """DOM XSS testleri gerçekleştirir"""
        try:
            # DOM XSS için JavaScript kodunu analiz et
            async with aiohttp.ClientSession() as session:
                async with session.get(target_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # JavaScript kodunda DOM manipülasyonu ara
                        js_patterns = [
                            r'document\.write\s*\([^)]*\)',
                            r'document\.writeln\s*\([^)]*\)',
                            r'innerHTML\s*=',
                            r'outerHTML\s*=',
                            r'eval\s*\([^)]*\)',
                            r'setTimeout\s*\([^)]*\)',
                            r'setInterval\s*\([^)]*\)'
                        ]
                        
                        for pattern in js_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                vuln = Vulnerability(
                                    title="Potansiyel DOM XSS",
                                    description="JavaScript kodunda DOM manipülasyonu tespit edildi",
                                    severity="medium",
                                    location=target_url,
                                    evidence=match
                                )
                                self.add_vulnerability(result, vuln)
                                
        except Exception as e:
            self.add_scan_log(result, f"DOM XSS test hatası: {e}", "warning")
    
    def get_scan_summary(self, result: ScanResult) -> Dict[str, Any]:
        """Tarama özeti döndürür"""
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
            "severity_distribution": severity_counts,
            "scan_duration": result.end_time - result.start_time if result.end_time else 0,
            "status": result.status
        }
