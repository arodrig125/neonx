#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Price Fetcher for NeonX
Fetches price data from pump.fun
"""

import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

COIN_ADDRESS = os.getenv("COIN_ADDRESS")
PUMP_FUN_URL = f"https://pump.fun/coin/{COIN_ADDRESS}"

def fetch_price_data():
    """
    Fetch price data from pump.fun
    
    Returns:
        dict: Dictionary containing price data
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(PUMP_FUN_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Note: These selectors will need to be updated based on the actual HTML structure of pump.fun
        # This is just a placeholder implementation
        
        try:
            # Try to find market cap
            market_cap_element = soup.find(text=lambda t: t and 'market cap:' in t.lower())
            if market_cap_element:
                market_cap_text = market_cap_element.parent.text
                market_cap = market_cap_text.split('market cap:')[1].strip()
            else:
                market_cap = "N/A"
                
            # Try to find price (this is just an example, adjust based on actual page)
            price = "N/A"  # Placeholder
            
            # Try to find holders count
            holders = "N/A"  # Placeholder
            
            return {
                "success": True,
                "market_cap": market_cap,
                "price": price,
                "holders": holders,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "market_cap": "N/A",
                "price": "N/A",
                "holders": "N/A",
                "error": f"Error parsing HTML: {str(e)}"
            }
            
    except requests.RequestException as e:
        return {
            "success": False,
            "market_cap": "N/A",
            "price": "N/A",
            "holders": "N/A",
            "error": f"Request error: {str(e)}"
        }

if __name__ == "__main__":
    # Test the function
    print("Fetching price data for NeonX...")
    data = fetch_price_data()
    
    if data["success"]:
        print(f"Market Cap: {data['market_cap']}")
        print(f"Price: {data['price']}")
        print(f"Holders: {data['holders']}")
    else:
        print(f"Error: {data['error']}")
