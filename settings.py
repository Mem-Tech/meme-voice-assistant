import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

VOICERSS_KEY = os.getenv('API_VOICERSS_KEY')
