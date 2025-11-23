import os
import sys
import logging
from urllib.parse import urlparse

def detect_environment():
    """Detect if running in desktop or CLI environment"""
    if 'DISPLAY' in os.environ and os.environ['DISPLAY']:
        return 'desktop'
    else:
        return 'cli'

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('system.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def validate_url(url):
    """Validate URL format"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def load_config(config_path='config.json'):
    """Load configuration from file"""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(config, config_path='config.json'):
    """Save configuration to file"""
    try:
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving config: {e}")
        return False
