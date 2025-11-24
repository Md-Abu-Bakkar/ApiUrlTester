#!/usr/bin/env python3
import requests
import json
import re
import time
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

class UniversalLoginSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.cookies = {}
        self.auth_tokens = {}
        self.logged_in = False
        
    def solve_math_captcha(self, text):
        """Solve simple math captchas"""
        try:
            # Pattern for "What is X + Y = ?"
            patterns = [
                r'What is (\d+) \+ (\d+) = \?',
                r'(\d+) \+ (\d+) =',
                r'(\d+)\s*\+\s*(\d+)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))
                    return str(num1 + num2)
            
            return None
        except:
            return None
    
    def detect_login_form(self, html_content):
        """Detect login form fields"""
        soup = BeautifulSoup(html_content, 'html.parser')
        login_info = {
            'username_field': 'username',
            'password_field': 'password',
            'captcha_field': None,
            'login_url': None,
            'form_data': {}
        }
        
        # Find all forms
        forms = soup.find_all('form')
        for form in forms:
            form_action = form.get('action', '')
            if any(keyword in form_action.lower() for keyword in ['login', 'signin', 'auth']):
                login_info['login_url'] = form_action
                
                # Find input fields
                inputs = form.find_all('input')
                for input_field in inputs:
                    input_name = input_field.get('name', '')
                    input_type = input_field.get('type', '').lower()
                    input_value = input_field.get('value', '')
                    
                    if input_type == 'text' and any(keyword in input_name.lower() 
                                                   for keyword in ['user', 'email', 'login']):
                        login_info['username_field'] = input_name
                    elif input_type == 'password':
                        login_info['password_field'] = input_name
                    elif any(keyword in input_name.lower() 
                            for keyword in ['captcha', 'capt', 'code']):
                        login_info['captcha_field'] = input_name
                    elif input_name and input_value:
                        login_info['form_data'][input_name] = input_value
        
        return login_info
    
    def perform_login(self, login_url, username, password, base_url=None):
        """Perform login with captcha solving"""
        try:
            # Get login page
            if base_url and not login_url.startswith('http'):
                login_url = base_url + login_url
            
            print(f"🔍 Accessing login page: {login_url}")
            response = self.session.get(login_url, timeout=30)
            
            if response.status_code != 200:
                return {'success': False, 'error': f'Login page unavailable: {response.status_code}'}
            
            # Detect login form
            login_info = self.detect_login_form(response.text)
            
            # Solve captcha if present
            captcha_answer = self.solve_math_captcha(response.text)
            if captcha_answer:
                print(f"✅ Captcha solved: {captcha_answer}")
            
            # Prepare login data
            login_data = login_info['form_data'].copy()
            login_data[login_info['username_field']] = username
            login_data[login_info['password_field']] = password
            
            if login_info['captcha_field'] and captcha_answer:
                login_data[login_info['captcha_field']] = captcha_answer
            
            # Determine final login URL
            final_login_url = login_info['login_url'] or login_url
            if base_url and not final_login_url.startswith('http'):
                final_login_url = base_url + final_login_url
            
            # Send login request
            login_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': login_url
            }
            
            print(f"🔐 Attempting login to: {final_login_url}")
            login_response = self.session.post(
                final_login_url,
                data=login_data,
                headers=login_headers,
                allow_redirects=True,
                timeout=30
            )
            
            # Check if login successful
            if login_response.status_code in [200, 302]:
                # Check for successful login indicators
                success_indicators = [
                    'dashboard' in login_response.url,
                    'logout' in login_response.text.lower(),
                    'welcome' in login_response.text.lower(),
                    login_response.history  # Redirect occurred
                ]
                
                if any(success_indicators):
                    self.cookies = dict(self.session.cookies)
                    self.logged_in = True
                    self.save_session()
                    
                    return {
                        'success': True,
                        'message': 'Login successful',
                        'cookies': self.cookies,
                        'redirect_url': login_response.url
                    }
            
            return {
                'success': False,
                'error': 'Login failed - check credentials or captcha'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_session(self):
        """Save session data for reuse"""
        session_data = {
            'cookies': self.cookies,
            'auth_tokens': self.auth_tokens,
            'timestamp': time.time()
        }
        
        os.makedirs('sessions', exist_ok=True)
        with open('sessions/session.json', 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self):
        """Load saved session"""
        try:
            with open('sessions/session.json', 'r') as f:
                session_data = json.load(f)
                self.cookies = session_data.get('cookies', {})
                self.auth_tokens = session_data.get('auth_tokens', {})
                self.logged_in = True
                return True
        except FileNotFoundError:
            return False
    
    def is_session_valid(self, test_url=None):
        """Check if session is still valid"""
        if not self.logged_in:
            return False
        
        if test_url:
            try:
                response = self.session.get(test_url, cookies=self.cookies, timeout=10)
                return response.status_code == 200
            except:
                return False
        
        return True
