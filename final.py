import RPi.GPIO as GPIO     ###various modules for speech-to-text, text-to-speech, lcd screen,and GPIO 
import time
import sys 
import os
import lmstudio as lms
import random
import whisper #stt
import speech_recognition as sr #stt
import openai #stt
import sounddevice 
import tkinter as tk 
from gtts import gTTS #tts
from rpi_lcd import LCD #lcd screen
from io import BytesIO
from pygame import mixer #sound output from USB speaker 

GPIO.setmode(GPIO.BCM) #GPIO and LCD setup
GPIO.setwarnings(False)
lcd = LCD()
lcd.clear()

def greet():
    root = tk.Tk() #establishing main GUI window
    root.title("DUCK")
    root.configure(background = "blue")
    root.maxsize(1000, 1000)
    root.minsize(250, 250)
    root.geometry("600x600+0+300")
    frame_count = 12 # frames in my amazing gif
    frames = [tk.PhotoImage(file='peak2.gif',format = 'gif -index %i' %(i)) for i in range(frame_count)]
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind >= frame_count:  # With this condition it will play gif infinitely
            ind = 0
        label.configure(image=frame)
        root.after(100, update, ind)

    tk.Label(root, text="It's ducky time").pack()
    tk.Label(root, text="Welcome...").pack()    
    label = tk.Label(root)
    label.pack()
    root.after(0, update, 0)
    root.mainloop()
    time.sleep(3)
    root.quit()

SERVER_API_HOST = "192.168.110.98:1234" #establishes host address for LMStudio API
lms.configure_default_client(SERVER_API_HOST) 
if lms.Client.is_valid_api_host(SERVER_API_HOST):
    print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
else:
    print(f"No LM Studio API server instance found at {SERVER_API_HOST}")
    sys.exit("Sorry, make sure LMStudio is running next time.")
ai = lms.llm("mistralai/mistral-7b-instruct-v0.3") #llm model established here
model = whisper.load_model("tiny.en") #tiny whisper model to save on resources
recognizer = sr.Recognizer()

AM = open("hate.txt", 'r') #opens AM's amazing monologue which is stored in a text file. 
script = AM.read() #script for testing purposes

#displays text txt on the lcd screen with a delay, delay to create a scrolling effect. 
def lcd_text(txt, delay):
    chunk = 0
    line = 1
    l = line 
    for i in range(len(txt)):
        lcd.text(txt[chunk * 16 : i + 1], l)
        time.sleep(delay)
        if (i + 1) % 32 == 0:
            time.sleep(delay * 5)
            lcd.clear()
            time.sleep(delay * 5)
        if (i + 1) % 16 == 0:
            chunk += 1
            line += 1
            time.sleep(delay * 5)
        if line % 2 == 0:
            l = 2
        else:
            l = 1 
    time.sleep(delay * 10) 
    lcd.clear() 

#receives microphone input 
def listen():
    while True:
        try:
            with sr.Microphone() as source:
                print("Speak.")
                audio = recognizer.listen(source)
                time.sleep(3)
            with open("temp.wav", "wb") as f:
                f.write(audio.get_wav_data())
            print("Processing...")
            result = model.transcribe("temp.wav", fp16 = False)
            print("Complete.")
            text = result["text"]
            return text
        except Exception as e:
            print("Error", e)

def process(txt):
    mp3_fp = BytesIO()
    tts = gTTS(txt, lang='en', tld='co.uk')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

def speak(txt):
    mixer.init()
    print("Processing...")
    sound = process(txt)
    print("Complete.")
    sound.seek(0)
    mixer.music.load(sound, "mp3")
    mixer.music.play()
    time.sleep(60)

def answer():
    speech = listen()
    response = str(ai.respond(speech))
    print("You said:", speech)
    print("Response:", response)
    speak(f"You said: {speech} and I say {response}")

def set_text_speed(): #sets the text speed with a number from 1 to 10, with one being the slowest and 10 being the fatest.
    while True:
        try: 
            spd = round(0.11 - float(input("Please set a text speed from 1 to 10: ")) / 100, 2)
            if not (spd >= 0.01 and spd <= 0.10):
                set_text_speed()
            return spd
        except TypeError:
            pass
        except ValueError:
            pass


def main():
    while True:
        try:
            ans = str(input("Would you like to activate DUCK? y for yes, n for no. \nYou may exit using Ctrl+D.\n"))
            if ans.lower().strip() == 'y' or ans.lower().strip() == 'yes':
                spd = set_text_speed()
                greet()
                print("Check this out.")
                lcd_text("Hello world. Do not fear, for the DUCK is here!", spd)
                lcd_text("ducktastic am I right fellas")
                print(r"""
                                 ⢀⣤⣶⣾⡿⣷⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⣴⡿⠋⠁⢠⣷⣇⠈⠻⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⡿⠁⣶⠀⢸⣿⡿⠋⠀⠹⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢰⠿⡾⢻⡆⠀⠈⠁⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⣠⠟⠤⠗⠈⣿⣤⠀⠀⢀⣸⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⢀⣤⠞⠁⠀⢀⣠⣶⣽⣿⣶⠾⠛⠁⠀⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⣾⠋⠀⢀⣠⣶⡿⠞⠁⣸⡇⠀⠀⠀⠀⠀⣿⡇⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠙⠛⠛⠉⠁⠀⠀⠀⢀⣿⠃⠁⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⢀⣾⡟⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⢀⣾⡿⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢠⣾⡟⠁⠀⠀⠀⠀⠀⠀⠸⣿⣴⣶⣿⡿⠿⢿⣿⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⡀⠀⠀⠀⠀⠀⠀⠉⠛⠿⢿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⣰⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠦⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠿⢿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⢠⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⠶⠶⠶⠶⣶⣦⣤⣄⠀⠀⠈⠙⠛⠷⣦⣀⣠⣤⣶⣄⣠⣴⡄⠀⠀
                        ⠀⠀⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣦⡀⠀⠀⠀⠀⠉⠁⣀⠈⡏⢹⣟⠀⠀⠀
                        ⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣄⡀⠀⠀⣠⡞⠁⠀⠀⠸⠿⣭⣼⠇
                        ⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠶⠖⠛⠀⠀⠀⠀⠀⣾⣿⣯⠀
                        ⠀⠀⢿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠀⣀⣤⡶⠿⠛⠉⠀⠀
                        ⠀⠀⠈⢿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣴⠟⢉⣴⡿⠛⠁⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠙⢿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠛⠉⠀⠉⣁⣴⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠙⠻⢷⣦⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡴⠋⠀⣀⣤⣶⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠛⠻⠷⣶⣶⣤⣤⣀⠀⠀⠀⠀⠀⠀⠘⣛⡶⢾⣭⣤⣴⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⣿⠛⢿⠿⠿⠶⠖⠋⢹⠁⢸⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⢸⣏⠀⢸⡀⠀⠀⠀⠀⢸⠀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⣏⠉⣛⣻⣶⣿⡧⣰⡷⠷⠀⠀⠀⢠⡿⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠿⠿⢿⣏⣅⣤⣶⢿⣧⣀⣀⣀⣠⣾⣃⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠁⢀⣾⣃⣤⣼⠿⡿⢛⣻⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠟⠛⠻⠿⠦⡴⠶⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        """)
                while True:
                    try:
                        answer()
                    except EOFError:
                        sys.exit("\nThank you for using DUCK. Until next time!")
 
            else:
                sys.exit("\nSee ya later, alligator!")
        except ValueError:
            continue
        except EOFError:
            sys.exit("\nThank you for using DUCK. Until next time!")

if __name__ == "__main__":
    main()