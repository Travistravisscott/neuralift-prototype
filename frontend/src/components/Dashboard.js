import React, {useEffect, useState} from 'react';
import Moodboard from './Moodboard';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000';

function Dashboard() {
  const [sessionId, setSessionId] = useState(null);
  const [neuraScore, setNeuraScore] = useState(0);
  const [status, setStatus] = useState('Idle');
  const [samples, setSamples] = useState([]);

  useEffect(() => {
    fetch(API_BASE + '/api/session/start', {method:'POST', headers:{'Content-Type':'application/json'}})
      .then(r=>r.json()).then(data => {
        setSessionId(data.session_id);
      });
  }, []);

  useEffect(() => {
    if (!sessionId) return;
    const t = setInterval(async () => {
      const res = await fetch(`${API_BASE}/api/session/summary?session_id=${sessionId}`);
      const body = await res.json();
      if (!body.error) {
        setNeuraScore(body.neura_score);
        setSamples(body.samples || []);
      }
    }, 2000);
    return ()=>clearInterval(t);
  }, [sessionId]);

  async function triggerZen() {
    setStatus('Zen Mode');
    setTimeout(()=>setStatus('Active'), 3000);
  }

  async function resetMind() {
    setStatus('Resetting');
    setTimeout(()=>setStatus('Active'), 2500);
  }

  return (
    <div className="card">
      <div style={{display:'flex',justifyContent:'space-between', alignItems:'center'}}>
        <div>
          <h2>NeuraScore: {neuraScore}</h2>
          <div className="status">
            <div className="dot" style={{background: neuraScore>80 ? '#00b894' : neuraScore>50 ? '#fdcb6e' : '#ff7675'}}></div>
            <div>{status}</div>
          </div>
        </div>
        <div>
          <div>Session: {sessionId ? sessionId.slice(-6) : '---'}</div>
          <div>Samples: {samples.length}</div>
        </div>
      </div>

      <div style={{marginTop:16}}>
        <div className="controls">
          <button className="button" onClick={triggerZen}>Enter Zen Mode</button>
          <button className="button small" onClick={resetMind}>Reset Mind (2 min)</button>
        </div>
      </div>

      <div style={{marginTop:18}}>
        <Moodboard samples={samples} />
      </div>
    </div>
  );
}

export default Dashboard;
