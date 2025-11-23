📋 Complete Installation Guide - Universal API Tester

🚀 Quick Start

One-Command Installation (Recommended)

bash

# For Desktop UI Mode (Termux Desktop/Linux) curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install.sh | bash -s desktop # For CLI Mode Only curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install.sh | bash -s cli

📱 Termux Installation (Android)

Method 1: Auto Install (Recommended)

bash

# Step 1: Update Termux pkg update && pkg upgrade -y # Step 2: Install curl if not available pkg install curl -y # Step 3: Run auto installer curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install.sh | bash -s desktop

Method 2: Manual Installation

bash

# Step 1: Install required packages pkg update && pkg upgrade -y pkg install python git wget curl tur-repo -y # Step 2: Install X11 for desktop mode pkg install x11-repo -y pkg install tur-repo -y pkg install turbo-x11 termux-x11 -y # Step 3: Clone repository git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git cd ApiUrlTester # Step 4: Install Python dependencies pip install requests python-telegram-bot pillow # Step 5: Make script executable chmod +x main.py install.sh # Step 6: Run the application python main.py

🖥️ Running in Termux Desktop Mode

bash

# Terminal 1: Start X11 server termux-x11 & # Terminal 2: Run application in desktop mode cd ApiUrlTester python main.py --mode desktop

⌨️ Running in Termux CLI Mode

bash

cd ApiUrlTester python main.py --mode cli

💻 Desktop/Linux Installation

Method 1: Auto Install (Recommended)

bash

# Download and run installer curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install.sh | bash -s desktop

Method 2: Manual Installation

bash

# Step 1: Install system dependencies sudo apt update && sudo apt install -y python3 python3-pip python3-tk git wget curl # Step 2: Clone repository git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git cd ApiUrlTester # Step 3: Install Python packages pip3 install requests python-telegram-bot pillow # Step 4: Make executable chmod +x main.py # Step 5: Run application python3 main.py

🖥️ Running in Desktop Mode (Linux)

bash

python3 main.py --mode desktop

⌨️ Running in CLI Mode (Linux)

bash

python3 main.py --mode cli

🤖 Telegram Bot Setup

Step 1: Create Telegram Bot

bash

# Search for @BotFather in Telegram # Send command: /newbot # Follow instructions to get bot token

Step 2: Configure Bot Token

bash

# Method 1: Through application UI # Go to Configuration tab → Telegram Bot section # Enter your bot token # Method 2: Edit config file manually nano config.json

Add your token in config.json:

json

{ "telegram_bot_token": "YOUR_BOT_TOKEN_HERE" }

Step 3: Start Bot

bash

# Through application UI # Go to Telegram Bot Control → Start Bot # Or through CLI cd ApiUrlTester python3 telegram_bot.py YOUR_BOT_TOKEN

🧪 How to Use the Application

Desktop UI Mode Features:

API Testing Tab - Test any API endpoint

Configuration Tab - Set credentials and tokens

Results Tab - View API responses

One-click testing with beautiful interface

CLI Mode Features:

Text-based menu with full functionality

Fast and lightweight operation

Same features as desktop version

Basic API Testing:

bash

# Example: Test GET request URL: https://jsonplaceholder.typicode.com/posts/1 Method: GET # Example: Test POST request URL: https://jsonplaceholder.typicode.com/posts Method: POST Headers: {"Content-Type": "application/json"} Body: {"title": "test", "body": "content", "userId": 1}

📁 File Structure

text

ApiUrlTester/ ├── main.py # Main application ├── install.sh # Auto-installer ├── requirements.txt # Python dependencies ├── config.json # Configuration file ├── desktop_ui.py # Desktop interface ├── cli_mode.py # CLI interface ├── telegram_bot.py # Telegram bot ├── api_tester.py # Core API testing logic ├── data_manager.py # Data saving system └── utils/ └── helpers.py # Utility functions

💾 Data Output Files

The tool automatically creates:

data.json - Structured API responses

data.txt - Human-readable logs

earnings.json - Detected earnings/coins

earnings.log - Earnings timeline

system.log - System operations log

🛠️ Troubleshooting

Common Issues & Solutions:

Issue: Desktop UI not starting in Termux

bash

# Solution: Ensure X11 is running pkg install turbo-x11 termux-x11 -y termux-x11 &

Issue: Python packages not installing

bash

# Solution: Upgrade pip and retry pip install --upgrade pip pip install requests python-telegram-bot pillow

Issue: Permission denied

bash

# Solution: Make scripts executable chmod +x main.py install.sh

Issue: Telegram bot not responding

bash

# Solution: Verify token and start bot # Check token in config.json # Start bot from Telegram Bot Control menu

Issue: API tests failing

bash

# Solution: Check internet connection curl -I https://google.com # Verify URL format and authentication

📞 Support

If you face any issues:

Check the troubleshooting section above

Verify all dependencies are installed

Ensure proper internet connection

Check file permissions

🎯 Features Summary

✅ Dual Mode - Desktop UI + CLI
✅ Universal API Testing - Any endpoint support
✅ Professional Design - Modern dark theme
✅ Telegram Bot - Remote control
✅ Auto Data Saving - Multiple formats
✅ One-Command Install - Fully automated
✅ Cross-Platform - Termux & Desktop
✅ Free & Open Source - No restrictions

📄 License

MIT License - Free to use, modify and distribute.
