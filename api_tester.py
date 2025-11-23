#!/usr/bin/env python3
import requests
import json
import time
from datetime import datetime
from urllib.parse import urlparse

class APITester:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Universal-API-Tester/1.0'
        })
        
    def test_endpoint(self, url, method='GET', headers=None, body=None, timeout=30):
        """
        Test any API endpoint with given parameters
        """
        start_time = time.time()
        
        try:
            # Prepare request parameters
            request_params = {
                'url': url,
                'headers': headers or {},
                'timeout': timeout
            }
            
            if method in ['POST', 'PUT', 'PATCH'] and body:
                if isinstance(body, (dict, list)):
                    request_params['json'] = body
                else:
                    request_params['data'] = body
                    
            # Make the request
            response = self.session.request(method, **request_params)
            response_time = time.time() - start_time
            
            # Prepare result
            result = {
                'url': url,
                'method': method,
                'headers': dict(response.headers),
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': datetime.now().isoformat(),
                'success': response.status_code < 400
            }
            
            # Try to parse response
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    result['response'] = response.json()
                else:
                    result['response'] = response.text
            except:
                result['response'] = response.text
                
            return result
            
        except requests.exceptions.Timeout:
            return {
                'url': url,
                'method': method,
                'status_code': 408,
                'response_time': timeout,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': 'Request timeout',
                'response': None
            }
        except requests.exceptions.ConnectionError:
            return {
                'url': url,
                'method': method,
                'status_code': 0,
                'response_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': 'Connection error',
                'response': None
            }
        except Exception as e:
            return {
                'url': url,
                'method': method,
                'status_code': 0,
                'response_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e),
                'response': None
            }
            
    def test_multiple_endpoints(self, endpoints):
        """
        Test multiple API endpoints
        """
        results = []
        for endpoint in endpoints:
            result = self.test_endpoint(
                endpoint['url'],
                endpoint.get('method', 'GET'),
                endpoint.get('headers'),
                endpoint.get('body')
            )
            results.append(result)
            
        return results

if __name__ == '__main__':
    # Test the class
    tester = APITester()
    print("API Tester class loaded successfully!")
