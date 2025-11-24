#!/usr/bin/env python3
import os
import json
from advanced_login import UniversalLoginSystem
from devtools_parser import AdvancedDevToolsParser
from api_tester import APITesterWithCodeGen

class UniversalAPITester:
    def __init__(self):
        self.parser = AdvancedDevToolsParser()
        self.login_system = UniversalLoginSystem()
        self.tester = APITesterWithCodeGen()
        self.config = {}
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {}
    
    def save_config(self):
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        self.clear_screen()
        print("🚀 UNIVERSAL API TESTER - PROFESSIONAL EDITION")
        print("=" * 60)
        print()
    
    def devtools_import_menu(self):
        self.print_header()
        print("📋 DEVTOLS DATA IMPORT")
        print("-" * 40)
        print()
        
        print("Paste your DevTools data below:")
        print("(Press Ctrl+D when finished)")
        print()
        
        content = ""
        try:
            while True:
                line = input()
                content += line + "\n"
        except EOFError:
            pass
        
        if not content.strip():
            print("❌ No data provided")
            input("Press Enter to continue...")
            return
        
        print("\n🔄 Parsing DevTools data...")
        apis = self.parser.parse_devtools_content(content)
        
        print(f"✅ Found {len(apis)} APIs")
        
        # Show detected APIs
        for i, api in enumerate(apis, 1):
            print(f"{i}. {api['method']} {api['url']}")
            if api['requires_login']:
                print("   🔐 Requires Login")
        
        # Check if login is needed
        login_api = self.parser.extract_login_info(apis)
        data_apis = self.parser.extract_data_apis(apis)
        
        if login_api and data_apis:
            print(f"\n🔑 Login required for {len(data_apis)} APIs")
            self.setup_login_and_test(login_api, data_apis)
        elif data_apis:
            print(f"\n🎯 Testing {len(data_apis)} APIs without login...")
            self.test_apis_directly(data_apis)
        else:
            print("❌ No testable APIs found")
        
        input("\nPress Enter to continue...")
    
    def setup_login_and_test(self, login_api, data_apis):
        """Setup login and test APIs"""
        print("\n🔐 LOGIN CONFIGURATION")
        print("-" * 30)
        
        # Get base URL from login API
        base_url = login_api['url'].split('/login')[0] if '/login' in login_api['url'] else None
        
        username = input("Username/Email: ").strip()
        password = input("Password: ").strip()
        login_url = input(f"Login URL [{login_api['url']}]: ").strip() or login_api['url']
        
        print(f"\n🔄 Attempting login to: {login_url}")
        login_result = self.login_system.perform_login(login_url, username, password, base_url)
        
        if login_result['success']:
            print("✅ Login successful!")
            print(f"🍪 Session cookies: {len(login_result['cookies'])}")
            
            # Test APIs with authentication
            self.test_apis_with_auth(data_apis, login_result['cookies'])
        else:
            print(f"❌ Login failed: {login_result.get('error', 'Unknown error')}")
    
    def test_apis_with_auth(self, apis, cookies):
        """Test APIs with authentication"""
        print(f"\n🎯 Testing {len(apis)} APIs with authentication...")
        
        for i, api in enumerate(apis, 1):
            print(f"\nTesting {i}/{len(apis)}: {api['method']} {api['url']}")
            result = self.tester.test_api(api, cookies)
            
            if result['success']:
                print("✅ SUCCESS - API is working!")
            else:
                print(f"❌ FAILED - Status: {result['status_code']}")
        
        self.show_results()
    
    def test_apis_directly(self, apis):
        """Test APIs without authentication"""
        print(f"\n🎯 Testing {len(apis)} APIs directly...")
        
        for i, api in enumerate(apis, 1):
            print(f"\nTesting {i}/{len(apis)}: {api['method']} {api['url']}")
            result = self.tester.test_api(api)
            
            if result['success']:
                print("✅ SUCCESS - API is working!")
            else:
                print(f"❌ FAILED - Status: {result['status_code']}")
        
        self.show_results()
    
    def show_results(self):
        """Show testing results and export options"""
        working_count = len(self.tester.working_apis)
        total_count = len(self.tester.results)
        
        print(f"\n📊 TESTING COMPLETED")
        print(f"✅ Working APIs: {working_count}/{total_count}")
        
        if working_count > 0:
            print(f"\n💾 EXPORT OPTIONS:")
            print("1. View Python Code")
            print("2. View cURL Commands") 
            print("3. Save All Codes to Files")
            print("4. Back to Menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self.show_python_codes()
            elif choice == '2':
                self.show_curl_commands()
            elif choice == '3':
                self.save_all_codes()
    
    def show_python_codes(self):
        """Show generated Python codes"""
        exported = self.tester.export_all_codes()
        
        for name, codes in exported.items():
            print(f"\n🐍 {name.upper()} - PYTHON CODE")
            print("=" * 50)
            print(codes['python'])
            print("\n" + "=" * 50)
            
            input("\nPress Enter for next code...")
    
    def show_curl_commands(self):
        """Show generated cURL commands"""
        exported = self.tester.export_all_codes()
        
        for name, codes in exported.items():
            print(f"\n🔄 {name.upper()} - CURL COMMAND")
            print("=" * 50)
            print(codes['curl'])
            print("\n" + "=" * 50)
            
            input("\nPress Enter for next command...")
    
    def save_all_codes(self):
        """Save all codes to files"""
        exported = self.tester.export_all_codes()
        
        os.makedirs('exported_codes', exist_ok=True)
        
        for name, codes in exported.items():
            # Save Python code
            with open(f'exported_codes/{name}.py', 'w') as f:
                f.write(codes['python'])
            
            # Save cURL command
            with open(f'exported_codes/{name}.curl', 'w') as f:
                f.write(codes['curl'])
            
            # Save API info
            with open(f'exported_codes/{name}_info.json', 'w') as f:
                json.dump(codes['api_info'], f, indent=2)
        
        print(f"✅ All codes saved to 'exported_codes/' directory")
        input("Press Enter to continue...")
    
    def main_menu(self):
        while True:
            self.print_header()
            print("1. 📋 Import DevTools Data")
            print("2. 🔐 Manual Login Setup") 
            print("3. 🎯 Test Single API")
            print("4. 📊 View Previous Results")
            print("5. ⚙️  Configuration")
            print("6. 🚪 Exit")
            print()
            
            choice = input("Select option: ").strip()
            
            if choice == '1':
                self.devtools_import_menu()
            elif choice == '2':
                self.manual_login_setup()
            elif choice == '3':
                self.test_single_api()
            elif choice == '4':
                self.view_previous_results()
            elif choice == '5':
                self.configuration_menu()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")

def main():
    tester = UniversalAPITester()
    tester.main_menu()

if __name__ == '__main__':
    main()
