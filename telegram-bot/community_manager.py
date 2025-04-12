#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NeonX Community Manager
Manages community features like meme sharing and statistics
"""

import os
import json
import time
import logging
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants
COMMUNITY_DATA_FILE = "community_data.json"
MEMES_DIRECTORY = "memes"

class CommunityManager:
    """Manages community features."""
    
    def __init__(self):
        """Initialize the community manager."""
        self.data = self._load_data()
        
        # Ensure memes directory exists
        if not os.path.exists(MEMES_DIRECTORY):
            os.makedirs(MEMES_DIRECTORY)
    
    def _load_data(self):
        """Load community data from file."""
        try:
            if os.path.exists(COMMUNITY_DATA_FILE):
                with open(COMMUNITY_DATA_FILE, 'r') as f:
                    return json.load(f)
            return {
                "users": {},
                "memes": [],
                "stats": {
                    "total_users": 0,
                    "active_users": 0,
                    "total_messages": 0,
                    "last_updated": 0
                }
            }
        except Exception as e:
            logger.error(f"Error loading community data: {e}")
            return {
                "users": {},
                "memes": [],
                "stats": {
                    "total_users": 0,
                    "active_users": 0,
                    "total_messages": 0,
                    "last_updated": 0
                }
            }
    
    def _save_data(self):
        """Save community data to file."""
        try:
            with open(COMMUNITY_DATA_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving community data: {e}")
    
    def register_user_activity(self, user_id, username=None, first_name=None, last_name=None):
        """
        Register user activity.
        
        Args:
            user_id (int): Telegram user ID
            username (str, optional): Telegram username
            first_name (str, optional): User's first name
            last_name (str, optional): User's last name
        """
        user_id = str(user_id)
        current_time = time.time()
        
        if user_id not in self.data["users"]:
            # New user
            self.data["users"][user_id] = {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "first_seen": current_time,
                "last_active": current_time,
                "message_count": 1
            }
            self.data["stats"]["total_users"] += 1
        else:
            # Existing user
            self.data["users"][user_id]["last_active"] = current_time
            self.data["users"][user_id]["message_count"] += 1
            
            # Update user info if provided
            if username:
                self.data["users"][user_id]["username"] = username
            if first_name:
                self.data["users"][user_id]["first_name"] = first_name
            if last_name:
                self.data["users"][user_id]["last_name"] = last_name
        
        # Update stats
        self.data["stats"]["total_messages"] += 1
        self.data["stats"]["last_updated"] = current_time
        
        # Calculate active users (active in the last 24 hours)
        active_count = 0
        for user in self.data["users"].values():
            if current_time - user["last_active"] < 86400:  # 24 hours in seconds
                active_count += 1
        self.data["stats"]["active_users"] = active_count
        
        self._save_data()
    
    def add_meme(self, file_id, user_id, caption=None):
        """
        Add a meme to the collection.
        
        Args:
            file_id (str): Telegram file ID
            user_id (int): User who submitted the meme
            caption (str, optional): Caption for the meme
        
        Returns:
            int: Index of the new meme
        """
        user_id = str(user_id)
        current_time = time.time()
        
        meme = {
            "file_id": file_id,
            "user_id": user_id,
            "caption": caption,
            "submitted_at": current_time,
            "likes": 0,
            "liked_by": []
        }
        
        self.data["memes"].append(meme)
        self._save_data()
        
        return len(self.data["memes"]) - 1
    
    def get_random_meme(self):
        """
        Get a random meme from the collection.
        
        Returns:
            dict: Meme data or None if no memes
        """
        if not self.data["memes"]:
            return None
        
        return random.choice(self.data["memes"])
    
    def get_top_memes(self, limit=5):
        """
        Get the top memes by likes.
        
        Args:
            limit (int): Maximum number of memes to return
        
        Returns:
            list: List of top memes
        """
        sorted_memes = sorted(self.data["memes"], key=lambda m: m["likes"], reverse=True)
        return sorted_memes[:limit]
    
    def like_meme(self, meme_index, user_id):
        """
        Like a meme.
        
        Args:
            meme_index (int): Index of the meme
            user_id (int): User who liked the meme
        
        Returns:
            bool: True if the meme was liked successfully, False otherwise
        """
        user_id = str(user_id)
        
        if meme_index < 0 or meme_index >= len(self.data["memes"]):
            return False
        
        meme = self.data["memes"][meme_index]
        
        # Check if the user already liked this meme
        if user_id in meme["liked_by"]:
            return False
        
        meme["likes"] += 1
        meme["liked_by"].append(user_id)
        
        self._save_data()
        return True
    
    def get_community_stats(self):
        """
        Get community statistics.
        
        Returns:
            dict: Community statistics
        """
        return self.data["stats"]
    
    def get_user_stats(self, user_id):
        """
        Get statistics for a specific user.
        
        Args:
            user_id (int): Telegram user ID
        
        Returns:
            dict: User statistics or None if user not found
        """
        user_id = str(user_id)
        return self.data["users"].get(user_id)
    
    def format_community_stats_message(self):
        """
        Format a message with community statistics.
        
        Returns:
            str: Formatted message
        """
        stats = self.get_community_stats()
        
        message = (
            "📊 *NeonX Community Statistics* 📊\n\n"
            f"*Total Users:* {stats['total_users']}\n"
            f"*Active Users (24h):* {stats['active_users']}\n"
            f"*Total Messages:* {stats['total_messages']}\n"
            f"*Total Memes:* {len(self.data['memes'])}\n\n"
            f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats['last_updated']))}"
        )
        
        return message

# Create a singleton instance
community_manager = CommunityManager()

if __name__ == "__main__":
    # Test the community manager
    print("Testing community manager...")
    
    # Register some user activity
    community_manager.register_user_activity(123456, "testuser", "Test", "User")
    community_manager.register_user_activity(789012, "anotheruser", "Another", "User")
    
    # Add some memes
    community_manager.add_meme("test_file_id_1", 123456, "Test meme 1")
    community_manager.add_meme("test_file_id_2", 789012, "Test meme 2")
    
    # Like a meme
    community_manager.like_meme(0, 789012)
    
    # Get community stats
    print(community_manager.format_community_stats_message())
    
    # Get a random meme
    print(community_manager.get_random_meme())
