# BraveBuddy 

Repository for Rutgers Health Hackathon 2024

## Overview
BraveBuddy is a compassionate companion designed for pediatric cancer patients aged 2-10. Understanding the unique challenges these children face, BraveBuddy aims to provide comfort, support, and a sense of normalcy during their treatment journey. Many children feel isolated, especially when their siblings lead a more typical life. BraveBuddy serves as a companion that not only normalizes their experience but also encourages them through tough moments.

---

## Features
- **Companion Toy:** BraveBuddy is a physical teddy bear/toy that stays with the child throughout their day, offering companionship during both hospital visits and at home.
- **Interactive Conversations:** BraveBuddy is equipped to engage in simple, comforting conversations. Children can ask questions and receive age-appropriate, reassuring responses.
- **Emotional Support:** The buddy is designed to comfort children in difficult moments. For instance, if a child expresses fear about a shot, BraveBuddy responds with encouragement like, “It’s okay, we’ll take it together. You’ve got this!”
- **Educational Guidance:** BraveBuddy helps explain medical processes and terms in a child-friendly way. For example, when asked about chemotherapy, it might say, “Chemotherapy is a special kind of medicine that helps fight the yucky sick cells in our body. It’s like a superhero helping our bodies get better. Do you want to know more? Or talk about something fun while we wait?”
- **Normalization of Experience:** By fostering a sense of companionship and understanding, BraveBuddy helps children feel less alone in their journey, normalizing their experiences and emotions.

---

## Purpose
BraveBuddy aims to:
  - Alleviate feelings of loneliness and isolation in pediatric cancer patients.
  - Provide emotional support and encouragement during challenging moments.
  - Educate children about their treatment in a comforting way.
  - Create a positive and comforting presence throughout their treatment journey.

---

## Tech Stack Used
- **Programming Language:**
  - Pyton
- **VA**
  - Openai API: Whisper.ai, GPT 4o mini
- **Database**
  - mongoDB Atlas -> for database (which helped in eliminating on-premise scaling bcz it is automatically scaled on the cloud)
- **Front end**
  - Streamlit -> You can fire up the front end using the command streamlit run app.py (for future releases)

---

## LLM (Large Language Model)
**LLM setup:**

1. Install FFmpeg (required for audio processing)
  - On Windows: choco install ffmpeg (requires Chocolatey)
  - On macOS: brew install ffmpeg (requires Homebrew)
2. Install Dependencies
  - Navigate to the project directory in your shell/terminal.
  - Run: pip install -r requirements.txt
3. Run the Application
  - Execute the main script: python main.py
  - For the frontend, run: streamlit run app.py

**LLM Functionalities:**
- Speech-to-Text (STT): The VA can understand and process user voice commands.
- Text-to-Speech (TTS): Reads out health-related information back to the user in a clear, natural tone.
- Short, Concise Responses: Provides brief, accurate responses to user queries.
- Clarification Handling: Requests clarification when user input is complex or unclear.
- Voice Interaction Deletion: Allows users to delete saved voice interactions to ensure privacy.
- LLM Integration Testing: Conducted integration tests for the large language model to ensure accurate conversation flow.
- User Interaction Logs: Captures logs of individual user interactions for review and improvement.
- End-of-Conversation Detection: Detects when a conversation has naturally ended and disengages to ensure a smooth user experience.
- Reminders: reminders for medications, their time and frequency of repetition.

---

## GitHub Setup for New Users

If you’re new to GitHub, follow these steps to set up the repository locally:

1. **Create a GitHub Account**: Go to [GitHub](https://github.com/) and sign up if you don’t already have an account.

2. **Install Git**: 
   - On Windows, download and install Git from [here](https://git-scm.com/download/win).
   - On macOS, use Homebrew by running `brew install git`.
   - On Linux, use your package manager, e.g., `sudo apt install git` for Ubuntu.

3. **Clone the Repository**:
   - Open your terminal or command prompt.
   - Run the following command to clone the repository:
     ```bash
     git clone https://github.com/YourUsername/BraveBuddy.git
     ```
   - Replace `YourUsername` with the GitHub username associated with the repository if it’s hosted on your account.

4. **Navigate to the Project Directory**:
   - Go to the directory where you cloned the repo:
     ```bash
     cd BraveBuddy
     ```

5. **Setting Up Git Remotes**:
   - If you plan to make changes and push them, add a remote origin:
     ```bash
     git remote add origin https://github.com/YourUsername/BraveBuddy.git
     ```

6. **Sync Changes**:
   - To pull any new changes from the repository, run:
     ```bash
     git pull origin main
     ```

---

This README provides a complete setup guide for users, including instructions on GitHub setup for beginners.


