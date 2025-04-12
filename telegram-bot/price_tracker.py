#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Price Tracker
Fetches and processes price data for the NeonX token from pump.fun
"""

import os
import time
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
COIN_ADDRESS = os.getenv("COIN_ADDRESS")
PUMP_FUN_URL = f"https://pump.fun/coin/{COIN_ADDRESS}"

# Cache for price data
price_cache = {
    "price": "N/A",
    "market_cap": "N/A",
    "holders": "N/A",
    "volume_24h": "N/A",
    "price_change_24h": "N/A",
    "last_updated": 0,
    "cache_duration": 300  # 5 minutes in seconds
}

def fetch_price_data(force_refresh=False):
    """
    Fetch price data from pump.fun
    
    Args:
        force_refresh (bool): Force refresh the cache even if it's not expired
        
    Returns:
        dict: Dictionary containing price data
    """
    current_time = time.time()
    
    # Return cached data if it's still valid
    if not force_refresh and (current_time - price_cache["last_updated"]) < price_cache["cache_duration"]:
        return price_cache
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(PUMP_FUN_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data from the page
        # Note: These selectors will need to be adjusted based on the actual HTML structure
        try:
            # This is a placeholder implementation - you'll need to inspect the actual HTML
            # of pump.fun to find the correct selectors for these values
            
            # Try to find price
            price = extract_price(soup)
            
            # Try to find market cap
            market_cap = extract_market_cap(soup)
            
            # Try to find holders count
            holders = extract_holders(soup)
            
            # Try to find 24h volume
            volume_24h = extract_volume(soup)
            
            # Try to find 24h price change
            price_change_24h = extract_price_change(soup)
            
            # Update cache
            price_cache.update({
                "price": price,
                "market_cap": market_cap,
                "holders": holders,
                "volume_24h": volume_24h,
                "price_change_24h": price_change_24h,
                "last_updated": current_time,
                "success": True,
                "error": None
            })
            
            return price_cache
            
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            price_cache.update({
                "last_updated": current_time,
                "success": False,
                "error": f"Error parsing HTML: {str(e)}"
            })
            return price_cache
            
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        price_cache.update({
            "last_updated": current_time,
            "success": False,
            "error": f"Request error: {str(e)}"
        })
        return price_cache

def extract_price(soup):
    """Extract price from the soup object."""
    # This is a placeholder - you'll need to adjust based on the actual HTML
    try:
        # Example: Find a div with class containing 'price' and extract the text
        price_element = soup.select_one('div[class*="price"]')
        if price_element:
            return price_element.text.strip()
        return "N/A"
    except Exception:
        return "N/A"

def extract_market_cap(soup):
    """Extract market cap from the soup object."""
    try:
        # Example: Find an element containing 'market cap' text
        market_cap_element = soup.find(text=lambda t: t and 'market cap' in t.lower())
        if market_cap_element:
            # Get the parent element and extract the value
            parent = market_cap_element.parent
            # This is simplified - you'll need to adjust based on actual HTML
            return parent.text.replace('Market Cap:', '').strip()
        return "N/A"
    except Exception:
        return "N/A"

def extract_holders(soup):
    """Extract holders count from the soup object."""
    try:
        # Example: Find an element containing 'holders' text
        holders_element = soup.find(text=lambda t: t and 'holders' in t.lower())
        if holders_element:
            # Get the parent element and extract the value
            parent = holders_element.parent
            # This is simplified - you'll need to adjust based on actual HTML
            return parent.text.replace('Holders:', '').strip()
        return "N/A"
    except Exception:
        return "N/A"

def extract_volume(soup):
    """Extract 24h volume from the soup object."""
    try:
        # Example: Find an element containing 'volume' text
        volume_element = soup.find(text=lambda t: t and 'volume' in t.lower())
        if volume_element:
            # Get the parent element and extract the value
            parent = volume_element.parent
            # This is simplified - you'll need to adjust based on actual HTML
            return parent.text.replace('Volume (24h):', '').strip()
        return "N/A"
    except Exception:
        return "N/A"

def extract_price_change(soup):
    """Extract 24h price change from the soup object."""
    try:
        # Example: Find an element containing 'change' text
        change_element = soup.find(text=lambda t: t and 'change' in t.lower())
        if change_element:
            # Get the parent element and extract the value
            parent = change_element.parent
            # This is simplified - you'll need to adjust based on actual HTML
            return parent.text.replace('Change (24h):', '').strip()
        return "N/A"
    except Exception:
        return "N/A"

def get_formatted_price_message():
    """Get a formatted message with price data."""
    data = fetch_price_data()
    
    # Format the message
    if data.get("success", False) or data.get("price") != "N/A":
        message = (
            "💰 *NeonX Price Information* 💰\n\n"
            f"*Current Price:* {data['price']}\n"
            f"*Market Cap:* {data['market_cap']}\n"
            f"*Holders:* {data['holders']}\n"
            f"*Volume (24h):* {data['volume_24h']}\n"
            f"*Price Change (24h):* {data['price_change_24h']}\n\n"
            f"Data from pump.fun\n"
            f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['last_updated']))}"
        )
    else:
        message = (
            "💰 *NeonX Price Information* 💰\n\n"
            "Unable to fetch current price data.\n"
            f"Please check manually at {PUMP_FUN_URL}\n\n"
            f"Error: {data.get('error', 'Unknown error')}"
        )
    
    return message

if __name__ == "__main__":
    # Test the function
    print("Fetching price data for NeonX...")
    print(get_formatted_price_message())
