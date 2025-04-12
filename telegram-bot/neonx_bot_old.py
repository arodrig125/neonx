#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Telegram Bot - Using older python-telegram-bot version
A simple bot to provide information about the NeonX meme coin on Solana.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
)

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
def start(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f"🚀 *Welcome to the NeonX Bot, {user.first_name}!* 🚀\n\n"
        f"NeonX is the ultimate Solana meme coin, illuminating the chain with the brightest vibes in crypto!\n\n"
        f"Use the commands below to learn more about NeonX:\n"
        f"/info - Get token information\n"
        f"/buy - Get link to buy NeonX\n"
        f"/links - Important links\n"
        f"/help - Show help message"
    )
    
    # Create keyboard with main options
    keyboard = [
        [
            InlineKeyboardButton("💰 Token Info", callback_data="info"),
            InlineKeyboardButton("🛒 Buy NeonX", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("🔗 Links", callback_data="links"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

def info(update: Update, context: CallbackContext) -> None:
    """Provide information about the NeonX token."""
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
    
    keyboard = [
        [InlineKeyboardButton("🔍 View on pump.fun", url=PUMP_FUN_URL)],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=info_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            info_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def buy(update: Update, context: CallbackContext) -> None:
    """Provide information on how to buy NeonX."""
    buy_message = (
        "🛒 *How to Buy NeonX* 🛒\n\n"
        "*Step 1:* Create a Solana wallet (Phantom, Solflare)\n"
        "*Step 2:* Buy SOL from an exchange and transfer to your wallet\n"
        "*Step 3:* Visit pump.fun and connect your wallet\n"
        "*Step 4:* Enter the NeonX token address:\n"
        f"`{COIN_ADDRESS}`\n"
        "*Step 5:* Set the amount of SOL you want to swap and complete the transaction\n\n"
        "Always do your own research before investing!"
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 Buy on pump.fun", url=PUMP_FUN_URL)],
        [
            InlineKeyboardButton("👻 Phantom", url="https://phantom.app/"),
            InlineKeyboardButton("☀️ Solflare", url="https://solflare.com/"),
        ],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=buy_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            buy_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def links(update: Update, context: CallbackContext) -> None:
    """Provide important links."""
    links_message = (
        "🔗 *Important NeonX Links* 🔗\n\n"
        "All the official links for NeonX:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🌐 Website", url=WEBSITE_URL)],
        [InlineKeyboardButton("💰 Buy on pump.fun", url=PUMP_FUN_URL)],
        [InlineKeyboardButton("💬 Telegram Group", url=TELEGRAM_GROUP)],
        [InlineKeyboardButton("🐦 Twitter", url=TWITTER_URL)],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=links_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            links_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 *NeonX Bot Commands* 🤖\n\n"
        "/start - Start the bot and see main menu\n"
        "/info - Get token information\n"
        "/buy - Get link to buy NeonX\n"
        "/links - Important links\n"
        "/help - Show this help message"
    )
    
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    query.answer()
    
    # Route to the appropriate function based on callback data
    if query.data == "start":
        start_callback(update, context)
    elif query.data == "info":
        info(update, context)
    elif query.data == "buy":
        buy(update, context)
    elif query.data == "links":
        links(update, context)
    elif query.data == "help":
        help_command(update, context)

def start_callback(update: Update, context: CallbackContext) -> None:
    """Handle the start callback from buttons."""
    user = update.callback_query.from_user
    welcome_message = (
        f"🚀 *Welcome to the NeonX Bot, {user.first_name}!* 🚀\n\n"
        f"NeonX is the ultimate Solana meme coin, illuminating the chain with the brightest vibes in crypto!\n\n"
        f"Use the commands below to learn more about NeonX:\n"
        f"/info - Get token information\n"
        f"/buy - Get link to buy NeonX\n"
        f"/links - Important links\n"
        f"/help - Show help message"
    )
    
    # Create keyboard with main options
    keyboard = [
        [
            InlineKeyboardButton("💰 Token Info", callback_data="info"),
            InlineKeyboardButton("🛒 Buy NeonX", callback_data="buy"),
        ],
        [
            InlineKeyboardButton("🔗 Links", callback_data="links"),
            InlineKeyboardButton("❓ Help", callback_data="help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.callback_query.edit_message_text(
        welcome_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup,
    )

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("info", info))
    dispatcher.add_handler(CommandHandler("buy", buy))
    dispatcher.add_handler(CommandHandler("links", links))
    
    # Register callback query handler
    dispatcher.add_handler(CallbackQueryHandler(button_handler))
    
    # Register error handler
    dispatcher.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started. Press Ctrl+C to stop.")
    
    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
