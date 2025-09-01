import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import os

class EnsembleModels:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.is_trained = False
        
    def create_models(self):
        """Initialize all models"""
        self.models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(n_estimators=50, random_state=42),
            'neural_network': MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        }
        
        # Create scalers for each model
        for model_name in self.models.keys():
            self.scalers[model_name] = StandardScaler()
    
    def train_models(self, X, y):
        """Train all models with the provided data"""
        self.create_models()
        
        for model_name, model in self.models.items():
            print(f"Training {model_name}...")
            
            # Scale features for neural network
            if model_name == 'neural_network':
                X_scaled = self.scalers[model_name].fit_transform(X)
                model.fit(X_scaled, y)
            else:
                model.fit(X, y)
        
        self.is_trained = True
        print("All models trained successfully!")
    
    def predict(self, X, model_name=None):
        """Make predictions using specified model or all models"""
        if not self.is_trained:
            # Return mock predictions if models aren't trained
            return self._mock_predict(X, model_name)
        
        if model_name:
            model = self.models[model_name]
            if model_name == 'neural_network':
                X_scaled = self.scalers[model_name].transform(X)
                return model.predict(X_scaled)
            else:
                return model.predict(X)
        else:
            # Return predictions from all models
            predictions = {}
            for name, model in self.models.items():
                if name == 'neural_network':
                    X_scaled = self.scalers[name].transform(X)
                    predictions[name] = model.predict(X_scaled)
                else:
                    predictions[name] = model.predict(X)
            return predictions
    
    def _mock_predict(self, X, model_name=None):
        """Generate mock predictions for demonstration"""
        # Convert X to array if it's a list
        if isinstance(X, list):
            X = np.array([X])
        elif isinstance(X, np.ndarray) and X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Generate realistic mock predictions based on input features
        base_predictions = {}
        
        for i in range(X.shape[0]):
            # Extract features (assuming standard order)
            try:
                # Try to use actual feature values for realistic prediction
                time_feature = X[i][4] if X.shape[1] > 4 else 12  # Hour of day
                peak_hour = X[i][5] if X.shape[1] > 5 else 0  # Is peak hour
                random_event = X[i][6] if X.shape[1] > 6 else 0  # Random event
                
                # Base prediction logic
                base_density = 0.3
                
                # Rush hour impact
                if time_feature in [8, 9, 17, 18, 19] or peak_hour == 1:
                    base_density += 0.3
                
                # Random event impact
                if random_event == 1:
                    base_density += 0.2
                
                # Add some variation for different models
                predictions = {
                    'linear_regression': max(0, min(1, base_density + np.random.normal(0, 0.05))),
                    'random_forest': max(0, min(1, base_density + np.random.normal(0, 0.03))),
                    'neural_network': max(0, min(1, base_density + np.random.normal(0, 0.04)))
                }
                
                base_predictions.update(predictions)
                
            except (IndexError, TypeError):
                # Fallback to random predictions
                predictions = {
                    'linear_regression': np.random.beta(2, 3),
                    'random_forest': np.random.beta(2, 3),
                    'neural_network': np.random.beta(2, 3)
                }
                base_predictions.update(predictions)
        
        if model_name:
            return np.array([base_predictions[model_name]])
        else:
            return {name: np.array([pred]) for name, pred in base_predictions.items()}
    
    def get_feature_importance(self, model_name='random_forest'):
        """Get feature importance from tree-based models"""
        if model_name in self.models and hasattr(self.models[model_name], 'feature_importances_'):
            return self.models[model_name].feature_importances_
        else:
            # Return mock importance scores
            return np.array([0.4, 0.3, 0.15, 0.1, 0.05])  # Mock importance
    
    def save_models(self, directory='models'):
        """Save trained models to disk"""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        for model_name, model in self.models.items():
            filename = os.path.join(directory, f'{model_name}_model.pkl')
            joblib.dump(model, filename)
        
        # Save scalers
        for scaler_name, scaler in self.scalers.items():
            filename = os.path.join(directory, f'{scaler_name}_scaler.pkl')
            joblib.dump(scaler, filename)
    
    def load_models(self, directory='models'):
        """Load models from disk"""
        model_names = ['linear_regression', 'random_forest', 'neural_network']
        
        for model_name in model_names:
            model_file = os.path.join(directory, f'{model_name}_model.pkl')
            scaler_file = os.path.join(directory, f'{model_name}_scaler.pkl')
            
            if os.path.exists(model_file):
                self.models[model_name] = joblib.load(model_file)
                
                if os.path.exists(scaler_file):
                    self.scalers[model_name] = joblib.load(scaler_file)
        
        if self.models:
            self.is_trained = True
            print(f"Loaded {len(self.models)} models from {directory}")
        else:
            print("No pre-trained models found. Using mock predictions.")
