import streamlit as st
import pickle
import pandas as pd
import numpy as np
import traceback

# Load the trained model
with open('peak.pkl', 'rb') as file:
    grid_search = pickle.load(file)

# Extract the best model
pipeline = grid_search.best_estimator_ if hasattr(grid_search, "best_estimator_") else grid_search

# Extract preprocessor and regressor
preprocessor = pipeline.named_steps['preprocessor']
regressor = pipeline.named_steps['regressor']

def preprocess_input(data):
    try:
        # Convert all values to strings to avoid type issues
        for key, value in data.items():
            if value is None or value == "":
                data[key] = "Unknown"  # Default for missing values
            else:
                data[key] = str(value)  # Convert everything to string

        # Convert to DataFrame
        input_df = pd.DataFrame([data])

        # Identify categorical transformers dynamically
        for name, transformer, columns in preprocessor.transformers_:
            if 'categorical' in name.lower():  # Identify categorical transformers
                if hasattr(transformer, 'categories_'):
                    known_categories = {
                        col: set(transformer.categories_[i]) for i, col in enumerate(columns)
                    }

                    # Replace unknown categories with "Unknown"
                    for col in columns:
                        if col in input_df.columns:
                            input_df[col] = input_df[col].apply(lambda x: x if x in known_categories[col] else "Unknown")

        # Apply preprocessor transformation
        transformed_input = preprocessor.transform(input_df)

        return transformed_input

    except Exception as e:
        st.error(f"⚠️ Preprocessing Error: {e}")
        return None



# Streamlit UI
st.title("Traffic Density Prediction")

# User input fields
city = st.text_input("City", value="Kukatpally")
vehicle_type = st.text_input("Vehicle Type", value="")
weather = st.text_input("Weather", value="Unknown")
day = st.number_input("Day Of Week", min_value=0, max_value=6, step=1, value=0)
time = st.number_input("Hour Of Day", min_value=0, max_value=23, step=1, value=0)
is_peak_hour = st.checkbox("Is Peak Hour")
random_event = st.checkbox("Random Event Occurred")

if st.button("Predict"):
    try:
        input_data = {
            'City': city,
            'Vehicle Type': vehicle_type,
            'Weather': weather,
            'Day Of Week': int(day),
            'Hour Of Day': int(time),
            'Is Peak Hour': int(is_peak_hour),
            'Random Event Occurred': int(random_event)
        }
        
        transformed_input = preprocess_input(input_data)

        if transformed_input is not None:
            prediction = regressor.predict(transformed_input)[0]

            # Predefined evaluation metrics
            mae = 0.11807073555916203
            mse = 0.027472183969773353
            rmse = np.sqrt(mse)

            st.success(f"Predicted Density: {prediction:.4f}")
            st.write(f"MAE: {mae:.4f}, RMSE: {rmse:.4f}")
        else:
            st.error("⚠️ Unable to process input due to preprocessing errors.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.text(traceback.format_exc())
