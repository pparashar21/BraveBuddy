import json
import os
from datetime import datetime
from bravebuddy_assitant.components.voice_interactions import tts_whisper

# Base directory is the folder containing this script file (assuming it's in "llm" folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths using os.path.join() for OS independence
USER_INFO_FILE = os.path.join(BASE_DIR, 'user_info.json')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
REMINDER_DIR = os.path.join(BASE_DIR, 'reminder')

os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REMINDER_DIR, exist_ok=True)


def select_voice():
    """Prompt the user to select a voice and return the selected voice."""
    voice_select_message = "Please select the voice of your choice"
    tts_whisper(voice_select_message)
    print("Please choose a voice to converse with:")
    print("1. Alloy\n2. Echo\n3. Fable\n4. Onyx\n5. Nova\n6. Shimmer")
    dic = {"1": "Alloy", "2": "Echo", "3": "Fable", "4": "Onyx", "5": "Nova", "6": "Shimmer"}
    while True:
        ip = input("Select an option (1-6):\t").strip()
        if ip in dic:
            return dic[ip]
        else:
            print("Invalid selection. Please choose a number between 1 and 6.")

def load_json_data(file_path, default_value):
    """General function to load JSON data with error handling."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {file_path} is corrupted. Returning default value.")
    return default_value

def load_user_info():
    """Load user information from a JSON file."""
    return load_json_data(USER_INFO_FILE, {})

def load_user_logs(username):
    """Load conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    return load_json_data(log_file, [])

def load_user_reminders(username):
    """Load reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    return load_json_data(reminder_file, [])

def save_data(file_path, value, username = "all"):
    try:
        with open(file_path, 'w') as f:
            json.dump(value, f, indent=4)
    except IOError as e:
        print(f"Error saving file at location: {file_path} for {username}")

def save_user_info(user_info):
    """Save user information to a JSON file."""
    save_data(USER_INFO_FILE, user_info)

def save_user_logs(username, logs):
    """Save conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    save_data(log_file, logs, username)

def save_user_reminders(username, reminders):
    """Save reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    save_data(reminder_file, reminders, username)

def add_reminder(username, reminder_details):
    """Add a new reminder to the user's reminders list."""
    reminders = load_user_reminders(username)
    reminders.append(reminder_details)
    save_user_reminders(username, reminders)

def add_preferences(username, reminder_details):
    """Add a new preference to the user's preferences list."""
    reminders = load_user_reminders(username)
    reminders.append(reminder_details)
    save_user_reminders(username, reminders)

def append_conversation(username, conversation):
    """Append a completed conversation session to the user's log."""
    logs = load_user_logs(username)
    logs.append(conversation)
    save_user_logs(username, logs)
