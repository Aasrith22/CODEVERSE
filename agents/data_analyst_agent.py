from crewai import Agent, Task
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.mock_data_generator import MockDataGenerator
from datetime import datetime
import json

class DataAnalystAgent:
    def __init__(self):
        self.data_generator = MockDataGenerator()
        self.agent = Agent(
            role='Traffic Data Analyst',
            goal='Analyze traffic patterns and identify trends from historical and simulated real-time data',
            backstory='Expert in traffic pattern analysis with ability to identify congestion trends and anomalies. Specializes in understanding urban traffic flow patterns, seasonal variations, and event-based traffic changes.',
            verbose=True,
            allow_delegation=False
        )
    
    def analyze_current_conditions(self, location):
        """Analyze current traffic conditions for a specific location"""
        try:
            # Get real-time simulation data
            current_data = self.data_generator.generate_real_time_simulation()
            
            # Perform comprehensive analysis
            analysis = {
                'timestamp': current_data['timestamp'],
                'location': location,
                'current_density': current_data['traffic_updates'].get(location, {}).get('density', 0.5),
                'trend_analysis': self.analyze_trends(location),
                'anomaly_detection': self.detect_anomalies(location, current_data),
                'peak_hour_prediction': self.predict_peak_hours(location),
                'weather_impact': self.assess_weather_impact(current_data['weather_conditions']),
                'event_impact': self.assess_event_impact(current_data['events'], location),
                'historical_comparison': self.compare_with_historical(location)
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error in data analysis: {str(e)}")
            return self._get_fallback_analysis(location)
    
    def analyze_trends(self, location):
        """Analyze traffic trends for the location"""
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()
        
        # Analyze weekly patterns
        weekly_pattern = self._analyze_weekly_pattern(current_day)
        
        # Analyze hourly patterns
        hourly_pattern = self._analyze_hourly_pattern(current_hour)
        
        # Seasonal trends (simplified)
        seasonal_trend = self._analyze_seasonal_trend()
        
        return {
            'weekly_pattern': weekly_pattern,
            'hourly_pattern': hourly_pattern,
            'seasonal_trend': seasonal_trend,
            'growth_rate': f"+{5 + (hash(location) % 10)}% compared to last month",
            'confidence_score': 0.85
        }
    
    def _analyze_weekly_pattern(self, current_day):
        """Analyze weekly traffic patterns"""
        if current_day < 5:  # Weekday
            return "High traffic on weekdays 8-10 AM and 6-8 PM due to office commutes"
        else:  # Weekend
            return "Moderate traffic on weekends with peaks during shopping hours 11 AM-2 PM"
    
    def _analyze_hourly_pattern(self, current_hour):
        """Analyze hourly traffic patterns"""
        if current_hour in [8, 9]:
            return "Morning rush hour - peak traffic expected"
        elif current_hour in [17, 18, 19]:
            return "Evening rush hour - heavy traffic anticipated"
        elif current_hour in [12, 13]:
            return "Lunch hour - moderate traffic increase"
        elif 22 <= current_hour or current_hour <= 5:
            return "Night hours - minimal traffic expected"
        else:
            return "Normal traffic flow expected"
    
    def _analyze_seasonal_trend(self):
        """Analyze seasonal traffic trends"""
        current_month = datetime.now().month
        
        if current_month in [6, 7, 8, 9]:  # Monsoon months
            return "Monsoon season - traffic increases due to weather conditions and slower movement"
        elif current_month in [11, 12, 1]:  # Festival season
            return "Festival season - increased traffic due to shopping and celebrations"
        else:
            return "Normal seasonal traffic patterns"
    
    def detect_anomalies(self, location, current_data):
        """Detect traffic anomalies"""
        location_traffic = current_data['traffic_updates'].get(location, {})
        current_density = location_traffic.get('density', 0.5)
        
        # Simple anomaly detection logic
        anomalies = []
        
        # Check for unusual density
        if current_density > 0.8:
            anomalies.append("Unusually high traffic density detected")
        
        # Check for rapid changes
        trend = location_traffic.get('trend', 'stable')
        if trend == 'increasing' and current_density > 0.6:
            anomalies.append("Rapid traffic increase detected")
        
        # Check event correlations
        event_correlations = []
        for event in current_data.get('events', []):
            if event['location'] == location or event['location'] == 'all':
                event_correlations.append(f"{event['name']} affecting {location}")
        
        return {
            'current_anomaly': len(anomalies) > 0,
            'anomaly_details': anomalies,
            'event_correlations': event_correlations,
            'severity': 'high' if len(anomalies) > 1 else 'medium' if anomalies else 'low'
        }
    
    def predict_peak_hours(self, location):
        """Predict peak traffic hours"""
        current_hour = datetime.now().hour
        
        # Define peak hours based on location characteristics
        location_peak_patterns = {
            'Madhapur': {'morning': [8, 9, 10], 'evening': [17, 18, 19, 20]},  # IT hub
            'Ameerpet': {'morning': [8, 9], 'evening': [17, 18, 19]},  # Commercial
            'Kukatpally': {'morning': [8, 9], 'evening': [17, 18, 19]},  # Residential + commercial
            'Secunderabad': {'morning': [8, 9], 'evening': [17, 18, 19]},  # Railway hub
            'Miyapur': {'morning': [8, 9], 'evening': [17, 18, 19]},  # Metro terminus
            'Bowenpally': {'morning': [8, 9], 'evening': [17, 18]}  # Residential
        }
        
        peak_hours = location_peak_patterns.get(location, {
            'morning': [8, 9], 'evening': [17, 18, 19]
        })
        
        # Predict next peak
        all_peaks = peak_hours['morning'] + peak_hours['evening']
        next_peaks = [h for h in all_peaks if h > current_hour]
        
        if not next_peaks:
            next_peaks = peak_hours['morning']  # Next day morning
        
        return {
            'next_peak_hour': min(next_peaks),
            'peak_periods': peak_hours,
            'current_status': 'peak' if current_hour in all_peaks else 'normal',
            'time_to_next_peak': min(next_peaks) - current_hour if next_peaks else 24 - current_hour + min(peak_hours['morning'])
        }
    
    def assess_weather_impact(self, weather_conditions):
        """Assess weather impact on traffic"""
        condition = weather_conditions.get('condition', 'Very Sunny')
        impact_factor = weather_conditions.get('impact_factor', 0.1)
        
        impact_descriptions = {
            'Very Sunny': 'Minimal weather impact on traffic flow',
            'Very Cold': 'Slight increase in traffic due to reduced walking/cycling',
            'Rain': 'Moderate traffic impact - slower speeds and increased congestion',
            'Stormy': 'Significant traffic disruption expected - heavy delays possible'
        }
        
        return {
            'condition': condition,
            'impact_factor': impact_factor,
            'description': impact_descriptions.get(condition, 'Unknown weather impact'),
            'recommendations': self._get_weather_recommendations(condition)
        }
    
    def _get_weather_recommendations(self, condition):
        """Get weather-based traffic recommendations"""
        recommendations = {
            'Very Sunny': ['Normal driving conditions', 'Stay hydrated during travel'],
            'Very Cold': ['Allow extra time for vehicle warm-up', 'Drive carefully on potentially icy roads'],
            'Rain': ['Reduce speed', 'Maintain safe following distance', 'Use headlights'],
            'Stormy': ['Avoid unnecessary travel', 'Check weather updates', 'Use alternative transportation if possible']
        }
        return recommendations.get(condition, ['Drive with caution'])
    
    def assess_event_impact(self, events, location):
        """Assess impact of events on traffic"""
        relevant_events = []
        total_impact = 0
        
        for event in events:
            if event['location'] == location or event['location'] == 'all':
                relevant_events.append(event)
                total_impact += event.get('traffic_impact', 0)
        
        return {
            'active_events': relevant_events,
            'total_impact_score': min(total_impact, 1.0),  # Cap at 1.0
            'event_count': len(relevant_events),
            'severity': 'high' if total_impact > 0.5 else 'medium' if total_impact > 0.2 else 'low'
        }
    
    def compare_with_historical(self, location):
        """Compare current conditions with historical data"""
        # Simulate historical comparison
        base_density = self.data_generator.base_traffic_patterns.get(location, 0.4)
        
        return {
            'historical_average': base_density,
            'current_vs_average': 'above average' if base_density > 0.5 else 'below average',
            'percentage_difference': f"{((base_density - 0.4) / 0.4 * 100):+.1f}%",
            'trend_direction': 'increasing' if base_density > 0.45 else 'stable'
        }
    
    def _get_fallback_analysis(self, location):
        """Provide fallback analysis if main analysis fails"""
        return {
            'timestamp': datetime.now().isoformat(),
            'location': location,
            'current_density': 0.5,
            'trend_analysis': {
                'weekly_pattern': 'Normal weekday traffic patterns',
                'hourly_pattern': 'Standard hourly variations',
                'seasonal_trend': 'Typical seasonal patterns',
                'growth_rate': '+3% compared to last month',
                'confidence_score': 0.7
            },
            'anomaly_detection': {
                'current_anomaly': False,
                'anomaly_details': [],
                'event_correlations': [],
                'severity': 'low'
            },
            'peak_hour_prediction': {
                'next_peak_hour': 17,
                'peak_periods': {'morning': [8, 9], 'evening': [17, 18, 19]},
                'current_status': 'normal',
                'time_to_next_peak': 5
            },
            'weather_impact': {
                'condition': 'Very Sunny',
                'impact_factor': 0.1,
                'description': 'Minimal weather impact on traffic flow',
                'recommendations': ['Normal driving conditions']
            },
            'event_impact': {
                'active_events': [],
                'total_impact_score': 0.0,
                'event_count': 0,
                'severity': 'low'
            },
            'historical_comparison': {
                'historical_average': 0.4,
                'current_vs_average': 'average',
                'percentage_difference': '+0.0%',
                'trend_direction': 'stable'
            }
        }
