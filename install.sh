#!/bin/bash

# Universal API Tester - Auto Installer
# One-command installation for Termux and Desktop

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    
    # Update packages
    pkg update -y
    pkg upgrade -y
    
    # Install required packages
    pkg install -y python git wget curl
    
    # Install X11 packages if needed
    if [ "$1" = "desktop" ]; then
        log_info "Installing X11 packages for desktop mode..."
        pkg install -y x11-repo
        pkg install -y turbo-x11 termux-x11
    fi
    
    log_success "Termux packages installed successfully"
}

# Install Python packages
install_python_packages() {
    log_info "Installing Python packages..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install required packages
    pip install requests python-telegram-bot pillow
    
    log_success "Python packages installed successfully"
}

# Setup desktop environment
setup_desktop_environment() {
    log_info "Setting up desktop environment..."
    
    # Create desktop shortcut
    cat > ~/Desktop/api-tester.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Universal API Tester
Comment=Professional API Testing Tool
Exec=python3 $(pwd)/main.py --mode desktop
Icon=$(pwd)/icon.png
Categories=Development;
Terminal=false
StartupNotify=true
EOF
    
    chmod +x ~/Desktop/api-tester.desktop
    log_success "Desktop shortcut created"
}

# Download project files
download_project() {
    log_info "Downloading project files..."
    
    # Clone or download project files
    if [ -d "universal-api-tester" ]; then
        log_warning "Project directory already exists, updating..."
        cd universal-api-tester
        git pull || log_warning "Could not update, using existing files"
    else
        git clone https://github.com/yourusername/universal-api-tester.git
        cd universal-api-tester
    fi
    
    log_success "Project files downloaded"
}

# Main installation function
main_installation() {
    log_info "Starting Universal API Tester installation..."
    
    ENV=$(detect_environment)
    log_info "Detected environment: $ENV"
    
    # Install system packages
    if [ "$ENV" = "termux" ]; then
        install_termux_packages "$1"
    else
        log_info "Desktop environment detected, installing system packages..."
        sudo apt update && sudo apt install -y python3 python3-pip python3-tk git wget curl
    fi
    
    # Download project
    download_project
    
    # Install Python packages
    install_python_packages
    
    # Setup desktop environment if requested
    if [ "$1" = "desktop" ] && [ "$ENV" = "desktop" ]; then
        setup_desktop_environment
    fi
    
    # Make scripts executable
    chmod +x main.py
    
    log_success "🎉 Installation completed successfully!"
    log_info ""
    
    if [ "$1" = "desktop" ] && [ "$ENV" = "termux" ]; then
        log_info "To start in desktop mode, run:"
        log_info "termux-x11 &"
        log_info "python3 main.py --mode desktop"
    elif [ "$1" = "desktop" ]; then
        log_info "To start in desktop mode, run:"
        log_info "python3 main.py --mode desktop"
    else
        log_info "To start in CLI mode, run:"
        log_info "python3 main.py --mode cli"
    fi
    
    log_info ""
    log_info "You can also double-click the desktop shortcut (if created)"
}

# Show usage
show_usage() {
    echo "Universal API Tester - Installation Script"
    echo ""
    echo "Usage: $0 [mode]"
    echo ""
    echo "Modes:"
    echo "  desktop    Install with desktop UI support"
    echo "  cli        Install only CLI mode (default)"
    echo "  help       Show this help message"
    echo ""
    echo "Example:"
    echo "  $0 desktop    # Install with desktop UI"
    echo "  $0 cli        # Install only CLI mode"
}

# Parse arguments
MODE="cli"
if [ $# -gt 0 ]; then
    case $1 in
        "desktop")
            MODE="desktop"
            ;;
        "cli")
            MODE="cli"
            ;;
        "help")
            show_usage
            exit 0
            ;;
        *)
            log_error "Invalid option: $1"
            show_usage
            exit 1
            ;;
    esac
fi

# Run main installation
main_installation "$MODE"
