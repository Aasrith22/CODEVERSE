// Junction coordinates data
const junctionData = {
    'Kukatpally': { lat: 17.493338, lng: 78.402547 },
    'Ameerpet': { lat: 17.434275, lng: 78.445403 },
    'Miyapur': { lat: 17.496653, lng: 78.361809 },
    'Bowenpally': { lat: 17.463865, lng: 78.472837 },
    'Secunderabad': { lat: 17.434962, lng: 78.500812 },
    'Madhapur': { lat: 17.451399, lng: 78.381218 }
};

// Initialize map
const map = L.map('map').setView([17.385044, 78.486671], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap contributors'
}).addTo(map);

// Store UI elements
const areaSelect = document.getElementById('area-select');
const timeInput = document.getElementById('time');
const daySelect = document.getElementById('day');
const weatherSelect = document.getElementById('weather');
const vehicleTypeSelect = document.getElementById('vehicle-type');
const randomEventsSelect = document.getElementById('random-events');
const peakHoursSelect = document.getElementById('peak-hours');
const predictBtn = document.getElementById('predict-btn');
const loadingOverlay = document.querySelector('.loading-overlay');
const resultsPanel = document.querySelector('.results-panel');

// Handle area selection
let currentMarker = null;
areaSelect.addEventListener('change', function (e) {
    const selectedArea = e.target.value;

    if (currentMarker) {
        currentMarker.remove();
        currentMarker = null;
    }

    if (selectedArea) {
        map.setView([junctionData[selectedArea].lat, junctionData[selectedArea].lng], 15);
        validateInputs();
    }
});

// Handle prediction request
predictBtn.addEventListener('click', async function () {
    const selectedArea = areaSelect.value;
    if (!selectedArea) return;

    if (currentMarker) {
        currentMarker.remove();
        currentMarker = null;
    }

    loadingOverlay.classList.add('active');

    try {
        const features = {
            City: selectedArea, // FIXED: Changed 'Area' to 'City' to match Flask API
            time: parseInt(timeInput.value),
            day: parseInt(daySelect.value),
            weather: weatherSelect.value,
            vehicleType: vehicleTypeSelect.value,
            isPeakHour: peakHoursSelect.value === "1" ? 1 : 0,
            randomEvent: randomEventsSelect.value === "1" ? 1 : 0
        };

        console.log("📡 Sending request with data:", JSON.stringify(features));

        const prediction = await getPrediction(features);
        currentMarker = createJunctionMarker(selectedArea, junctionData[selectedArea], prediction.density);
        currentMarker.addTo(map);
        currentMarker.openPopup();

        updateResults(prediction);
        showToast('Prediction completed successfully!');
    } catch (error) {
        console.error('❌ Error fetching prediction:', error);
        showToast('Failed to get prediction. Please try again.', 'error');
    } finally {
        loadingOverlay.classList.remove('active');
    }
});

// Function to get prediction from Flask API
async function getPrediction(features) {
    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(features),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log("Received prediction:", data);
        return data;
    } catch (error) {
        console.error('Error fetching prediction:', error);
        throw error;
    }
}

// Function to create a marker with density-based color
function createJunctionMarker(name, coords, density) {
    const trafficStyle = getTrafficColor(density);
    const marker = L.circle([coords.lat, coords.lng], {
        radius: 300,
        fillColor: trafficStyle.color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: trafficStyle.opacity
    });

    marker.bindPopup(`
        <div class="junction-popup">
            <div class="name">${name} Junction</div>
            <div class="traffic-info">Traffic Density: ${(density * 100).toFixed(1)}%</div>
        </div>
    `);
    return marker;
}

// Get traffic color based on density
function getTrafficColor(density) {
    if (density <= 0.33) {
        return { color: '#4CAF50', opacity: 0.4 };
    } else if (density <= 0.66) {
        return { color: '#ff9800', opacity: 0.6 };
    } else {
        return { color: '#f44336', opacity: 0.8 };
    }
}

// Update results panel
function updateResults(prediction) {
    document.querySelector('.meter-fill').style.width = `${prediction.density * 100}%`;
    document.getElementById('predicted-density').textContent = prediction.density.toFixed(2);
    document.getElementById('mae-value').textContent = prediction.mae.toFixed(4);
    document.getElementById('rmse-value').textContent = prediction.mse.toFixed(4);
    resultsPanel.classList.add('active');
}

// Show toast notification
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

// Validate form inputs
function validateInputs() {
    const isValid = [
        timeInput.value !== '',
        daySelect.value !== '',
        weatherSelect.value !== '',
        areaSelect.value !== '',
        randomEventsSelect.value !== '',
        peakHoursSelect.value !== '',
        vehicleTypeSelect.value !== ''
    ].every(Boolean);
    predictBtn.disabled = !isValid;
}

// Add validation listeners
[timeInput, daySelect, weatherSelect, randomEventsSelect, peakHoursSelect, vehicleTypeSelect].forEach(input => {
    input.addEventListener('change', validateInputs);
});

// Populate hours dropdown
function populateHours() {
    for (let i = 0; i < 24; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = i.toString().padStart(2, '0') + ':00';
        timeInput.appendChild(option);
    }
}
populateHours();
