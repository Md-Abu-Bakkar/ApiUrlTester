#!/usr/bin/env python3
import requests
import re
import json
import time
from bs4 import BeautifulSoup

class UniversalLoginSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.logged_in = False
        self.cookies = {}
    
    def solve_math_captcha(self, text):
        """Solve math captcha like 'What is X + Y = ?'"""
        patterns = [
            r'What is (\d+) \+ (\d+) = \?',
            r'(\d+) \+ (\d+) =',
            r'(\d+)\s*\+\s*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    num1 = int(match.group(1))
                    num2 = int(match.group(2))
                    result = num1 + num2
                    print(f"🧮 Captcha solved: {num1} + {num2} = {result}")
                    return str(result)
                except:
                    continue
        return None
    
    def detect_login_form(self, html_content):
        """Detect login form fields automatically"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        login_info = {
            'username_field': 'username',
            'password_field': 'password', 
            'captcha_field': None,
            'form_action': None,
            'form_data': {}
        }
        
        # Find all forms
        forms = soup.find_all('form')
        for form in forms:
            form_action = form.get('action', '')
            
            # Check if this is likely a login form
            if any(keyword in form_action.lower() for keyword in ['login', 'signin', 'auth', '']) or \
               any(keyword in str(form).lower() for keyword in ['username', 'password', 'login']):
                
                login_info['form_action'] = form_action
                
                # Extract input fields
                inputs = form.find_all('input')
                for input_field in inputs:
                    input_name = input_field.get('name', '')
                    input_type = input_field.get('type', '').lower()
                    input_value = input_field.get('value', '')
                    
                    if input_type == 'text' and any(keyword in input_name.lower() for keyword in ['user', 'email', 'login']):
                        login_info['username_field'] = input_name
                    elif input_type == 'password':
                        login_info['password_field'] = input_name
                    elif any(keyword in input_name.lower() for keyword in ['captcha', 'capt', 'code']):
                        login_info['captcha_field'] = input_name
                    elif input_name and input_value and input_type not in ['submit', 'button']:
                        login_info['form_data'][input_name] = input_value
        
        return login_info
    
    def perform_login(self, login_url, username, password, base_url=None):
        """Perform complete login process"""
        try:
            # Build complete URL
            if base_url and not login_url.startswith('http'):
                full_login_url = urljoin(base_url, login_url)
            else:
                full_login_url = login_url
            
            print(f"🔍 Accessing login page: {full_login_url}")
            
            # Get login page
            response = self.session.get(full_login_url, timeout=30)
            if response.status_code != 200:
                return {'success': False, 'error': f'Cannot access login page: {response.status_code}'}
            
            # Detect login form
            login_info = self.detect_login_form(response.text)
            print(f"📝 Detected form fields: {login_info}")
            
            # Solve captcha if present
            captcha_answer = self.solve_math_captcha(response.text)
            
            # Prepare login data
            login_data = login_info['form_data'].copy()
            login_data[login_info['username_field']] = username
            login_data[login_info['password_field']] = password
            
            if login_info['captcha_field'] and captcha_answer:
                login_data[login_info['captcha_field']] = captcha_answer
            
            # Determine action URL
            if login_info['form_action']:
                action_url = urljoin(full_login_url, login_info['form_action'])
            else:
                action_url = full_login_url
            
            print(f"🎯 Attempting login to: {action_url}")
            
            # Send login request
            login_headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Referer': full_login_url
            }
            
            login_response = self.session.post(
                action_url,
                data=login_data,
                headers=login_headers,
                allow_redirects=True,
                timeout=30
            )
            
            # Check login success
            if self._check_login_success(login_response):
                self.cookies = dict(self.session.cookies)
                self.logged_in = True
                
                print("✅ Login successful!")
                print(f"🍪 Session cookies: {len(self.cookies)}")
                
                return {
                    'success': True,
                    'cookies': self.cookies,
                    'message': 'Login successful',
                    'final_url': login_response.url
                }
            else:
                return {
                    'success': False, 
                    'error': 'Login failed - check credentials or captcha'
                }
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _check_login_success(self, response):
        """Check if login was successful"""
        # Check for redirect to dashboard/client area
        if any(keyword in response.url for keyword in ['client', 'dashboard', 'admin']):
            return True
        
        # Check response content for success indicators
        success_indicators = [
            'dashboard' in response.text.lower(),
            'logout' in response.text.lower(),
            'welcome' in response.text.lower(),
            'success' in response.text.lower()
        ]
        
        # Check for failure indicators
        failure_indicators = [
            'invalid' in response.text.lower(),
            'error' in response.text.lower(),
            'failed' in response.text.lower(),
            'incorrect' in response.text.lower()
        ]
        
        if any(success_indicators) and not any(failure_indicators):
            return True
        
        # If we were redirected away from login page, consider it success
        if response.history and 'login' not in response.url:
            return True
            
        return False
    
    def test_protected_url(self, url, cookies=None):
        """Test if we can access a protected URL"""
        try:
            test_cookies = cookies or self.cookies
            response = self.session.get(url, cookies=test_cookies, timeout=10)
            return response.status_code == 200
        except:
            return False
