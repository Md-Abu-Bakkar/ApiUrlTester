#!/usr/bin/env python3
import requests
import time
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cloudscraper

class CloudflareBypass:
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
    
    def bypass_cloudflare(self, url):
        """Bypass Cloudflare protection"""
        try:
            response = self.scraper.get(url)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'cookies': dict(response.cookies),
                    'user_agent': self.scraper.headers['User-Agent'],
                    'session_established': True
                }
            else:
                return self.selenium_bypass(url)
        except Exception as e:
            return self.selenium_bypass(url)
    
    def selenium_bypass(self, url):
        """Use Selenium to bypass Cloudflare"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Wait for Cloudflare challenge to complete
            time.sleep(5)
            
            # Get cookies
            cookies = driver.get_cookies()
            cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            
            driver.quit()
            
            return {
                'success': True,
                'cookies': cookie_dict,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'session_established': True
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def extract_cloudflare_cookies(self, html_content):
        """Extract Cloudflare cookies from page"""
        cookies = {}
        
        # Look for common Cloudflare cookie patterns
        cf_patterns = [
            r'__cfduid=([^;]+)',
            r'cf_clearance=([^;]+)',
            r'__cflb=([^;]+)'
        ]
        
        for pattern in cf_patterns:
            match = re.search(pattern, html_content)
            if match:
                cookie_name = pattern.split('=')[0]
                cookies[cookie_name] = match.group(1)
        
        return cookies
