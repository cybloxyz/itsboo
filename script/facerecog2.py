import cv2
import mediapipe as mp
import math

# -----------------------
# Setup Face Mesh
# -----------------------
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# -----------------------
# Helper: deteksi senyum
# -----------------------
def is_smiling(landmarks, frame_w, frame_h):
    """
    Deteksi senyum sederhana berdasarkan jarak bibir.
    landmarks: list titik wajah
    frame_w, frame_h: ukuran frame
    """

    left = landmarks[31]
    right = landmarks[290]
    top = landmarks[0]
    bottom = landmarks[13]

    mouth_width = math.hypot((right.x - left.x)*frame_w, (right.y - left.y)*frame_h)
    mouth_height = math.hypot((top.x - bottom.x)*frame_w, (top.y - bottom.y)*frame_h)

    ratio = mouth_height / mouth_width

    return ratio < 0.15


cap = cv2.VideoCapture(0)
window_name = "Realtime Photobooth"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_h, frame_w = frame.shape[:2]
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    smiling = False

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Gambar mesh wajah
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            # Cek senyum
            smiling = is_smiling(face_landmarks.landmark, frame_w, frame_h)

    # Notifikasi SENYUM!!! jika belum senyum
    if not smiling:
        cv2.putText(frame, "SENYUM!!!", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Tampilkan frame
    cv2.imshow(window_name, frame)

    # tunggu 10ms supaya window responsive
    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
