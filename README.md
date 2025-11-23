🚀 Universal API Testing + Automation Tool

<div align="center">

https://img.shields.io/badge/Version-2.0-ff69b4
https://img.shields.io/badge/Python-3.8+-blue
https://img.shields.io/badge/Platform-Termux%2520%257C%2520Linux%2520%257C%2520Windows-green
https://img.shields.io/badge/License-MIT-yellow

The Ultimate API Reverse Engineering & Automation Platform

Features • Installation • Usage • Advanced Features • Examples

</div>

📖 Overview

Universal API Tester is a powerful, dual-mode API testing and automation tool that works seamlessly in both Termux Desktop and Pure CLI environments. With the latest v2.0 update, it now includes advanced capabilities for automated login systems, captcha solving, Cloudflare bypass, and intelligent API reverse engineering.

🎯 What's New in v2.0

🔥 Advanced Features Added

🔐 Universal Login System - Automated authentication for any platform

🤖 Captcha Solver - Math captcha + Cloudflare + reCAPTCHA support

🛡️ Cloudflare Bypass - Automatic protection bypass

🧪 DevTools Parser - Convert any copied content to API requests

🔄 Multi-Method Testing - Try all HTTP methods automatically

💾 Code Export - Generate Python, cURL, JavaScript code

🧠 Smart Detection - Auto-detect API structures and authentication

✨ Features

🖥️ Dual Mode Execution

Desktop UI Mode - Modern Radium UI-inspired interface with smooth animations

CLI Mode - Fast, lightweight terminal interface

Auto-detection - Automatically selects the best mode for your environment

🌐 Universal API Support

✅ Any REST API - GET, POST, PUT, DELETE methods

✅ Authentication - Token-based, Cookie-based, Session-based

✅ Headers & Parameters - Custom headers and query parameters

✅ JSON/XML Responses - Full support for all response types

✅ File Uploads - Multipart form data support

🔐 Advanced Security Features

Auto Login System - Username/Password, Email login, Token authentication

Captcha Solving - Math captcha, Cloudflare challenges, reCAPTCHA v2

Session Management - Automatic cookie and token storage

CSRF Protection - Auto-extract and use CSRF tokens

🛠️ Developer Tools

DevTools Parser - Paste cURL, fetch, axios code → Auto-convert to requests

Multi-Method Testing - Automatically try all HTTP methods

Code Generation - Export working API code in multiple languages

Request Reconstruction - Build valid API calls from random DevTools data

📊 Data Management

Auto Saving - JSON, TXT, log files with earnings detection

Real-time Logging - System logs, earnings logs, response logs

Export Capabilities - Download results in multiple formats

🤖 Integration Features

Telegram Bot - Remote control via Telegram

Desktop Shortcuts - Quick launch from desktop

Configuration Management - Save and load settings

🚀 Installation

One-Command Installation (Recommended)

bash

# For Desktop UI (Termux Desktop or Linux) curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install.sh | bash -s desktop

# For CLI only curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTemain/main/install.sh | bash -s cli                       

# Install Advanced Features curl -L https://raw.githubusercontent.com/Md-Abu-Bakkar/ApiUrlTester/main/install_advanced.sh | bash

Manual Installation

bash

# Clone repository git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git cd ApiUrlTester                           

# Install dependencies pip install -r requirements.txt

# Install advanced dependencies pip install beautifulsoup4 cloudscraper selenium Pillow                                            

# Run the tool python main.py --mode cli

Termux Specific Installation

bash

# Update packages pkg update && pkg upgrade

# Install required packages pkg install python git wget curl

# Install Python dependencies pip install requests python-telegram-bot beautifulsoup4 cloudscraper                       

# For desktop mode (optional) pkg install x11-repo pkg install turbo-x11 termux-x11

📖 Usage

Basic API Testing

bash

# CLI Mode python main.py --mode cli

# Desktop Mode python main.py --mode desktop

# Auto-detect Mode python main.py

Main Menu Options

🔧 Test API Endpoint - Basic API testing

🔐 Login & Access Protected API - Protected API access

🚀 Advanced Login System - Smart login with captcha solving

🧪 DevTools Parser - Convert DevTools content to API requests

🔄 Multi-Method Tester - Try all HTTP methods automatically

💾 Code Export - Generate code for successful requests

⚙️ Configuration - Manage settings and credentials

📊 View Results - Check previous test results

🤖 Telegram Bot Control - Manage Telegram bot

🚪 Exit - Exit the application

🔥 Advanced Features

🧠 Smart Login System

The advanced login system automatically handles:

Form-based Login - Username/password forms

JSON API Login - RESTful authentication endpoints

CSRF Protection - Auto-extract and use CSRF tokens

Redirect Handling - Follow login redirects automatically

Session Persistence - Save cookies and tokens for reuse

python

# Example: Automated login flow 1. User enters login URL, username, password 2. Tool detects login type and required fields 3. Solves captcha if present 4. Bypasses Cloudflare protection if active 5. Performs login and stores session 6. Uses session for subsequent API calls

🤖 Captcha Solving

Supported Captcha Types:

✅ Math Captcha - "What is 5 + 3?" → Auto-solve

✅ Cloudflare Challenge - JS challenge bypass

✅ reCAPTCHA v2 - Checkbox and invisible

✅ hCaptcha - Basic support

✅ Image Captcha - Manual solving with image display

🛡️ Cloudflare Bypass

Automatic Cloudflare protection bypass:

Cookie Generation - Create valid Cloudflare cookies

JS Challenge Solver - Execute JavaScript challenges

Session Management - Maintain bypassed sessions

403/503 Bypass - Handle blocked requests

🧪 DevTools Parser

Supported Input Types:

📋 cURL Commands - curl -X GET https://api.example.com

📜 JavaScript fetch - fetch('https://api.example.com')

🔧 Axios Code - axios.get('https://api.example.com')

📄 Raw Headers - HTTP header blocks

🔗 API URLs - Direct URL input

Example:

bash

# Paste this cURL command: curl -X POST 'https://api.example.com/login' \ -H 'Content-Type: application/json' \ -H 'Authorization: Bearer token123' \ --data '{"username":"user","password":"pass"}'                                        

# Tool automatically extracts:

# - URL: https://api.example.com/login              

# - Method: POST

# - Headers: Content-Type, Authorization           

# - JSON Body: username and password

🔄 Multi-Method Testing

When you're unsure which HTTP method works:

python

# Tool automatically tries: 1. GET request 2. POST request 3. PUT request 4. DELETE request 5. With/without authentication 6. With/without cookies 7. Different header combinations

# Stops when successful response is found

💾 Code Export System

Generate working code for any successful API call:

Export Formats:

🐍 Python - requests library code

🔄 cURL - Command line curl commands

📜 JavaScript - Fetch API code

📟 Node.js - Axios/request code

Example Generated Python Code:

python

import requests def make_request(): url = "https://api.example.com/data" headers = { "Authorization": "Bearer your_token", "Content-Type": "application/json" } response = requests.get(url, headers=headers, timeout=30) print(f"Status: {response.status_code}") print(f"Response: {response.json()}") return response if __name__ == "__main__": make_request()

📁 File Structure

text

ApiUrlTester/ ├── main.py # Main application ├── desktop_ui.py # Desktop interface ├── cli_mode.py # CLI interface ├── api_tester.py # Core API testing ├── data_manager.py # Data saving system ├── telegram_bot.py # Telegram bot ├── advanced_login.py # 🔥 NEW: Advanced login system ├── captcha_solver.py # 🔥 NEW: Captcha solving ├── devtools_parser.py # 🔥 NEW: DevTools content parser ├── cloudflare_bypass.py # 🔥 NEW: Cloudflare protection bypass ├── multi_method_tester.py # 🔥 NEW: Multi-method testing ├── code_exporter.py # 🔥 NEW: Code generation ├── config.json # Configuration file ├── requirements.txt # Python dependencies ├── install.sh # Installation script ├── install_advanced.sh # 🔥 NEW: Advanced features install └── utils/ ├── helpers.py # Utility functions ├── validators.py # Input validation └── __init__.py

📊 Output Files

The tool automatically creates and manages:

data.json - Structured API response data

data.txt - Human-readable log format

earnings.json - Detected earnings/coins data

earnings.log - Earnings timeline log

system.log - System operations log

sessions/ - Saved login sessions

exported_code/ - Generated code files

🤖 Telegram Bot Integration

Bot Commands:

/start - Show control panel

/test <url> - Test API endpoint

/login - Login to protected API

/results - Get latest test results

/logs - Download log files

/status - Check system status

Setup:

Create bot with @BotFather

Get API token

Set token in configuration

Start bot from Telegram menu

🎯 Real-World Use Cases

💰 Earning Panels & SMS Panels

Reverse engineer panel APIs

Automate login and data fetching

Detect earnings and payments

Create Telegram bots for monitoring

🔐 Protected APIs

Bypass authentication systems

Handle complex login flows

Maintain sessions automatically

Extract API endpoints

🧪 API Development

Test RESTful endpoints

Generate client code

Document API structures

Debug API responses

🤖 Automation

Create automation scripts

Build monitoring systems

Generate API clients

Reverse engineer web apps

🐛 Troubleshooting

Common Issues & Solutions

❌ Desktop UI not starting in Termux:

bash

# Ensure X11 server is running termux-x11 &

# Start desktop mode python main.py --mode desktop

❌ Python packages installation failed:

bash

# Upgrade pip first pip install --upgrade pip 

# Install individually pip install requests pip install python-telegram-bot pip install beautifulsoup4

❌ Cloudflare bypass not working:

Ensure cloudscraper and selenium are installed

Check internet connection

Try manual captcha solving option

❌ Telegram bot not responding:

Verify bot token in configuration

Check if bot is started with @BotFather

Ensure internet connectivity

❌ Permission errors:

bash

# Make scripts executable chmod +x *.py chmod +x install.sh

🔧 Configuration

Edit config.json to customize:

json

{ "username": "your_username", "password": "your_password", "api_token": "your_api_token", "telegram_bot_token": "bot_token", "login_url": "https://example.com/login", "protected_api_url": "https://example.com/api/data", "default_headers": { "Content-Type": "application/json", "User-Agent": "Universal-API-Tester/2.0" }, "auto_save": true, "timeout": 30, "max_retries": 3 }

🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

Development Setup:

bash

git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git cd ApiUrlTester pip install -r requirements.txt python main.py --mode cli

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Termux Community - For amazing Android development environment

Python Developers - For excellent libraries and tools

Open Source Community - For continuous inspiration and support

<div align="center">

⭐ Star this repository if you find it helpful!

🔔 Watch for updates and new features

🐛 Report issues and suggest improvements

</div>

📞 Support

If you need help or have questions:

Check the Issues page

Create a new issue with detailed description

Provide error logs and steps to reproduce

Made with ❤️ for the developer community

Happy API Testing! 🚀
