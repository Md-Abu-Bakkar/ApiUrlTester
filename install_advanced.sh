#!/bin/bash

echo "Installing advanced dependencies for Universal API Tester..."

pip install beautifulsoup4 cloudscraper selenium Pillow

# Download ChromeDriver for Selenium (adjust version as needed)
wget https://storage.googleapis.com/chrome-for-testing-public/120.0.6099.109/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "Advanced dependencies installed successfully!"
