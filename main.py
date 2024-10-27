import json
import os
import re
from datetime import datetime, timedelta
from voice_interactions import stt_whisper, tts_whisper
from chat_completion import openai_complete

# File and directory configurations
USER_INFO_FILE = 'llm/user_info.json'
LOGS_DIR = 'llm/logs'
REMINDER_DIR = 'llm/reminder'

# Ensure the logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(REMINDER_DIR, exist_ok=True)

def load_user_info():
    """Load user information from a JSON file."""
    if os.path.exists(USER_INFO_FILE):
        try:
            with open(USER_INFO_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Error: user_info.json is corrupted. Starting with empty user info.")
    return {}

def save_user_info(user_info):
    """Save user information to a JSON file."""
    try:
        with open(USER_INFO_FILE, 'w') as f:
            json.dump(user_info, f, indent=4)
    except IOError as e:
        print(f"Error saving user info: {e}")

def load_user_reminders(username):
    """Load reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    if os.path.exists(reminder_file):
        try:
            with open(reminder_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {reminder_file} is corrupted. Starting with empty reminders.")
    return []

def save_user_reminders(username, reminders):
    """Save reminders for a specific user."""
    reminder_file = os.path.join(REMINDER_DIR, f"{username}_reminders.json")
    try:
        with open(reminder_file, 'w') as f:
            json.dump(reminders, f, indent=4)
    except IOError as e:
        print(f"Error saving reminders for {username}: {e}")

def add_reminder(username, reminder_details):
    """Add a new reminder to the user's reminders list."""
    reminders = load_user_reminders(username)
    reminders.append(reminder_details)
    save_user_reminders(username, reminders)

def load_user_logs(username):
    """Load conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: {log_file} is corrupted. Starting with empty logs.")
    return []

def save_user_logs(username, logs):
    """Save conversation logs for a specific user."""
    log_file = os.path.join(LOGS_DIR, f"{username}.json")
    try:
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=4)
    except IOError as e:
        print(f"Error saving logs for {username}: {e}")

def append_conversation(username, conversation):
    """Append a completed conversation session to the user's log."""
    logs = load_user_logs(username)
    logs.append(conversation)
    save_user_logs(username, logs)

def summarize_conversation(conversation):
    """Generate a summary of a conversation session."""
    summary = []
    for msg in conversation['messages']:
        user_message = msg['user_message']
        bot_response = msg['bot_response']
        summary.append(f"You: {user_message}\nBot: {bot_response}")
    return '\n'.join(summary)

def main_func():
    user_info = load_user_info()
    
    print("Login:\n")
    login_message = "Hi Kiddo! So happy to meet you!"
    tts_whisper(login_message)
    name = input("Can you enter your name to continue your conversation:\t").strip().upper()
    age = input("Enter your age to continue your conversation:\t").strip().upper()
    gender = input("Enter your gender to continue your conversation:\t").strip().upper()
    lang = input("Enter your language to continue your conversation:\t").strip().upper()
    
    if not name:
        name_empty_message = "Name cannot be empty. Exiting."
        tts_whisper(name_empty_message)
        return
    
    if name not in user_info:
        welcome_message = f"Welcome {name}! Your best bud Brave Bear is here!"
        tts_whisper(welcome_message)
        user_info[name] = {"age":age, "gender":gender, "language" : lang}
        save_user_info(user_info)
    else:
        voice = user_info[name]
        welcome_back_message = f"Welcome back, {name}! Always so much fun to meet ya kiddo!"
        tts_whisper(welcome_back_message)
    
    # Load previous logs to build the initial context
    past_logs = load_user_logs(name)
    context = []
    for session in past_logs:
        for entry in session.get('messages', []):
            context.append((entry['user_message'], entry['bot_response']))
    
    # Initialize current conversation session
    current_conversation = {
        'timestamp': datetime.now().isoformat(),
        'messages': []
    }
    
    while True:
        user_message = stt_whisper().strip()
        
        if user_message.lower() == 'exit':
            print("Ending conversation session.")
            break
       
        print(f"You: {user_message}")
        bot_response = openai_complete(user_message, context, age, gender, name, lang)
    
        # Attempt to extract and parse the JSON part
        json_match = re.search(r"\{[^}]+\}+", bot_response.replace("\n", ""), re.DOTALL)

        if json_match:
            json_str = json_match.group(0).strip()  # Get the matched JSON string
            json_str = json_str.replace("'", '"')

            try:
                bot_response_dict = json.loads(json_str)  # Parse it to a dictionary
                reminder_file_path = os.path.join("reminder", f"{name}_reminder.json")
                print(f"Debug: Saving reminder to {reminder_file_path}")
                add_reminder(name, bot_response_dict)
    
            except json.JSONDecodeError:
                print("Debug: bot_response is not a valid JSON string")
        
        # Update context for the current session
        context.append((user_message, bot_response))

        if re.sub(r'[^\w\s]', '', bot_response) == 'See you then kiddo Always so much fun to meet you':
            print("See you then kiddo! Always so much fun to meet you")
            break
        
        # Add to current conversation
        current_conversation['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
        })
    
    # Append the completed conversation to the user's log
    append_conversation(name, current_conversation)
    print(f"Conversation session saved for user '{name}'.")

if __name__ == "__main__":
    main_func()
