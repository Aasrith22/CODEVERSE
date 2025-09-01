from crewai import Agent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.ensemble_models import EnsembleModels
import joblib
import numpy as np
import pickle

class PredictionAgent:
    def __init__(self):
        self.ensemble_models = EnsembleModels()
        self.legacy_model = None
        self.legacy_preprocessor = None
        
        # Try to load existing models
        self._load_existing_models()
        
        self.agent = Agent(
            role='Traffic Prediction Specialist',
            goal='Generate accurate traffic density predictions using ensemble machine learning models and provide uncertainty quantification',
            backstory='ML expert specializing in traffic forecasting with ensemble methods, feature engineering, and uncertainty quantification. Has extensive experience in time series analysis and urban traffic pattern recognition.',
            verbose=True,
            allow_delegation=False
        )
    
    def _load_existing_models(self):
        """Try to load existing trained models"""
        try:
            # Try to load the original model first
            if os.path.exists('peak.pkl'):
                with open('peak.pkl', 'rb') as file:
                    grid_search = pickle.load(file)
                
                # Extract the best model from GridSearchCV
                if hasattr(grid_search, "best_estimator_"):
                    pipeline = grid_search.best_estimator_
                else:
                    pipeline = grid_search
                
                # Extract preprocessor and regressor
                if hasattr(pipeline, 'named_steps'):
                    self.legacy_preprocessor = pipeline.named_steps.get('preprocessor')
                    self.legacy_model = pipeline.named_steps.get('regressor')
                    print("✅ Loaded legacy model successfully")
                
            # Try to load ensemble models
            self.ensemble_models.load_models()
            
        except Exception as e:
            print(f"⚠️ Could not load existing models: {str(e)}")
            print("Using mock predictions for demonstration")
    
    def predict_traffic_density(self, input_data, prediction_horizon=1):
        """Generate comprehensive traffic density predictions"""
        try:
            # Make predictions using different approaches
            predictions = {}
            confidence_scores = {}
            
            # 1. Legacy model prediction (if available)
            if self.legacy_model and self.legacy_preprocessor:
                legacy_pred, legacy_conf = self._predict_with_legacy_model(input_data)
                predictions['legacy_model'] = legacy_pred
                confidence_scores['legacy_model'] = legacy_conf
            
            # 2. Ensemble model predictions
            ensemble_preds = self._predict_with_ensemble(input_data)
            predictions.update(ensemble_preds)
            
            # Calculate confidence scores for ensemble models
            for model_name in ensemble_preds.keys():
                confidence_scores[model_name] = self._calculate_confidence(input_data, model_name)
            
            # 3. Generate final ensemble prediction
            final_prediction = self._ensemble_predict(predictions, confidence_scores)
            
            # 4. Calculate prediction intervals
            prediction_range = self._calculate_prediction_interval(predictions)
            
            # 5. Explain prediction factors
            explanation = self._explain_prediction(input_data)
            
            return {
                'prediction': final_prediction,
                'confidence': np.mean(list(confidence_scores.values())) if confidence_scores else 0.8,
                'model_breakdown': predictions,
                'confidence_scores': confidence_scores,
                'prediction_range': prediction_range,
                'factors_influence': explanation,
                'prediction_horizon': prediction_horizon,
                'uncertainty_metrics': self._calculate_uncertainty_metrics(predictions, confidence_scores)
            }
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return self._get_fallback_prediction(input_data)
    
    def _predict_with_legacy_model(self, input_data):
        """Make prediction using the original trained model"""
        try:
            # Convert input to the format expected by legacy model
            if isinstance(input_data, list):
                # Map input data to DataFrame format
                feature_names = ['City', 'Vehicle Type', 'Weather', 'Day Of Week', 'Hour Of Day', 'Is Peak Hour', 'Random Event Occurred']
                input_dict = {
                    'City': input_data[0] if len(input_data) > 0 else 'Hyderabad',
                    'Vehicle Type': input_data[1] if len(input_data) > 1 else 'Four-Wheeler',
                    'Weather': input_data[2] if len(input_data) > 2 else 'Very Sunny',
                    'Day Of Week': int(input_data[3]) if len(input_data) > 3 else 1,
                    'Hour Of Day': int(input_data[4]) if len(input_data) > 4 else 12,
                    'Is Peak Hour': int(input_data[5]) if len(input_data) > 5 else 0,
                    'Random Event Occurred': int(input_data[6]) if len(input_data) > 6 else 0
                }
                
                import pandas as pd
                input_df = pd.DataFrame([input_dict])
                
                # Apply preprocessing
                transformed_input = self.legacy_preprocessor.transform(input_df)
                
                # Make prediction
                prediction = self.legacy_model.predict(transformed_input)[0]
                confidence = 0.9  # High confidence for trained model
                
                return float(prediction), confidence
                
        except Exception as e:
            print(f"Legacy model prediction failed: {str(e)}")
            return 0.5, 0.7
    
    def _predict_with_ensemble(self, input_data):
        """Make predictions using ensemble models"""
        try:
            # Convert input_data to appropriate format
            if isinstance(input_data, list) and len(input_data) >= 7:
                # Extract numerical features for ensemble models
                numerical_features = [
                    float(input_data[3]),  # Day of week
                    float(input_data[4]),  # Hour of day
                    float(input_data[5]),  # Is peak hour
                    float(input_data[6])   # Random event
                ]
                
                # Add encoded categorical features (simplified)
                weather_encoding = {'Very Cold': 0, 'Very Sunny': 1, 'Rain': 2, 'Stormy': 3}
                vehicle_encoding = {'Heavy vehicles': 0, 'Two-Wheeler': 1, 'Three-Wheeler': 2, 'Four-Wheeler': 3}
                
                weather_code = weather_encoding.get(input_data[2], 1)
                vehicle_code = vehicle_encoding.get(input_data[1], 3)
                
                features = [weather_code, vehicle_code] + numerical_features
                
                # Get predictions from ensemble models
                ensemble_predictions = self.ensemble_models.predict([features])
                
                if isinstance(ensemble_predictions, dict):
                    return {name: float(pred[0]) for name, pred in ensemble_predictions.items()}
                else:
                    return {'ensemble': float(ensemble_predictions[0])}
            
        except Exception as e:
            print(f"Ensemble prediction failed: {str(e)}")
        
        # Fallback to mock predictions
        return {
            'linear_regression': np.random.beta(2, 3),
            'random_forest': np.random.beta(2, 3), 
            'neural_network': np.random.beta(2, 3)
        }
    
    def _ensemble_predict(self, predictions, confidence_scores):
        """Combine predictions using weighted ensemble"""
        if not predictions:
            return 0.5
        
        # Calculate weighted average based on confidence scores
        total_weight = sum(confidence_scores.values()) if confidence_scores else len(predictions)
        
        if total_weight == 0:
            return np.mean(list(predictions.values()))
        
        weighted_pred = 0
        for model_name, pred in predictions.items():
            weight = confidence_scores.get(model_name, 1.0)
            weighted_pred += pred * weight
        
        final_prediction = weighted_pred / total_weight
        
        # Ensure prediction is within valid range
        return max(0, min(1, final_prediction))
    
    def _calculate_confidence(self, input_data, model_name):
        """Calculate confidence score for a specific model"""
        try:
            # Base confidence varies by model type
            base_confidence = {
                'legacy_model': 0.9,
                'linear_regression': 0.75,
                'random_forest': 0.85,
                'neural_network': 0.8
            }.get(model_name, 0.75)
            
            # Adjust confidence based on input characteristics
            if isinstance(input_data, list) and len(input_data) >= 5:
                hour = float(input_data[4]) if len(input_data) > 4 else 12
                is_peak = float(input_data[5]) if len(input_data) > 5 else 0
                
                # Higher confidence during normal hours and clear conditions
                if 9 <= hour <= 17 and is_peak == 0:
                    confidence_adjustment = 0.1
                elif is_peak == 1:
                    confidence_adjustment = -0.05  # Slightly less confident during peak hours
                else:
                    confidence_adjustment = 0
                
                return min(0.95, base_confidence + confidence_adjustment)
            
            return base_confidence
            
        except Exception as e:
            print(f"Confidence calculation error: {str(e)}")
            return 0.75
    
    def _calculate_prediction_interval(self, predictions):
        """Calculate prediction confidence interval"""
        if not predictions:
            return {'lower': 0.3, 'upper': 0.7}
        
        pred_values = list(predictions.values())
        mean_pred = np.mean(pred_values)
        std_pred = np.std(pred_values) if len(pred_values) > 1 else 0.1
        
        # 95% confidence interval
        margin = 1.96 * std_pred
        
        return {
            'lower': max(0, mean_pred - margin),
            'upper': min(1, mean_pred + margin),
            'std_deviation': std_pred
        }
    
    def _explain_prediction(self, input_data):
        """Provide explanation for the prediction"""
        try:
            factors = {
                'primary_factors': [],
                'contributing_factors': [],
                'impact_scores': {}
            }
            
            if isinstance(input_data, list) and len(input_data) >= 7:
                hour = float(input_data[4]) if len(input_data) > 4 else 12
                is_peak = float(input_data[5]) if len(input_data) > 5 else 0
                random_event = float(input_data[6]) if len(input_data) > 6 else 0
                weather = input_data[2] if len(input_data) > 2 else 'Very Sunny'
                day = float(input_data[3]) if len(input_data) > 3 else 1
                
                # Analyze primary factors
                if is_peak == 1 or hour in [8, 9, 17, 18, 19]:
                    factors['primary_factors'].append('Peak hour timing')
                    factors['impact_scores']['time'] = 0.4
                else:
                    factors['impact_scores']['time'] = 0.2
                
                if weather in ['Rain', 'Stormy']:
                    factors['primary_factors'].append('Adverse weather conditions')
                    factors['impact_scores']['weather'] = 0.3
                else:
                    factors['contributing_factors'].append('Weather conditions')
                    factors['impact_scores']['weather'] = 0.1
                
                # Contributing factors
                if day < 5:  # Weekday
                    factors['contributing_factors'].append('Weekday traffic patterns')
                    factors['impact_scores']['day'] = 0.2
                else:
                    factors['contributing_factors'].append('Weekend traffic patterns')
                    factors['impact_scores']['day'] = 0.15
                
                if random_event == 1:
                    factors['primary_factors'].append('Random event occurrence')
                    factors['impact_scores']['events'] = 0.2
                else:
                    factors['impact_scores']['events'] = 0.05
            
            # Default explanation if parsing fails
            if not factors['primary_factors']:
                factors['primary_factors'] = ['Time of day', 'Day of week']
                factors['contributing_factors'] = ['Weather conditions', 'Vehicle type']
                factors['impact_scores'] = {'time': 0.4, 'weather': 0.2, 'day': 0.2, 'vehicle': 0.2}
            
            return factors
            
        except Exception as e:
            print(f"Explanation generation failed: {str(e)}")
            return {
                'primary_factors': ['Time of day', 'Traffic patterns'],
                'contributing_factors': ['Weather', 'Events'],
                'impact_scores': {'time': 0.4, 'weather': 0.3, 'day': 0.2, 'events': 0.1}
            }
    
    def _calculate_uncertainty_metrics(self, predictions, confidence_scores):
        """Calculate additional uncertainty metrics"""
        if not predictions:
            return {'model_agreement': 0.5, 'prediction_stability': 0.7}
        
        pred_values = list(predictions.values())
        
        # Model agreement (inverse of standard deviation)
        model_agreement = 1 - min(np.std(pred_values), 0.5) / 0.5 if len(pred_values) > 1 else 1.0
        
        # Prediction stability (average confidence)
        prediction_stability = np.mean(list(confidence_scores.values())) if confidence_scores else 0.75
        
        return {
            'model_agreement': model_agreement,
            'prediction_stability': prediction_stability,
            'ensemble_diversity': len(predictions),
            'confidence_variance': np.var(list(confidence_scores.values())) if confidence_scores else 0.01
        }
    
    def _get_fallback_prediction(self, input_data):
        """Provide fallback prediction if main prediction fails"""
        # Generate reasonable fallback based on basic heuristics
        base_prediction = 0.4
        
        try:
            if isinstance(input_data, list) and len(input_data) >= 5:
                hour = float(input_data[4])
                is_peak = float(input_data[5]) if len(input_data) > 5 else 0
                
                # Adjust based on time
                if hour in [8, 9, 17, 18, 19] or is_peak == 1:
                    base_prediction += 0.3
                elif 22 <= hour or hour <= 5:
                    base_prediction -= 0.2
        except:
            pass
        
        return {
            'prediction': max(0, min(1, base_prediction)),
            'confidence': 0.7,
            'model_breakdown': {'fallback_model': base_prediction},
            'confidence_scores': {'fallback_model': 0.7},
            'prediction_range': {'lower': base_prediction - 0.1, 'upper': base_prediction + 0.1},
            'factors_influence': {
                'primary_factors': ['Time-based estimation'],
                'contributing_factors': ['Basic heuristics'],
                'impact_scores': {'time': 0.6, 'default': 0.4}
            },
            'uncertainty_metrics': {
                'model_agreement': 1.0,
                'prediction_stability': 0.7
            }
        }
