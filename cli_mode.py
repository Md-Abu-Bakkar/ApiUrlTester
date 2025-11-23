# Add these imports at the top
from advanced_login import AdvancedLoginSystem
from captcha_solver import CaptchaSolver
from devtools_parser import DevToolsParser
from cloudflare_bypass import CloudflareBypass
from multi_method_tester import MultiMethodTester
from code_exporter import CodeExporter

# Add these new methods to the CLIMenu class:

def advanced_login_menu(self):
    """Advanced login system with captcha and Cloudflare bypass"""
    self.print_header()
    print("🔐 ADVANCED LOGIN SYSTEM")
    print("-" * 40)
    print()
    
    login_system = AdvancedLoginSystem()
    captcha_solver = CaptchaSolver()
    cloudflare_bypass = CloudflareBypass()
    
    print("1. 🔍 Auto-Detect Login System")
    print("2. 🚀 Smart Login (Auto Captcha + Cloudflare)")
    print("3. ↩️ Back")
    print()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        self.auto_detect_login()
    elif choice == '2':
        self.smart_login_flow()
    elif choice == '3':
        return
    else:
        input("❌ Invalid option. Press Enter to continue...")

def auto_detect_login(self):
    """Auto-detect login system type"""
    login_url = input("Enter login URL: ").strip()
    username = input("Enter username/email: ").strip()
    password = input("Enter password: ").strip()
    
    login_system = AdvancedLoginSystem()
    
    print("🔄 Analyzing login system...")
    login_info = login_system.detect_login_type(login_url, username, password)
    
    print("\n📊 Login System Analysis:")
    print(f"🔗 URL: {login_info.get('url')}")
    print(f"📄 Content Type: {login_info.get('content_type')}")
    print(f"📝 Has Form: {login_info.get('has_form')}")
    print(f"🔐 Has CSRF: {login_info.get('has_csrf')}")
    print(f"🛡️ Cloudflare: {login_info.get('has_cloudflare')}")
    print(f"📋 Login Fields: {login_info.get('login_fields')}")
    
    input("\nPress Enter to continue...")

def smart_login_flow(self):
    """Complete smart login flow with captcha and Cloudflare"""
    self.print_header()
    print("🚀 SMART LOGIN FLOW")
    print("-" * 40)
    print()
    
    login_url = input("Enter login URL: ").strip()
    username = input("Enter username/email: ").strip()
    password = input("Enter password: ").strip()
    
    login_system = AdvancedLoginSystem()
    captcha_solver = CaptchaSolver()
    cloudflare_bypass = CloudflareBypass()
    
    print("\n🔄 Starting smart login...")
    
    # Step 1: Check for Cloudflare
    print("1. Checking Cloudflare protection...")
    cf_result = cloudflare_bypass.bypass_cloudflare(login_url)
    if cf_result.get('success'):
        print("✅ Cloudflare bypassed!")
        # Update session with Cloudflare cookies
        login_system.cookies.update(cf_result.get('cookies', {}))
    
    # Step 2: Perform login
    print("2. Attempting login...")
    login_result = login_system.perform_login(login_url, username, password)
    
    if login_result.get('success'):
        print("✅ Login successful!")
        print(f"📊 Status: {login_result.get('status_code')}")
        print(f"🍪 Cookies stored: {len(login_system.cookies)}")
        
        # Step 3: Test protected API
        protected_url = input("\nEnter protected API URL to test (optional): ").strip()
        if protected_url:
            self.test_with_auth(protected_url, login_system.cookies)
    else:
        print(f"❌ Login failed: {login_result.get('error')}")
    
    input("\nPress Enter to continue...")

def devtools_parser_menu(self):
    """Parse DevTools copied content"""
    self.print_header()
    print("🧪 DEVTOOLS PARSER")
    print("-" * 40)
    print()
    
    print("Paste any content from DevTools (cURL, fetch, headers, etc.):")
    print("Press Ctrl+D (Linux/Mac) or Ctrl+Z (Windows) when done:")
    
    user_input = ""
    try:
        while True:
            line = input()
            user_input += line + "\n"
    except EOFError:
        pass
    
    parser = DevToolsParser()
    parsed_data = parser.parse_any_input(user_input)
    
    print("\n✅ Parsed Results:")
    print(f"🔗 URL: {parsed_data.get('url')}")
    print(f"⚡ Method: {parsed_data.get('method')}")
    print(f"📋 Headers: {len(parsed_data.get('headers', {}))} items")
    print(f"🍪 Cookies: {len(parsed_data.get('cookies', {}))} items")
    print(f"📦 Data: {parsed_data.get('data')}")
    print(f"📄 JSON Body: {parsed_data.get('json_body')}")
    
    # Ask if user wants to test this request
    if parsed_data.get('url'):
        test = input("\nTest this request? (y/n): ").strip().lower()
        if test == 'y':
            self.test_parsed_request(parsed_data)
    
    input("\nPress Enter to continue...")

def multi_method_test_menu(self):
    """Test API with multiple methods"""
    self.print_header()
    print("🔄 MULTI-METHOD API TESTER")
    print("-" * 40)
    print()
    
    url = input("Enter API URL: ").strip()
    
    tester = MultiMethodTester()
    print(f"\n🔄 Testing all methods on: {url}")
    
    results = tester.test_all_methods(url)
    
    working_method = tester.find_working_method(results)
    if working_method:
        print(f"\n✅ Working method found: {working_method}")
        
        # Export code for working method
        exporter = CodeExporter()
        request_data = {
            'url': url,
            'method': working_method,
            'headers': results[working_method].get('headers', {})
        }
        
        python_code = exporter.export_python_code(request_data)
        curl_code = exporter.export_curl_code(request_data)
        
        print("\n💾 Code exported:")
        print("📝 Python code saved to: exported_code/api_request.py")
        print("🔄 cURL command saved to: exported_code/api_request.curl")
        
        # Save files
        exporter.save_code_file(python_code, 'api_request', 'py')
        exporter.save_code_file(curl_code, 'api_request', 'curl')
    else:
        print("\n❌ No working method found")
    
    input("\nPress Enter to continue...")

def code_export_menu(self):
    """Export API request as code"""
    self.print_header()
    print("💾 CODE EXPORT SYSTEM")
    print("-" * 40)
    print()
    
    # Load latest successful request
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and data:
                latest_request = data[-1]
            else:
                latest_request = data
    except:
        print("❌ No API test data found. Please test an API first.")
        input("Press Enter to continue...")
        return
    
    exporter = CodeExporter()
    
    print("Select export format:")
    print("1. 🐍 Python Code")
    print("2. 🔄 cURL Command")
    print("3. 📜 JavaScript Code")
    print("4. 📁 All Formats")
    print("5. ↩️ Back")
    print()
    
    choice = input("Select option (1-5): ").strip()
    
    request_data = {
        'url': latest_request.get('url'),
        'method': latest_request.get('method', 'GET'),
        'headers': latest_request.get('headers', {})
    }
    
    if choice == '1':
        code = exporter.export_python_code(request_data)
        filepath = exporter.save_code_file(code, 'api_request', 'py')
        print(f"✅ Python code saved to: {filepath}")
    elif choice == '2':
        code = exporter.export_curl_code(request_data)
        filepath = exporter.save_code_file(code, 'api_request', 'curl')
        print(f"✅ cURL command saved to: {filepath}")
    elif choice == '3':
        code = exporter.export_javascript_code(request_data)
        filepath = exporter.save_code_file(code, 'api_request', 'js')
        print(f"✅ JavaScript code saved to: {filepath}")
    elif choice == '4':
        # Export all formats
        python_code = exporter.export_python_code(request_data)
        curl_code = exporter.export_curl_code(request_data)
        js_code = exporter.export_javascript_code(request_data)
        
        exporter.save_code_file(python_code, 'api_request', 'py')
        exporter.save_code_file(curl_code, 'api_request', 'curl')
        exporter.save_code_file(js_code, 'api_request', 'js')
        
        print("✅ All formats exported to exported_code/ directory")
    elif choice == '5':
        return
    else:
        print("❌ Invalid option")
    
    input("\nPress Enter to continue...")

# Update the main_menu method to include new options:
def main_menu(self):
    while True:
        self.print_header()
        print("1. 🔧 Test API Endpoint")
        print("2. 🔐 Login & Access Protected API")
        print("3. 🚀 Advanced Login System")  # NEW
        print("4. 🧪 DevTools Parser")  # NEW
        print("5. 🔄 Multi-Method Tester")  # NEW
        print("6. 💾 Code Export")  # NEW
        print("7. ⚙️ Configuration")
        print("8. 📊 View Results")
        print("9. 🤖 Telegram Bot Control")
        print("10. 🚪 Exit")
        print()
        
        choice = input("Select option (1-10): ").strip()
        
        if choice == '1':
            self.test_api_menu()
        elif choice == '2':
            self.login_protected_api_menu()
        elif choice == '3':  # NEW
            self.advanced_login_menu()
        elif choice == '4':  # NEW
            self.devtools_parser_menu()
        elif choice == '5':  # NEW
            self.multi_method_test_menu()
        elif choice == '6':  # NEW
            self.code_export_menu()
        elif choice == '7':
            self.config_menu()
        elif choice == '8':
            self.view_results_menu()
        elif choice == '9':
            self.telegram_menu()
        elif choice == '10':
            print("👋 Goodbye!")
            break
        else:
            input("❌ Invalid option. Press Enter to continue...")
