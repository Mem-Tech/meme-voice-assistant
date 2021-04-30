import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

VOICERSS_KEY = os.getenv('API_VOICERSS_KEY')
VOICE_API_ID = 0 # 0 - voicerss, others - to be continued
VK_TOKEN = os.getenv('VK_TOKEN')
VK_USER_LOGIN = os.getenv('VK_USER_LOGIN')
VK_USER_PASS = os.getenv('VK_USER_PASS')
VK_USER_ID = os.getenv('VK_USER_ID')
VK_PUBLIC_IDS = os.getenv('VK_PUBLIC_IDS').split(",")
VK_CHAT_ID = os.getenv('VK_CHAT_ID')
