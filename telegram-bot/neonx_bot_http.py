#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Telegram Bot - HTTP API Version
A very simple bot that uses the Telegram Bot API directly via HTTP requests.
"""

import os
import time
import json
import logging
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
BOT_TOKEN = os.getenv("BOT_TOKEN")
COIN_ADDRESS = os.getenv("COIN_ADDRESS")
PUMP_FUN_URL = f"https://pump.fun/coin/{COIN_ADDRESS}"
MEXC_URL = "https://www.mexc.com/dex/trade?pair_ca=HE2uwAY5Y5pU7qLKQXaccuySajYKmrsk1Ekjb5u8nqDJ&chain_id=100000&token_ca=8GBj4X4xBwL2qsdTkkkfkXub5w8YgcE96CJ7gLV3pump&base_token_ca=So11111111111111111111111111111111111111112"
WEBSITE_URL = "https://neonxcoin.xyz"
TELEGRAM_GROUP = "https://t.me/neonxcoin_sol"
TWITTER_URL = "https://twitter.com/"  # Update with your Twitter handle

# Telegram API URL
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    """Send a message to a chat."""
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    return response.json()

def get_updates(offset=None):
    """Get updates from Telegram."""
    url = f"{API_URL}/getUpdates"
    params = {"timeout": 30}
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()

def handle_message(message):
    """Handle incoming messages."""
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text.startswith("/start"):
        handle_start(chat_id, message)
    elif text.startswith("/info"):
        handle_info(chat_id)
    elif text.startswith("/buy"):
        handle_buy(chat_id)
    elif text.startswith("/links"):
        handle_links(chat_id)
    elif text.startswith("/help"):
        handle_help(chat_id)
    else:
        send_message(chat_id, "I don't understand that command. Try /help to see available commands.")

def handle_start(chat_id, message):
    """Handle the /start command."""
    user_first_name = message["from"].get("first_name", "there")
    welcome_message = (
        f"🚀 Welcome to the NeonX Bot, {user_first_name}! 🚀\n\n"
        f"NeonX is the ultimate Solana meme coin, illuminating the chain with the brightest vibes in crypto!\n\n"
        f"Use the commands below to learn more about NeonX:\n"
        f"/info - Get token information\n"
        f"/buy - Get links to buy NeonX on pump.fun or trade on MEXC DEX\n"
        f"/links - Important links\n"
        f"/help - Show help message"
    )
    send_message(chat_id, welcome_message)

def handle_info(chat_id):
    """Handle the /info command."""
    info_message = (
        "💡 *NeonX Token Information* 💡\n\n"
        "*Name:* NeonX\n"
        "*Symbol:* NEONX\n"
        "*Blockchain:* Solana\n"
        "*Total Supply:* 1,000,000,000 NEONX\n"
        f"*Token Address:* `{COIN_ADDRESS}`\n\n"
        "*Created On:* pump.fun\n\n"
        "NeonX is a community-driven meme coin on Solana with no utility or intrinsic value. "
        "This token exists purely for fun and community engagement. Always do your own research before trading meme coins."
    )
    send_message(chat_id, info_message)

def handle_buy(chat_id):
    """Handle the /buy command."""
    buy_message = (
        "🛒 *How to Buy NeonX* 🛒\n\n"
        "*Step 1:* Create a Solana wallet (Phantom, Solflare)\n"
        "*Step 2:* Buy SOL from an exchange and transfer to your wallet\n"
        "*Step 3:* Visit pump.fun or MEXC DEX and connect your wallet\n"
        "*Step 4:* Enter the NeonX token address (if needed):\n"
        f"`{COIN_ADDRESS}`\n"
        "*Step 5:* Set the amount of SOL you want to swap and complete the transaction\n\n"
        f"Buy on pump.fun: {PUMP_FUN_URL}\n"
        f"Trade on MEXC DEX: {MEXC_URL}\n\n"
        "Always do your own research before investing!"
    )
    send_message(chat_id, buy_message)

def handle_links(chat_id):
    """Handle the /links command."""
    links_message = (
        "🔗 *Important NeonX Links* 🔗\n\n"
        f"*Website:* {WEBSITE_URL}\n"
        f"*Buy on pump.fun:* {PUMP_FUN_URL}\n"
        f"*Trade on MEXC DEX:* {MEXC_URL}\n"
        f"*Telegram Group:* {TELEGRAM_GROUP}\n"
        f"*Twitter:* {TWITTER_URL}"
    )
    send_message(chat_id, links_message)

def handle_help(chat_id):
    """Handle the /help command."""
    help_text = (
        "🤖 *NeonX Bot Commands* 🤖\n\n"
        "/start - Start the bot and see main menu\n"
        "/info - Get token information\n"
        "/buy - Get links to buy NeonX on pump.fun or trade on MEXC DEX\n"
        "/links - Important links\n"
        "/help - Show this help message"
    )
    send_message(chat_id, help_text)

def main():
    """Start the bot."""
    logger.info("Starting bot...")

    # Get bot info
    response = requests.get(f"{API_URL}/getMe")
    bot_info = response.json()
    logger.info(f"Bot started: @{bot_info['result']['username']}")

    # Main loop
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            if "result" in updates and updates["result"]:
                for update in updates["result"]:
                    if "message" in update and "text" in update["message"]:
                        handle_message(update["message"])

                    # Update offset to acknowledge processed updates
                    offset = update["update_id"] + 1

            time.sleep(1)
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
