from pocketsphinx import LiveSpeech
import serial
import time
import pygame
import pyttsx3

# Sambung ke Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # tunggu Arduino siap

# Setup musik
pygame.mixer.init()
pygame.mixer.music.load("move.mp3")
pygame.mixer.music.set_volume(0.5)  # set volume 50%

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('volume', 0.5)  # 50% volume
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # lambat 50

# Setup PocketSphinx
speech = LiveSpeech(lm=False, keyphrase='move', kws_threshold=1e-20)

print("magic words?...")

for phrase in speech:
    text = str(phrase).lower()
    if 'move' in text:
        print("i'll move on")
        arduino.write(b'move\n')
        engine.say("you are my everything..")
        engine.runAndWait()
        pygame.mixer.music.play()
        # tunggu musik selesai biar tidak langsung exit
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        break
