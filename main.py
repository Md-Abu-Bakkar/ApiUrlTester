#!/usr/bin/env python3
import os
import sys
import json
import argparse
from utils.helpers import detect_environment, setup_logging

def main():
    """Main entry point for the Universal API Tester"""
    parser = argparse.ArgumentParser(description='🚀 Universal API Testing + Automation Tool')
    parser.add_argument('--mode', choices=['auto', 'desktop', 'cli'], default='auto',
                       help='Run in specific mode')
    parser.add_argument('--config', default='config.json',
                       help='Path to config file')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Check and install missing dependencies
    check_dependencies()
    
    # Detect environment and run appropriate mode
    if args.mode == 'auto':
        env = detect_environment()
        if env == 'desktop':
            from desktop_ui import run_desktop_ui
            run_desktop_ui()
        else:
            from cli_mode import run_cli_mode
            run_cli_mode()
    elif args.mode == 'desktop':
        from desktop_ui import run_desktop_ui
        run_desktop_ui()
    else:
        from cli_mode import run_cli_mode
        run_cli_mode()

def check_dependencies():
    """Check and install missing dependencies automatically"""
    try:
        import requests
        import telegram
        import bs4
        import cloudscraper
    except ImportError as e:
        print(f"🔧 Installing missing dependency: {e}")
        os.system(f"pip install {str(e).split()[-1]}")
        print("✅ Dependency installed successfully")

if __name__ == '__main__':
    main()
