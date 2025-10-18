import time
import numpy as np
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

LEFT_EYE_IDX = [33, 7, 163, 144, 145, 153, 154, 155, 133]
RIGHT_EYE_IDX = [362, 382, 381, 380, 374, 373, 390, 249, 263]

face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False,
                                  max_num_faces=1,
                                  refine_landmarks=True,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

def _landmark_to_point(landmark, w, h):
    return np.array([int(landmark.x * w), int(landmark.y * h)])

def eye_openness_ratio(landmarks, eye_idx, w, h):
    pts = [_landmark_to_point(landmarks[i], w, h) for i in eye_idx]
    left = pts[0]
    right = pts[-1]
    top = pts[1]
    bottom = pts[4]
    horiz = np.linalg.norm(right - left)
    vert = np.linalg.norm(top - bottom) + 1e-6
    ratio = vert / horiz
    return ratio

def analyze_frame(frame):
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    timestamp = time.time()
    if not results.multi_face_landmarks:
        return {'eye_open_ratio': None, 'blink': False, 'timestamp': timestamp, 'has_face': False}
    lm = results.multi_face_landmarks[0].landmark
    left_ratio = eye_openness_ratio(lm, LEFT_EYE_IDX, w, h)
    right_ratio = eye_openness_ratio(lm, RIGHT_EYE_IDX, w, h)
    ratio = float((left_ratio + right_ratio) / 2.0)
    blink = ratio < 0.12
    norm = (ratio - 0.08) / (0.25 - 0.08)
    norm = max(0.0, min(1.0, norm))
    return {'eye_open_ratio': norm, 'blink': blink, 'timestamp': timestamp, 'has_face': True}
