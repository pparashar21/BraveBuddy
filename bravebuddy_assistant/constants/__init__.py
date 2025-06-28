import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
RESPONSES_FILE = os.path.join(BASE_DIR, 'curr_response.json')
USER_INFO_FILE = os.path.join(BASE_DIR, 'login_info.json')
ARTIFCATS_DIR = os.path.join(BASE_DIR, 'Artifacts')
# LOGS_DIR = os.path.join(BASE_DIR, 'conversations')
# REMINDER_DIR = os.path.join(BASE_DIR, 'reminder')