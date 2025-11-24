#!/bin/bash

# Universal API Tester - Complete Auto Installer
# One command installation with all advanced features

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Detect environment
detect_environment() {
    if [ -d "/data/data/com.termux" ]; then
        echo "termux"
    else
        echo "desktop"
    fi
}

# Install Termux packages
install_termux_packages() {
    log_info "Installing Termux packages..."
    pkg update -y && pkg upgrade -y
    pkg install -y python git wget curl termux-api
    
    # Install Chrome and ChromeDriver for Selenium
    pkg install -y tur-repo
    pkg install -y chromedriver
    
    log_success "Termux packages installed"
}

# Install Python packages
install_python_packages() {
    log_info "Installing Python packages..."
    
    # Basic packages
    pip install requests python-telegram-bot beautifulsoup4 cloudscraper
    
    # Advanced packages
    pip install selenium pillow pyparsing requests-toolbelt
    
    # Try to install additional packages
    pip install urllib3 certifi idna charset-normalizer || log_warning "Some packages failed but continuing..."
    
    log_success "Python packages installed"
}

# Download and setup project
setup_project() {
    log_info "Setting up project..."
    
    cd ~
    if [ -d "Universal-API-Tester" ]; then
        log_info "Updating existing installation..."
        cd Universal-API-Tester
        git pull || log_warning "Could not update, using existing"
    else
        log_info "Downloading latest version..."
        git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git Universal-API-Tester
        cd Universal-API-Tester
    fi
    
    # Create necessary directories
    mkdir -p sessions exported_code utils
    
    log_success "Project setup completed"
}

# Create desktop launcher (for desktop environments)
create_desktop_launcher() {
    if [ "$1" = "desktop" ]; then
        log_info "Creating desktop launcher..."
        
        cat > ~/Desktop/API-Tester.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Universal API Tester
Comment=Advanced API Testing Tool with Login & Captcha Solver
Exec=python3 $HOME/Universal-API-Tester/main.py --mode desktop
Icon=utilities-terminal
Categories=Development;Network;
Terminal=true
StartupNotify=true
EOF
        
        chmod +x ~/Desktop/API-Tester.desktop
        log_success "Desktop launcher created"
    fi
}

# Create run script
create_run_script() {
    log_info "Creating run scripts..."
    
    # Main run script
    cat > ~/run-api-tester.sh << EOF
#!/bin/bash
cd ~/Universal-API-Tester
python3 main.py
EOF
    
    # CLI run script
    cat > ~/run-api-cli.sh << EOF
#!/bin/bash
cd ~/Universal-API-Tester
python3 main.py --mode cli
EOF
    
    chmod +x ~/run-api-tester.sh ~/run-api-cli.sh
    log_success "Run scripts created"
}

# Main installation function
main_installation() {
    log_info "🚀 Starting Universal API Tester Installation..."
    
    ENV=$(detect_environment)
    log_info "Detected environment: $ENV"
    
    # Install system packages
    if [ "$ENV" = "termux" ]; then
        install_termux_packages
    else
        log_info "Desktop environment detected"
        sudo apt update && sudo apt install -y python3 python3-pip python3-tk git wget curl || true
    fi
    
    # Setup project
    setup_project
    
    # Install Python packages
    install_python_packages
    
    # Create launchers
    create_desktop_launcher "$ENV"
    create_run_script
    
    log_success "🎉 Installation Completed Successfully!"
    log_info ""
    log_info "📱 Quick Start Commands:"
    log_info "  ./run-api-tester.sh    # Auto-detect mode"
    log_info "  ./run-api-cli.sh       # CLI mode only"
    log_info ""
    log_info "🖥️  Or run directly:"
    log_info "  cd ~/Universal-API-Tester"
    log_info "  python3 main.py --mode cli"
    log_info ""
    log_info "🌟 Features Included:"
    log_info "  ✅ Advanced Login System"
    log_info "  ✅ Captcha Solver"
    log_info "  ✅ Cloudflare Bypass"
    log_info "  ✅ DevTools Parser"
    log_info "  ✅ Multi-Method Testing"
    log_info "  ✅ Code Export"
    log_info "  ✅ Telegram Bot"
    log_info "  ✅ Professional Dashboard"
}

# Run installation
main_installation
