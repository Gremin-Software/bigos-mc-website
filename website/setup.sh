#!/usr/bin/env bash

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Stop script on errors
set -e

# Move website directory contents
echo "Moving website contents to /var/www/bigos-mc-website..."
if [ -d "/var/www/bigos-mc-website" ]; then
  echo "Directory /var/www/bigos-mc-website already exists. Proceeding to move files..."
else
  mkdir -p /var/www/bigos-mc-website
fi
cp -r ./website/* /var/www/bigos-mc-website/

# Change to the website directory
cd /var/www/bigos-mc-website

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "Installing required Python packages..."
pip install -r requirements.txt

# Start the application using Gunicorn
echo "Starting the application with Gunicorn..."
nohup gunicorn --reload -w 4 -b 0.0.0.0:8000 app:app &
