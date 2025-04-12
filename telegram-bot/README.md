# NeonX Telegram Bot

A feature-rich Telegram bot for the NeonX meme coin on Solana, providing token information, price tracking, alerts, and community engagement features.

## Features

- **Token Information**: Details about NeonX token, including address, supply, etc.
- **Price Tracking**: Real-time price data from pump.fun
- **Buy Guide**: Step-by-step instructions for purchasing NeonX
- **Price Alerts**: Set custom alerts for price movements
- **Community Features**: Meme sharing and community statistics
- **Important Links**: Quick access to all official NeonX links

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- A Telegram bot token (obtained from [@BotFather](https://t.me/BotFather))

### Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/neonx.git
   cd neonx/telegram-bot
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with the following content:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   COIN_ADDRESS=8GBj4X4xBwL2qsdTkkkfkXub5w8YgcE96CJ7gLV3pump
   CHAT_ID=your_admin_chat_id_here  # Optional: for admin notifications
   ```

4. Run the bot:
   ```bash
   python neonx_bot_enhanced.py
   ```

## Creating a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Start a chat and send the command `/newbot`
3. Follow the instructions to create a new bot
4. Once created, BotFather will provide you with a token - copy this to your `.env` file

## Deployment

For 24/7 operation, deploy the bot to a VPS:

### Automatic Deployment (Ubuntu/Debian)

1. SSH into your VPS
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/neonx.git
   cd neonx/telegram-bot
   ```

3. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```

4. Run the deployment script as root:
   ```bash
   sudo ./deploy.sh
   ```

5. Edit the `.env` file with your bot token:
   ```bash
   sudo nano /home/neonxbot/neonx/telegram-bot/.env
   ```

### Manual Deployment

1. Install Python and required packages:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip git supervisor
   ```

2. Create a dedicated user:
   ```bash
   sudo useradd -m -s /bin/bash neonxbot
   ```

3. Clone the repository:
   ```bash
   cd /home/neonxbot
   sudo git clone https://github.com/yourusername/neonx.git
   sudo chown -R neonxbot:neonxbot neonx
   ```

4. Install dependencies:
   ```bash
   sudo pip3 install -r neonx/telegram-bot/requirements.txt
   ```

5. Create the `.env` file:
   ```bash
   sudo nano /home/neonxbot/neonx/telegram-bot/.env
   ```
   Add your bot token and other settings.

6. Set up supervisor or systemd:

   **Using Supervisor:**
   ```bash
   sudo cp /home/neonxbot/neonx/telegram-bot/neonxbot.conf /etc/supervisor/conf.d/
   sudo supervisorctl reread
   sudo supervisorctl update
   ```

   **Using Systemd:**
   ```bash
   sudo cp /home/neonxbot/neonx/telegram-bot/neonxbot.service /etc/systemd/system/
   sudo systemctl enable neonxbot
   sudo systemctl start neonxbot
   ```

## Bot Commands

- `/start` - Start the bot and see main menu
- `/info` - Get token information
- `/price` - Check current price
- `/buy` - Get link to buy NeonX
- `/alerts` - Manage your price alerts
- `/setalert` - Set a new price alert
- `/meme` - View and share memes
- `/stats` - Community statistics
- `/links` - Important links
- `/help` - Show help message

## Setting Price Alerts

You can set price alerts in three ways:

1. **Price Above**: Get notified when the price rises above a threshold
   ```bash
   /setalert above 0.0001
   ```

2. **Price Below**: Get notified when the price falls below a threshold
   ```bash
   /setalert below 0.00005
   ```

3. **Percent Change**: Get notified when the price changes by a certain percentage
   ```bash
   /setalert percent 5
   ```

## Customization

You can customize the bot by editing the following files:

- `neonx_bot_enhanced.py` - Main bot code
- `price_tracker.py` - Price tracking functionality
- `alerts_manager.py` - Price alerts management
- `community_manager.py` - Community features

## Troubleshooting

If the bot stops working:

1. Check the logs:
   ```bash
   sudo supervisorctl tail -f neonxbot
   ```
   or
   ```bash
   sudo journalctl -u neonxbot
   ```

2. Restart the bot:
   ```bash
   sudo supervisorctl restart neonxbot
   ```
   or
   ```bash
   sudo systemctl restart neonxbot
   ```

3. Check the `.env` file to ensure your bot token is correct

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for informational purposes only. It does not provide financial advice. Always do your own research before investing in cryptocurrencies, especially meme coins.
