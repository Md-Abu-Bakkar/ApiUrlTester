#!/usr/bin/env python3
import os
import json
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from devtools_parser import AdvancedDevToolsParser
from advanced_login import UniversalLoginSystem
from api_tester import APITester

class UniversalAPITester:
    def __init__(self):
        self.parser = AdvancedDevToolsParser()
        self.login_system = UniversalLoginSystem()
        self.tester = APITester()
        self.config = {}
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        self.clear_screen()
        print("🚀 UNIVERSAL API TESTER - PROFESSIONAL EDITION")
        print("=" * 60)
        print()
    
    def devtools_import_flow(self):
        """Complete DevTools import and testing flow"""
        self.print_header()
        print("📋 DEVTOLS DATA IMPORT & TESTING")
        print("=" * 50)
        print()
        
        print("Paste your DevTools data below:")
        print("(Press Ctrl+D when finished)")
        print()
        
        # Collect multi-line input
        content_lines = []
        try:
            while True:
                line = input()
                content_lines.append(line)
        except EOFError:
            pass
        
        content = '\n'.join(content_lines)
        
        if not content.strip():
            print("❌ No data provided")
            input("Press Enter to continue...")
            return
        
        print("\n🔄 Parsing DevTools data...")
        
        # Parse the content
        try:
            requests = self.parser.parse_raw_devtools(content)
            
            if not requests:
                print("❌ No API endpoints found in the data")
                input("Press Enter to continue...")
                return
            
            # Show detected APIs
            print(f"\n📊 Detected {len(requests)} API endpoints:")
            for i, req in enumerate(requests, 1):
                print(f"{i}. {req['method']} {req['url']}")
                if req['requires_login']:
                    print("   🔐 Requires Login")
                print(f"   Type: {req['api_type']}")
            
            # Extract different types of APIs
            login_api = self.parser.extract_login_info(requests)
            data_apis = self.parser.extract_data_apis(requests)
            base_url = self.parser.get_base_url(requests)
            
            print(f"\n🎯 Summary:")
            print(f"   • Login APIs: {1 if login_api else 0}")
            print(f"   • Data APIs: {len(data_apis)}")
            print(f"   • Base URL: {base_url}")
            
            # Ask user what to do
            print(f"\n🔧 What would you like to do?")
            print("1. Test all APIs with login (if required)")
            print("2. Test only data APIs without login")
            print("3. Manual login setup")
            print("4. Back to menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.test_with_login(login_api, data_apis, base_url)
            elif choice == '2':
                self.test_without_login(data_apis)
            elif choice == '3':
                self.manual_login_setup(login_api, data_apis, base_url)
            elif choice == '4':
                return
            else:
                print("❌ Invalid option")
                
        except Exception as e:
            print(f"❌ Error parsing data: {e}")
        
        input("\nPress Enter to continue...")
    
    def test_with_login(self, login_api, data_apis, base_url):
        """Test APIs with login"""
        if not login_api:
            print("❌ No login API found in the data")
            print("🔧 Please provide login information manually")
            self.manual_login_setup(login_api, data_apis, base_url)
            return
        
        print(f"\n🔐 LOGIN CONFIGURATION")
        print("=" * 30)
        
        username = input("Username/Email: ").strip()
        password = input("Password: ").strip()
        
        if not username or not password:
            print("❌ Username and password required")
            return
        
        print(f"\n🔄 Attempting login...")
        login_result = self.login_system.perform_login(
            login_api['url'], 
            username, 
            password, 
            base_url
        )
        
        if login_result['success']:
            print("✅ Login successful! Testing APIs...")
            self.test_apis(data_apis, login_result['cookies'])
        else:
            print(f"❌ Login failed: {login_result.get('error', 'Unknown error')}")
    
    def test_without_login(self, data_apis):
        """Test APIs without login"""
        if not data_apis:
            print("❌ No data APIs found to test")
            return
        
        print(f"\n🎯 Testing {len(data_apis)} APIs without authentication...")
        self.test_apis(data_apis)
    
    def manual_login_setup(self, login_api, data_apis, base_url):
        """Manual login setup"""
        print(f"\n🔐 MANUAL LOGIN SETUP")
        print("=" * 30)
        
        login_url = input(f"Login URL [{login_api['url'] if login_api else ''}]: ").strip()
        if not login_url and login_api:
            login_url = login_api['url']
        
        username = input("Username/Email: ").strip()
        password = input("Password: ").strip()
        
        if not login_url or not username or not password:
            print("❌ Login URL, username and password required")
            return
        
        if not base_url:
            base_url = input("Base URL (optional): ").strip()
        
        print(f"\n🔄 Attempting login...")
        login_result = self.login_system.perform_login(login_url, username, password, base_url)
        
        if login_result['success']:
            print("✅ Login successful! Testing APIs...")
            self.test_apis(data_apis, login_result['cookies'])
        else:
            print(f"❌ Login failed: {login_result.get('error', 'Unknown error')}")
    
    def test_apis(self, apis, auth_cookies=None):
        """Test a list of APIs"""
        if not apis:
            print("❌ No APIs to test")
            return
        
        print(f"\n🧪 TESTING {len(apis)} APIS...")
        print("=" * 50)
        
        for i, api in enumerate(apis, 1):
            print(f"\n[{i}/{len(apis)}] ", end="")
            self.tester.test_api_endpoint(api, auth_cookies)
        
        self.show_test_results()
    
    def show_test_results(self):
        """Show testing results and export options"""
        stats = self.tester.get_stats()
        
        print(f"\n📊 TESTING COMPLETED")
        print("=" * 30)
        print(f"✅ Successful: {stats['successful']}")
        print(f"❌ Failed: {stats['failed']}")
        print(f"📈 Success Rate: {stats['success_rate']:.1f}%")
        
        if stats['successful'] > 0:
            print(f"\n💾 EXPORT OPTIONS:")
            print("1. View Python Codes")
            print("2. Save All Codes to Files")
            print("3. View Detailed Results")
            print("4. Back to Menu")
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                self.view_python_codes()
            elif choice == '2':
                self.save_all_codes()
            elif choice == '3':
                self.view_detailed_results()
    
    def view_python_codes(self):
        """View generated Python codes"""
        exported = self.tester.export_all_codes()
        
        for name, data in exported.items():
            print(f"\n🐍 {name.upper()} - PYTHON CODE")
            print("=" * 60)
            print(data['python'])
            print("=" * 60)
            
            if input("\nPress Enter for next code or 'q' to quit: ").strip().lower() == 'q':
                break
    
    def save_all_codes(self):
        """Save all codes to files"""
        exported = self.tester.export_all_codes()
        
        # Create directory
        os.makedirs('exported_codes', exist_ok=True)
        
        for name, data in exported.items():
            # Save Python code
            with open(f'exported_codes/{name}.py', 'w', encoding='utf-8') as f:
                f.write(data['python'])
            
            # Save API info
            with open(f'exported_codes/{name}_info.json', 'w', encoding='utf-8') as f:
                json.dump(data['api_info'], f, indent=2, ensure_ascii=False)
        
        print(f"✅ All codes saved to 'exported_codes/' directory")
        print(f"📁 {len(exported)} Python files created")
        input("Press Enter to continue...")
    
    def view_detailed_results(self):
        """View detailed testing results"""
        print(f"\n📋 DETAILED RESULTS")
        print("=" * 50)
        
        for i, result in enumerate(self.tester.results, 1):
            status_icon = "✅" if result['success'] else "❌"
            print(f"\n{i}. {status_icon} {result['method']} {result['url']}")
            print(f"   Status: {result['status_code']}, Time: {result['response_time']:.2f}s")
            
            if not result['success'] and 'error' in result:
                print(f"   Error: {result['error']}")
        
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        while True:
            self.print_header()
            print("1. 📋 Import DevTools Data & Test APIs")
            print("2. 🧪 Test Single API URL")
            print("3. 🔐 Manual Login Test")
            print("4. 📊 View Previous Results")
            print("5. 💾 Export Management")
            print("6. 🚪 Exit")
            print()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.devtools_import_flow()
            elif choice == '2':
                self.test_single_api()
            elif choice == '3':
                self.manual_login_test()
            elif choice == '4':
                self.view_previous_results()
            elif choice == '5':
                self.export_management()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def test_single_api(self):
        """Test a single API URL"""
        self.print_header()
        print("🧪 TEST SINGLE API")
        print("=" * 40)
        print()
        
        url = input("Enter API URL: ").strip()
        if not url:
            print("❌ URL required")
            return
        
        method = input("Method [GET]: ").strip().upper() or "GET"
        
        api_info = {
            'url': url,
            'method': method,
            'headers': {},
            'cookies': {}
        }
        
        print(f"\n🔄 Testing {method} {url}...")
        result = self.tester.test_api_endpoint(api_info)
        
        if result['success']:
            print("✅ API test successful!")
            
            # Generate and show code
            code = self.tester.generate_python_code(result)
            print(f"\n🐍 GENERATED PYTHON CODE:")
            print("=" * 50)
            print(code)
            print("=" * 50)
            
            save = input("\nSave this code? (y/n): ").strip().lower()
            if save == 'y':
                os.makedirs('exported_codes', exist_ok=True)
                with open('exported_codes/single_api.py', 'w', encoding='utf-8') as f:
                    f.write(code)
                print("✅ Code saved to 'exported_codes/single_api.py'")
        else:
            print("❌ API test failed")
        
        input("\nPress Enter to continue...")
    
    def manual_login_test(self):
        """Manual login test"""
        self.print_header()
        print("🔐 MANUAL LOGIN TEST")
        print("=" * 40)
        print()
        
        login_url = input("Login URL: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        base_url = input("Base URL (optional): ").strip()
        
        if not login_url or not username or not password:
            print("❌ Login URL, username and password required")
            return
        
        print(f"\n🔄 Attempting login...")
        login_result = self.login_system.perform_login(login_url, username, password, base_url)
        
        if login_result['success']:
            print("✅ Login successful!")
            print(f"🍪 Session cookies: {len(login_result['cookies'])}")
            
            # Test a protected URL
            test_url = input("\nTest protected URL (optional): ").strip()
            if test_url:
                can_access = self.login_system.test_protected_url(test_url, login_result['cookies'])
                if can_access:
                    print("✅ Can access protected URL!")
                else:
                    print("❌ Cannot access protected URL")
        else:
            print(f"❌ Login failed: {login_result.get('error', 'Unknown error')}")
        
        input("\nPress Enter to continue...")
    
    def view_previous_results(self):
        """View previous testing results"""
        if not self.tester.results:
            print("❌ No previous results found")
            input("Press Enter to continue...")
            return
        
        self.show_test_results()
    
    def export_management(self):
        """Manage exported codes"""
        self.print_header()
        print("💾 EXPORT MANAGEMENT")
        print("=" * 40)
        print()
        
        if not os.path.exists('exported_codes'):
            print("❌ No exported codes directory found")
            input("Press Enter to continue...")
            return
        
        files = os.listdir('exported_codes')
        if not files:
            print("❌ No exported files found")
            input("Press Enter to continue...")
            return
        
        print(f"📁 Found {len(files)} files in 'exported_codes/':")
        for file in files:
            print(f"  📄 {file}")
        
        print(f"\n1. View a file")
        print("2. Delete all exports")
        print("3. Back to menu")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == '1':
            filename = input("Enter filename: ").strip()
            if filename in files:
                with open(f'exported_codes/{filename}', 'r', encoding='utf-8') as f:
                    print(f"\n📄 {filename}:")
                    print("=" * 50)
                    print(f.read())
                    print("=" * 50)
            else:
                print("❌ File not found")
        elif choice == '2':
            confirm = input("Delete all exported files? (y/n): ").strip().lower()
            if confirm == 'y':
                for file in files:
                    os.remove(f'exported_codes/{file}')
                print("✅ All exported files deleted")
        
        input("\nPress Enter to continue...")

def main():
    tester = UniversalAPITester()
    tester.main_menu()

if __name__ == '__main__':
    main()
