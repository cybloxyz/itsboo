##################################################
#
#    code by: nfnaa
#
##################################################

#imports
import cv2
import mediapipe as mp
import numpy as np
import pygame
import os
import sys
import pyttsx3
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
    
#hands
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils
hands = mphands.Hands()

cam = cv2.VideoCapture(0)

piano_sign = resource("piano_gesture")
knownMelody = []
knownMelodyenc = []
x = []
y = []

#sound-piano
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

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
            
    cv2.imshow("piano with gesture!")
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cam.release()
cv2.destroyAllWindows()