import os
import struct
import sys
from datetime import datetime
import numpy as np
import pyaudio
import soundfile
from porcupine import Porcupine
from util import *
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


def listenmic():
    num_keywords = 1
    print('Waiting hotword jarvis:')
    porcupine = None
    pa = None
    audio_stream = None
    try:
        porcupine = Porcupine(library_path='lib/libpv_porcupine.dll', model_file_path='lib/porcupine_params.pv',
                              keyword_file_paths=['keywords/jarvis_windows.ppn'], sensitivities=[0.5])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                               frames_per_buffer=porcupine.frame_length, input_device_index=None)
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if num_keywords == 1 and result:

                print('Listening')
                playmp3("mp3/activation.mp3")
                with sr.Microphone() as source:
                    audio = r.listen(source)
                try:
                    print(r.recognize_google(audio, language="ru-RU"))
                    phrase = r.recognize_google(audio, language="ru-RU")
                    speakme(phrase)
                    print('Waiting hotword jarvis:')
                except sr.UnknownValueError:
                    print("Voice assistant cannot hear phrase")
                    print('Waiting hotword jarvis:')
                except sr.RequestError as e:
                    print("Service error; {0}".format(e))

    finally:
        if porcupine is not None: porcupine.delete()
        if audio_stream is not None: audio_stream.close()
        if pa is not None: pa.terminate()
    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']


listenmic()
