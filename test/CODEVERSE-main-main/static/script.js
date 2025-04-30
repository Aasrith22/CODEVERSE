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
const timeSelect = document.getElementById('time');
const daySelect = document.getElementById('day');
const weatherSelect = document.getElementById('weather');
const predictBtn = document.getElementById('predict-btn');
const loadingOverlay = document.querySelector('.loading-overlay');
const resultsPanel = document.querySelector('.results-panel');
const vehicleTypeSelect = document.getElementById('vehicle-type');
const randomEventsSelect = document.getElementById('random-events');
const peakHoursSelect = document.getElementById('peak-hours');

// Store current active marker
let currentMarker = null;

// Get traffic color based on density
function getTrafficColor(density) {
    if (density <= 0.33) return { color: '#4CAF50', opacity: 0.4 }; // Green - Low Traffic
    if (density <= 0.66) return { color: '#ff9800', opacity: 0.6 }; // Orange - Medium Traffic
    return { color: '#f44336', opacity: 0.8 }; // Red - High Traffic
}

// Create a marker for the selected junction
function createJunctionMarker(name, coords, density) {
    const trafficStyle = getTrafficColor(density);
    const marker = L.circle([coords.lat, coords.lng], {
        radius: 300,
        fillColor: trafficStyle.color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: trafficStyle.opacity,
        className: `junction-marker ${name.toLowerCase()}`
    });

    marker.bindPopup(`
        <div class="junction-popup">
            <div class="name">${name} Junction</div>
            <div class="coordinates">
                ${coords.lat.toFixed(6)}, ${coords.lng.toFixed(6)}
            </div>
            <div class="traffic-info">
                Traffic Density: ${(density * 100).toFixed(1)}%
            </div>
        </div>
    `);

    return marker;
}

// Handle area selection
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
    if (!selectedArea) {
        showToast("Please select an area", "error");
        return;
    }

    if (currentMarker) {
        currentMarker.remove();
        currentMarker = null;
    }

    loadingOverlay.classList.add('active');

    try {
        const requestData = {
            city: document.getElementById('city-select')?.value || '',
            vehicleType: vehicleTypeSelect.value,
            weather: weatherSelect.value,
            day: parseInt(daySelect.value),
            time: timeSelect.value,
            isPeakHour: peakHoursSelect.value === "1",
            randomEvent: randomEventsSelect.value === "1"
        };

        console.log("Sending request:", requestData);

        // Send POST request to Flask server
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) throw new Error('Failed to fetch prediction');

        const prediction = await response.json();
        if (prediction.error) throw new Error(prediction.error);

        // Create a marker with the returned density value
        currentMarker = createJunctionMarker(selectedArea, junctionData[selectedArea], prediction.density);
        currentMarker.addTo(map);
        currentMarker.openPopup();

        // Update results
        updateResults(prediction);
        showToast('Prediction completed successfully!', 'success');
    } catch (error) {
        console.error("Prediction Error:", error);
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        loadingOverlay.classList.remove('active');
    }
});

// Function to update the UI with prediction results
function updateResults(prediction) {
    const densityMeter = document.querySelector('.meter-fill');
    const densityValue = document.getElementById('predicted-density');
    const maeValue = document.getElementById('mae-value');
    const rmseValue = document.getElementById('rmse-value');

    if (densityMeter) densityMeter.style.width = `${prediction.density * 100}%`;
    if (densityValue) densityValue.textContent = prediction.density.toFixed(2);
    if (maeValue) maeValue.textContent = prediction.mae.toFixed(4);
    if (rmseValue) rmseValue.textContent = prediction.rmse.toFixed(4);

    resultsPanel?.classList.add('active');
}

// Form validation
function validateInputs() {
    const isValid = [
        areaSelect.value, timeSelect.value, daySelect.value, weatherSelect.value, vehicleTypeSelect.value,
        randomEventsSelect.value, peakHoursSelect.value
    ].every(value => value !== "");

    predictBtn.disabled = !isValid;
}

// Add validation listeners
[timeSelect, daySelect, weatherSelect, randomEventsSelect, peakHoursSelect, vehicleTypeSelect].forEach(input => {
    input?.addEventListener('change', validateInputs);
});

// Populate hours dropdown
function populateHours() {
    for (let i = 0; i < 24; i++) {
        const option = document.createElement('option');
        option.value = i.toString().padStart(2, '0') + ':00';
        option.textContent = option.value;
        timeSelect.appendChild(option);
    }
}

// Initialize hours dropdown
populateHours();

// Toast notification function
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;

    const container = document.querySelector('.toast-container');
    container.appendChild(toast);

    // Remove toast after 3 seconds
    setTimeout(() => toast.remove(), 3000);
}
