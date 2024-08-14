#!/usr/bin/env bash

# Ensure script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Stop script on errors
set -e

# Update package list and install necessary software
apt update
apt install -y nginx certbot python3-certbot-nginx

# Move the preconfigured bigos-website to `available` websites directory
if [ -f /etc/nginx/sites-available/bigos-website ]; then
  echo "File already exists in /etc/nginx/sites-available/. Backing up the existing file."
  mv /etc/nginx/sites-available/bigos-website /etc/nginx/sites-available/bigos-website.bak
fi
mv ./bigos-website /etc/nginx/sites-available/

# Symlink the 'available' bigos website to `enabled` websites directory
if [ ! -L /etc/nginx/sites-enabled/bigos-website ]; then
  ln -s /etc/nginx/sites-available/bigos-website /etc/nginx/sites-enabled/
fi

# Enable and start nginx service
systemctl enable nginx
systemctl start nginx

# Get a new certificate for bigos.org.pl to enable https
certbot --nginx -m bigos@bigos.org.pl --agree-tos -v -d bigos.org.pl

# Reload nginx if necessary
# systemctl reload nginx
# systemctl restart nginx
