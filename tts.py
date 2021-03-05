import requests
from settings import VOICERSS_KEY


def tts(text):
    url = "http://api.voicerss.org/"
    querystring = {"key": VOICERSS_KEY, "hl": "ru-ru", "c": "mp3", "f": "44khz_16bit_stereo",
                   "src": text}

    headers = {
        'x-rapidapi-key': VOICERSS_KEY,
        'x-rapidapi-host': "api.voicerss.org"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    open('phrase.mp3', 'wb').write(response.content)


tts("Привет, мир!")
