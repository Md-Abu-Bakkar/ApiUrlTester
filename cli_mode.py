#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from data_manager import DataManager
from api_tester import APITester
from utils.helpers import validate_url

# Import advanced modules
from advanced_login import AdvancedLoginSystem
from captcha_solver import CaptchaSolver
from cloudflare_bypass import CloudflareBypass
from devtools_parser import DevToolsParser
from multi_method_tester import MultiMethodTester
from code_exporter import CodeExporter

class CLIMenu:
    def __init__(self):
        self.data_manager = DataManager()
        self.api_tester = APITester()
        self.config = self.load_config()
        
        # Initialize advanced systems
        self.login_system = AdvancedLoginSystem()
        self.captcha_solver = CaptchaSolver()
        self.cloudflare_bypass = CloudflareBypass()
        self.devtools_parser = DevToolsParser()
        self.multi_tester = MultiMethodTester()
        self.code_exporter = CodeExporter()
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'auto_save': True, 'timeout': 30}
            
    def save_config(self):
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
            print("✅ Configuration saved successfully!")
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
    def print_header(self):
        self.clear_screen()
        print("=" * 70)
        print("           🚀 UNIVERSAL API TESTER - ADVANCED EDITION")
        print("=" * 70)
        print()
        
    def main_menu(self):
        while True:
            self.print_header()
            print("1. 🔧 Basic API Testing")
            print("2. 🔐 Advanced Login System")
            print("3. 🧪 DevTools Parser")
            print("4. 🔄 Multi-Method Tester") 
            print("5. 💾 Code Export")
            print("6. 🤖 Telegram Bot Control")
            print("7. ⚙️  Configuration")
            print("8. 📊 View Results")
            print("9. 🚪 Exit")
            print()
            
            choice = input("Select option (1-9): ").strip()
            
            if choice == '1':
                self.basic_api_test()
            elif choice == '2':
                self.advanced_login_menu()
            elif choice == '3':
                self.devtools_parser_menu()
            elif choice == '4':
                self.multi_method_test()
            elif choice == '5':
                self.code_export_menu()
            elif choice == '6':
                self.telegram_menu()
            elif choice == '7':
                self.config_menu()
            elif choice == '8':
                self.view_results_menu()
            elif choice == '9':
                print("👋 Goodbye!")
                break
            else:
                input("❌ Invalid option. Press Enter to continue...")

    def advanced_login_menu(self):
        """Advanced login system with all features"""
        while True:
            self.print_header()
            print("🔐 ADVANCED LOGIN SYSTEM")
            print("-" * 50)
            print()
            
            print("1. 🚀 Smart Login (Auto Captcha + Cloudflare)")
            print("2. 🔍 Auto-Detect Login System")
            print("3. 🛡️  Cloudflare Bypass Only")
            print("4. 🧮 Math Captcha Solver")
            print("5. ↩️  Back to Main Menu")
            print()
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.smart_login_flow()
            elif choice == '2':
                self.auto_detect_login()
            elif choice == '3':
                self.cloudflare_bypass_menu()
            elif choice == '4':
                self.math_captcha_solver()
            elif choice == '5':
                break
            else:
                input("❌ Invalid option. Press Enter to continue...")

    def smart_login_flow(self):
        """Complete smart login flow"""
        self.print_header()
        print("🚀 SMART LOGIN FLOW")
        print("-" * 50)
        print()
        
        login_url = input("Enter login URL: ").strip()
        username = input("Enter username/email: ").strip()
        password = input("Enter password: ").strip()
        target_url = input("Enter target API URL (optional): ").strip()
        
        print("\n🔄 Starting smart login process...")
        
        try:
            # Step 1: Cloudflare bypass
            print("1. 🛡️  Checking Cloudflare protection...")
            cf_result = self.cloudflare_bypass.bypass_cloudflare(login_url)
            if cf_result.get('success'):
                print("   ✅ Cloudflare bypassed!")
            else:
                print("   ℹ️  No Cloudflare protection detected")
            
            # Step 2: Perform login
            print("2. 🔐 Attempting login...")
            login_result = self.login_system.perform_login(login_url, username, password)
            
            if login_result.get('success'):
                print("   ✅ Login successful!")
                print(f"   📊 Status: {login_result.get('status_code')}")
                print(f"   🍪 Cookies stored: {len(self.login_system.cookies)}")
                
                # Step 3: Test target API with authentication
                if target_url:
                    print("3. 🎯 Testing protected API...")
                    self.test_with_auth(target_url, self.login_system.cookies)
            else:
                print(f"   ❌ Login failed: {login_result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error in smart login: {e}")
        
        input("\nPress Enter to continue...")

    def devtools_parser_menu(self):
        """DevTools content parser"""
        self.print_header()
        print("🧪 DEVTOOLS PARSER")
        print("-" * 50)
        print()
        
        print("Paste any content from browser DevTools:")
        print("(cURL, fetch, headers, JSON, etc.)")
        print("Press Ctrl+D when done:")
        print()
        
        user_input = ""
        try:
            while True:
                line = input()
                user_input += line + "\n"
        except EOFError:
            pass
        
        if not user_input.strip():
            print("❌ No input provided")
            input("Press Enter to continue...")
            return
        
        print("\n🔄 Parsing content...")
        parsed_data = self.devtools_parser.parse_any_input(user_input)
        
        print("\n✅ Parsing Results:")
        print(f"🔗 URL: {parsed_data.get('url') or 'Not found'}")
        print(f"⚡ Method: {parsed_data.get('method', 'GET')}")
        print(f"📋 Headers: {len(parsed_data.get('headers', {}))} items")
        print(f"🍪 Cookies: {len(parsed_data.get('cookies', {}))} items")
        
        if parsed_data.get('json_body'):
            print(f"📄 JSON Body: {json.dumps(parsed_data['json_body'], indent=2)[:200]}...")
        elif parsed_data.get('data'):
            print(f"📦 Data: {parsed_data['data'][:200]}...")
        
        # Test the parsed request
        if parsed_data.get('url'):
            test = input("\nTest this request? (y/n): ").strip().lower()
            if test == 'y':
                self.test_parsed_request(parsed_data)
        
        input("\nPress Enter to continue...")

    def multi_method_test(self):
        """Test API with multiple methods"""
        self.print_header()
        print("🔄 MULTI-METHOD API TESTER")
        print("-" * 50)
        print()
        
        url = input("Enter API URL: ").strip()
        
        if not validate_url(url):
            input("❌ Invalid URL format. Press Enter to continue...")
            return
        
        print(f"\n🔄 Testing all methods on: {url}")
        print("This may take a few seconds...")
        
        results = self.multi_tester.test_all_methods(url)
        
        working_method = self.multi_tester.find_working_method(results)
        if working_method:
            print(f"\n✅ Working method found: {working_method}")
            
            # Export code for working method
            request_data = {
                'url': url,
                'method': working_method,
                'headers': results[working_method].get('headers', {})
            }
            
            # Save all code formats
            python_code = self.code_exporter.export_python_code(request_data)
            curl_code = self.code_exporter.export_curl_code(request_data)
            js_code = self.code_exporter.export_javascript_code(request_data)
            
            self.code_exporter.save_code_file(python_code, 'api_request', 'py')
            self.code_exporter.save_code_file(curl_code, 'api_request', 'curl')
            self.code_exporter.save_code_file(js_code, 'api_request', 'js')
            
            print("\n💾 Code exported to 'exported_code/' directory:")
            print("   📝 Python: api_request.py")
            print("   🔄 cURL: api_request.curl") 
            print("   📜 JavaScript: api_request.js")
        else:
            print("\n❌ No working method found")
        
        input("\nPress Enter to continue...")

    def basic_api_test(self):
        """Original basic API testing"""
        self.print_header()
        print("🔧 BASIC API TESTING")
        print("-" * 50)
        print()
        
        url = input("Enter API URL: ").strip()
        if not validate_url(url):
            input("❌ Invalid URL format. Press Enter to continue...")
            return
            
        print("\nAvailable methods: GET, POST, PUT, DELETE")
        method = input("Enter method [GET]: ").strip().upper() or "GET"
        
        print("\nEnter headers (JSON format, empty for default):")
        headers_input = input().strip()
        headers = json.loads(headers_input) if headers_input else {}
        
        body = {}
        if method in ['POST', 'PUT']:
            print("\nEnter request body (JSON format, empty for none):")
            body_input = input().strip()
            body = json.loads(body_input) if body_input else {}
            
        print(f"\n🔄 Testing {method} {url}...")
        
        try:
            response = self.api_tester.test_endpoint(url, method, headers, body)
            self.data_manager.save_response(response)
            
            print("✅ API Test Completed!")
            print(f"📊 Status Code: {response.get('status_code')}")
            print(f"⏱️  Response Time: {response.get('response_time', 0):.2f}s")
            print(f"💾 Saved to: data.json, data.txt")
            
            # Show preview
            response_data = response.get('response', {})
            if isinstance(response_data, dict):
                preview = json.dumps(response_data, indent=2)[:500] + "..." 
            else:
                preview = str(response_data)[:500] + "..."
                
            print(f"\n📄 Response Preview:\n{preview}")
            
        except Exception as e:
            print(f"❌ Error testing API: {e}")
            
        input("\nPress Enter to continue...")

    # ... (other methods like config_menu, view_results_menu, telegram_menu remain same)

def run_cli_mode():
    """Entry point for CLI mode"""
    try:
        menu = CLIMenu()
        menu.main_menu()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to continue...")

if __name__ == '__main__':
    run_cli_mode()
