import cv2
import face_recognition
import os
import numpy as np
import subprocess as sp
import pyttsx3
import time

engine = pyttsx3.init()
engine.setProperty('volume', 0.5)  # 50% volume
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 60) 

faces_dir = "faces"
known_face_encodings = []
known_face_names = []
hon = "na"

speech_started = False

def run_speech():
    sp.Popen(["python3", "talk/talk.py"])

for filename in os.listdir(faces_dir):
    if filename.endswith(".jpg")or filename.endswith(".png"):
        img_path=os.path.join(faces_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if len(encoding)>0:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])
            
cam = cv2.VideoCapture(0)

def what():
    cam.release()
    cv2.destroyAllWindows()

while True:
    ret, frame = cam.read()
    if not ret:
        break
    
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
        
       if name == na:
           cv2.putText(frame, "yes it's you <3", (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
           if not speech_started:
               engine.say("yes it is you and will always you")
               engine.runAndWait()
               run_speech()
               speech_started = True
      
        else:
            cv2.putText(frame, f"{name} no it isn't you", (left, top-20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

            
    cv2.imshow("approving..", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()