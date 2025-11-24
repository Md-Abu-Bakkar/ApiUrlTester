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
        """Test a single API endpoint"""
        try:
            url = api_info['url']
            method = api_info.get('method', 'GET').upper()
            headers = api_info.get('headers', {})
            cookies = auth_cookies or api_info.get('cookies', {})
            
            print(f"🔧 Testing {method} {url}")
            
            # Prepare request
            request_kwargs = {
                'url': url,
                'headers': headers,
                'cookies': cookies,
                'timeout': 15
            }
            
            # Add data based on method
            if method in ['POST', 'PUT'] and 'params' in api_info:
                request_kwargs['data'] = api_info['params']
            elif method == 'GET' and 'params' in api_info:
                request_kwargs['params'] = api_info['params']
            
            start_time = time.time()
            response = self.session.request(method, **request_kwargs)
            response_time = time.time() - start_time
            
            # Create result
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
            
            # Parse response
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    result['response'] = response.json()
                else:
                    result['response'] = response.text[:1000]  # Limit text response
            except:
                result['response'] = response.text[:1000] if response.text else "No content"
            
            # Store result
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
        """Generate Python code for working API"""
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

        # Add request data
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
    elif method == 'PUT':
        response = session.put(url, headers=headers, cookies=cookies"""
        
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
        """Export all working APIs as code files"""
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
        """Get testing statistics"""
        total = len(self.results)
        successful = len(self.working_apis)
        failed = total - successful
        
        return {
            'total_tested': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }
