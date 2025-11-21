# Talking Duck

## Project Overview
The main functionality of this project is to have a duck that listens and responds to your questions and ideas.

The program greet the user and checks if a local AI server is running through LMStudio. If this is not activated, th e program will not work and be terminated. The program greets the user with a pop-up window and a GIF of a duck. After the window closes, the user is prompted to set the text speed for an LCD screen that will display responses. THe user is prompted to speak, and the speech is fed through whisper speech-to-text, processed by the AI model in LMStudio, and spoken aloud through Google text-to-speech. A few moments after answering, the user is prompted to speak again. This cycle repeats until they choose to exit the program.

## How to Build

### Materials

1. Raspberry Pi 4
2. USB Microphone
3. USB Speaker
4. 4 Male-Female Jumper Wires
5. Breadboard
6. 12 X 2 LCD Screen
7. T-Cobbler & Ribbon Cable
