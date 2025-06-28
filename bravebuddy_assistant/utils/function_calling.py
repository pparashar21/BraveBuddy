import json
import os
from bravebuddy_assistant.utils.helper import *
from datetime import datetime
from bravebuddy_assistant.constants import *

def reminders(username:str, remind:dict) -> None:
    append_reminder(username, remind)
    return

def preferences(username: str, preference_type: str, preference_detail: str, sentiment: str):
    """
    Store user preferences in a JSON file. Each user has their own preferences file that maintains
    a history of their stated preferences with timestamps.
    
    Args:
        username (str): The user's name
        preference_type (str): Category of the preference (food, hobby, etc.)
        preference_detail (str): Detailed description of the preference
        sentiment (str): Whether it's a like, dislike, or neutral preference
    """
    # Create preferences directory if it doesn't exist
    preferences_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_preferences')
    os.makedirs(preferences_dir, exist_ok=True)
    
    # Path to user's preferences file
    preferences_file = os.path.join(preferences_dir, f"{username.lower()}_preferences.json")
    
    try:
        # Load existing preferences if file exists
        if os.path.exists(preferences_file):
            with open(preferences_file, 'r', encoding='utf-8') as f:
                preferences = json.load(f)
        else:
            preferences = {
                "user": username,
                "last_updated": None,
                "preferences": []
            }
        
        # Create new preference entry
        new_preference = {
            "type": preference_type,
            "detail": preference_detail,
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Add new preference to the list
        preferences["preferences"].append(new_preference)
        preferences["last_updated"] = datetime.now().isoformat()
        
        # Write updated preferences back to file
        with open(preferences_file, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, indent=2, ensure_ascii=False)
            
        print(f"Successfully stored preference for {username}: {preference_detail}")
        return True
        
    except Exception as e:
        print(f"Error storing preference for {username}: {str(e)}")
        raise

def get_user_preferences(username: str) -> dict:
    """
    Retrieve all stored preferences for a given user.
    
    Args:
        username (str): The user's name
        
    Returns:
        dict: Dictionary containing all user preferences
    """
    preferences_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_preferences')
    preferences_file = os.path.join(preferences_dir, f"{username.lower()}_preferences.json")
    
    try:
        if os.path.exists(preferences_file):
            with open(preferences_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error retrieving preferences for {username}: {str(e)}")
        return None

def get_preferences_by_type(username: str, preference_type: str) -> list:
    """
    Retrieve all preferences of a specific type for a given user.
    
    Args:
        username (str): The user's name
        preference_type (str): Type of preferences to retrieve (e.g., 'food', 'hobby')
        
    Returns:
        list: List of preferences of the specified type
    """
    preferences = get_user_preferences(username)
    if preferences and 'preferences' in preferences:
        return [
            pref for pref in preferences['preferences']
            if pref['type'] == preference_type
        ]
    return []

