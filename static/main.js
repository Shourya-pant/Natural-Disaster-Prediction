let map;
let marker;

function initMap() {
  map = L.map('map').setView([20.59, 78.96], 5);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  map.on('click', function (e) {
    const lat = e.latlng.lat;
    const lng = e.latlng.lng;

    if (marker) map.removeLayer(marker);

    marker = L.marker([lat, lng]).addTo(map);

    fetchPrediction(lat, lng);
  });

  
  document.getElementById('reset-btn').addEventListener('click', () => {
    if (marker) map.removeLayer(marker);
    resetBars();
  });
}

function fetchPrediction(lat, lng) {
  fetch(`/predict?lat=${lat}&lng=${lng}`)
    .then(res => {
      if (!res.ok) throw new Error('Network response was not OK');
      return res.json();
    })
    .then(data => {
      if (data.error) {
        alert('Error: ' + data.error);
        return;
      }
      animateBar('eq', data.earthquake);
      animateBar('flood', data.flood);
      animateBar('fire', data.wildfire);

      document.getElementById('count-eq').textContent = `${data.counts.earthquake} nearby`;
      document.getElementById('count-flood').textContent = `${data.counts.flood} nearby`;
      document.getElementById('count-fire').textContent = `${data.counts.wildfire} nearby`;

      updateDashboardColor(data);
    })
    .catch(err => {
      console.error('Prediction fetch error:', err);
      alert('Prediction service is unavailable.');
    });
}

function animateBar(type, percent) {
  const fill = document.getElementById(`fill-${type}`);
  fill.style.height = `${percent}%`;

  let color = 'green';
  if (percent > 70) color = 'red';
  else if (percent > 40) color = 'orange';
  fill.style.backgroundColor = color;

  if (percent > 80) {
    fill.classList.add('glow');
  } else {
    fill.classList.remove('glow');
  }
}

function updateDashboardColor(data) {
  const dashboard = document.querySelector('.dashboard');
  const maxRisk = Math.max(data.earthquake, data.flood, data.wildfire);

  if (maxRisk > 90) {
    dashboard.style.backgroundColor = '#ff4d4d'; 
  } else if (maxRisk > 70) {
    dashboard.style.backgroundColor = '#ffa500'; 
  } else if (maxRisk > 40) {
    dashboard.style.backgroundColor = '#ffff66'; 
    dashboard.style.backgroundColor = '#111'; 
  }
}

function resetBars() {
  document.querySelectorAll('.bar-fill').forEach(fill => {
    fill.style.height = '0';
    fill.classList.remove('glow');
    fill.style.backgroundColor = 'green';
  });
  document.querySelectorAll('.bar-count').forEach(count => {
    count.textContent = '0 nearby';
  });
  const dashboard = document.querySelector('.dashboard');
  dashboard.style.backgroundColor = '#111';
}

document.addEventListener('DOMContentLoaded', initMap);
