import cv2
import face_recognition
import os
import numpy as np
import subprocess as sp
import pyttsx3
import time
import mediapipe as mp
from sklearn.neighbors import KNeighborsClassifier
import threading
import pyaudio
import vosk
import serial

#serial initial
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1 )
time.sleep(2)

#speech_gesture
speechg = {
    "halo" : "hello",
    "aku" : "i am",
    "mau" : "want",
    "belajar" : "study",
    "senang berkenalan" : "nice to meet you",
    "na" : "nafisa",
    "peace" : "peace",
    "sama sama" : "you are welcome",
    "fuck" : "fuck",
    "maaf" : "sorry",
    "good" : "good",
    "thanks" : "thank you",
    "tolong" : "help",
    "love_you" : "i love you"
 }


#hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()
#hand sign
sign_dir = "gestures"
x = []
y = []
known_sign = []
know_sign_encodings = []

#sounds
engine = pyttsx3.init()
engine.setProperty('volume', 0.5)  # 50% volume
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 60) 
spoken = set()

#faces
cam = cv2.VideoCapture(0)
faces_dir = "faces"
known_face_encodings = []
known_face_names = []
hon = "na"

#flag
speech_started = False

#definition
def run_speech():
    sp.Popen(["python3", "talk/talk.py"])
    
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def what():
    cam.release()
    cv2.destroyAllWindows()

for filename in os.listdir(faces_dir):
    if filename.endswith(".jpg")or filename.endswith(".png"):
        img_path=os.path.join(faces_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if len(encoding)>0:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

x = []
y = []

for filename in os.listdir(sign_dir):
    if filename.endswith(".npy"):
        path = os.path.join(sign_dir, filename)
        data = np.load(path)

        # pastikan 2D: 1 sample -> (1, 63)
        if data.ndim == 1:
            data = data.reshape(1, -1)

        label = os.path.splitext(filename)[0]
 
        for sample in data:
            x.append(sample)
            y.append(label)

x = np.array(x)  # sekarang pasti (total_samples, 63)
y = np.array(y)  # (total_samples,)
print(f"x shape: {x.shape}, y shape: {y.shape}")


clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(x, y)
            
while True:
    ret, frame = cam.read()
    if not ret:
        break
    
    #Hands recognition
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

#sign  recognition 
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
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
            if gesture == "love_you":
                arduino.write(b'love you <3\n')
                
            elif gesture == "aku":
                arduino.write(b'i am\n')
                
            elif gesture == "good":
                arduino.write(b'good\n')
                
            elif gesture == "belajar":
                arduino.write(b'study\n')
                
            elif gesture == "fuck":
                arduino.write(b'fuck\n')
                
            elif gesture == 'halo':
                arduino.write(b'hello\n')
                
            elif gesture == 'kamu':
                arduino.write(b'you\n')
                
            elif gesture == "mau":
                arduino.write(b'want\n')
                
            elif gesture == "na":
                arduino.write(b'na\n')
                
            elif gesture == "no":
                arduino.write(b'no\n')
                
            elif gesture == "peace":
                arduino.write(b'peace\n')
                
            elif gesture == "sama sama":
                arduino.write(b'you\'re welcome!\n')
                
            elif gesture == "senang berkenalan":
                arduino.write(b'nice to meet u\n')
                
            elif gesture == "sorry":
                arduino.write(b'sorry\n')
                
            elif gesture == "thanks":
                arduino.write(b'thank you\n')
                
            elif gesture == "tolong":
                arduino.write(b'help\n')
            else:
                pass
                        
            cv2.putText(frame, f"{pred[0]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1 , (0,255,0), 3)
    
            
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    face_names = []
    
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
        face_names.append(name)
        
        if name == "Unknown":
            new_name = f"unlisted_{len(known_face_names)+1}"
            save_path = os.path.join(faces_dir, new_name + ".jpg")
            cv2.imwrite(save_path, frame)
            print(f"new face detected, automatically saved as {new_name}")
            known_face_encodings.append(face_encoding)
            known_face_names.append(new_name)
            
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        
        if name == "na":
           cv2.putText(frame, "yes it's you <3", (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
           if not speech_started:
               engine.say("hello, it is nice to see you here..")
               engine.runAndWait()            
               speech_started = True
      
        else:
            cv2.putText(frame, f"{name} no it isn't you", (left, top-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)
            

            
    cv2.imshow("approving..", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()