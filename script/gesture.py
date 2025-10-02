import cv2 
import mediapipe as mp
import numpy as np
import os
import time

name = input("gesture: ")

cam = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

capture = False

sample = 0
want = 30
filename = f'gestures/{name}.npy'
if os.path.exists(filename):
    data = np.load(filename)
else:
    data =np.empty((0, 63))

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
    
    key = cv2.waitKey(1)
    
    if not capture:
        status = "press c to save gestures..."
        cv2.putText(image, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    if key == ord('c') and not capture: 
        print("capturing...")
        capture = True
        time.sleep(1.5)      
    
    last_capture = 0
    delay = 5  

    if capture and landmarks is not None and sample < want:
        if time.time() - last_capture >= delay:
            data = np.vstack([data, landmarks])
            sample += 1
            print(f"Saved sample {sample}/{want}")
            last_capture = time.time()

    if sample >= want:
        np.save(filename, data)
        print(f"All {want} samples saved to {filename} -> {data.shape}")
        break 

    elif key == ord('q'):
        break
    
    cv2.imshow("capturing gesture", image)

cam.release()
cv2.destroyAllWindows()
        
    

    