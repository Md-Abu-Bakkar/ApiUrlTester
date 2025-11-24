cat > install_complete.sh << 'EOF'
#!/bin/bash
echo "🚀 Complete Universal API Tester Installation"
echo "=============================================="

# Check if in correct directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Please run from project directory."
    exit 1
fi

echo "📦 Installing Python packages..."
pip install requests beautifulsoup4 cloudscraper

echo "📁 Creating necessary directories..."
mkdir -p sessions exported_codes logs utils

echo "🔧 Creating required Python files..."

# Create devtools_parser.py
cat > devtools_parser.py << 'PYEOF'
#!/usr/bin/env python3
import re
import json
from urllib.parse import urljoin, urlparse

class AdvancedDevToolsParser:
    def __init__(self):
        self.session_cookies = {}
        
    def parse_raw_devtools(self, content):
        print("🔄 Parsing DevTools content...")
        
        lines = content.split('\\n')
        requests = []
        current_request = {}
        
        for line in lines:
            line = line.strip()
            
            # Detect new request
            if line.startswith('scheme') or ('http' in line.lower() and any(x in line for x in ['GET', 'POST', 'PUT', 'DELETE'])):
                if current_request and 'url' in current_request:
                    requests.append(current_request)
                current_request = {'headers': {}, 'cookies': {}, 'method': 'GET'}
            
            # Extract URL components
            if line.startswith('scheme'):
                current_request['scheme'] = line.split('\\t')[-1].strip()
            elif line.startswith('host'):
                current_request['host'] = line.split('\\t')[-1].strip()
            elif line.startswith('filename'):
                current_request['path'] = line.split('\\t')[-1].strip()
            elif 'Address' in line and 'http' in line:
                current_request['url'] = line.split('\\t')[-1].strip()
            
            # Extract method
            elif 'Status' in line and any(method in line for method in ['GET', 'POST', 'PUT', 'DELETE']):
                for method in ['GET', 'POST', 'PUT', 'DELETE']:
                    if method in line:
                        current_request['method'] = method
                        break
            
            # Headers
            elif line and ':' in line and not line.startswith('\\t'):
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
            
            # Request parameters
            elif line and '\\t' in line and '=' in line and not line.startswith(' '):
                if 'params' not in current_request:
                    current_request['params'] = {}
                
                parts = line.split('\\t')
                if len(parts) >= 2 and '=' in parts[-1]:
                    key_value = parts[-1].split('=', 1)
                    if len(key_value) == 2:
                        current_request['params'][key_value[0].strip()] = key_value[1].strip()
        
        # Add last request
        if current_request and 'url' in current_request:
            requests.append(current_request)
        
        # Normalize requests
        normalized_requests = []
        for req in requests:
            normalized = self._normalize_request(req)
            if normalized:
                normalized_requests.append(normalized)
        
        print(f"✅ Found {len(normalized_requests)} API endpoints")
        return normalized_requests
    
    def _parse_cookies(self, cookie_string, request):
        if 'cookies' not in request:
            request['cookies'] = {}
        
        cookies = cookie_string.split(';')
        for cookie in cookies:
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                request['cookies'][key.strip()] = value.strip()
    
    def _normalize_request(self, request):
        if 'url' not in request:
            if all(k in request for k in ['scheme', 'host', 'path']):
                request['url'] = f"{request['scheme']}://{request['host']}{request['path']}"
            else:
                return None
        
        if 'method' not in request:
            request['method'] = 'GET'
        
        # Add params to URL for GET
        if request['method'] == 'GET' and 'params' in request and request['params']:
            param_string = '&'.join([f"{k}={v}" for k, v in request['params'].items()])
            if '?' in request['url']:
                request['url'] += '&' + param_string
            else:
                request['url'] += '?' + param_string
        
        request['api_type'] = self._detect_api_type(request)
        request['requires_login'] = self._requires_login(request)
        
        return request
    
    def _detect_api_type(self, request):
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
        cookies = request.get('cookies', {})
        if any('session' in key.lower() or 'auth' in key.lower() for key in cookies.keys()):
            return True
        
        headers = request.get('headers', {})
        if any(key.lower() in ['authorization', 'x-auth-token'] for key in headers.keys()):
            return True
        
        auth_patterns = ['/client/', '/dashboard', '/admin', '/user', '/res/']
        if any(pattern in request['url'] for pattern in auth_patterns):
            return True
        
        return False
    
    def extract_login_info(self, requests):
        login_requests = [req for req in requests if req['api_type'] == 'login']
        return login_requests[0] if login_requests else None
    
    def extract_data_apis(self, requests):
        return [req for req in requests if req['api_type'] in ['data_api', 'unknown'] and req['api_type'] != 'resource']
    
    def get_base_url(self, requests):
        for req in requests:
            if 'url' in req:
                parsed = urlparse(req['url'])
                return f"{parsed.scheme}://{parsed.netloc}"
        return None
PYEOF

# Create advanced_login.py
cat > advanced_login.py << 'PYEOF'
#!/usr/bin/env python3
import requests
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class UniversalLoginSystem:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        self.logged_in = False
        self.cookies = {}
    
    def solve_math_captcha(self, text):
        patterns = [
            r'What is (\\d+) \\+ (\\d+) = \\?',
            r'(\\d+) \\+ (\\d+) =',
            r'(\\d+)\\s*\\+\\s*(\\d+)'
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
        soup = BeautifulSoup(html_content, 'html.parser')
        
        login_info = {
            'username_field': 'username',
            'password_field': 'password', 
            'captcha_field': None,
            'form_action': None,
            'form_data': {}
        }
        
        forms = soup.find_all('form')
        for form in forms:
            form_action = form.get('action', '')
            
            if any(keyword in form_action.lower() for keyword in ['login', 'signin', 'auth', '']) or \\
               any(keyword in str(form).lower() for keyword in ['username', 'password', 'login']):
                
                login_info['form_action'] = form_action
                
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
        try:
            if base_url and not login_url.startswith('http'):
                full_login_url = urljoin(base_url, login_url)
            else:
                full_login_url = login_url
            
            print(f"🔍 Accessing login page: {full_login_url}")
            
            response = self.session.get(full_login_url, timeout=30)
            if response.status_code != 200:
                return {'success': False, 'error': f'Cannot access login page: {response.status_code}'}
            
            login_info = self.detect_login_form(response.text)
            print(f"📝 Detected form fields: {login_info}")
            
            captcha_answer = self.solve_math_captcha(response.text)
            
            login_data = login_info['form_data'].copy()
            login_data[login_info['username_field']] = username
            login_data[login_info['password_field']] = password
            
            if login_info['captcha_field'] and captcha_answer:
                login_data[login_info['captcha_field']] = captcha_answer
            
            if login_info['form_action']:
                action_url = urljoin(full_login_url, login_info['form_action'])
            else:
                action_url = full_login_url
            
            print(f"🎯 Attempting login to: {action_url}")
            
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
        if any(keyword in response.url for keyword in ['client', 'dashboard', 'admin']):
            return True
        
        success_indicators = [
            'dashboard' in response.text.lower(),
            'logout' in response.text.lower(),
            'welcome' in response.text.lower(),
            'success' in response.text.lower()
        ]
        
        failure_indicators = [
            'invalid' in response.text.lower(),
            'error' in response.text.lower(),
            'failed' in response.text.lower(),
            'incorrect' in response.text.lower()
        ]
        
        if any(success_indicators) and not any(failure_indicators):
            return True
        
        if response.history and 'login' not in response.url:
            return True
            
        return False
    
    def test_protected_url(self, url, cookies=None):
        try:
            test_cookies = cookies or self.cookies
            response = self.session.get(url, cookies=test_cookies, timeout=10)
            return response.status_code == 200
        except:
            return False
PYEOF

# Create api_tester.py
cat > api_tester.py << 'PYEOF'
#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.working_apis = []
        
    def test_api_endpoint(self, api_info, auth_cookies=None):
        try:
            url = api_info['url']
            method = api_info.get('method', 'GET').upper()
            headers = api_info.get('headers', {})
            cookies = auth_cookies or api_info.get('cookies', {})
            
            print(f"🔧 Testing {method} {url}")
            
            request_kwargs = {
                'url': url,
                'headers': headers,
                'cookies': cookies,
                'timeout': 15
            }
            
            if method in ['POST', 'PUT'] and 'params' in api_info:
                request_kwargs['data'] = api_info['params']
            elif method == 'GET' and 'params' in api_info:
                request_kwargs['params'] = api_info['params']
            
            start_time = time.time()
            response = self.session.request(method, **request_kwargs)
            response_time = time.time() - start_time
            
            result = {
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'response_time': response_time,
                'success': response.status_code == 200,
                'timestamp': datetime.now().isoformat(),
                'request_headers': headers,
                'cookies_used': cookies,
                'api_info': api_info
            }
            
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    result['response'] = response.json()
                else:
                    result['response'] = response.text[:1000]
            except:
                result['response'] = response.text[:1000] if response.text else "No content"
            
            self.results.append(result)
            
            if result['success']:
                self.working_apis.append(result)
                print(f"✅ SUCCESS: Status {response.status_code}, Time: {response_time:.2f}s")
                if result.get('response'):
                    print(f"   📄 Response: {str(result['response'])[:100]}...")
            else:
                print(f"❌ FAILED: Status {response.status_code}")
            
            return result
            
        except Exception as e:
            error_result = {
                'url': api_info['url'],
                'method': api_info.get('method', 'GET'),
                'status_code': 0,
                'response_time': 0,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            self.results.append(error_result)
            print(f"💥 ERROR: {e}")
            return error_result
    
    def generate_python_code(self, api_result):
        api_info = api_result['api_info']
        
        code = f"""#!/usr/bin/env python3
import requests
import json

# API Configuration
url = "{api_info['url']}"
method = "{api_info.get('method', 'GET')}"

headers = {json.dumps(api_info.get('headers', {}), indent=4, ensure_ascii=False)}

cookies = {json.dumps(api_info.get('cookies', {}), indent=4, ensure_ascii=False)}
"""

        if api_info.get('method') in ['POST', 'PUT'] and api_info.get('params'):
            code += f"""
data = {json.dumps(api_info['params'], indent=4, ensure_ascii=False)}
"""
        elif api_info.get('method') == 'GET' and api_info.get('params'):
            code += f"""
params = {json.dumps(api_info['params'], indent=4, ensure_ascii=False)}
"""

        code += """
# Create session and make request
session = requests.Session()

try:
    if method == 'GET':
        response = session.get(url, headers=headers, cookies=cookies"""
        
        if api_info.get('method') == 'GET' and api_info.get('params'):
            code += ", params=params"
        
        code += """)
    elif method == 'POST':
        response = session.post(url, headers=headers, cookies=cookies"""
        
        if api_info.get('method') in ['POST', 'PUT'] and api_info.get('params'):
            code += ", data=data"
        
        code += """)
    else:
        response = session.request(method, url, headers=headers, cookies=cookies)

    print(f"Status Code: {response.status_code}")
    print(f"URL: {url}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("✅ SUCCESS - Response JSON:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print("✅ SUCCESS - Response Text:")
            print(response.text)
    else:
        print(f"❌ FAILED - Status: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"💥 Request failed: {e}")

print("\\n" + "="*50)
print("API Test Completed!")
"""

        return code
    
    def export_all_codes(self):
        exported = {}
        
        for i, api_result in enumerate(self.working_apis):
            python_code = self.generate_python_code(api_result)
            
            exported[f"api_{i+1}"] = {
                'python': python_code,
                'api_info': api_result['api_info'],
                'result': {
                    'status_code': api_result['status_code'],
                    'response_time': api_result['response_time'],
                    'success': api_result['success']
                }
            }
        
        return exported
    
    def get_stats(self):
        total = len(self.results)
        successful = len(self.working_apis)
        failed = total - successful
        
        return {
            'total_tested': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }
PYEOF

# Create utils/__init__.py
cat > utils/__init__.py << 'PYEOF'
# Utils package
PYEOF

echo "✅ All files created successfully!"
echo ""
echo "🚀 Now testing the installation..."
python -c "import requests, json, re; print('✅ Basic imports working')"

echo ""
echo "🎉 Installation completed successfully!"
echo "📁 Project location: ~/Universal-API-Tester"
echo "🚀 Run the tool: python main.py"
echo ""
echo "📋 Features available:"
echo "   • DevTools Data Parser"
echo "   • Automatic Login System" 
echo "   • API Testing"
echo "   • Python Code Generation"
EOF

# Script executable করুন
chmod +x install_complete.sh

# Installation run করুন
./install_complete.sh
