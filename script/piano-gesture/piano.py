######################################################
# this is the main code for playing piano w/ gestures#
#    code by: nfnaa                                  #
#                                                    #
######################################################

#imports
import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import sys
import time
from sklearn.neighbors import KNeighborsClassifier
import sys

#####################################################
#
#               inisialisasi kode
#
#####################################################
#defdef
def resource(relative):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath("."), relative)

#sound-piano
pygame.mixer.init()

def melodies():
    if gesture == "a":
        pygame.mixer.music.load(resource("piano/a6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "b":
        pygame.mixer.music.load(resource("piano/b6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "c":
        pygame.mixer.music.load(resource("piano/c6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "d":
        pygame.mixer.music.load(resource("piano/d6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "e":
        pygame.mixer.music.load(resource("piano/e6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "f":
        pygame.mixer.music.load(resource("piano/f6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "g":
        pygame.mixer.music.load(resource("piano/g.mp3"))
        pygame.mixer.music.set_volume(0.09)
        pygame.mixer.music.play()
    elif gesture == "h":
        pygame.mixer.music.load(resource("piano/g6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "i":
        pygame.mixer.music.load(resource("piano/b6.mp3"))
        pygame.mixer.music.set_volume(2)
        pygame.mixer.music.play()
    elif gesture == "stop":
        pygame.mixer.music.stop()
    else:
        pass
    
#hands
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils
hands = mphands.Hands()

cam = cv2.VideoCapture(0)

piano_sign = resource("piano_gestures")
knownMelody = []
knownMelodyenc = []
x = []
y = []

last_play = 0
cooldown = 0.8

for filename in os.listdir(piano_sign):
    if filename.endswith(".npy"):
        path = os.path.join(piano_sign, filename)
        data = np.load(path)
        
        if data.ndim == 1:
            data = data.reshape(1, -1)
        
        label = os.path.splitext(filename)[0]
        
        for sample in data:
            x.append(sample)
            y.append(label)
            
x = np.array(x)
y = np.array(y)


clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(x, y)
#######################################################
#
#                      kode utama
#
#######################################################

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    imageRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mpdrawing.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)
            basex, basey, basez = (
                hand_landmarks.landmark[0].x,
                hand_landmarks.landmark[0].y,
                hand_landmarks.landmark[0].z
            )
            
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x - basex, lm.y - basey, lm.z - basez])
            landmarks = np.array(landmarks).flatten()
            
            pred = clf.predict([landmarks])
            gesture = pred[0]
            
            print(gesture)
            
            if time.time() - last_play > cooldown:
                melodies()
                last_play = time.time()
            
    cv2.imshow("piano with gesture!", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()