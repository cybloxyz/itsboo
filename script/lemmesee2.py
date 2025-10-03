import cv2
import numpy as np
import os
import face_recognition
import subprocess as sp
import pyttsx3
import time
import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
import threading 
import pyaudio
import vosk

#hands
mphands = mp.solutions.hands
mpdrawing = mp.solutions.drawing_utils 
hands = mphands.Hands()

#hand sign
sign_dir = "gestures"