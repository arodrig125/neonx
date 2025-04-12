#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Telegram Bot
A bot to provide information about the NeonX meme coin on Solana.
"""

import os
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telegram import Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
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
BOT_USERNAME = os.getenv("BOT_USERNAME")
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
        f"/price - Check current price\n"
        f"/buy - Get link to buy NeonX\n"
        f"/stats - Community statistics\n"
        f"/links - Important links\n"
        f"/faq - Frequently asked questions"
    )

    # Create keyboard with main options
    keyboard = [
        [
            InlineKeyboardButton("💰 Token Info", callback_data="info"),
            InlineKeyboardButton("📈 Price", callback_data="price"),
        ],
        [
            InlineKeyboardButton("🛒 Buy NeonX", callback_data="buy"),
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
        ],
        [
            InlineKeyboardButton("🔗 Links", callback_data="links"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
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

def get_price_data():
    """Fetch the current price data from pump.fun."""
    try:
        response = requests.get(PUMP_FUN_URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # This is a placeholder - you'll need to adjust the selectors based on the actual HTML structure
        market_cap_text = soup.select_one('text:contains("market cap:")').parent.text
        market_cap = market_cap_text.split('market cap:')[1].strip()

        # Extract price (this is just an example, you'll need to adjust based on the actual page)
        # For now, we'll return a placeholder
        return {
            "market_cap": market_cap,
            "price": "Fetching price data...",  # Placeholder
            "holders": "N/A",  # Placeholder
        }
    except Exception as e:
        logger.error(f"Error fetching price data: {e}")
        return {
            "market_cap": "N/A",
            "price": "Unable to fetch price data",
            "holders": "N/A",
        }

def price(update: Update, context: CallbackContext) -> None:
    """Show the current price of NeonX."""
    # In a real implementation, you would fetch the price from an API
    # For now, we'll use placeholder data
    price_message = (
        "💰 *NeonX Current Price* 💰\n\n"
        "*Price:* $0.00000X\n"
        "*Market Cap:* $X,XXX\n"
        "*24h Change:* +XX%\n\n"
        "Data from pump.fun\n"
        "Last updated: Just now"
    )

    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_price")],
        [InlineKeyboardButton("🛒 Buy Now", url=PUMP_FUN_URL)],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=price_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            price_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def refresh_price(update: Update, context: CallbackContext) -> None:
    """Refresh the price data."""
    update.callback_query.answer("Refreshing price data...")
    price(update, context)

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

def stats(update: Update, context: CallbackContext) -> None:
    """Show community statistics."""
    stats_message = (
        "📊 *NeonX Community Stats* 📊\n\n"
        "*Holders:* XXX+\n"
        "*Telegram Members:* XXX+\n"
        "*Twitter Followers:* XXX+\n\n"
        "Join our growing community today!"
    )

    keyboard = [
        [
            InlineKeyboardButton("💬 Join Telegram", url=TELEGRAM_GROUP),
            InlineKeyboardButton("🐦 Follow Twitter", url=TWITTER_URL),
        ],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=stats_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            stats_message,
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

def faq(update: Update, context: CallbackContext) -> None:
    """Show frequently asked questions."""
    faq_message = (
        "❓ *Frequently Asked Questions* ❓\n\n"
        "*Q: What is NeonX?*\n"
        "A: NeonX is a community-driven meme coin built on the Solana blockchain through pump.fun. With a total supply of 1 billion tokens, NeonX is all about fun, memes, and community - no utility, just vibes!\n\n"
        "*Q: How can I buy NeonX?*\n"
        "A: You can buy NeonX on pump.fun. Simply connect your Solana wallet, enter the NeonX token address, and swap your SOL for NEONX.\n\n"
        "*Q: Is NeonX safe to invest in?*\n"
        "A: Like all cryptocurrencies, especially meme coins, NeonX carries investment risks. Always do your own research and only invest what you can afford to lose.\n\n"
        "*Q: What makes NeonX different?*\n"
        "A: NeonX stands out with its vibrant community and eye-catching neon aesthetic. We're all about creating the most entertaining and engaging meme coin community on Solana."
    )

    keyboard = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Handle both direct command and callback
    if update.callback_query:
        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=faq_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )
    else:
        update.message.reply_text(
            faq_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup,
        )

def button_handler(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    query.answer()

    # Route to the appropriate function based on callback data
    if query.data == "start":
        start(update, context)
    elif query.data == "info":
        info(update, context)
    elif query.data == "price":
        price(update, context)
    elif query.data == "refresh_price":
        refresh_price(update, context)
    elif query.data == "buy":
        buy(update, context)
    elif query.data == "stats":
        stats(update, context)
    elif query.data == "links":
        links(update, context)
    elif query.data == "faq":
        faq(update, context)

def unknown(update: Update, context: CallbackContext) -> None:
    """Handle unknown commands."""
    update.message.reply_text(
        "Sorry, I didn't understand that command. Use /help to see available commands."
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "🤖 *NeonX Bot Commands* 🤖\n\n"
        "/start - Start the bot and see main menu\n"
        "/info - Get token information\n"
        "/price - Check current price\n"
        "/buy - Get link to buy NeonX\n"
        "/stats - Community statistics\n"
        "/links - Important links\n"
        "/faq - Frequently asked questions\n"
        "/help - Show this help message"
    )
    update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

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
    dispatcher.add_handler(CommandHandler("price", price))
    dispatcher.add_handler(CommandHandler("buy", buy))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("links", links))
    dispatcher.add_handler(CommandHandler("faq", faq))

    # Register callback query handler
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Register message handler for unknown commands
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started. Press Ctrl+C to stop.")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
