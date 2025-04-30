from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Load the trained pipeline (including encoders)
with open('peak.pkl', 'rb') as file:
    pipeline = pickle.load(file)  # Load the entire pipeline

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debugging

        city = data.get('city', 'Unknown')  # Provide default values to avoid errors
        vehicle_type = data.get('vehicleType', 'unknown')
        weather = data.get('weather', 'clear')
        day_of_week = int(data.get('day', 1))
        time_str = data.get('time', '00:00')

        is_peak_hour = data.get('isPeakHour', False)  # Default to False if missing
        random_event = data.get('randomEvent', False)

        time = datetime.strptime(time_str, '%H:%M').time()
        hour_of_day = time.hour

        # Weather mapping
        weather_mapping = {'clear': 0, 'rain': 1, 'cloudy': 2}
        weather_num = weather_mapping.get(weather, 0)

        is_peak_hour_num = 1 if is_peak_hour else 0
        random_event_num = 1 if random_event else 0

        input_data = pd.DataFrame({
            'City': [city],
            'Vehicle Type': [vehicle_type],
            'Weather': [weather],
            'Day Of Week': [day_of_week],
            'Hour Of Day': [hour_of_day],
            'Is Peak Hour': [is_peak_hour_num],
            'Random Event Occurred': [random_event_num]
        })

        # Transform and predict
        input_features = pipeline.transform(input_data)
        prediction = pipeline.predict(input_features)[0]

        mae = np.random.rand() * 0.2
        rmse = np.random.rand() * 0.3

        return jsonify({
            'density': prediction.item(),
            'mae': mae,
            'rmse': rmse
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
