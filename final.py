import RPi.GPIO as GPIO     ###various modules for speech-to-text, text-to-speech, lcd screen,and GPIO 
import time
import random
import whisper
import speech_recognition as sr
import openai
from gtts import gTTS
from rpi_lcd import LCD
from io import BytesIO
from pygame import mixer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

model = whisper.load_model("base")
recognizer = sr.Recognizer()

GPIO.setup(26, GPIO.IN)

AM = open("hate.txt", 'r')
script = AM.read()

def listen():
    while True:
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
        try:
            with sr.Microphone(device_index=0) as source:
                print("Say something")
                audio = recognizer.listen(source)

            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())


            result = model.transcribe("temp.wav")
            text = result["text"]
            print("You said:", text)
        except Exception as e:
            print("Error", e)

def speak(txt):
    mp3_fp = BytesIO()
    tts = gTTS(txt, lang='en', tld='co.uk')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

listen()
"""mixer.init()
sound = speak(script)
sound.seek(0)
mixer.music.load(sound, "mp3")
mixer.music.play()

time.sleep(60)
#TTS speaking function above




lcd = LCD()

lcd.clear()
text_output = "testing testing one two three"



lcd.text(text_output, 1)
time.sleep(5)
lcd.clear() """
