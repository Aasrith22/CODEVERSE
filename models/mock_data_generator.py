import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

class MockDataGenerator:
    def __init__(self):
        self.locations = ['Ameerpet', 'Kukatpally', 'Madhapur', 'Bowenpally', 'Miyapur', 'Secunderabad']
        self.weather_conditions = ['Very Cold', 'Very Sunny', 'Rain', 'Stormy']
        self.vehicle_types = ['Heavy vehicles', 'Two-Wheeler', 'Three-Wheeler', 'Four-Wheeler']
        
        # Traffic patterns for realistic simulation
        self.rush_hours = [8, 9, 17, 18, 19]
        self.lunch_hours = [12, 13]
        self.base_traffic_patterns = {
            'Ameerpet': 0.4,
            'Kukatpally': 0.5,
            'Madhapur': 0.6,  # IT hub - higher traffic
            'Bowenpally': 0.3,
            'Miyapur': 0.4,
            'Secunderabad': 0.5
        }
    
    def generate_historical_data(self, days=365):
        """Generate synthetic historical traffic data"""
        data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            day_of_week = current_date.weekday()
            
            for hour in range(24):
                for location in self.locations:
                    # Base traffic level for location
                    base_density = self.base_traffic_patterns[location]
                    
                    # Time-based modifications
                    if hour in self.rush_hours:
                        traffic_multiplier = 1.5 if day_of_week < 5 else 1.2  # Weekday vs weekend
                    elif hour in self.lunch_hours:
                        traffic_multiplier = 1.3
                    elif 22 <= hour or hour <= 5:  # Night hours
                        traffic_multiplier = 0.3
                    else:
                        traffic_multiplier = 1.0
                    
                    # Weather impact
                    weather = random.choice(self.weather_conditions)
                    weather_impact = {
                        'Very Sunny': 0.1,
                        'Very Cold': 0.15,
                        'Rain': 0.4,
                        'Stormy': 0.6
                    }[weather]
                    
                    # Random events
                    random_event = random.random() < 0.1  # 10% chance
                    event_impact = 0.3 if random_event else 0
                    
                    # Calculate final density
                    density = base_density * traffic_multiplier
                    density += weather_impact + event_impact
                    density += random.gauss(0, 0.1)  # Add noise
                    density = max(0, min(1, density))  # Clamp between 0 and 1
                    
                    data.append({
                        'timestamp': current_date + timedelta(hours=hour),
                        'location': location,
                        'density': density,
                        'weather': weather,
                        'day_of_week': day_of_week,
                        'hour': hour,
                        'is_peak_hour': int(hour in self.rush_hours),
                        'random_event': int(random_event),
                        'vehicle_type': random.choice(self.vehicle_types)
                    })
        
        return pd.DataFrame(data)
    
    def generate_real_time_simulation(self):
        """Simulate real-time data updates"""
        current_time = datetime.now()
        hour = current_time.hour
        day_of_week = current_time.weekday()
        
        simulated_data = {
            'timestamp': current_time.isoformat(),
            'traffic_updates': self.simulate_current_traffic(hour, day_of_week),
            'weather_conditions': self.simulate_weather(),
            'events': self.simulate_events(hour)
        }
        return simulated_data
    
    def simulate_current_traffic(self, hour, day_of_week):
        """Generate current traffic for all locations"""
        traffic_data = {}
        
        for location in self.locations:
            base_density = self.base_traffic_patterns[location]
            
            # Time-based modifications
            if hour in self.rush_hours:
                multiplier = 1.5 if day_of_week < 5 else 1.2
            elif hour in self.lunch_hours:
                multiplier = 1.3
            elif 22 <= hour or hour <= 5:
                multiplier = 0.3
            else:
                multiplier = 1.0
            
            density = base_density * multiplier
            density += random.gauss(0, 0.1)  # Add noise
            density = max(0, min(1, density))
            
            # Determine trend
            trends = ['increasing', 'decreasing', 'stable']
            weights = [0.3, 0.3, 0.4]  # Stable is most common
            
            traffic_data[location] = {
                'density': density,
                'trend': random.choices(trends, weights=weights)[0],
                'confidence': random.uniform(0.75, 0.95)
            }
        
        return traffic_data
    
    def simulate_weather(self):
        """Simulate current weather conditions"""
        condition = random.choice(self.weather_conditions)
        
        weather_data = {
            'condition': condition,
            'temperature': random.randint(18, 40),
            'humidity': random.randint(40, 90),
            'visibility': random.choice(['Good', 'Moderate', 'Poor']),
            'impact_factor': {
                'Very Sunny': 0.1,
                'Very Cold': 0.15,
                'Rain': 0.4,
                'Stormy': 0.6
            }[condition]
        }
        
        return weather_data
    
    def simulate_events(self, hour):
        """Simulate current events affecting traffic"""
        events = []
        
        # Rush hour events
        if hour in self.rush_hours:
            events.append({
                'name': 'Rush Hour Traffic',
                'location': 'all',
                'impact_radius': 5,
                'traffic_impact': 0.3,
                'start_time': f"{hour:02d}:00",
                'end_time': f"{hour+1:02d}:00"
            })
        
        # Random events
        if random.random() < 0.15:  # 15% chance of random event
            event_types = [
                {'name': 'Road Construction', 'impact': 0.4},
                {'name': 'Accident', 'impact': 0.5},
                {'name': 'Festival/Event', 'impact': 0.3},
                {'name': 'VIP Movement', 'impact': 0.6}
            ]
            
            event = random.choice(event_types)
            events.append({
                'name': event['name'],
                'location': random.choice(self.locations),
                'impact_radius': random.randint(1, 3),
                'traffic_impact': event['impact'],
                'start_time': f"{hour:02d}:00",
                'end_time': f"{hour+2:02d}:00"
            })
        
        return events
    
    def get_location_coordinates(self, location):
        """Get coordinates for map display"""
        coordinates = {
            'Kukatpally': {'lat': 17.493338, 'lng': 78.402547},
            'Ameerpet': {'lat': 17.434275, 'lng': 78.445403},
            'Miyapur': {'lat': 17.496653, 'lng': 78.361809},
            'Bowenpally': {'lat': 17.463865, 'lng': 78.472837},
            'Secunderabad': {'lat': 17.434962, 'lng': 78.500812},
            'Madhapur': {'lat': 17.451399, 'lng': 78.381218}
        }
        return coordinates.get(location, {'lat': 17.4435, 'lng': 78.4484})  # Default to Hyderabad center
