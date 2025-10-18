import cv2
import time
import requests
from focus_processor import analyze_frame

API = 'http://localhost:5000'
r = requests.post(API + '/api/session/start', json={})
session = r.json().get('session_id')
print("Session:", session)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open webcam")
    exit()

last_sent = 0
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        res = analyze_frame(frame)
        payload = {
            'session_id': session,
            'eye_open_ratio': res.get('eye_open_ratio'),
            'blink': bool(res.get('blink')),
            'has_face': bool(res.get('has_face')),
            'timestamp': res.get('timestamp')
        }
        now = time.time()
        if now - last_sent > 0.7:
            try:
                requests.post(API + '/api/session/event', json=payload, timeout=1.5)
            except Exception as e:
                print("post error", e)
            last_sent = now

        cv2.putText(frame, f"OpenRatio: {res.get('eye_open_ratio'):.2f}" if res.get('eye_open_ratio') is not None else "No face", (30,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        cv2.imshow('NeuraLift WebCam (press q to quit)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    try:
        summ = requests.get(API + f'/api/session/summary?session_id={session}').json()
        print("Session summary:", summ)
    except:
        pass
