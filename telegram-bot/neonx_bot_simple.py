#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Telegram Bot - Simple Version
A very simple bot to provide information about the NeonX meme coin on Solana.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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
WEBSITE_URL = "https://neonxcoin.xyz"
TELEGRAM_GROUP = "https://t.me/neonxcoin_sol"
TWITTER_URL = "https://twitter.com/"  # Update with your Twitter handle

# Bot command functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"🚀 Welcome to the NeonX Bot, {user.first_name}! 🚀\n\n"
        f"NeonX is the ultimate Solana meme coin, illuminating the chain with the brightest vibes in crypto!\n\n"
        f"Use the commands below to learn more about NeonX:\n"
        f"/info - Get token information\n"
        f"/buy - Get link to buy NeonX\n"
        f"/links - Important links\n"
        f"/help - Show help message"
    )
    
    await update.message.reply_text(welcome_message)

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide information about the NeonX token."""
    info_message = (
        "💡 NeonX Token Information 💡\n\n"
        "Name: NeonX\n"
        "Symbol: NEONX\n"
        "Blockchain: Solana\n"
        "Total Supply: 1,000,000,000 NEONX\n"
        f"Token Address: {COIN_ADDRESS}\n\n"
        "Created On: pump.fun\n\n"
        "NeonX is a community-driven meme coin on Solana with no utility or intrinsic value. "
        "This token exists purely for fun and community engagement. Always do your own research before trading meme coins."
    )
    
    await update.message.reply_text(info_message)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide information on how to buy NeonX."""
    buy_message = (
        "🛒 How to Buy NeonX 🛒\n\n"
        "Step 1: Create a Solana wallet (Phantom, Solflare)\n"
        "Step 2: Buy SOL from an exchange and transfer to your wallet\n"
        "Step 3: Visit pump.fun and connect your wallet\n"
        "Step 4: Enter the NeonX token address:\n"
        f"{COIN_ADDRESS}\n"
        "Step 5: Set the amount of SOL you want to swap and complete the transaction\n\n"
        f"Buy on pump.fun: {PUMP_FUN_URL}\n\n"
        "Always do your own research before investing!"
    )
    
    await update.message.reply_text(buy_message)

async def links(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide important links."""
    links_message = (
        "🔗 Important NeonX Links 🔗\n\n"
        f"Website: {WEBSITE_URL}\n"
        f"Buy on pump.fun: {PUMP_FUN_URL}\n"
        f"Telegram Group: {TELEGRAM_GROUP}\n"
        f"Twitter: {TWITTER_URL}"
    )
    
    await update.message.reply_text(links_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 NeonX Bot Commands 🤖\n\n"
        "/start - Start the bot and see main menu\n"
        "/info - Get token information\n"
        "/buy - Get link to buy NeonX\n"
        "/links - Important links\n"
        "/help - Show this help message"
    )
    
    await update.message.reply_text(help_text)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("buy", buy))
    application.add_handler(CommandHandler("links", links))
    
    # Register error handler
    application.add_error_handler(error_handler)

    # Start the Bot
    application.run_polling()
    logger.info("Bot started. Press Ctrl+C to stop.")

if __name__ == '__main__':
    main()
