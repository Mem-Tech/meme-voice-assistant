import speech_recognition as sr
import requests, shutil, os, time, re
from pygame import mixer
from settings import VOICERSS_KEY

mixer.init()
r = sr.Recognizer()


def playmp3(filepath):
    global stop
    stop = 0
    song = mixer.music.load(filepath)
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.1)
        if (stop == 1):
            break
    mixer.music.stop()


def speakme(mytext):
    print('Voice assistait said: ' + mytext)
    fm = 'mp3/' + re.sub('[^а-яА-Я]', '', mytext)
    fm = fm[:200]
    fm = fm + '.mp3'
    if not (os.path.exists(fm)):
        mytext = mytext.replace(' ', '+')
        api_url = "http://api.voicerss.org/"
        querystring = {"key": VOICERSS_KEY, "hl": "ru-ru", "c": "mp3", "f": "44khz_16bit_stereo",
                       "src": mytext}
        headers = {
            'x-rapidapi-key': VOICERSS_KEY,
            'x-rapidapi-host': "api.voicerss.org"
        }
        r = requests.request("GET", api_url, headers=headers, params=querystring)
        if r.status_code == 200:
            open(fm, 'wb').write(r.content)

    playmp3(fm)