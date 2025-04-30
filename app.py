from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the trained model (GridSearchCV object)
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

        # Apply preprocessor transformation
        transformed_input = preprocessor.transform(input_df)

        return transformed_input
    except Exception as e:
        print("⚠️ Preprocessing Error:", str(e))
        raise e  # Rethrow error for debugging

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("🔍 Received Data:", data)  # Debugging

        # Map input to correct feature names
        input_data = {
            'City': data['City'],
            'Vehicle Type': data['vehicleType'],
            'Weather': data['weather'],
            'Day Of Week': int(data['day']),
            'Hour Of Day': int(data['time']),
            'Is Peak Hour': int(data['isPeakHour']),  # Convert boolean to int
            'Random Event Occurred': int(data['randomEvent'])  # Convert boolean to int
        }

        # Apply preprocessor to transform input
        transformed_input = preprocess_input(input_data)

        # Make prediction using the trained regressor
        prediction = regressor.predict(transformed_input)[0]  # Extract scalar value

        # Evaluation metrics (predefined from previous results)
        mae = 0.11807073555916203
        mse = 0.027472183969773353
        rmse = mse ** 0.5  # Compute RMSE from MSE

        return jsonify({
            'density': prediction.item(),
            'mae': mae,
            'rmse': rmse
        })

    except Exception as e:
        print("❌ Error during prediction:", str(e))
        print(traceback.format_exc())  # Print full traceback
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
