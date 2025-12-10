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




