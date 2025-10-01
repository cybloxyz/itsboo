import cv2
import face_recognition
import os
import numpy as np

faces_dir = "faces"
known_face_encodings = []
known_face_names = []

# Load database wajah dari folder faces/
for filename in os.listdir(faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(faces_dir, filename)
        image = face_recognition.load_image_file(img_path)
        encoding = face_recognition.face_encodings(image)
        if len(encoding) > 0:
            known_face_encodings.append(encoding[0])
            known_face_names.append(os.path.splitext(filename)[0])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
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

        # Automatic storing jika Unknown
        if name == "Unknown":
            new_name = f"person_{len(known_face_names)+1}"
            save_path = os.path.join(faces_dir, new_name + ".jpg")
            cv2.imwrite(save_path, frame)
            print(f"Saved new face automatically as {new_name}")
            known_face_encodings.append(face_encoding)
            known_face_names.append(new_name)

    # Gambar kotak & nama
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4; right *= 4; bottom *= 4; left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
