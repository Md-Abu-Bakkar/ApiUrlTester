#!/usr/bin/env python3
import requests
import json
import time

class MultiMethodTester:
    def __init__(self):
        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
        self.session = requests.Session()
    
    def test_all_methods(self, url, auth_data=None, custom_headers=None):
        """Try all HTTP methods to find working one"""
        results = {}
        
        for method in self.methods:
            try:
                print(f"🔄 Trying {method} request...")
                
                request_kwargs = {
                    'url': url,
                    'timeout': 10
                }
                
                # Add authentication if available
                if auth_data:
                    if 'cookies' in auth_data:
                        request_kwargs['cookies'] = auth_data['cookies']
                    if 'headers' in auth_data:
                        if custom_headers:
                            custom_headers.update(auth_data['headers'])
                        else:
                            custom_headers = auth_data['headers']
                
                if custom_headers:
                    request_kwargs['headers'] = custom_headers
                
                # Make request
                response = self.session.request(method, **request_kwargs)
                
                results[method] = {
                    'status_code': response.status_code,
                    'success': response.status_code == 200,
                    'response_time': 0,  # Would calculate in real implementation
                    'headers': dict(response.headers),
                    'response_preview': self.get_response_preview(response)
                }
                
                if response.status_code == 200:
                    print(f"✅ {method} successful!")
                    break
                else:
                    print(f"❌ {method} failed: {response.status_code}")
                    
            except Exception as e:
                results[method] = {
                    'success': False,
                    'error': str(e)
                }
                print(f"❌ {method} error: {e}")
        
        return results
    
    def get_response_preview(self, response):
        """Get preview of response content"""
        try:
            content = response.text
            if len(content) > 200:
                return content[:200] + '...'
            return content
        except:
            return "No content"
    
    def find_working_method(self, results):
        """Find which method worked"""
        for method, result in results.items():
            if result.get('success'):
                return method
        return None
