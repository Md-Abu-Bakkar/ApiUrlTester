#!/usr/bin/env python3
import re
import json
from urllib.parse import urljoin, urlparse, parse_qs

class AdvancedDevToolsParser:
    def __init__(self):
        self.session_cookies = {}
        
    def parse_raw_devtools(self, content):
        """Parse raw DevTools content and extract all API information"""
        print("🔄 Parsing DevTools content...")
        
        lines = content.split('\n')
        requests = []
        current_request = {}
        in_headers = False
        in_request_payload = False
        
        for line in lines:
            line = line.strip()
            
            # Detect new request
            if line.startswith('scheme') or 'http' in line.lower() and any(x in line for x in ['GET', 'POST', 'PUT', 'DELETE']):
                if current_request and 'url' in current_request:
                    requests.append(current_request)
                current_request = {'headers': {}, 'cookies': {}}
                in_headers = False
                in_request_payload = False
            
            # Extract URL components
            if line.startswith('scheme'):
                current_request['scheme'] = line.split('\t')[-1].strip()
            elif line.startswith('host'):
                current_request['host'] = line.split('\t')[-1].strip()
            elif line.startswith('filename'):
                current_request['path'] = line.split('\t')[-1].strip()
            elif 'Address' in line and 'http' in line:
                current_request['url'] = line.split('\t')[-1].strip()
            
            # Extract method from status line
            elif 'Status' in line and any(method in line for method in ['GET', 'POST', 'PUT', 'DELETE']):
                for method in ['GET', 'POST', 'PUT', 'DELETE']:
                    if method in line:
                        current_request['method'] = method
                        break
            
            # Headers section
            elif line and ':' in line and not line.startswith('\t'):
                if 'headers' not in current_request:
                    current_request['headers'] = {}
                
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    current_request['headers'][key] = value
                    
                    # Extract cookies
                    if key.lower() == 'cookie':
                        self._parse_cookies(value, current_request)
            
            # Request payload parameters
            elif line and '\t' in line and '=' in line and not line.startswith(' '):
                if 'params' not in current_request:
                    current_request['params'] = {}
                
                parts = line.split('\t')
                if len(parts) >= 2 and '=' in parts[-1]:
                    key_value = parts[-1].split('=', 1)
                    if len(key_value) == 2:
                        current_request['params'][key_value[0].strip()] = key_value[1].strip()
        
        # Add the last request
        if current_request and 'url' in current_request:
            requests.append(current_request)
        
        # Build complete URLs and normalize
        normalized_requests = []
        for req in requests:
            normalized = self._normalize_request(req)
            if normalized:
                normalized_requests.append(normalized)
        
        print(f"✅ Found {len(normalized_requests)} API endpoints")
        return normalized_requests
    
    def _parse_cookies(self, cookie_string, request):
        """Parse cookie string into dictionary"""
        if 'cookies' not in request:
            request['cookies'] = {}
        
        cookies = cookie_string.split(';')
        for cookie in cookies:
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                request['cookies'][key.strip()] = value.strip()
    
    def _normalize_request(self, request):
        """Normalize request data and build complete URL"""
        # Build URL if not complete
        if 'url' not in request:
            if all(k in request for k in ['scheme', 'host', 'path']):
                request['url'] = f"{request['scheme']}://{request['host']}{request['path']}"
            else:
                return None
        
        # Set default method
        if 'method' not in request:
            request['method'] = 'GET'
        
        # Add parameters to URL for GET requests
        if request['method'] == 'GET' and 'params' in request and request['params']:
            param_string = '&'.join([f"{k}={v}" for k, v in request['params'].items()])
            if '?' in request['url']:
                request['url'] += '&' + param_string
            else:
                request['url'] += '?' + param_string
        
        # Detect API type
        request['api_type'] = self._detect_api_type(request)
        request['requires_login'] = self._requires_login(request)
        
        return request
    
    def _detect_api_type(self, request):
        """Detect the type of API"""
        url = request['url'].lower()
        
        if 'login' in url or 'signin' in url or 'auth' in url:
            return 'login'
        elif 'data_smscdr' in url or 'data_' in url:
            return 'data_api'
        elif 'dashboard' in url or 'admin' in url:
            return 'dashboard'
        elif '.js' in url or '.css' in url or 'jquery' in url:
            return 'resource'
        else:
            return 'unknown'
    
    def _requires_login(self, request):
        """Check if API requires authentication"""
        # Check cookies for session
        cookies = request.get('cookies', {})
        if any('session' in key.lower() or 'auth' in key.lower() for key in cookies.keys()):
            return True
        
        # Check headers for auth tokens
        headers = request.get('headers', {})
        if any(key.lower() in ['authorization', 'x-auth-token', 'x-csrf-token'] for key in headers.keys()):
            return True
        
        # Check URL patterns that typically require auth
        auth_patterns = ['/client/', '/dashboard', '/admin', '/user', '/res/']
        if any(pattern in request['url'] for pattern in auth_patterns):
            return True
        
        return False
    
    def extract_login_info(self, requests):
        """Extract login-related information"""
        login_requests = [req for req in requests if req['api_type'] == 'login']
        if login_requests:
            return login_requests[0]
        return None
    
    def extract_data_apis(self, requests):
        """Extract data APIs that need testing"""
        return [req for req in requests if req['api_type'] in ['data_api', 'unknown'] and not req['api_type'] == 'resource']
    
    def get_base_url(self, requests):
        """Extract base URL from requests"""
        for req in requests:
            if 'url' in req:
                parsed = urlparse(req['url'])
                return f"{parsed.scheme}://{parsed.netloc}"
        return None
