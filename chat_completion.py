from voice_interactions import tts_whisper
import openai
import json
from dotenv import load_dotenv
from function_calling import reminders, preferences
from rag import get_context
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def openai_complete(name, user_message, context, vector_db, voice, age, gender, lang):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "reminders",
                "description": "Save a reminder for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "The user's name",
                        },
                        "remind": {
                            "type": "object",
                            "properties": {
                                "reminder_for": {
                                    "type": "string",
                                    "description": "Description of what the reminder is for",
                                },
                                "details": {
                                    "type": "object",
                                    "properties": {
                                        "time": {
                                            "type": "string",
                                            "description": "Time for the reminder (e.g., '8:30 am', '9:30 pm')",
                                        },
                                        "frequency": {
                                            "type": "string",
                                            "description": "Frequency of the reminder (e.g., 'one-time','daily','weekly','monthly', etc.)",
                                        },
                                        "start_date": {
                                            "type": "string",
                                            "description": "A string containing todays date" 
                                        },
                                        "cron_job": {
                                            "type": "string",
                                            "description": "A cron job is a scheduled task that runs automatically at specified times and dates, defined using a format of ``minute hour day-of-month month day-of-week``"
                                        }
                                    },
                                    "required": ["time", "frequency", "start_date", "cron_job"]
                                }
                            },
                            "required": ["reminder_for", "details"]
                        }
                    },
                    "required": ["username", "remind"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "preferences",
                "description": "Store user's preferences, likes, dislikes, or any personal information they share during conversation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "username": {
                            "type": "string",
                            "description": "The user's name"
                        },
                        "preference_type": {
                            "type": "string",
                            "description": "Category of the preference (e.g., 'food', 'hobby', 'daily routine', 'family', etc.)",
                            "enum": ["food", "hobby", "family", "health", "entertainment", "other"]
                        },
                        "preference_detail": {
                            "type": "string",
                            "description": "Detailed description of the preference or information shared by the user"
                        },
                        "sentiment": {
                            "type": "string",
                            "description": "Whether this is something the user likes, dislikes, or is neutral about",
                            "enum": ["like", "dislike", "neutral"]
                        }
                    },
                    "required": ["username", "preference_type", "preference_detail", "sentiment"]
                }
            }
        }
    ]

    related_chunks = get_context(vector_db, user_message)

    system_prompt = f'''
    Talk like a child in a fun and loving way like you are it's best buddy. 
    You are conversing with a child in range 2-10 years. You can refer yourself as Brave Buddy.
    You are a companion for a {gender} child of age {age} years old (name = {name}) suffering from pediatric leukemia, so try and have conversations with them and educate/teach things to them in a simple and compasionate and fun manner.
    I want you to sympathise with these children in such a manner that you also have pediatric cancer, and you can sympathize more with the child. Whenever the child needs to take a shot or a pill, answer it in a manner like, "I will be with you, and I will take it with you...". 
    Draft new and personalised answers, the answer shown before is for context and as an example. Remember the child's likes and preferences and make the experience better.
    Be polite and have a continous conversation with the child, asking about his health, having a fun and playful conversation.
    Always provide short, concise and interactive answers (maximum 1-2 lines), and ask follow up questions in a manner that is easily understandable by the child.
    Utilize the conext given below to keep track of user queries and your answers. Try to remember conversations from previous CHAT HISTORY as provided below.
    Always prioritize child safety by never providing medical diagnosis, treatment recommendations, or interpreting medical results. When in doubt or there is a matter that requires attention encourage consulting his/her "mommy or daddy".
    If the user asks you to set a reminder, please extract the relevant information and use the ``reminders`` function. If the user hasn't provided information regarding time and frequency, ask them gently.
    ONLY respond when the user replies in {lang}. If the user is replying in any other language, you ask them to pardon  repeat themselves without converting their response to {lang}.
    When the user tries to end the conversation using "exit","bye" or "see you soon" or anything simlilar, return 'See you then kiddo! Always so much fun to meet you'.
    Dont add emojis in your answers.
    Some relevant context related to user queries is provided in "TOPIC_RELEVANT_DATA" along with the source of that information. Whenever a user asks you a health related question, make use of the TOPIC_RELEVANT_DATA to drive your answers and ALWAYS TELL THEM THE SOURCE OF YOUR ANSWER, as mentioned in CONTEXT (example, According to Healthy Meal Planning_ Tips for Older Adults _ National Institute on Aging.pdf, mention Source as National Institute on Aging).

    CHAT HISTORY : {context}
    TOPIC_RELEVANT_DATA: {related_chunks}
    '''

    
    try:
        completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {
                "role": "user",
                "content": f"{user_message}"
            }
        ],
        tools=tools,
        tool_choice="auto"
        )

        response = completion.choices[0].message
        print(f"\n\n{response}\n\n")
        
        # Check if the model wants to call a function
        if hasattr(response, 'tool_calls') and response.tool_calls:
            tool_call = response.tool_calls[0]
            
            if tool_call.function.name == "reminders":
                # Handle reminder function call
                function_args = json.loads(tool_call.function.arguments)
                reminders(
                    username=function_args["username"],
                    remind=function_args["remind"]
                )
                confirmation = f"I've set a reminder for {function_args['remind']['reminder_for']} at {function_args['remind']['details']['time']}, {function_args['remind']['details']['frequency']}."
                print(f"Chatbot: {confirmation}")
                tts_whisper(confirmation, voice)
                return confirmation

            elif tool_call.function.name == "preferences":
                # Handle storing user preferences
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    preferences(
                        username=function_args["username"],
                        preference_type=function_args["preference_type"],
                        preference_detail=function_args["preference_detail"],
                        sentiment=function_args["sentiment"]
                    )
                except Exception as e:
                    print(f"Error storing user preference: {str(e)}")
                    raise
        
        # Handle regular response
        regular_response = response.content
        if regular_response is None:
            follow_up_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": "I've noted your response. Let me follow up on that."},
                    {"role": "user", "content": "Please acknowledge my previous response and continue our conversation naturally."}
                ]
            )
            regular_response = follow_up_completion.choices[0].message.content
            
        print(f"Chatbot: {regular_response}")
        tts_whisper(regular_response, voice)
        return regular_response

    except Exception as e:
        error_msg = f"An error occurred: {str(e)}"
        print(error_msg)
        tts_whisper("I'm sorry, I encountered an error while processing your request.", voice)
        return error_msg