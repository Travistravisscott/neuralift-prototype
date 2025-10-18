# NeuraLift Prototype

This repository contains a local prototype for **NeuraLift** — an AI focus companion for GPAi.
It includes:
- `backend/` : Flask backend, MediaPipe-based focus processor, webcam client
- `frontend/` : React frontend prototype (Dashboard + Moodboard)

## Quick start (local demo)

### Backend
1. `cd backend`
2. Create venv:
   - `python -m venv venv`
   - `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`
4. Run: `python app.py` (runs at http://localhost:5000)

### Webcam client
1. In backend venv, run: `python webcam_client.py`
2. Webcam client opens camera, sends focus events to backend.

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm start` (runs at http://localhost:3000)
4. In production, set `REACT_APP_API_BASE` env variable to the backend URL.

## Notes
- This is a prototype for demo/report only. Make sure to get user consent before enabling webcam capture.
- For deployment, host backend (Render/Heroku) and frontend (Vercel/Netlify).
