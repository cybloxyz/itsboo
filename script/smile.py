import cv2
import mediapipe as mp
import numpy as np

# =========================
# Inisialisasi MediaPipe Hands
# =========================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# =========================
# Inisialisasi Haar Cascade Face & Smile
# =========================
facelib = cv2.CascadeClassifier('frontalface.xml')
smilelib = cv2.CascadeClassifier('casc_smile.xml')

# =========================
# Buka webcam
# =========================
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Gagal membaca frame")
        break

    # =========================
    # Face detection (grayscale)
    # =========================
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facelib.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Smile detection di dalam ROI wajah
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        smiles = smilelib.detectMultiScale(roi_gray, scaleFactor=1.5, minNeighbors=15, minSize=(25, 25))
        for (sx, sy, sw, sh) in smiles:
            cv2.putText(frame, "great, i know you", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2, cv2.LINE_AA)
            cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0,255,0), 2)

    # =========================
    # Hand tracking (MediaPipe)
    # =========================
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # =========================
    # Tampilkan frame gabungan
    # =========================
    cv2.imshow('Face + Smile + Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================
# Bersihkan
# =========================
cap.release()
cv2.destroyAllWindows()
