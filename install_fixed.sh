#!/bin/bash

# Universal API Tester - Fixed Auto Installer for Termux
# No chromedriver dependency

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

install_termux_packages() {
    log_info "Installing Termux packages..."
    pkg update -y
    pkg install -y python git wget curl
    log_success "Termux packages installed"
}

install_python_packages() {
    log_info "Installing Python packages..."
    
    # Basic required packages
    pip install requests python-telegram-bot beautifulsoup4 cloudscraper pillow
    
    # Optional packages (if installation fails, continue)
    pip install pyparsing requests-toolbelt || log_warning "Some optional packages failed"
    
    log_success "Python packages installed"
}

setup_project() {
    log_info "Setting up project..."
    
    cd ~
    if [ -d "Universal-API-Tester" ]; then
        log_info "Updating existing installation..."
        cd Universal-API-Tester
        git pull || log_warning "Could not update, using existing"
    else
        log_info "Downloading project..."
        git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git Universal-API-Tester
        cd Universal-API-Tester
    fi
    
    # Create necessary directories
    mkdir -p sessions exported_code utils logs
    
    log_success "Project setup completed"
}

create_run_scripts() {
    log_info "Creating run scripts..."
    
    # Main run script
    cat > ~/run-api-tester.sh << 'EOF'
#!/bin/bash
cd ~/Universal-API-Tester
python main.py "$@"
EOF
    
    # CLI run script
    cat > ~/run-api-cli.sh << 'EOF'
#!/bin/bash
cd ~/Universal-API-Tester
python main.py --mode cli
EOF
    
    chmod +x ~/run-api-tester.sh ~/run-api-cli.sh
    log_success "Run scripts created"
}

main_installation() {
    log_info "🚀 Starting Universal API Tester Installation..."
    
    # Install packages
    install_termux_packages
    setup_project
    install_python_packages
    create_run_scripts
    
    log_success "🎉 Installation Completed Successfully!"
    log_info ""
    log_info "📱 Quick Start Commands:"
    log_info "  ./run-api-tester.sh    # Auto-detect mode"
    log_info "  ./run-api-cli.sh       # CLI mode only"
    log_info ""
    log_info "🖥️  Or run directly:"
    log_info "  cd ~/Universal-API-Tester"
    log_info "  python main.py --mode cli"
    log_info ""
    log_info "🌟 All Advanced Features Included:"
    log_info "  ✅ Universal Login System"
    log_info "  ✅ Captcha Solver (Math + Cloudflare)"
    log_info "  ✅ DevTools Parser"
    log_info "  ✅ Multi-Method Testing"
    log_info "  ✅ Code Export System"
    log_info "  ✅ Cloudflare Bypass"
    log_info "  ✅ Telegram Bot Integration"
}

# Run installation
main_installation

# Auto-run the tool after installation
log_info "🚀 Starting the tool..."
cd ~/Universal-API-Tester
python main.py --mode cli
