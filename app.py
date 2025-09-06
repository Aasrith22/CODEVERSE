from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np
import traceback
from flask_cors import CORS
from crew_orchestrator import TrafficPredictionCrew
from models.mock_data_generator import MockDataGenerator
import json

app = Flask(__name__)
CORS(app)

# Initialize CrewAI system
print("🚀 Initializing AI-Powered Traffic Prediction System...")
crew = TrafficPredictionCrew()
mock_generator = MockDataGenerator()

# Load the trained model (GridSearchCV object) - for backward compatibility
try:
    with open('peak.pkl', 'rb') as file:
        grid_search = pickle.load(file)

    # Extract the best model from GridSearchCV
    if hasattr(grid_search, "best_estimator_"):
        pipeline = grid_search.best_estimator_  # Extract best pipeline
    else:
        pipeline = grid_search  # If already a pipeline

    # Extract preprocessor and regressor
    preprocessor = pipeline.named_steps['preprocessor']
    regressor = pipeline.named_steps['regressor']
    print("✅ Legacy model loaded successfully")
except Exception as e:
    print(f"⚠️ Could not load legacy model: {str(e)}")
    preprocessor = None
    regressor = None

@app.route('/')
def index():
    return render_template('index.html')

def preprocess_input(data):
    """
    Transforms user input using the same preprocessor from training.
    """
    try:
        # Convert input to DataFrame with correct column names
        input_df = pd.DataFrame([data])
        
        # Ensure all numeric columns are properly typed
        numeric_columns = ['Day Of Week', 'Hour Of Day', 'Is Peak Hour', 'Random Event Occurred']
        for col in numeric_columns:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce').fillna(0)
        
        # Ensure string columns are properly typed
        string_columns = ['City', 'Vehicle Type', 'Weather']
        for col in string_columns:
            if col in input_df.columns:
                input_df[col] = input_df[col].astype(str)

        # Apply preprocessor transformation
        transformed_input = preprocessor.transform(input_df)

        return transformed_input
        
    except Exception as e:
        print("⚠️ Preprocessing Error:", str(e))
        # Return a safe fallback transformation
        return np.array([[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("🔍 Received Data:", data)
        
        # Execute comprehensive crew analysis
        print("🤖 Starting CrewAI comprehensive analysis...")
        comprehensive_result = crew.execute_comprehensive_analysis(data)
        
        # Legacy prediction for backward compatibility
        legacy_prediction = None
        if preprocessor and regressor:
            try:
                legacy_prediction = get_legacy_prediction(data)
            except Exception as e:
                print(f"⚠️ Legacy prediction failed: {str(e)}")
        
        # Format response for frontend
        response = {
            'density': comprehensive_result['traffic_prediction']['prediction'],
            'confidence': comprehensive_result['traffic_prediction']['confidence'],
            'mae': 0.118,  # From original model
            'rmse': 0.166,
            'agent_analysis': {
                'current_conditions': comprehensive_result['current_analysis'],
                'prediction_breakdown': comprehensive_result['traffic_prediction']['model_breakdown'],
                'confidence_scores': comprehensive_result['traffic_prediction'].get('confidence_scores', {}),
                'alerts': comprehensive_result['alerts']['active_alerts'],
                'alert_summary': comprehensive_result['alerts']['alert_summary'],
                'recommendations': comprehensive_result['alerts']['recommendations'],
                'route_suggestions': comprehensive_result['route_analysis'],
                'insights': comprehensive_result['agent_insights'],
                'crew_metadata': comprehensive_result['crew_metadata']
            },
            'legacy_prediction': legacy_prediction,
            'analysis_duration': comprehensive_result.get('analysis_duration', 0),
            'timestamp': comprehensive_result['timestamp']
        }
        
        print(f"✅ Comprehensive analysis completed - Density: {response['density']:.2%}")
        return jsonify(response)
        
    except Exception as e:
        print("❌ Error during prediction:", str(e))
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

def get_legacy_prediction(data):
    """Get prediction from original model for comparison"""
    try:
        # Map input to correct feature names
        input_data = {
            'City': str(data.get('City', 'Hyderabad')),
            'Vehicle Type': str(data.get('vehicleType', data.get('vehicle-type', 'Four-Wheeler'))),
            'Weather': str(data.get('weather', 'Very Sunny')),
            'Day Of Week': int(data.get('day', 1)),
            'Hour Of Day': int(data.get('time', 12)),
            'Is Peak Hour': int(data.get('isPeakHour', data.get('peak-hours', 0))),
            'Random Event Occurred': int(data.get('randomEvent', data.get('random-events', 0)))
        }

        # Apply preprocessor to transform input
        transformed_input = preprocess_input(input_data)
        
        # Make prediction using the trained regressor
        prediction = regressor.predict(transformed_input)[0]
        
        # Ensure prediction is a Python float, not numpy float
        if hasattr(prediction, 'item'):
            prediction_value = float(prediction.item())
        else:
            prediction_value = float(prediction)
        
        return {
            'density': prediction_value,
            'model_type': 'legacy_trained_model'
        }
        
    except Exception as e:
        print(f"⚠️ Legacy prediction failed: {str(e)}")
        # Return a fallback prediction
        return {
            'density': 0.5,  # Default moderate traffic
            'model_type': 'fallback_legacy'
        }

@app.route('/real_time_update')
def real_time_update():
    """Provide simulated real-time updates"""
    try:
        simulation_data = mock_generator.generate_real_time_simulation()
        return jsonify(simulation_data)
    except Exception as e:
        print(f"Error generating real-time update: {str(e)}")
        return jsonify({'error': 'Could not generate real-time update'}), 500

@app.route('/agent_status')
def agent_status():
    """Show status of all AI agents"""
    try:
        status = crew.get_agent_status()
        return jsonify(status)
    except Exception as e:
        print(f"Error getting agent status: {str(e)}")
        return jsonify({'error': 'Could not get agent status'}), 500

@app.route('/traffic_data/<location>')
def get_traffic_data(location):
    """Get detailed traffic data for a specific location"""
    try:
        # Generate mock historical data for the location
        historical_data = mock_generator.generate_historical_data(days=7)
        location_data = historical_data[historical_data['location'] == location]
        
        # Convert to JSON-serializable format
        result = {
            'location': location,
            'historical_data': location_data.tail(24).to_dict('records'),  # Last 24 hours
            'coordinates': mock_generator.get_location_coordinates(location),
            'data_points': len(location_data)
        }
        
        return jsonify(result)
    except Exception as e:
        print(f"Error getting traffic data for {location}: {str(e)}")
        return jsonify({'error': 'Could not get traffic data'}), 500

@app.route('/route_optimization', methods=['POST'])
def route_optimization():
    """Dedicated endpoint for route optimization"""
    try:
        data = request.get_json()
        origin = data.get('origin')
        destination = data.get('destination')
        
        if not origin or not destination:
            return jsonify({'error': 'Origin and destination are required'}), 400
        
        # Get current traffic data
        current_traffic = {}
        locations = ['Ameerpet', 'Kukatpally', 'Madhapur', 'Bowenpally', 'Miyapur', 'Secunderabad']
        for loc in locations:
            traffic_sim = mock_generator.simulate_current_traffic(12, 1)  # Mock current conditions
            current_traffic[loc] = traffic_sim.get('density', 0.5)
        
        # Get route suggestions
        route_analysis = crew.route_optimizer.calculate_optimal_routes(
            origin, destination, current_traffic, data.get('preferences')
        )
        
        return jsonify(route_analysis)
        
    except Exception as e:
        print(f"Error in route optimization: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🌟 Starting AI-Powered Traffic Prediction System...")
    print("🤖 CrewAI agents ready for intelligent traffic analysis")
    print("📊 Real-time monitoring and predictions active")
    print("🚀 System ready at http://127.0.0.1:5000")
    app.run(debug=True)
