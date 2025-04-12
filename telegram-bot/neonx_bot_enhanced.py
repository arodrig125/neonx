#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Telegram Bot - Enhanced Version
A feature-rich bot for the NeonX meme coin on Solana with price tracking, alerts, and community features.
"""

import os
import time
import json
import logging
import threading
import requests
from dotenv import load_dotenv

# Import our custom modules
from price_tracker import get_formatted_price_message, fetch_price_data
from alerts_manager import alerts_manager
from community_manager import community_manager

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
CHAT_ID = os.getenv("CHAT_ID")  # Admin chat ID for notifications

# Telegram API URL
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# Global variables
last_price_data = None
user_states = {}  # Track user states for multi-step commands

def send_message(chat_id, text, reply_markup=None):
    """Send a message to a chat."""
    url = f"{API_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

    response = requests.post(url, data=data)
    return response.json()

def send_photo(chat_id, photo, caption=None, reply_markup=None):
    """Send a photo to a chat."""
    url = f"{API_URL}/sendPhoto"
    data = {
        "chat_id": chat_id,
        "photo": photo,
        "parse_mode": "Markdown"
    }

    if caption:
        data["caption"] = caption

    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)

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
    user_id = message["from"]["id"]
    username = message["from"].get("username")
    first_name = message["from"].get("first_name")
    last_name = message["from"].get("last_name")

    # Register user activity
    community_manager.register_user_activity(user_id, username, first_name, last_name)

    # Check if this is a text message
    if "text" in message:
        text = message["text"]

        # Check if user is in a specific state
        if user_id in user_states:
            handle_user_state(user_id, chat_id, text, message)
            return

        # Handle commands
        if text.startswith("/start"):
            handle_start(chat_id, message)
        elif text.startswith("/info"):
            handle_info(chat_id)
        elif text.startswith("/price"):
            handle_price(chat_id)
        elif text.startswith("/buy"):
            handle_buy(chat_id)
        elif text.startswith("/links"):
            handle_links(chat_id)
        elif text.startswith("/help"):
            handle_help(chat_id)
        elif text.startswith("/alerts"):
            handle_alerts(chat_id, user_id)
        elif text.startswith("/setalert"):
            handle_set_alert(chat_id, user_id, text)
        elif text.startswith("/meme"):
            handle_meme(chat_id)
        elif text.startswith("/stats"):
            handle_stats(chat_id)
        else:
            # Not a recognized command
            send_message(chat_id, "I don't understand that command. Try /help to see available commands.")

    # Check if this is a photo (potential meme)
    elif "photo" in message:
        handle_photo(chat_id, user_id, message)

def handle_user_state(user_id, chat_id, text, message):
    """Handle user in a specific state."""
    state = user_states[user_id]

    if state["action"] == "set_alert":
        try:
            threshold = float(text)
            alert_type = state["alert_type"]

            success = alerts_manager.add_alert(user_id, alert_type, threshold, chat_id)

            if success:
                if alert_type == "price_above":
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price goes above {threshold}.")
                elif alert_type == "price_below":
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price goes below {threshold}.")
                elif alert_type == "percent_change":
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price changes by {threshold}% or more.")
            else:
                send_message(chat_id, "❌ You already have this alert set up.")
        except ValueError:
            send_message(chat_id, "❌ Please enter a valid number.")

        # Clear the user state
        del user_states[user_id]

    elif state["action"] == "add_meme_caption":
        file_id = state["file_id"]
        caption = text

        community_manager.add_meme(file_id, user_id, caption)
        send_message(chat_id, "✅ Your meme has been added to the collection! Use /meme to see random memes.")

        # Clear the user state
        del user_states[user_id]

def handle_start(chat_id, message):
    """Handle the /start command."""
    user_first_name = message["from"].get("first_name", "there")
    welcome_message = (
        f"🚀 *Welcome to the NeonX Bot, {user_first_name}!* 🚀\n\n"
        f"NeonX is the ultimate Solana meme coin, illuminating the chain with the brightest vibes in crypto!\n\n"
        f"Use the commands below to learn more about NeonX:\n"
        f"/info - Get token information\n"
        f"/price - Check current price\n"
        f"/buy - Get links to buy NeonX on pump.fun or trade on MEXC DEX\n"
        f"/alerts - Set price alerts\n"
        f"/meme - View and share memes\n"
        f"/stats - Community statistics\n"
        f"/links - Important links\n"
        f"/help - Show help message"
    )

    # Create inline keyboard
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "💰 Token Info", "callback_data": "info"},
                {"text": "📈 Price", "callback_data": "price"}
            ],
            [
                {"text": "🛒 Buy NeonX", "callback_data": "buy"},
                {"text": "🔔 Alerts", "callback_data": "alerts"}
            ],
            [
                {"text": "🎭 Memes", "callback_data": "meme"},
                {"text": "📊 Stats", "callback_data": "stats"}
            ],
            [
                {"text": "🔗 Links", "callback_data": "links"},
                {"text": "❓ Help", "callback_data": "help"}
            ]
        ]
    }

    send_message(chat_id, welcome_message, keyboard)

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

    keyboard = {
        "inline_keyboard": [
            [{"text": "🔍 View on pump.fun", "url": PUMP_FUN_URL}],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, info_message, keyboard)

def handle_price(chat_id):
    """Handle the /price command."""
    price_message = get_formatted_price_message()

    keyboard = {
        "inline_keyboard": [
            [{"text": "🔄 Refresh", "callback_data": "refresh_price"}],
            [{"text": "🛒 Buy Now", "url": PUMP_FUN_URL}],
            [{"text": "🔔 Set Alert", "callback_data": "set_alert"}],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, price_message, keyboard)

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
        "Always do your own research before investing!"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🚀 Buy on pump.fun", "url": PUMP_FUN_URL}],
            [{"text": "📊 Trade on MEXC DEX", "url": MEXC_URL}],
            [
                {"text": "👻 Phantom", "url": "https://phantom.app/"},
                {"text": "☀️ Solflare", "url": "https://solflare.com/"}
            ],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, buy_message, keyboard)

def handle_links(chat_id):
    """Handle the /links command."""
    links_message = (
        "🔗 *Important NeonX Links* 🔗\n\n"
        "All the official links for NeonX:"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🌐 Website", "url": WEBSITE_URL}],
            [{"text": "💰 Buy on pump.fun", "url": PUMP_FUN_URL}],
            [{"text": "📊 Trade on MEXC DEX", "url": MEXC_URL}],
            [{"text": "💬 Telegram Group", "url": TELEGRAM_GROUP}],
            [{"text": "🐦 Twitter", "url": TWITTER_URL}],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, links_message, keyboard)

def handle_help(chat_id):
    """Handle the /help command."""
    help_text = (
        "🤖 *NeonX Bot Commands* 🤖\n\n"
        "/start - Start the bot and see main menu\n"
        "/info - Get token information\n"
        "/price - Check current price\n"
        "/buy - Get links to buy NeonX on pump.fun or trade on MEXC DEX\n"
        "/alerts - Manage your price alerts\n"
        "/setalert - Set a new price alert\n"
        "/meme - View and share memes\n"
        "/stats - Community statistics\n"
        "/links - Important links\n"
        "/help - Show this help message"
    )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, help_text, keyboard)

def handle_alerts(chat_id, user_id):
    """Handle the /alerts command."""
    user_alerts = alerts_manager.get_user_alerts(user_id)

    if not user_alerts:
        message = (
            "🔔 *Your Price Alerts* 🔔\n\n"
            "You don't have any price alerts set up yet.\n\n"
            "Use /setalert to set a new alert."
        )
    else:
        message = "🔔 *Your Price Alerts* 🔔\n\n"

        for i, alert in enumerate(user_alerts):
            if alert["type"] == "price_above":
                message += f"{i+1}. Alert when price goes above {alert['threshold']}\n"
            elif alert["type"] == "price_below":
                message += f"{i+1}. Alert when price goes below {alert['threshold']}\n"
            elif alert["type"] == "percent_change":
                message += f"{i+1}. Alert when price changes by {alert['threshold']}% or more\n"

        message += "\nUse /setalert to set a new alert."

    keyboard = {
        "inline_keyboard": [
            [{"text": "➕ Set New Alert", "callback_data": "set_alert"}],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, message, keyboard)

def handle_set_alert(chat_id, user_id, text):
    """Handle the /setalert command."""
    parts = text.split()

    if len(parts) == 1:
        # No parameters provided, show options
        message = (
            "🔔 *Set a Price Alert* 🔔\n\n"
            "Choose the type of alert you want to set:"
        )

        keyboard = {
            "inline_keyboard": [
                [{"text": "⬆️ Price Above", "callback_data": "alert_above"}],
                [{"text": "⬇️ Price Below", "callback_data": "alert_below"}],
                [{"text": "📊 Percent Change", "callback_data": "alert_percent"}],
                [{"text": "🔙 Back", "callback_data": "alerts"}]
            ]
        }

        send_message(chat_id, message, keyboard)
    else:
        # Parameters provided
        try:
            alert_type = parts[1].lower()
            threshold = float(parts[2])

            if alert_type in ["above", "up"]:
                success = alerts_manager.add_alert(user_id, "price_above", threshold, chat_id)
                if success:
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price goes above {threshold}.")
                else:
                    send_message(chat_id, "❌ You already have this alert set up.")

            elif alert_type in ["below", "down"]:
                success = alerts_manager.add_alert(user_id, "price_below", threshold, chat_id)
                if success:
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price goes below {threshold}.")
                else:
                    send_message(chat_id, "❌ You already have this alert set up.")

            elif alert_type in ["percent", "change", "%"]:
                success = alerts_manager.add_alert(user_id, "percent_change", threshold, chat_id)
                if success:
                    send_message(chat_id, f"✅ Alert set! You will be notified when the price changes by {threshold}% or more.")
                else:
                    send_message(chat_id, "❌ You already have this alert set up.")

            else:
                send_message(chat_id, "❌ Invalid alert type. Use 'above', 'below', or 'percent'.")

        except (IndexError, ValueError):
            send_message(
                chat_id,
                "❌ Invalid format. Use:\n"
                "/setalert above 0.0001\n"
                "/setalert below 0.00005\n"
                "/setalert percent 5"
            )

def handle_meme(chat_id):
    """Handle the /meme command."""
    meme = community_manager.get_random_meme()

    if not meme:
        message = (
            "🎭 *NeonX Memes* 🎭\n\n"
            "No memes have been shared yet.\n\n"
            "Be the first to share a meme! Just send a photo to this chat."
        )
        send_message(chat_id, message)
    else:
        caption = meme.get("caption", "")
        if not caption:
            caption = "🎭 *NeonX Meme*"

        keyboard = {
            "inline_keyboard": [
                [{"text": "🔄 Another Meme", "callback_data": "another_meme"}],
                [{"text": "🔙 Back to Menu", "callback_data": "start"}]
            ]
        }

        send_photo(chat_id, meme["file_id"], caption, keyboard)

def handle_photo(chat_id, user_id, message):
    """Handle a photo message (potential meme)."""
    # Get the file ID of the largest photo
    file_id = message["photo"][-1]["file_id"]

    # Check if there's a caption
    if "caption" in message:
        # Add the meme with the provided caption
        community_manager.add_meme(file_id, user_id, message["caption"])
        send_message(chat_id, "✅ Your meme has been added to the collection! Use /meme to see random memes.")
    else:
        # Ask for a caption
        send_message(chat_id, "Please enter a caption for your meme:")

        # Set user state to wait for caption
        user_states[user_id] = {
            "action": "add_meme_caption",
            "file_id": file_id
        }

def handle_stats(chat_id):
    """Handle the /stats command."""
    stats_message = community_manager.format_community_stats_message()

    # Add price information
    price_data = fetch_price_data()
    if price_data.get("success", False) or price_data.get("price") != "N/A":
        stats_message += "\n\n" + (
            "💰 *Current Price Information* 💰\n"
            f"*Price:* {price_data['price']}\n"
            f"*Market Cap:* {price_data['market_cap']}\n"
            f"*Holders:* {price_data['holders']}"
        )

    keyboard = {
        "inline_keyboard": [
            [{"text": "🔄 Refresh", "callback_data": "refresh_stats"}],
            [{"text": "🔙 Back to Menu", "callback_data": "start"}]
        ]
    }

    send_message(chat_id, stats_message, keyboard)

def handle_callback_query(callback_query):
    """Handle callback queries from inline keyboards."""
    query_id = callback_query["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    user_id = callback_query["from"]["id"]
    data = callback_query["data"]

    # Answer the callback query to stop the loading indicator
    requests.post(
        f"{API_URL}/answerCallbackQuery",
        data={"callback_query_id": query_id}
    )

    # Register user activity
    community_manager.register_user_activity(
        user_id,
        callback_query["from"].get("username"),
        callback_query["from"].get("first_name"),
        callback_query["from"].get("last_name")
    )

    # Handle different callback data
    if data == "start":
        handle_start(chat_id, {"from": callback_query["from"]})
    elif data == "info":
        handle_info(chat_id)
    elif data == "price":
        handle_price(chat_id)
    elif data == "refresh_price":
        # Force refresh price data
        handle_price(chat_id)
    elif data == "buy":
        handle_buy(chat_id)
    elif data == "links":
        handle_links(chat_id)
    elif data == "help":
        handle_help(chat_id)
    elif data == "alerts":
        handle_alerts(chat_id, user_id)
    elif data == "set_alert":
        handle_set_alert(chat_id, user_id, "/setalert")
    elif data == "alert_above":
        send_message(chat_id, "Please enter the price threshold for your alert (e.g., 0.0001):")
        user_states[user_id] = {
            "action": "set_alert",
            "alert_type": "price_above"
        }
    elif data == "alert_below":
        send_message(chat_id, "Please enter the price threshold for your alert (e.g., 0.00005):")
        user_states[user_id] = {
            "action": "set_alert",
            "alert_type": "price_below"
        }
    elif data == "alert_percent":
        send_message(chat_id, "Please enter the percentage change threshold for your alert (e.g., 5):")
        user_states[user_id] = {
            "action": "set_alert",
            "alert_type": "percent_change"
        }
    elif data == "meme":
        handle_meme(chat_id)
    elif data == "another_meme":
        handle_meme(chat_id)
    elif data == "stats":
        handle_stats(chat_id)
    elif data == "refresh_stats":
        handle_stats(chat_id)

def check_price_alerts():
    """Check price alerts in a separate thread."""
    global last_price_data

    while True:
        try:
            # Fetch current price data
            current_data = fetch_price_data(force_refresh=True)

            if current_data.get("success", False) and current_data.get("price") != "N/A":
                current_price = float(current_data["price"])
                previous_price = float(last_price_data["price"]) if last_price_data and last_price_data.get("price") != "N/A" else None

                # Check alerts
                triggered_alerts = alerts_manager.check_alerts(current_price, previous_price)

                # Send notifications for triggered alerts
                for alert_data in triggered_alerts:
                    chat_id = alert_data["chat_id"]
                    message = alerts_manager.format_alert_message(alert_data)
                    send_message(chat_id, message)

                # Update last price data
                last_price_data = current_data

            # Sleep for 5 minutes
            time.sleep(300)

        except Exception as e:
            logger.error(f"Error in price alert thread: {e}")
            time.sleep(60)  # Sleep for 1 minute on error

def main():
    """Start the bot."""
    logger.info("Starting bot...")

    # Get bot info
    response = requests.get(f"{API_URL}/getMe")
    bot_info = response.json()
    logger.info(f"Bot started: @{bot_info['result']['username']}")

    # Send startup notification to admin
    if CHAT_ID:
        send_message(CHAT_ID, f"🚀 NeonX Bot started! @{bot_info['result']['username']}")

    # Start price alert thread
    alert_thread = threading.Thread(target=check_price_alerts)
    alert_thread.daemon = True
    alert_thread.start()

    # Main loop
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            if "result" in updates and updates["result"]:
                for update in updates["result"]:
                    if "message" in update and "text" in update.get("message", {}):
                        handle_message(update["message"])
                    elif "message" in update and "photo" in update.get("message", {}):
                        handle_message(update["message"])
                    elif "callback_query" in update:
                        handle_callback_query(update["callback_query"])

                    # Update offset to acknowledge processed updates
                    offset = update["update_id"] + 1

            time.sleep(1)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
