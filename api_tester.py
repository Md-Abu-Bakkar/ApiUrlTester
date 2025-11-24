#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime

class APITesterWithCodeGen:
    def __init__(self):
        self.session = requests.Session()
        self.results = []
        self.working_apis = []
        
    def test_api(self, api_info, auth_cookies=None):
        """Test a single API endpoint"""
        try:
            url = api_info['url']
            method = api_info.get('method', 'GET')
            headers = api_info.get('headers', {})
            cookies = auth_cookies or api_info.get('cookies', {})
            params = api_info.get('params', {})
            
            # Prepare request
            request_kwargs = {
                'url': url,
                'headers': headers,
                'cookies': cookies,
                'timeout': 30
            }
            
            # Add data for POST/PUT requests
            if method in ['POST', 'PUT'] and api_info.get('data'):
                request_kwargs['data'] = api_info['data']
            elif method == 'GET' and params:
                request_kwargs['params'] = params
            
            start_time = time.time()
            response = self.session.request(method, **request_kwargs)
            response_time = time.time() - start_time
            
            result = {
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': datetime.now().isoformat(),
                'success': response.status_code == 200,
                'headers': dict(response.headers),
                'request_headers': headers,
                'cookies_used': cookies,
                'api_info': api_info
            }
            
            # Try to parse response
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    result['response'] = response.json()
                else:
                    result['response'] = response.text
            except:
                result['response'] = response.text
            
            if result['success']:
                self.working_apis.append(result)
                print(f"✅ SUCCESS: {method} {url} - {response.status_code}")
            else:
                print(f"❌ FAILED: {method} {url} - {response.status_code}")
            
            self.results.append(result)
            return result
            
        except Exception as e:
            error_result = {
                'url': api_info['url'],
                'method': api_info.get('method', 'GET'),
                'status_code': 0,
                'response_time': 0,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e),
                'api_info': api_info
            }
            self.results.append(error_result)
            print(f"💥 ERROR: {api_info['url']} - {e}")
            return error_result
    
    def generate_python_code(self, api_result):
        """Generate Python code for working API"""
        api_info = api_result['api_info']
        url = api_info['url']
        method = api_info.get('method', 'GET')
        headers = api_info.get('headers', {})
        cookies = api_info.get('cookies', {})
        
        code = f"""#!/usr/bin/env python3
import requests
import json

# API Configuration
url = "{url}"
method = "{method}"

headers = {json.dumps(headers, indent=4)}

cookies = {json.dumps(cookies, indent=4)}
"""

        if method in ['POST', 'PUT'] and api_info.get('data'):
            code += f"""
data = {json.dumps(api_info['data'], indent=4)}
"""
        elif method == 'GET' and api_info.get('params'):
            code += f"""
params = {json.dumps(api_info['params'], indent=4)}
"""

        code += """
# Make request
session = requests.Session()

try:
    if method == 'GET':
        response = session.get(url, headers=headers, cookies=cookies"""
        
        if method == 'GET' and api_info.get('params'):
            code += ", params=params"
        
        code += """)
    elif method == 'POST':
        response = session.post(url, headers=headers, cookies=cookies"""
        
        if method in ['POST', 'PUT'] and api_info.get('data'):
            code += ", data=data"
        
        code += """)
    elif method == 'PUT':
        response = session.put(url, headers=headers, cookies=cookies"""
        
        if method in ['POST', 'PUT'] and api_info.get('data'):
            code += ", data=data"
        
        code += """)
    else:
        response = session.request(method, url, headers=headers, cookies=cookies)

    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Response JSON:", json.dumps(data, indent=2))
        except:
            print("Response Text:", response.text)
    else:
        print(f"Error: {response.status_code}")
        print("Response:", response.text)

except Exception as e:
    print(f"Request failed: {e}")

print("\\n✅ API call completed!")
"""

        return code
    
    def generate_curl_command(self, api_result):
        """Generate cURL command for working API"""
        api_info = api_result['api_info']
        url = api_info['url']
        method = api_info.get('method', 'GET')
        headers = api_info.get('headers', {})
        
        curl_cmd = f"curl -X {method} \\\n"
        curl_cmd += f"  '{url}' \\\n"
        
        for key, value in headers.items():
            curl_cmd += f"  -H '{key}: {value}' \\\n"
        
        if method in ['POST', 'PUT'] and api_info.get('data'):
            data_str = json.dumps(api_info['data'])
            curl_cmd += f"  --data-raw '{data_str}' \\\n"
        
        curl_cmd += "  --compressed"
        
        return curl_cmd
    
    def export_all_codes(self):
        """Export all working APIs as code"""
        exported_codes = {}
        
        for i, api_result in enumerate(self.working_apis):
            python_code = self.generate_python_code(api_result)
            curl_code = self.generate_curl_command(api_result)
            
            exported_codes[f"api_{i+1}"] = {
                'python': python_code,
                'curl': curl_code,
                'api_info': api_result['api_info']
            }
        
        return exported_codes
