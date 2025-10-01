import cv2
import mediapipe as mp

# Inisialisasi modul face detection
mp_face = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Buat detektor wajah
face_detection = mp_face.FaceDetection(model_selection=0, min_detection_confidence=0.5)

# Buka webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Ubah ke RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Deteksi wajah
    results = face_detection.process(frame_rgb)

    # Gambar deteksi
    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(frame, detection)

    # Tampilkan hasil
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
