#!/usr/bin/env python3
import re
import requests
import base64
from PIL import Image
import io
import math

class CaptchaSolver:
    def __init__(self):
        self.supported_types = ['math', 'text', 'image', 'cloudflare']
    
    def solve_math_captcha(self, text):
        """Solve simple math captchas like 'What is 5 + 3?'"""
        try:
            # Extract numbers and operator
            numbers = re.findall(r'\d+', text)
            if len(numbers) >= 2:
                num1 = int(numbers[0])
                num2 = int(numbers[1])
                
                if '+' in text:
                    return str(num1 + num2)
                elif '-' in text:
                    return str(num1 - num2)
                elif '*' in text or '×' in text:
                    return str(num1 * num2)
                elif '/' in text or '÷' in text:
                    return str(num1 // num2) if num2 != 0 else '0'
            
            # Try to evaluate the expression directly
            math_expr = re.findall(r'[0-9+\-*/().]+', text)
            if math_expr:
                try:
                    result = eval(math_expr[0])
                    return str(int(result))
                except:
                    pass
            
            return None
        except:
            return None
    
    def detect_captcha_type(self, html_content):
        """Detect what type of captcha is present"""
        html_lower = html_lower.lower()
        
        if any(word in html_lower for word in ['captcha', 'recaptcha', 'hcaptcha']):
            if 'recaptcha' in html_lower:
                return 'recaptcha'
            elif 'hcaptcha' in html_lower:
                return 'hcaptcha'
            else:
                return 'image_captcha'
        
        # Check for math captcha
        math_patterns = [
            r'what is \d+ [+\-*/] \d+',
            r'\d+ [+\-*/] \d+ =',
            r'solve.*\d+ [+\-*/] \d+'
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, html_lower, re.IGNORECASE):
                return 'math_captcha'
        
        return 'unknown'
    
    def extract_captcha_image(self, html_content):
        """Extract captcha image URL from HTML"""
        soup = BeautifulSoup(html_content, 'html.parser')
        captcha_imgs = soup.find_all('img', src=re.compile(r'captcha', re.I))
        
        for img in captcha_imgs:
            src = img.get('src', '')
            if src:
                return src
        return None
    
    def solve_automatically(self, html_content):
        """Try to solve captcha automatically"""
        captcha_type = self.detect_captcha_type(html_content)
        
        if captcha_type == 'math_captcha':
            # Extract math question
            math_match = re.search(r'(what is|solve)?\s*(\d+)\s*([+\-*/])\s*(\d+)', html_content, re.IGNORECASE)
            if math_match:
                num1 = int(math_match.group(2))
                operator = math_match.group(3)
                num2 = int(math_match.group(4))
                
                if operator == '+':
                    return str(num1 + num2)
                elif operator == '-':
                    return str(num1 - num2)
                elif operator == '*':
                    return str(num1 * num2)
                elif operator == '/':
                    return str(num1 // num2) if num2 != 0 else '0'
        
        return None
    
    def manual_captcha_solver(self, image_url=None, question=None):
        """Handle manual captcha solving"""
        if image_url:
            print(f"🔍 Captcha Image URL: {image_url}")
            print("Please solve the captcha manually and enter the value:")
            return input("Captcha Answer: ")
        elif question:
            print(f"❓ Captcha Question: {question}")
            return input("Your Answer: ")
        else:
            return input("Enter captcha solution: ")
