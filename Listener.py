API = "AIzaSyDABPIwb1sMDdqm4r11_a_LCkRuFtvZHxk" # assigns API to secret API key.
import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import random
import operator
import speech_recognition
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
from urllib.request import urlopen
from vosk import Model, KaldiRecognizer
import pyaudio
import google.generativeai as genai
import pyttsx3 as tts
import pygame
import threading as t
from gtts import gTTS
from time import sleep
import pygame
import random
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession('/home/raspberry/.local/lib/python3.11/site-packages/wolframclient/evaluation/kernel')

pygame.init()

def speak(text):
    global JTALKING
    global UTALKING
    tts = gTTS(text)
    tts.save("voice.wav")
    sleep(0.5)
    talking = pygame.mixer.Sound('/home/raspberry/PROJECT-SPECTRA-VOICE/voice.wav')
    print(text)
    JTALKING = True
    UTALKING = False
    talking.play()
    while pygame.mixer.get_busy():
        pass
    JTALKING = False
    
engine = tts.init()
listener = Model(r"/home/raspberry/PROJECT-SPECTRA-VOICE/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(listener, 16000)
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

JTALKING = True
UTALKING = False

class imageHandler:
  def __init__ ( self ):
    self.pics = dict()

  def loadFromFile ( self, filename, id=None ):
    if id == None: id = filename
    self.pics [ id ] = pygame.image.load ( filename ).convert()

  def loadFromSurface ( self, surface, id ):
    self.pics [ id ] = surface.convert_alpha()

  def render ( self, surface, id, position = None, clear = False, size = None ):
    if clear == True:
      surface.fill ( (5,2,23) ) #

    if position == None:
      picX = int ( surface.get_width() / 2 - self.pics [ id ].get_width() / 2 )
    else:
      picX = position [0]
      picY = position [1]

    if size == None:
      surface.blit ( self.pics [ id ], ( picX, picY ) ) #

    else:
      surface.blit ( pygame.transform.smoothscale ( self.pics [ id ], size ), ( picX, picY ) )





def display():
    global screen
    pygame.display.init() # Initiates the display pygame
    screen = pygame.display.set_mode((1000,600), pygame.NOFRAME| pygame.HIDDEN) #uncomment this line for smaller window
    #screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #allows fullscreen #comment this line out for smaller window
    global handler
    handler = imageHandler()
    
    i = 1
    print("GUI initalizing: 0% complete")
    while i <= 90:
        handler.loadFromFile( "/home/raspberry/PROJECT-SPECTRA-VOICE/JarvisAnimatedFiles/"+str(i)+".gif", str(i) )
        i = i+1
        if i == 45:
            print("GUI initalizing: 25% complete")
    i = 101
    print("GUI initalizing: 50% complete")
    while i <= 190:
        handler.loadFromFile( "/home/raspberry/PROJECT-SPECTRA-VOICE/JarvisAnimatedFiles/"+str(i)+".jpg", str(i) )
        i = i+1
        if i == 145:
            print("GUI initalizing: 75% complete")
    print("GUI initilalizing: 100% complete")
        


def face():
    display()
    A = 200
    B = -5
    x = 600
    y = 550
    global UTALKING, JTALKING
    global handler
    global screen
    COUNT = 1
    if UTALKING or JTALKING:
        screen = pygame.display.set_mode((1000, 600), pygame.NOFRAME | pygame.SHOWN)
    while UTALKING or JTALKING:
        if UTALKING:
            if COUNT >= 91:
                COUNT = COUNT - 100
            img = str(COUNT)
            handler.render(screen, img, (A, B), True, (x,y))
            pygame.display.update(A,B,x,y)
            time.sleep(0.2)
            COUNT = COUNT + 1
            if COUNT == 90:
                COUNT = 1
        elif JTALKING:
            if COUNT <= 100:
                COUNT = COUNT + 100
            img = str(COUNT)
            handler.render(screen, img, (A, B), True, (x,y))
            pygame.display.update(A,B,x,y)
            time.sleep(0.2)
            COUNT = COUNT + 1
            if COUNT == 190:
                COUNT = 101
    screen = pygame.display.set_mode((1000, 600), pygame.NOFRAME| pygame.HIDDEN)


def GetUserInput():
    text = recognizer.Result()
    unfixed = text[14:-3]
    print(unfixed)
    return unfixed

def WolfA_GMI(Input):
    Wolf = 0
    Gemini = 0
    GMI = ['write', 'story', 'instruct', 'tell', 'you', 'me', 'create', 'imagine', 'code', 'why']
    WLF = ['what', 'who', 'is', 'when', 'where']
    for word in GMI:
        if word in Input:
            Gemini = Gemini + 1
    for word in WLF:
        if word in Input:
            Wolf = Wolf + 1
    if (Gemini > Wolf) or (Gemini == Wolf):
        words = chat.send_message("Here is a request from a user: " + Input + ". Please provide a response. Do not say anything else")
        return words
    else:
        try:
            words = session.evaluate(wl.WolframAlpha("number of moons of Saturn", "Result"))
            return words
        except:
            words = chat.send_message("Here is a request from a user: " + Input + ". Please provide a response. Do not say anything else")
            return words
    
SpectrumGUI = t.Thread(target=face)
SpectrumGUI.start()

genai.configure(api_key=API) # Tells gen AI which API to use
model = genai.GenerativeModel('gemini-pro') # Assigns which model is in use and names it model
chat = model.start_chat(history=[])
response = chat.send_message("You are a personal digital assistant, built into a pair of smart glasses. Your name is SPECTRUM. You are a little bit like JARVIS from Iron Man. You are kind and friendly. Please say hello in a kind, creative, and short way. Come up with something new every time. Do not say anything else.")
speak(response.text)

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        userInput = GetUserInput()    
        if 'spectrum' in userInput:
            UTALKING = True
            userInput = userInput.split('spectrum', 1)
            userInput = userInput[1]
            print(userInput)
            if (('the time' in userInput) or ('time is it' in userInput)) and not('in' in userInput):
                now = datetime.datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Current Time =", current_time)
                speak(f"The time is {current_time}")
            else:
                 response = WolfA_GMI(userInput)
                 gen_str = ['Generating.', 'One moment please', 'Hmm. Let me think.', 'Just a moment', 'Thinking.']
                 speak(random.choice(gen_str))
                 speak(response)
                
    