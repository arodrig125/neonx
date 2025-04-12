#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Alerts Manager
Manages price alerts for users
"""

import os
import json
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
ALERTS_FILE = "user_alerts.json"

class AlertsManager:
    """Manages price alerts for users."""
    
    def __init__(self):
        """Initialize the alerts manager."""
        self.alerts = self._load_alerts()
    
    def _load_alerts(self):
        """Load alerts from file."""
        try:
            if os.path.exists(ALERTS_FILE):
                with open(ALERTS_FILE, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading alerts: {e}")
            return {}
    
    def _save_alerts(self):
        """Save alerts to file."""
        try:
            with open(ALERTS_FILE, 'w') as f:
                json.dump(self.alerts, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving alerts: {e}")
    
    def add_alert(self, user_id, alert_type, threshold, chat_id=None):
        """
        Add a new alert for a user.
        
        Args:
            user_id (int): Telegram user ID
            alert_type (str): Type of alert ('price_above', 'price_below', 'percent_change')
            threshold (float): Threshold value for the alert
            chat_id (int, optional): Chat ID to send the alert to. Defaults to user_id.
        
        Returns:
            bool: True if the alert was added successfully, False otherwise
        """
        user_id = str(user_id)  # Convert to string for JSON serialization
        chat_id = chat_id or user_id
        
        if user_id not in self.alerts:
            self.alerts[user_id] = []
        
        # Check if this alert already exists
        for alert in self.alerts[user_id]:
            if alert['type'] == alert_type and alert['threshold'] == threshold:
                return False
        
        # Add the new alert
        self.alerts[user_id].append({
            'type': alert_type,
            'threshold': threshold,
            'chat_id': chat_id,
            'created_at': time.time(),
            'triggered': False,
            'last_triggered': None
        })
        
        self._save_alerts()
        return True
    
    def remove_alert(self, user_id, alert_index):
        """
        Remove an alert for a user.
        
        Args:
            user_id (int): Telegram user ID
            alert_index (int): Index of the alert to remove
        
        Returns:
            bool: True if the alert was removed successfully, False otherwise
        """
        user_id = str(user_id)
        
        if user_id not in self.alerts:
            return False
        
        if alert_index < 0 or alert_index >= len(self.alerts[user_id]):
            return False
        
        self.alerts[user_id].pop(alert_index)
        
        # Remove the user entry if they have no more alerts
        if not self.alerts[user_id]:
            del self.alerts[user_id]
        
        self._save_alerts()
        return True
    
    def get_user_alerts(self, user_id):
        """
        Get all alerts for a user.
        
        Args:
            user_id (int): Telegram user ID
        
        Returns:
            list: List of alerts for the user
        """
        user_id = str(user_id)
        return self.alerts.get(user_id, [])
    
    def get_all_alerts(self):
        """
        Get all alerts for all users.
        
        Returns:
            dict: Dictionary of all alerts
        """
        return self.alerts
    
    def check_alerts(self, current_price, previous_price=None):
        """
        Check all alerts against the current price.
        
        Args:
            current_price (float): Current price of the token
            previous_price (float, optional): Previous price of the token for percent change alerts
        
        Returns:
            list: List of triggered alerts with user_id and alert details
        """
        triggered_alerts = []
        
        try:
            current_price = float(current_price)
            if previous_price is not None:
                previous_price = float(previous_price)
        except (ValueError, TypeError):
            logger.error(f"Invalid price values: current={current_price}, previous={previous_price}")
            return triggered_alerts
        
        for user_id, user_alerts in self.alerts.items():
            for i, alert in enumerate(user_alerts):
                triggered = False
                
                if alert['type'] == 'price_above' and current_price >= alert['threshold']:
                    triggered = True
                elif alert['type'] == 'price_below' and current_price <= alert['threshold']:
                    triggered = True
                elif alert['type'] == 'percent_change' and previous_price is not None:
                    percent_change = ((current_price - previous_price) / previous_price) * 100
                    if abs(percent_change) >= alert['threshold']:
                        triggered = True
                
                if triggered and not alert['triggered']:
                    # Mark the alert as triggered
                    self.alerts[user_id][i]['triggered'] = True
                    self.alerts[user_id][i]['last_triggered'] = time.time()
                    
                    triggered_alerts.append({
                        'user_id': user_id,
                        'chat_id': alert['chat_id'],
                        'alert': alert,
                        'current_price': current_price,
                        'previous_price': previous_price
                    })
                elif not triggered:
                    # Reset the triggered flag if the condition is no longer met
                    self.alerts[user_id][i]['triggered'] = False
        
        if triggered_alerts:
            self._save_alerts()
        
        return triggered_alerts
    
    def format_alert_message(self, alert_data):
        """
        Format an alert message.
        
        Args:
            alert_data (dict): Alert data from check_alerts
        
        Returns:
            str: Formatted alert message
        """
        alert = alert_data['alert']
        current_price = alert_data['current_price']
        previous_price = alert_data['previous_price']
        
        if alert['type'] == 'price_above':
            return (
                "🚨 *NeonX Price Alert* 🚨\n\n"
                f"Price has risen above your alert threshold of {alert['threshold']}!\n"
                f"Current price: {current_price}"
            )
        elif alert['type'] == 'price_below':
            return (
                "🚨 *NeonX Price Alert* 🚨\n\n"
                f"Price has fallen below your alert threshold of {alert['threshold']}!\n"
                f"Current price: {current_price}"
            )
        elif alert['type'] == 'percent_change':
            percent_change = ((current_price - previous_price) / previous_price) * 100
            direction = "increased" if percent_change > 0 else "decreased"
            return (
                "🚨 *NeonX Price Alert* 🚨\n\n"
                f"Price has {direction} by {abs(percent_change):.2f}%!\n"
                f"Previous price: {previous_price}\n"
                f"Current price: {current_price}"
            )
        
        return "🚨 *NeonX Price Alert* 🚨\n\nYour price alert has been triggered!"

# Create a singleton instance
alerts_manager = AlertsManager()

if __name__ == "__main__":
    # Test the alerts manager
    print("Testing alerts manager...")
    
    # Add some test alerts
    alerts_manager.add_alert(123456, 'price_above', 0.0001)
    alerts_manager.add_alert(123456, 'price_below', 0.00005)
    alerts_manager.add_alert(789012, 'percent_change', 5)
    
    # Check alerts
    triggered = alerts_manager.check_alerts(0.00011, 0.0001)
    for alert in triggered:
        print(alerts_manager.format_alert_message(alert))
    
    # Get user alerts
    print(alerts_manager.get_user_alerts(123456))
    
    # Remove an alert
    alerts_manager.remove_alert(123456, 0)
    print(alerts_manager.get_user_alerts(123456))
