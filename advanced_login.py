#!/usr/bin/env python3
import requests
import json
import re
import time
import os
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

class AdvancedLoginSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.cookies = {}
        self.auth_tokens = {}
        self.csrf_tokens = {}
        
    def detect_login_type(self, login_url, username, password):
        """Detect what type of login system is used"""
        try:
            response = self.session.get(login_url, timeout=10)
            content_type = response.headers.get('content-type', '').lower()
            html_content = response.text.lower()
            
            login_info = {
                'url': login_url,
                'content_type': content_type,
                'has_form': 'form' in html_content,
                'has_json': 'application/json' in content_type,
                'has_csrf': 'csrf' in html_content or 'token' in html_content,
                'has_cloudflare': 'cloudflare' in response.headers.get('server', '').lower(),
                'login_fields': self.extract_login_fields(response.text)
            }
            
            return login_info
        except Exception as e:
            return {'error': str(e)}
    
    def extract_login_fields(self, html_content):
        """Extract login form fields automatically"""
        soup = BeautifulSoup(html_content, 'html.parser')
        forms = soup.find_all('form')
        login_fields = {}
        
        for form in forms:
            inputs = form.find_all('input')
            for input_field in inputs:
                name = input_field.get('name', '')
                input_type = input_field.get('type', '').lower()
                
                if input_type in ['text', 'email'] and any(keyword in name.lower() for keyword in ['user', 'email', 'login']):
                    login_fields['username_field'] = name
                elif input_type == 'password':
                    login_fields['password_field'] = name
                elif any(keyword in name.lower() for keyword in ['csrf', 'token', 'auth']):
                    login_fields['csrf_field'] = name
                    login_fields['csrf_value'] = input_field.get('value', '')
        
        return login_fields
    
    def extract_csrf_token(self, response_text):
        """Extract CSRF tokens from HTML"""
        patterns = [
            r'name="csrf_token" value="([^"]+)"',
            r'name="_token" value="([^"]+)"',
            r'name="authenticity_token" value="([^"]+)"',
            r'csrf-token" content="([^"]+)"',
            r'"csrfToken":"([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_text)
            if match:
                return match.group(1)
        return None
    
    def perform_login(self, login_url, username, password, login_type='auto', custom_headers=None):
        """Perform automated login with various methods"""
        try:
            # Get login page first to extract tokens
            response = self.session.get(login_url)
            csrf_token = self.extract_csrf_token(response.text)
            login_fields = self.extract_login_fields(response.text)
            
            # Prepare login data based on detected fields
            login_data = {}
            
            if login_fields.get('username_field'):
                login_data[login_fields['username_field']] = username
            else:
                login_data['username'] = username
                login_data['email'] = username
                
            if login_fields.get('password_field'):
                login_data[login_fields['password_field']] = password
            else:
                login_data['password'] = password
                
            if csrf_token and login_fields.get('csrf_field'):
                login_data[login_fields['csrf_field']] = csrf_token
            
            # Prepare headers
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            if custom_headers:
                headers.update(custom_headers)
            
            # Send login request
            login_response = self.session.post(
                login_url,
                data=login_data,
                headers=headers,
                allow_redirects=True
            )
            
            # Store session data
            self.cookies = dict(self.session.cookies)
            self.save_session_data()
            
            return {
                'success': login_response.status_code in [200, 302],
                'status_code': login_response.status_code,
                'cookies': dict(self.session.cookies),
                'headers': dict(login_response.headers),
                'redirected': len(login_response.history) > 0
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_session_data(self):
        """Save session data for reuse"""
        session_data = {
            'cookies': self.cookies,
            'auth_tokens': self.auth_tokens,
            'csrf_tokens': self.csrf_tokens,
            'timestamp': time.time()
        }
        
        os.makedirs('sessions', exist_ok=True)
        with open('sessions/latest_session.json', 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session_data(self):
        """Load saved session data"""
        try:
            with open('sessions/latest_session.json', 'r') as f:
                session_data = json.load(f)
                self.cookies = session_data.get('cookies', {})
                self.auth_tokens = session_data.get('auth_tokens', {})
                self.csrf_tokens = session_data.get('csrf_tokens', {})
                return True
        except FileNotFoundError:
            return False
    
    def is_logged_in(self, test_url=None):
        """Check if we're still logged in"""
        if test_url:
            try:
                response = self.session.get(test_url, cookies=self.cookies)
                return response.status_code == 200
            except:
                return False
        return len(self.cookies) > 0
