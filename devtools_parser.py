#!/usr/bin/env python3
import re
import json
import urllib.parse
from urllib.parse import parse_qs, urlparse

class AdvancedDevToolsParser:
    def __init__(self):
        self.patterns = {
            'curl': r'curl\s+[\'"]?([^\'"]+)[\'"]?',
            'fetch': r'fetch\([\'"]([^\'"]+)[\'"][^)]*{([^}]*)}',
            'axios': r'axios\.(?:get|post|put|delete)\([\'"]([^\'"]+)[\'"][^)]*{([^}]*)}',
            'headers': r'([a-zA-Z\-]+):\s*([^\n]+)',
            'json_body': r'(\{[\s\S]*?\})',
            'url_params': r'(\?[^\s]+)',
            'cookie': r'Cookie:\s*([^\n]+)'
        }
    
    def parse_devtools_content(self, content):
        """Parse any DevTools copied content and extract all APIs"""
        lines = content.split('\n')
        apis = []
        current_api = {}
        
        for line in lines:
            line = line.strip()
            
            # Detect new API section
            if any(keyword in line for keyword in ['scheme', 'http', 'https', 'filename', 'Address']):
                if current_api and any(key in current_api for key in ['url', 'headers', 'method']):
                    apis.append(current_api)
                    current_api = {}
            
            # Extract URL components
            if line.startswith('scheme'):
                current_api['scheme'] = line.split('\t')[-1].strip()
            elif line.startswith('host'):
                current_api['host'] = line.split('\t')[-1].strip()
            elif line.startswith('filename'):
                current_api['path'] = line.split('\t')[-1].strip()
            elif line.startswith('Address'):
                current_api['full_url'] = line.split('\t')[-1].strip()
            
            # Extract headers
            elif not line.startswith('\t') and ':' in line and not line.startswith(' '):
                if 'headers' not in current_api:
                    current_api['headers'] = {}
                key, value = line.split(':', 1)
                current_api['headers'][key.strip()] = value.strip()
            
            # Extract request parameters (form data)
            elif '\t' in line and '=' in line:
                if 'params' not in current_api:
                    current_api['params'] = {}
                key, value = line.split('\t')[-1].strip().split('=', 1)
                current_api['params'][key] = value
            
            # Detect method from status line
            elif 'Status' in line and 'OK' in line:
                current_api['method'] = 'GET'  # Default, will be updated
            
            # Extract cookies
            elif 'Cookie' in line and ':' in line:
                if 'cookies' not in current_api:
                    current_api['cookies'] = {}
                cookie_line = line.split(':', 1)[1].strip()
                cookies = self.parse_cookies(cookie_line)
                current_api['cookies'].update(cookies)
        
        # Add the last API
        if current_api and any(key in current_api for key in ['url', 'headers', 'method']):
            apis.append(current_api)
        
        return self.normalize_apis(apis)
    
    def parse_cookies(self, cookie_string):
        """Parse cookie string into dictionary"""
        cookies = {}
        pairs = cookie_string.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies
    
    def normalize_apis(self, apis):
        """Normalize and complete API information"""
        normalized_apis = []
        
        for api in apis:
            # Build complete URL
            if 'full_url' in api:
                url = api['full_url']
            else:
                scheme = api.get('scheme', 'http')
                host = api.get('host', '')
                path = api.get('path', '')
                url = f"{scheme}://{host}{path}"
            
            # Add parameters to URL if GET request
            if 'params' in api and api.get('method', 'GET') == 'GET':
                param_string = '&'.join([f"{k}={v}" for k, v in api['params'].items()])
                url = f"{url}?{param_string}" if '?' not in url else f"{url}&{param_string}"
            
            normalized_api = {
                'url': url,
                'method': api.get('method', 'GET'),
                'headers': api.get('headers', {}),
                'cookies': api.get('cookies', {}),
                'params': api.get('params', {}),
                'requires_login': self.detect_login_requirement(api),
                'api_type': self.detect_api_type(api)
            }
            
            # Add POST data if available
            if api.get('method') in ['POST', 'PUT'] and 'params' in api:
                normalized_api['data'] = api['params']
            
            normalized_apis.append(normalized_api)
        
        return normalized_apis
    
    def detect_login_requirement(self, api):
        """Detect if API requires login"""
        url = api.get('full_url', '') or api.get('url', '')
        headers = api.get('headers', {})
        
        # Check for session cookies
        if any('session' in key.lower() or 'auth' in key.lower() 
               for key in headers.keys()):
            return True
        
        # Check for authentication headers
        if any(key.lower() in ['authorization', 'x-auth-token'] 
               for key in headers.keys()):
            return True
        
        # Check URL patterns that typically require auth
        auth_patterns = ['/client/', '/dashboard', '/admin', '/user']
        if any(pattern in url for pattern in auth_patterns):
            return True
        
        return False
    
    def detect_api_type(self, api):
        """Detect the type of API"""
        url = api.get('full_url', '') or api.get('url', '')
        
        if 'data_smscdr' in url:
            return 'sms_data'
        elif 'login' in url or 'signin' in url:
            return 'authentication'
        elif 'dashboard' in url:
            return 'dashboard'
        elif 'jquery' in url or '.js' in url:
            return 'resource'
        else:
            return 'data_api'
    
    def extract_login_info(self, apis):
        """Extract login information from APIs"""
        login_apis = [api for api in apis if api['api_type'] == 'authentication']
        if login_apis:
            return login_apis[0]
        return None
    
    def extract_data_apis(self, apis):
        """Extract data APIs that need to be tested"""
        return [api for api in apis if api['api_type'] in ['sms_data', 'data_api']]
