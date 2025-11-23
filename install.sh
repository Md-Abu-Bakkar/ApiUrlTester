#!/bin/bash

# Universal API Tester - Auto Installer
# For Repository: https://github.com/Md-Abu-Bakkar/ApiUrlTester

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

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
    
    pkg update -y
    pkg upgrade -y
    pkg install -y python git wget curl
    
    log_success "Termux packages installed"
}

# Install desktop packages
install_desktop_packages() {
    log_info "Installing system packages..."
    
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3 python3-pip python3-tk git wget curl
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip git wget curl tkinter
    elif command -v pacman &> /dev/null; then
        sudo pacman -Syu python python-pip git wget curl tk
    else
        log_warning "Unknown package manager, please install python3 manually"
    fi
    
    log_success "System packages installed"
}

# Install Python packages
install_python_packages() {
    log_info "Installing Python packages..."
    
    pip3 install --upgrade pip
    pip3 install requests python-telegram-bot pillow
    
    log_success "Python packages installed"
}

# Download project from your repository
download_project() {
    log_info "Downloading project files..."
    
    if [ -d "ApiUrlTester" ]; then
        log_info "Project exists, updating..."
        cd ApiUrlTester
        git pull || log_warning "Could not update, using existing files"
    else
        git clone https://github.com/Md-Abu-Bakkar/ApiUrlTester.git
        cd ApiUrlTester
    fi
    
    log_success "Project files downloaded"
}

# Main installation
main_installation() {
    log_info "Starting API Tester installation..."
    
    ENV=$(detect_environment)
    log_info "Environment: $ENV"
    
    # Install system packages
    if [ "$ENV" = "termux" ]; then
        install_termux_packages
    else
        install_desktop_packages
    fi
    
    # Download project
    download_project
    
    # Install Python packages
    install_python_packages
    
    # Make scripts executable
    chmod +x main.py
    
    log_success "🎉 Installation completed!"
    log_info ""
    log_info "To start the tool:"
    log_info "cd ApiUrlTester"
    
    if [ "$1" = "desktop" ]; then
        log_info "python3 main.py --mode desktop"
        log_info "Or: python3 main.py (auto-detection)"
    else
        log_info "python3 main.py --mode cli"
    fi
    
    log_info ""
    log_info "📖 Full documentation: https://github.com/Md-Abu-Bakkar/ApiUrlTester"
}

# Show usage
show_usage() {
    echo "API Url Tester - Installation"
    echo ""
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  desktop    Install with desktop UI"
    echo "  cli        Install CLI mode (default)"
    echo ""
    echo "Example:"
    echo "  $0 cli        # Install CLI mode"
}

# Parse arguments
MODE=${1:-"cli"}
case $MODE in
    "desktop"|"cli")
        ;;
    *)
        log_error "Invalid mode: $MODE"
        show_usage
        exit 1
        ;;
esac

# Run installation
main_installation "$MODE"
