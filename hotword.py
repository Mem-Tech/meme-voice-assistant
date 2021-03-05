import os
import struct
import sys
from datetime import datetime
import numpy as np
import pyaudio
from porcupine import Porcupine
from util import *
import speech_recognition as sr
from settings import VK_TOKEN, VK_USER_ID
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_part.vktools import write_msg_vk
from tools.mp3tools import playmp3, speakme

r = sr.Recognizer()
vk = vk_api.VkApi(token=VK_TOKEN)
longpoll = VkLongPoll(vk)


def get_new_posts():
    print('')


def listenmic():
    num_keywords = 1
    print('Waiting hotword:')
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
                    if phrase == 'Отправь мем':
                        speakme('Отправляю')
                        write_msg_vk(vk_api, vk, VK_USER_ID, phrase)
                    print('Waiting hotword:')
                except sr.UnknownValueError:
                    print("Voice assistant cannot hear phrase")
                    print('Waiting hotword:')
                except sr.RequestError as e:
                    print("Service error; {0}".format(e))

    finally:
        if porcupine is not None: porcupine.delete()
        if audio_stream is not None: audio_stream.close()
        if pa is not None: pa.terminate()
    _AUDIO_DEVICE_INFO_KEYS = ['index', 'name', 'defaultSampleRate', 'maxInputChannels']


if __name__ == '__main__':
    listenmic()
