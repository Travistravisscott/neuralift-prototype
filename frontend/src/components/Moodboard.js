import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js';
Chart.register(LineElement, PointElement, CategoryScale, LinearScale);

function Moodboard({samples}) {
  const labels = samples.map((_,i)=>i+1);
  const data = {
    labels,
    datasets: [
      {
        label: 'Focus (0..1)',
        data: samples,
        tension: 0.3,
        fill: true,
      }
    ]
  };
  return (
    <div className="card">
      <h3>Moodboard — Focus Trend</h3>
      {samples.length ? <Line data={data} /> : <div style={{padding:10}}>No focus samples yet — start the webcam script to feed data.</div>}
    </div>
  );
}

export default Moodboard;
