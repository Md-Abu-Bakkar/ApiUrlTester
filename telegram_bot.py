import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import json
import os
import requests
from api_tester import APITester
from data_manager import DataManager

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.api_tester = APITester()
        self.data_manager = DataManager()
        
        # Register handlers
        self.setup_handlers()
        
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("test", self.test_api))
        self.application.add_handler(CommandHandler("login", self.login_protected))
        self.application.add_handler(CommandHandler("results", self.get_results))
        self.application.add_handler(CommandHandler("logs", self.get_logs))
        self.application.add_handler(CommandHandler("status", self.get_status))
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message when command /start is issued."""
        keyboard = [
            [
                InlineKeyboardButton("🚀 Test API", callback_data="test_api"),
                InlineKeyboardButton("🔐 Login API", callback_data="login_api"),
            ],
            [
                InlineKeyboardButton("📊 Results", callback_data="get_results"),
                InlineKeyboardButton("📋 Logs", callback_data="get_logs"),
            ],
            [
                InlineKeyboardButton("📈 Status", callback_data="get_status"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            '🤖 *Universal API Tester Bot*\n\n'
            'I can help you test APIs, login to protected systems, and manage results!\n\n'
            'Available commands:\n'
            '/start - Show this menu\n'
            '/test <url> [method] - Test an API endpoint\n' 
            '/login - Login to protected API\n'
            '/results - Get latest test results\n'
            '/logs - Download log files\n'
            '/status - Check system status',
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def login_protected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Login to protected API"""
        try:
            # Load config
            with open('config.json', 'r') as f:
                config = json.load(f)
                
            login_url = config.get('login_url')
            protected_url = config.get('protected_api_url')
            username = config.get('username')
            password = config.get('password')
            
            if not all([login_url, username, password]):
                await update.message.reply_text(
                    '❌ *Missing Configuration*\n\n'
                    'Please set in config:\n'
                    '• Login URL\n• Username\n• Password\n• Protected API URL',
                    parse_mode='Markdown'
                )
                return
                
            await update.message.reply_text('🔄 Logging in to protected API...')
            
            # Login request
            login_data = {'username': username, 'password': password}
            login_response = requests.post(login_url, json=login_data)
            
            if login_response.status_code == 200:
                # Access protected API
                headers = {}
                try:
                    token = login_response.json().get('token') or login_response.json().get('access_token')
                    if token:
                        headers['Authorization'] = f'Bearer {token}'
                except:
                    pass
                    
                protected_response = requests.get(protected_url, headers=headers, cookies=login_response.cookies)
                
                result = {
                    'url': protected_url,
                    'method': 'GET',
                    'status_code': protected_response.status_code,
                    'timestamp': datetime.now().isoformat(),
                    'success': protected_response.status_code == 200,
                    'type': 'protected_api'
                }
                
                try:
                    result['response'] = protected_response.json()
                except:
                    result['response'] = protected_response.text
                    
                self.data_manager.save_response(result)
                
                if result['success']:
                    await update.message.reply_text(
                        f'✅ *Protected API Access Successful!*\n\n'
                        f'📊 Status: {result["status_code"]}\n'
                        f'🔐 Type: Protected API\n'
                        f'💾 Saved to logs',
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        f'❌ *Protected API Access Failed*\n\n'
                        f'📊 Status: {result["status_code"]}\n'
                        f'🔐 Type: Protected API',
                        parse_mode='Markdown'
                    )
            else:
                await update.message.reply_text(
                    f'❌ *Login Failed!*\n\n'
                    f'Status: {login_response.status_code}\n'
                    f'Response: {login_response.text}',
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            await update.message.reply_text(f'❌ Error: {str(e)}')
        
    # ... rest of the existing methods remain same
    async def test_api(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Test an API endpoint"""
        if not context.args:
            await update.message.reply_text(
                '❌ Please provide a URL to test.\n'
                'Usage: /test <url> [method]\n'
                'Example: /test https://api.example.com/data GET'
            )
            return
            
        url = context.args[0]
        method = context.args[1].upper() if len(context.args) > 1 else 'GET'
        
        await update.message.reply_text(f'🔄 Testing {method} {url}...')
        
        try:
            result = self.api_tester.test_endpoint(url, method)
            self.data_manager.save_response(result)
            
            if result['success']:
                message = (
                    f'✅ *API Test Successful!*\n\n'
                    f'📊 *Status Code:* {result["status_code"]}\n'
                    f'⏱️ *Response Time:* {result["response_time"]:.2f}s\n'
                    f'🕐 *Timestamp:* {result["timestamp"]}\n'
                    f'💾 *Saved to:* data.json, data.txt'
                )
            else:
                message = (
                    f'❌ *API Test Failed!*\n\n'
                    f'📊 *Status Code:* {result["status_code"]}\n'
                    f'⏱️ *Response Time:* {result["response_time"]:.2f}s\n'
                    f'🕐 *Timestamp:* {result["timestamp"]}\n'
                    f'🚨 *Error:* {result.get("error", "Unknown error")}'
                )
                
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f'❌ Error testing API: {str(e)}')
            
    async def get_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get latest test results"""
        try:
            if os.path.exists('data.json'):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                    
                if isinstance(data, list) and data:
                    latest = data[-1]  # Get latest result
                    message = (
                        f'📊 *Latest Test Results*\n\n'
                        f'🌐 *URL:* {latest.get("url", "N/A")}\n'
                        f'⚡ *Method:* {latest.get("method", "N/A")}\n'
                        f'📋 *Status:* {latest.get("status_code", "N/A")}\n'
                        f'⏱️ *Time:* {latest.get("response_time", 0):.2f}s\n'
                        f'✅ *Success:* {latest.get("success", False)}\n'
                        f'🕐 *When:* {latest.get("timestamp", "N/A")}'
                    )
                    if latest.get('type') == 'protected_api':
                        message += '\n🔐 *Type:* Protected API'
                else:
                    message = 'No test results found.'
            else:
                message = 'No test results found.'
                
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f'❌ Error getting results: {str(e)}')
            
    async def get_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send log files"""
        log_files = ['system.log', 'earnings.log', 'data.txt']
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'rb') as f:
                        await update.message.reply_document(
                            document=f,
                            filename=log_file,
                            caption=f'📋 {log_file}'
                        )
                except Exception as e:
                    await update.message.reply_text(f'❌ Error sending {log_file}: {str(e)}')
            else:
                await update.message.reply_text(f'📭 {log_file} not found')
                
    async def get_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get system status"""
        try:
            # Count test results
            test_count = 0
            protected_count = 0
            if os.path.exists('data.json'):
                with open('data.json', 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        test_count = len(data)
                        protected_count = len([x for x in data if x.get('type') == 'protected_api'])
                    else:
                        test_count = 1
                        if data.get('type') == 'protected_api':
                            protected_count = 1
                    
            # Check log sizes
            system_log_size = os.path.getsize('system.log') if os.path.exists('system.log') else 0
            earnings_log_size = os.path.getsize('earnings.log') if os.path.exists('earnings.log') else 0
            
            message = (
                f'📈 *System Status*\n\n'
                f'🧪 *Total Tests:* {test_count}\n'
                f'🔐 *Protected APIs:* {protected_count}\n'
                f'📊 *System Log Size:* {system_log_size} bytes\n'
                f'💰 *Earnings Log Size:* {earnings_log_size} bytes\n'
                f'🤖 *Bot Status:* ✅ Online\n'
                f'🛠️ *API Tester:* ✅ Ready'
            )
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f'❌ Error getting status: {str(e)}')
            
    def run(self):
        """Start the bot"""
        self.application.run_polling()

def start_bot(token):
    """Start the Telegram bot"""
    bot = TelegramBot(token)
    print("🤖 Telegram Bot Started! Press Ctrl+C to stop.")
    bot.run()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        start_bot(sys.argv[1])
    else:
        print("Please provide bot token: python telegram_bot.py <token>")
