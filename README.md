# BraveBuddy
Repository for Rutgers Health Hackathon 2024

## Overview
BraveBuddy is a compassionate companion designed for pediatric cancer patients aged 2-10. Understanding the unique challenges these children face, BraveBuddy aims to provide comfort, support, and a sense of normalcy during their treatment journey. Many children feel isolated, especially when their siblings lead a more typical life. BraveBuddy serves as a companion that not only normalizes their experience but also encourages them through tough moments.

## Features
Companion Toy: BraveBuddy is a physical teddy bear/toy that stays with the child throughout their day, offering companionship during both hospital visits and at home.
Interactive Conversations: BraveBuddy is equipped to engage in simple, comforting conversations. Children can ask questions and receive age-appropriate, reassuring responses.
Emotional Support: The buddy is designed to comfort children in difficult moments. For instance, if a child expresses fear about a shot, BraveBuddy responds with encouragement like, “It’s okay, we’ll take it together. You’ve got this!”
Educational Guidance: BraveBuddy helps explain medical processes and terms in a child-friendly way. For example, when asked about chemotherapy, it might say, “Chemotherapy is a special kind of medicine that helps fight the yucky sick cells in our body. It’s like a superhero helping our bodies get better. Do you want to know more? Or talk about something fun while we wait?”
Normalization of Experience: By fostering a sense of companionship and understanding, BraveBuddy helps children feel less alone in their journey, normalizing their experiences and emotions.

## Purpose
BraveBuddy aims to:
Alleviate feelings of loneliness and isolation in pediatric cancer patients.
Provide emotional support and encouragement during challenging moments.
Educate children about their treatment in a comforting way.
Create a positive and comforting presence throughout their treatment journey.


## Tech Stack used:
**Python**
**VA**
  - Openai API: Whisper.ai, GPT 4o mini
  
**Database**
  - mongoDB Atlas -> for database (which helped in eliminating on-premise scaling bcz it is automatically scaled on the cloud)

**Front end**
- Streamlit -> You can fire up the front end using the command streamlit run app.py (for future releases)

## LLM:
**LLM setup:**

Install ffmpeg
Using chocolatey for windows: choco install ffmpeg
Using homebrew for macOS brew install ffmpeg
Navigate to in your shell/terminal
Install all the necessary python libraries using pip install -r requirements.txt
Run main.py

** LLM Functionalities: **
Speech-to-Text (STT): The VA can understand and process user voice commands.
Text-to-Speech (TTS): Reads out health-related information back to the user in a clear, natural tone.
Short, Concise Responses: Provides brief, accurate responses to user queries.
Clarification Handling: Requests clarification when user input is complex or unclear.
Voice Interaction Deletion: Allows users to delete saved voice interactions to ensure privacy.
LLM Integration Testing: Conducted integration tests for the large language model to ensure accurate conversation flow.
User Interaction Logs: Captures logs of individual user interactions for review and improvement.
End-of-Conversation Detection: Detects when a conversation has naturally ended and disengages to ensure a smooth user experience.
Reminders: reminders for medications, their time and frequency of repetition.



