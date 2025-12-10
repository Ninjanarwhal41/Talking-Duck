# Talking Duck

## Project Overview
The main functionality of this project is to have a duck that listens and responds to your questions and ideas.

The program greets the user and checks if a local AI server is running through LMStudio. The model in use is Phi 4 Mini Instruct model with 3 billion parameters. If this is not activated, the program will be terminated. The program begins by greeting the user with a pop-up window and a silly GIF of a duck. After the window is closed by a button, the user is prompted to set the text speed for an LCD screen that will display information. The user is prompted to speak, and the speech is fed through whisper speech-to-text, processed by the AI model in LMStudio, and spoken aloud through Google text-to-speech. A few moments after answering, the user is prompted to speak again. This cycle repeats until they choose to exit the program.

## How to Build

### Materials

1. Raspberry Pi 4
2. USB Microphone
3. USB Speaker
4. 4 Male-Female Jumper Wires
5. Breadboard
6. 12 X 2 LCD Screen
7. T-Cobbler & Ribbon Cable
8. 1 duck (any size will do)

### Wiring

The wiring for this project is simple, you only need to wire the LCD screen up to the breadboard of the Pi. 

1. Attach the 1st jumper wire - match the pins labeled GND (ground) on the breadboard and LCD screen
2. Attach the 2nd jumper wire - match the pins labeled VCC and 5V on the breadboard and LCD screen
3. Attach the 3rd jumper wire - match the pins labeled SDA on the breadboard and LCD screen
4. Attach the 4th jumper wire - match the pins labeled SCL on the breadboard and LCD screen

![20251210_141305](https://github.com/user-attachments/assets/f1b3f526-384c-45bf-b3d9-d7bb3d913577)
![20251210_141241](https://github.com/user-attachments/assets/17b59a98-a133-4be0-83b6-dda37b6cc37a)

### Setting up the AI model

First, download LM Studio, and make sure your computer meets the requirements to run it. 

It can be downloaded [here](https://lmstudio.ai/download).
Search in models for Phi 4 Mini Instruct. If you want to try downloading another model, feel free to! There are tons out there.
<img width="2243" height="1238" alt="image" src="https://github.com/user-attachments/assets/8f88a825-081a-40e0-941b-67c42d8495f9" />

Load the model and ensure the server is toggled as 'running'
<img width="2249" height="924" alt="image" src="https://github.com/user-attachments/assets/40c76534-3620-434a-b7d0-ea8e483afae6" />

Create a preset and experiment with customizing setttings such as temperature, different system prompts, and limiting the response length of the model.
Limiting the response length was especially useful for me as it saves a lot of waiting time. 
<img width="2249" height="924" alt="image" src="https://github.com/user-attachments/assets/e7c823b7-ca2d-47a6-a61d-173ebf18a37c" />
<img width="492" height="945" alt="image" src="https://github.com/user-attachments/assets/5b648041-7e3d-40ed-83b4-1b94195c6d27" />

### Writing the code 

There are quite a few modules needed to actually run the program.

Some will need to be installed using pip, because they are not built in.
```
pip install lmms
pip install whisper
pip install pygame
pip install rpi_lcd
pip install gtts
pip install RPI.GPIO
pip install sounddevice
```
If you receive any other errors about a module not being installed, simply install it using 
```
pip install module
```
Create the program:

```python
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
    root.wm_attributes("-topmost", True)
    root.title("DUCK")
    root.configure(background = "blue")
    root.maxsize(1000, 1000)
    root.minsize(250, 250)
    root.geometry("600x600+0+300")
    frame_count = 12 # frames in my amazing gif
    frames = [tk.PhotoImage(file='peak2.gif',format = 'gif -index %i' %(i)) for i in range(frame_count)]
    is_active = True
    def update(ind):
        frame = frames[ind]
        ind += 1
        if ind >= frame_count:  # With this condition it will play gif infinitely
            ind = 0
        label.configure(image=frame)
        if is_active:
            root.after(100, update, ind)
    after_id = root.after(0, update, 0)

    def close():
        root.after_cancel(after_id) 
        global is_active
        is_active = False
        root.destroy()

    tk.Label(root, text="It's ducky time").pack()
    tk.Label(root, text="Welcome...").pack()
    tk.Button(root, activebackground = "orange", activeforeground = "yellow", text="Click to continue", command = close).pack(pady=20)
    label = tk.Label(root)
    label.pack()
    if is_active:
        root.after(0, update, 0)
    root.mainloop()

SERVER_API_HOST = "192.168.110.98:1234" #establishes host address for LMStudio API
lms.configure_default_client(SERVER_API_HOST) 
if lms.Client.is_valid_api_host(SERVER_API_HOST):
    print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
else:
    print(f"No LM Studio API server instance found at {SERVER_API_HOST}")
    sys.exit("Sorry, make sure LMStudio is running next time.\nYou need to have LMSTudio active in order to use DUCK")
ai = lms.llm("mistralai/mistral-7b-instruct-v0.3") #llm model established here
model = whisper.load_model("tiny.en") #tiny whisper model to save on resources/time
recognizer = sr.Recognizer()

AM = open("hate.txt", 'r') #opens AM's amazing monologue which is stored in a text file. 
script = AM.read() #script for testing purposes

#displays text on the lcd screen with a delay to create a scrolling effect. 
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
            with open("temp.wav", "wb") as file:
                file.write(audio.get_wav_data())
            print("Processing, please wait...")
            result = model.transcribe("temp.wav", fp16 = False)
            print("Complete.")
            text = result["text"]
            return text
        except Exception as e:
            print("Error", e)

def process(txt):
    mp3_fp = BytesIO()
    tts = gTTS(txt, lang='en', tld='com.au')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

def speak(txt):
    mixer.init()
    print("Processing, pleease wait...")
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
    speak(f"Quack! {response}")

def set_text_speed(): #sets the text speed with a number from 1 to 10, with one being the slowest and 10 being the fatest.
    while True:
        try: 
            spd = round(0.11 - float(input("Please set a text speed from 1 to 10: ")) / 100, 2)
            if not (spd >= 0.01 and spd <= 0.10):
                set_text_speed()
            return spd
        except ValueError:
            pass


def main():
    while True:
        try:
            ans = str(input("Would you like to activate DUCK? y for yes, n for no. \nYou may exit using Ctrl+D.\n"))
            if ans.lower().strip() == 'y' or ans.lower().strip() == 'yes':
                greet()
                spd = set_text_speed()
                print("Check this out, take a look at the LCD screen--->")
                time.sleep(1)
                lcd_text("Hello world. Do not fear, for the DUCK is here!", spd)
                lcd_text("What can I help you with?", spd)
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
                        ans = input(f"Press any key to ask a question, use Ctrl + D to exit.\nIf you want to change your text speed, press t.")
                        if ans.lower().strip() == "t":
                            set_text_speed()
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
```

### Testing the project

When you run your program, it should behave like the procedure in the beginning describes. The program should be able to respond to multiple questions in a row, 
but please be patient! It takes a long time for everything to process. The LCD screen should display text properly and adapt to changes in text speed. 

## References
[LM Studio Download](https://lmstudio.ai/download)
[Creating Buttons in Tkinter](https://www.geeksforgeeks.org/python/python-creating-a-button-in-tkinter/)
[LM Studio Python Docs](https://lmstudio.ai/docs/python/llm-prediction/chat-completion)
