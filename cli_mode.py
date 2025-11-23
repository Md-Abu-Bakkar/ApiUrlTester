import os
import json
import requests
from datetime import datetime
from data_manager import DataManager
from api_tester import APITester
from utils.helpers import validate_url

class CLIMenu:
    def __init__(self):
        self.data_manager = DataManager()
        self.api_tester = APITester()
        self.config = self.load_config()
        
    def load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
            
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
        print("=" * 60)
        print("           🚀 UNIVERSAL API TESTER - CLI MODE")
        print("=" * 60)
        print()
        
    def main_menu(self):
        while True:
            self.print_header()
            print("1. 🔧 Test API Endpoint")
            print("2. ⚙️  Configuration")
            print("3. 📊 View Results")
            print("4. 🤖 Telegram Bot Control")
            print("5. 🚪 Exit")
            print()
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == '1':
                self.test_api_menu()
            elif choice == '2':
                self.config_menu()
            elif choice == '3':
                self.view_results_menu()
            elif choice == '4':
                self.telegram_menu()
            elif choice == '5':
                print("👋 Goodbye!")
                break
            else:
                input("❌ Invalid option. Press Enter to continue...")
                
    def test_api_menu(self):
        self.print_header()
        print("🔧 API TESTING")
        print("-" * 40)
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
            
            # Show preview of response
            response_data = response.get('response', {})
            if isinstance(response_data, dict):
                preview = json.dumps(response_data, indent=2)[:500] + "..." if len(json.dumps(response_data)) > 500 else json.dumps(response_data, indent=2)
            else:
                preview = str(response_data)[:500] + "..." if len(str(response_data)) > 500 else str(response_data)
                
            print(f"\n📄 Response Preview:\n{preview}")
            
        except Exception as e:
            print(f"❌ Error testing API: {e}")
            
        input("\nPress Enter to continue...")
        
    def config_menu(self):
        while True:
            self.print_header()
            print("⚙️  CONFIGURATION")
            print("-" * 40)
            print()
            
            print(f"1. 👤 Username: {self.config.get('username', 'Not set')}")
            print(f"2. 🔑 Password: {'*' * len(self.config.get('password', '')) if self.config.get('password') else 'Not set'}")
            print(f"3. 🎫 API Token: {self.config.get('api_token', 'Not set')}")
            print(f"4. 🤖 Telegram Bot Token: {self.config.get('telegram_bot_token', 'Not set')}")
            print("5. 💾 Save Configuration")
            print("6. ↩️  Back to Main Menu")
            print()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.config['username'] = input("Enter username: ").strip()
            elif choice == '2':
                self.config['password'] = input("Enter password: ").strip()
            elif choice == '3':
                self.config['api_token'] = input("Enter API token: ").strip()
            elif choice == '4':
                self.config['telegram_bot_token'] = input("Enter Telegram bot token: ").strip()
            elif choice == '5':
                self.save_config()
                input("Press Enter to continue...")
            elif choice == '6':
                break
            else:
                input("❌ Invalid option. Press Enter to continue...")
                
    def view_results_menu(self):
        self.print_header()
        print("📊 VIEW RESULTS")
        print("-" * 40)
        print()
        
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                print(f"Total tests: {len(data)}")
                for i, test in enumerate(data[-5:], 1):  # Show last 5 tests
                    print(f"\n{i}. {test.get('url', 'N/A')}")
                    print(f"   Method: {test.get('method', 'N/A')}")
                    print(f"   Status: {test.get('status_code', 'N/A')}")
                    print(f"   Time: {test.get('timestamp', 'N/A')}")
            else:
                print("Latest test:")
                print(f"URL: {data.get('url', 'N/A')}")
                print(f"Method: {data.get('method', 'N/A')}")
                print(f"Status: {data.get('status_code', 'N/A')}")
                print(f"Response: {json.dumps(data.get('response', {}), indent=2)[:200]}...")
                
        except FileNotFoundError:
            print("❌ No test results found.")
        except Exception as e:
            print(f"❌ Error reading results: {e}")
            
        input("\nPress Enter to continue...")
        
    def telegram_menu(self):
        self.print_header()
        print("🤖 TELEGRAM BOT CONTROL")
        print("-" * 40)
        print()
        
        if not self.config.get('telegram_bot_token'):
            print("❌ Please set Telegram bot token in configuration first.")
            input("Press Enter to continue...")
            return
            
        print("1. 🚀 Start Telegram Bot")
        print("2. ⏹️  Stop Telegram Bot")
        print("3. ↩️  Back")
        print()
        
        choice = input("Select option (1-3): ").strip()
        
        if choice == '1':
            print("🚀 Starting Telegram bot...")
            # Import and start bot here
            from telegram_bot import start_bot
            try:
                start_bot(self.config['telegram_bot_token'])
            except Exception as e:
                print(f"❌ Error starting bot: {e}")
        elif choice == '2':
            print("⏹️  Stopping Telegram bot...")
            # Implement bot stopping logic
        elif choice == '3':
            return
        else:
            input("❌ Invalid option. Press Enter to continue...")

def run_cli_mode():
    menu = CLIMenu()
    menu.main_menu()