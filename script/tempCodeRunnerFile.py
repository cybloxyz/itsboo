import cv2 
import mediapipe as mp
import numpy as np
import os

name = input("gesture: ")

cam = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

while True:
    success, image = cam.read()
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            base_x, base_y, base_z = (
                hand_landmarks.landmark[0].x, 
                hand_landmarks.landmark[0].y, 
                hand_landmarks.landmark[0].z
                )
            landmarks = []
            
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x - base_x, lm.y - base_y, lm.z - base_z])
            landmarks = np.array(landmarks).flatten()
    
    cv2.imshow("capturing gesture", image)
    key = cv2.waitKey(1)
    
    if key == ord('c') and landmarks is not None:
        filename = f'gestures/{name}.npy'
        
        np.save(filename, landmarks)
       
        if os.path.exists(filename):
            data = np.load(filename)
            data = np.vstack([data, landmarks])
        else:
            data = np.array([landmarks])
            
        np.save(filename, data)
        print(f'saved {filename} -> {data.shape}')

    elif key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
        
    

    