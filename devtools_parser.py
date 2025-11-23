#!/usr/bin/env python3
import re
import json
import urllib.parse

class DevToolsParser:
    def __init__(self):
        self.patterns = {
            'curl': r'curl\s+([^\']+?)\s+([^\']+?)(?:\s+-H\s+\'([^\']+)\')*\s*(?:--data-raw\s+\'([^\']+)\')?',
            'fetch': r'fetch\([\'"]([^\'"]+)[\'"][^)]*{([^}]*)}',
            'axios': r'axios\.(?:get|post|put|delete)\([\'"]([^\'"]+)[\'"][^)]*{([^}]*)}',
            'headers': r'([a-zA-Z\-]+):\s*([^\n]+)',
            'json': r'\{[^{}]*"[^"]*":[^}]*\}',
            'url': r'https?://[^\s\'"]+'
        }
    
    def parse_any_input(self, user_input):
        """Parse any DevTools copied content"""
        result = {
            'url': None,
            'method': 'GET',
            'headers': {},
            'cookies': {},
            'data': None,
            'json_body': None,
            'params': {}
        }
        
        # Try to detect input type
        input_type = self.detect_input_type(user_input)
        
        if input_type == 'curl':
            return self.parse_curl(user_input)
        elif input_type == 'fetch':
            return self.parse_fetch(user_input)
        elif input_type == 'axios':
            return self.parse_axios(user_input)
        elif input_type == 'headers':
            return self.parse_raw_headers(user_input)
        elif input_type == 'url':
            result['url'] = user_input.strip()
            return result
        else:
            # Try mixed content parsing
            return self.parse_mixed_content(user_input)
    
    def detect_input_type(self, text):
        """Detect what type of DevTools content this is"""
        text = text.strip()
        
        if text.startswith('curl '):
            return 'curl'
        elif 'fetch(' in text:
            return 'fetch'
        elif 'axios.' in text:
            return 'axios'
        elif re.search(r'^[A-Za-z\-]+:\s*.+', text, re.MULTILINE):
            return 'headers'
        elif re.match(r'^https?://', text):
            return 'url'
        else:
            return 'mixed'
    
    def parse_curl(self, curl_command):
        """Parse cURL command"""
        result = {
            'url': None,
            'method': 'GET',
            'headers': {},
            'cookies': {},
            'data': None,
            'json_body': None
        }
        
        # Extract URL
        url_match = re.search(r"curl\s+['\"]([^'\"]+)['\"]", curl_command)
        if not url_match:
            url_match = re.search(r'curl\s+([^\s\']+)', curl_command)
        
        if url_match:
            result['url'] = url_match.group(1)
        
        # Extract method
        if '-X' in curl_command:
            method_match = re.search(r'-X\s+([A-Z]+)', curl_command)
            if method_match:
                result['method'] = method_match.group(1)
        
        # Extract headers
        header_matches = re.findall(r"-H\s+['\"]([^'\"]+)['\"]", curl_command)
        for header in header_matches:
            if ':' in header:
                key, value = header.split(':', 1)
                result['headers'][key.strip()] = value.strip()
                
                # Extract cookies from headers
                if key.strip().lower() == 'cookie':
                    cookies = self.parse_cookie_header(value.strip())
                    result['cookies'].update(cookies)
        
        # Extract data
        data_matches = re.findall(r"--data-raw\s+['\"]([^'\"]+)['\"]", curl_command)
        if data_matches:
            result['data'] = data_matches[0]
            try:
                result['json_body'] = json.loads(data_matches[0])
            except:
                pass
        
        return result
    
    def parse_fetch(self, fetch_code):
        """Parse JavaScript fetch code"""
        result = {
            'url': None,
            'method': 'GET',
            'headers': {},
            'data': None
        }
        
        # Extract URL
        url_match = re.search(r"fetch\(['\"]([^'\"]+)['\"]", fetch_code)
        if url_match:
            result['url'] = url_match.group(1)
        
        # Extract method and headers from options
        options_match = re.search(r'\{([^}]+)\}', fetch_code)
        if options_match:
            options_text = options_match.group(1)
            
            # Method
            method_match = re.search(r"method:\s*['\"]([^'\"]+)['\"]", options_text, re.IGNORECASE)
            if method_match:
                result['method'] = method_match.group(1).upper()
            
            # Headers
            headers_match = re.search(r"headers:\s*\{([^}]+)\}", options_text)
            if headers_match:
                headers_text = headers_match.group(1)
                header_pairs = re.findall(r"['\"]?([^:'\"]+)['\"]?\s*:\s*['\"]?([^,'\"]+)['\"]?", headers_text)
                for key, value in header_pairs:
                    result['headers'][key.strip()] = value.strip()
            
            # Body
            body_match = re.search(r"body:\s*JSON\.stringify\(([^)]+)\)", options_text)
            if body_match:
                try:
                    result['json_body'] = json.loads(body_match.group(1).replace("'", '"'))
                except:
                    result['data'] = body_match.group(1)
        
        return result
    
    def parse_cookie_header(self, cookie_header):
        """Parse cookie header string into dict"""
        cookies = {}
        pairs = cookie_header.split(';')
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookies[key.strip()] = value.strip()
        return cookies
    
    def parse_mixed_content(self, text):
        """Parse mixed DevTools content"""
        result = {
            'url': None,
            'method': 'GET',
            'headers': {},
            'cookies': {},
            'data': None
        }
        
        # Extract URL
        url_match = re.search(r'https?://[^\s\']+', text)
        if url_match:
            result['url'] = url_match.group(0)
        
        # Extract headers
        header_matches = re.findall(r'([A-Za-z\-]+):\s*([^\n]+)', text)
        for key, value in header_matches:
            result['headers'][key] = value.strip()
            
            if key.lower() == 'cookie':
                cookies = self.parse_cookie_header(value)
                result['cookies'].update(cookies)
        
        # Extract JSON body
        json_match = re.search(r'(\{.*\})', text, re.DOTALL)
        if json_match:
            try:
                result['json_body'] = json.loads(json_match.group(1))
            except:
                result['data'] = json_match.group(1)
        
        return result
