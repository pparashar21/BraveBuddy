import re
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from bravebuddy_assitant.components.voice_interactions import stt_whisper, tts_whisper
from bravebuddy_assitant.components.chat_completion import openai_complete
# from update_health_question_counter_data import update_health_question_counter, save_user_health_question_counter, load_health_questions
from bravebuddy_assitant.utils.helper import *
from bravebuddy_assitant.components.rag import load_vector_db, create_vector_db
from bravebuddy_assitant.components.emotion_detection import analyze_emotion

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

        voice = select_voice()
        user_info[name] = {'age':age, 'gender':gender, 'language':lang, 'voice':voice}
        save_user_info(user_info)
    else:
        voice = user_info[name]
        welcome_back_message = f"Welcome back, {name}! Always so much fun to meet ya kiddo!"
        tts_whisper(welcome_back_message)

    
    past_logs = load_user_logs(name)
    context = []
    for session in past_logs:
        for entry in session.get('messages', []):
            context.append((entry['timestamp'], entry['user_message'], entry['bot_response']))

    SAVE_DIR = os.path.join(BASE_DIR, "vector_db")
    if os.path.exists(SAVE_DIR):
        embeddings = OpenAIEmbeddings()
        vector_db = load_vector_db(SAVE_DIR, embeddings)
    else:
        vector_db = create_vector_db(SAVE_DIR)

    print("\nYou can start your conversation. Say 'exit' to end.")
    
    cur_time = datetime.now().isoformat()
    current_conversation = {
        'timestamp': cur_time,
        'messages': []
    } 
    
    while True:
        user_message = stt_whisper().strip()
        # user_message = input()
        
        if user_message.lower() == 'exit':
            print("Ending conversation session.")
            break
        
        print(f"You: {user_message}")
        bot_response = openai_complete(name, user_message, context, vector_db, voice, age, gender, lang)
        cur_time = datetime.now().isoformat()
        context.append((cur_time, user_message, bot_response))

        if "alright then" in re.sub(r'[^\w\s]', '', bot_response).lower() or "have a great day ahead" in re.sub(r'[^\w\s]', '', bot_response).lower():
            current_conversation['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
            })
            break
        
        current_conversation['messages'].append({
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response
        })

    
    append_conversation(name, current_conversation)
    print(f"Conversation session saved for user '{name}'.")

    # Emotion detection for the current session
    analyze_emotion(current_conversation)

if __name__ == "__main__":
    main_func()

