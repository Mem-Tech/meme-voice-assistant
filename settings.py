import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

VOICERSS_KEY = os.getenv('API_VOICERSS_KEY')
VK_TOKEN = os.getenv('VK_TOKEN')
VK_USER_ID = os.getenv('VK_USER_ID')