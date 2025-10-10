import RPi.GPIO as GPIO     ###various modules for speech-to-text, text-to-speech, lcd screen,and GPIO 
import time
import random
import whisper #stt
import speech_recognition as sr #stt
import openai #stt
from gtts import gTTS #tts
from rpi_lcd import LCD #lcd screen
from io import BytesIO
from pygame import mixer #tts

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.IN) #setting up microphone input on pin 26 
lcd = LCD()
lcd.clear()
text_output = "hello world, hello world! hello world."


model = whisper.load_model("base")
recognizer = sr.Recognizer()

AM = open("hate.txt", 'r')
script = AM.read()

def lcd_text(txt)
    for i in range(len(txt)):
        lcd.text(txt[i : i + 1])
        time.sleep(0.1)
    #goal is to create a scrolling effect, not sure if this will work. 
    time.sleep(3) #stays for 3 seconds after 
    lcd.clear() 

def listen():
    while True:
        try:
            with sr.Microphone() as source:
                print("Speaketh.")
                audio = recognizer.listen(source)

            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())


            result = model.transcribe("temp.wav")
            text = result["text"]
            print("You said:", text)
            return text
        except Exception as e:
            print("Error", e)

def speak(txt):
    mp3_fp = BytesIO()
    tts = gTTS(txt, lang='en', tld='co.uk')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

listen()
lcd_txt(script)
"""mixer.init()
sound = speak(script)
sound.seek(0)
mixer.music.load(sound, "mp3")
mixer.music.play()

time.sleep(60)
#TTS speaking function above
"""

