import os
import struct
import sys
from datetime import datetime
from time import sleep

import numpy as np
import pyaudio
from porcupine import Porcupine

from Classes.MemePost import PostWithValidPhotos
from util import *
import speech_recognition as sr
from settings import VK_TOKEN, VK_USER_ID, VK_PUBLIC_IDS, VK_CHAT_ID, VK_USER_PASS, VK_USER_LOGIN
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_part.vktools import write_msg_vk_user, get_memes, get_random_meme, write_msg_vk_chat
from tools.mp3tools import playmp3, speakme

r = sr.Recognizer()


# vk = vk_api.VkApi(token=VK_TOKEN)

# longpoll = VkLongPoll(vk)


def auth_handler():
    key = input("Enter authentication code: ")
    remember_device = True

    return key, remember_device


# vk_session = vk_api.VkApi(VK_USER_LOGIN, VK_USER_PASS, auth_handler=auth_handler, scope='messages')
vk_session = vk_api.VkApi(token=VK_TOKEN)

try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()


def get_new_posts():
    print('')


def assistant_words_func(x):
    return {
        1: 'отправь мем',
        2: 'отошли мем',
        3: 'пошли мем',
    }[x]


assistant_meme_words = {
    1: 'отправь мем',
    2: 'отошли мем',
    3: 'пошли мем',
    4: 'отправить мем',
    5: 'мем'
}

chat_names = {
    1: 'техномемы',
    2: 'техно мемы',
    3: 'мемы',
    4: 'техно'
}


def where_to_send():
    # playmp3("mp3/activation.mp3")
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        print(r.recognize_google(audio, language="ru-RU"))
        phrase = r.recognize_google(audio, language="ru-RU")
        for chat in chat_names.values():
            if phrase.lower() == chat:
                mem_post = get_random_meme(VK_PUBLIC_IDS)
                atts = mem_post.formatted_photos
                text = mem_post.text
                write_msg_vk_chat(vk_api, vk, VK_CHAT_ID, text, atts)
                speakme('отправила!')
    except sr.UnknownValueError:
        print("Voice assistant cannot hear phrase")
        speakme('Не услышала')
        print('Waiting hotword:')

    except sr.RequestError as e:
        print("Service error; {0}".format(e))
    #finally:
    #    speakme('повтори')


def listenmic():
    num_keywords = 1
    print('Waiting hotword:')
    porcupine = None
    pa = None
    audio_stream = None
    try:
        porcupine = Porcupine(library_path='lib/libpv_porcupine.dll', model_file_path='lib/porcupine_params.pv',
                              keyword_file_paths=['keywords/jarvis_windows.ppn'], sensitivities=[0.9])
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

                    for value in assistant_meme_words.values():
                        if phrase.lower() == value:
                            speakme('куда')
                            where_to_send()
                            # mem_post = get_random_meme(VK_PUBLIC_IDS)
                            # atts = mem_post.formatted_photos
                            # text = mem_post.text
                            # write_msg_vk_chat(vk_api, vk, VK_CHAT_ID, text, atts)

                            # write_msg_vk_chat(vk_api, vk, VK_CHAT_ID, text, atts)
                            print(value)

                    print('Waiting hotword:')
                except sr.UnknownValueError:
                    print("Voice assistant cannot hear phrase")
                    speakme('Не услышала')
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
