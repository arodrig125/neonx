#!/bin/bash

# NeonX Telegram Bot Deployment Script
# This script helps set up the NeonX Telegram Bot on a VPS

# Exit on error
set -e

echo "=== NeonX Telegram Bot Deployment ==="
echo "This script will set up the NeonX Telegram Bot on your server."
echo

# Check if running as root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

# Update system
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install dependencies
echo "Installing dependencies..."
apt-get install -y python3 python3-pip git supervisor

# Create a dedicated user for the bot
echo "Creating dedicated user 'neonxbot'..."
useradd -m -s /bin/bash neonxbot || echo "User already exists"

# Clone the repository
echo "Cloning the repository..."
cd /home/neonxbot
if [ -d "neonx" ]; then
    echo "Repository already exists, updating..."
    cd neonx
    git pull
else
    git clone https://github.com/yourusername/neonx.git
    cd neonx
fi

# Set permissions
chown -R neonxbot:neonxbot /home/neonxbot/neonx

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r telegram-bot/requirements.txt

# Create directories for data
echo "Creating data directories..."
mkdir -p /home/neonxbot/neonx/telegram-bot/memes
chown -R neonxbot:neonxbot /home/neonxbot/neonx/telegram-bot/memes

# Set up supervisor configuration
echo "Setting up supervisor configuration..."
cat > /etc/supervisor/conf.d/neonxbot.conf << EOF
[program:neonxbot]
command=python3 /home/neonxbot/neonx/telegram-bot/neonx_bot_enhanced.py
directory=/home/neonxbot/neonx/telegram-bot
user=neonxbot
autostart=true
autorestart=true
stderr_logfile=/var/log/neonxbot.err.log
stdout_logfile=/var/log/neonxbot.out.log
EOF

# Reload supervisor
echo "Reloading supervisor..."
supervisorctl reread
supervisorctl update

# Check status
echo "Checking bot status..."
supervisorctl status neonxbot

echo
echo "=== Deployment Complete ==="
echo "The NeonX Telegram Bot should now be running."
echo "Check the logs with: supervisorctl tail -f neonxbot"
echo "Restart the bot with: supervisorctl restart neonxbot"
echo
