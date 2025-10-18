from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import compute_neurascore, generate_nudge
import time

app = Flask(__name__)
CORS(app)

SESSIONS = {}

@app.route('/api/session/start', methods=['POST'])
def start_session():
    data = request.json or {}
    session_id = str(int(time.time()*1000))
    SESSIONS[session_id] = {
        'focus_samples': [],
        'blink_events': 0,
        'start_ts': time.time(),
        'last_ts': time.time(),
        'events': []
    }
    return jsonify({'session_id': session_id})

@app.route('/api/session/event', methods=['POST'])
def session_event():
    data = request.json or {}
    sid = data.get('session_id')
    if sid not in SESSIONS:
        return jsonify({'error': 'invalid session'}), 400
    s = SESSIONS[sid]
    s['events'].append(data)
    if data.get('has_face'):
        ratio = data.get('eye_open_ratio')
        if ratio is not None:
            s['focus_samples'].append(ratio)
    if data.get('blink'):
        s['blink_events'] += 1
    s['last_ts'] = data.get('timestamp', time.time())
    return jsonify({'status': 'ok'})

@app.route('/api/session/summary', methods=['GET'])
def session_summary():
    sid = request.args.get('session_id')
    if sid not in SESSIONS:
        return jsonify({'error': 'invalid session'}), 400
    s = SESSIONS[sid]
    duration = s['last_ts'] - s['start_ts']
    score = compute_neurascore(s['focus_samples'])
    nudge = generate_nudge(score, s['blink_events'], duration)
    return jsonify({
        'neura_score': score,
        'duration_sec': duration,
        'blink_events': s['blink_events'],
        'nudge': nudge,
        'samples': s['focus_samples'][-50:]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
