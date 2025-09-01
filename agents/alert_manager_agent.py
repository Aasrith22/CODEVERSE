from crewai import Agent
from datetime import datetime, timedelta
import random

class AlertManagerAgent:
    def __init__(self):
        self.alert_thresholds = {
            'high_traffic': 0.7,
            'medium_traffic': 0.4,
            'traffic_spike': 0.3,  # Sudden increase threshold
            'weather_impact': 0.3,
            'event_impact': 0.2
        }
        
        self.alert_history = []  # Track recent alerts to avoid spam
        
        self.agent = Agent(
            role='Traffic Alert Coordinator',
            goal='Monitor traffic levels, generate timely alerts, and provide proactive notifications with actionable recommendations for optimal user experience',
            backstory='Alert management specialist with expertise in real-time monitoring, predictive alerting, and user experience optimization. Experienced in traffic incident management and emergency response coordination.',
            verbose=True,
            allow_delegation=False
        )
    
    def generate_alerts(self, current_predictions, historical_data, user_preferences=None):
        """Generate comprehensive alerts based on current conditions"""
        try:
            alerts = []
            
            # Set default preferences
            if user_preferences is None:
                user_preferences = {
                    'alert_sensitivity': 'medium',  # low, medium, high
                    'preferred_routes': [],
                    'commute_times': ['08:00', '17:00'],
                    'vehicle_type': 'Four-Wheeler'
                }
            
            # 1. Traffic density alerts
            traffic_alerts = self._generate_traffic_alerts(current_predictions, user_preferences)
            alerts.extend(traffic_alerts)
            
            # 2. Weather-based alerts
            weather_alerts = self._generate_weather_alerts(historical_data)
            alerts.extend(weather_alerts)
            
            # 3. Event-based alerts
            event_alerts = self._generate_event_alerts()
            alerts.extend(event_alerts)
            
            # 4. Predictive alerts
            predictive_alerts = self._generate_predictive_alerts(current_predictions)
            alerts.extend(predictive_alerts)
            
            # 5. Route optimization alerts
            route_alerts = self._generate_route_alerts(current_predictions, user_preferences)
            alerts.extend(route_alerts)
            
            # Filter and prioritize alerts
            filtered_alerts = self._filter_and_prioritize_alerts(alerts, user_preferences)
            
            # Generate summary and recommendations
            alert_summary = self._create_alert_summary(filtered_alerts)
            recommendations = self._generate_recommendations(filtered_alerts, current_predictions)
            
            return {
                'active_alerts': filtered_alerts,
                'alert_summary': alert_summary,
                'recommendations': recommendations,
                'alert_statistics': self._calculate_alert_statistics(filtered_alerts),
                'next_update': self._calculate_next_update_time()
            }
            
        except Exception as e:
            print(f"Alert generation error: {str(e)}")
            return self._get_fallback_alerts()
    
    def _generate_traffic_alerts(self, predictions, preferences):
        """Generate alerts based on traffic density predictions"""
        alerts = []
        sensitivity = preferences.get('alert_sensitivity', 'medium')
        
        # Adjust thresholds based on sensitivity
        threshold_adjustments = {
            'low': 0.1,
            'medium': 0.0,
            'high': -0.1
        }
        adjustment = threshold_adjustments.get(sensitivity, 0.0)
        
        for location, prediction_data in predictions.items():
            if isinstance(prediction_data, dict):
                density = prediction_data.get('prediction', 0.5)
                confidence = prediction_data.get('confidence', 0.8)
            else:
                density = prediction_data
                confidence = 0.8
            
            # High traffic alert
            if density > (self.alert_thresholds['high_traffic'] + adjustment):
                severity = 'critical' if density > 0.9 else 'warning'
                alerts.append({
                    'id': f"traffic_high_{location}_{int(datetime.now().timestamp())}",
                    'type': 'high_traffic',
                    'severity': severity,
                    'location': location,
                    'title': f'Heavy Traffic Alert - {location}',
                    'message': f'Heavy traffic expected in {location}. Current prediction: {density:.1%}',
                    'density': density,
                    'confidence': confidence,
                    'eta_impact': self._calculate_eta_impact(density),
                    'suggestions': self._get_traffic_suggestions(location, density),
                    'timestamp': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(hours=2)).isoformat(),
                    'priority': self._calculate_priority('high_traffic', density, confidence)
                })
            
            # Medium traffic alert (for high sensitivity users)
            elif density > (self.alert_thresholds['medium_traffic'] + adjustment) and sensitivity == 'high':
                alerts.append({
                    'id': f"traffic_medium_{location}_{int(datetime.now().timestamp())}",
                    'type': 'medium_traffic',
                    'severity': 'info',
                    'location': location,
                    'title': f'Moderate Traffic - {location}',
                    'message': f'Moderate traffic levels in {location}. Plan accordingly.',
                    'density': density,
                    'confidence': confidence,
                    'eta_impact': self._calculate_eta_impact(density),
                    'suggestions': self._get_traffic_suggestions(location, density),
                    'timestamp': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(hours=1)).isoformat(),
                    'priority': self._calculate_priority('medium_traffic', density, confidence)
                })
        
        return alerts
    
    def _generate_weather_alerts(self, historical_data):
        """Generate weather-related traffic alerts"""
        alerts = []
        
        # Simulate current weather conditions
        weather_conditions = ['Very Sunny', 'Very Cold', 'Rain', 'Stormy']
        current_weather = random.choice(weather_conditions)
        
        weather_impacts = {
            'Very Sunny': {'impact': 0.1, 'message': 'Clear weather conditions'},
            'Very Cold': {'impact': 0.15, 'message': 'Cold weather may affect traffic flow'},
            'Rain': {'impact': 0.4, 'message': 'Rainy conditions causing traffic delays'},
            'Stormy': {'impact': 0.6, 'message': 'Severe weather causing significant traffic disruption'}
        }
        
        weather_info = weather_impacts.get(current_weather, weather_impacts['Very Sunny'])
        
        if weather_info['impact'] > self.alert_thresholds['weather_impact']:
            severity = 'warning' if weather_info['impact'] > 0.5 else 'info'
            alerts.append({
                'id': f"weather_{current_weather.lower().replace(' ', '_')}_{int(datetime.now().timestamp())}",
                'type': 'weather_impact',
                'severity': severity,
                'location': 'all',
                'title': f'Weather Alert - {current_weather}',
                'message': weather_info['message'],
                'weather_condition': current_weather,
                'impact_factor': weather_info['impact'],
                'suggestions': self._get_weather_suggestions(current_weather),
                'timestamp': datetime.now().isoformat(),
                'expires_at': (datetime.now() + timedelta(hours=4)).isoformat(),
                'priority': self._calculate_priority('weather', weather_info['impact'], 0.9)
            })
        
        return alerts
    
    def _generate_event_alerts(self):
        """Generate event-based alerts"""
        alerts = []
        current_time = datetime.now()
        current_hour = current_time.hour
        current_day = current_time.weekday()
        
        # Rush hour alerts
        if current_hour in [8, 9, 17, 18, 19] and current_day < 5:
            alerts.append({
                'id': f"rush_hour_{current_hour}_{current_day}",
                'type': 'rush_hour',
                'severity': 'info',
                'location': 'all',
                'title': 'Rush Hour Traffic',
                'message': 'Rush hour traffic expected across all major routes',
                'duration_estimate': '1-2 hours',
                'suggestions': [
                    'Allow extra travel time',
                    'Consider using public transportation',
                    'Avoid major junctions if possible'
                ],
                'timestamp': current_time.isoformat(),
                'expires_at': (current_time + timedelta(hours=2)).isoformat(),
                'priority': 3
            })
        
        # Weekend traffic patterns
        if current_day >= 5 and 11 <= current_hour <= 14:
            alerts.append({
                'id': f"weekend_shopping_{current_hour}_{current_day}",
                'type': 'weekend_traffic',
                'severity': 'info',
                'location': 'Kukatpally',
                'title': 'Weekend Shopping Traffic',
                'message': 'Increased traffic near shopping areas during weekend hours',
                'duration_estimate': '2-3 hours',
                'suggestions': [
                    'Expect delays near malls and shopping centers',
                    'Consider alternative routes',
                    'Plan shopping trips for off-peak hours'
                ],
                'timestamp': current_time.isoformat(),
                'expires_at': (current_time + timedelta(hours=3)).isoformat(),
                'priority': 2
            })
        
        # Random events simulation
        if random.random() < 0.15:  # 15% chance of random event
            event_types = [
                {
                    'name': 'Road Construction',
                    'impact': 0.4,
                    'location': random.choice(['Ameerpet', 'Madhapur', 'Kukatpally']),
                    'duration': '3-4 hours'
                },
                {
                    'name': 'Traffic Accident',
                    'impact': 0.5,
                    'location': random.choice(['Secunderabad', 'Bowenpally', 'Miyapur']),
                    'duration': '1-2 hours'
                },
                {
                    'name': 'Cultural Event',
                    'impact': 0.3,
                    'location': random.choice(['Ameerpet', 'Secunderabad']),
                    'duration': '4-6 hours'
                }
            ]
            
            event = random.choice(event_types)
            alerts.append({
                'id': f"event_{event['name'].lower().replace(' ', '_')}_{int(current_time.timestamp())}",
                'type': 'random_event',
                'severity': 'warning' if event['impact'] > 0.4 else 'info',
                'location': event['location'],
                'title': f"{event['name']} - {event['location']}",
                'message': f"{event['name']} reported in {event['location']} area",
                'impact_factor': event['impact'],
                'duration_estimate': event['duration'],
                'suggestions': [
                    f"Avoid {event['location']} area if possible",
                    "Use alternative routes",
                    "Allow extra travel time"
                ],
                'timestamp': current_time.isoformat(),
                'expires_at': (current_time + timedelta(hours=6)).isoformat(),
                'priority': self._calculate_priority('event', event['impact'], 0.8)
            })
        
        return alerts
    
    def _generate_predictive_alerts(self, predictions):
        """Generate predictive alerts based on trends"""
        alerts = []
        current_hour = datetime.now().hour
        
        # Predict upcoming traffic spikes
        for location, prediction_data in predictions.items():
            if isinstance(prediction_data, dict):
                density = prediction_data.get('prediction', 0.5)
                confidence = prediction_data.get('confidence', 0.8)
            else:
                density = prediction_data
                confidence = 0.8
            
            # Predict if traffic will increase in the next hour
            next_hour_multiplier = 1.0
            if current_hour + 1 in [8, 9, 17, 18, 19]:
                next_hour_multiplier = 1.3
            
            predicted_next_density = min(density * next_hour_multiplier, 1.0)
            
            if predicted_next_density > 0.7 and density < 0.6:
                alerts.append({
                    'id': f"predictive_{location}_{int(datetime.now().timestamp())}",
                    'type': 'traffic_spike_prediction',
                    'severity': 'info',
                    'location': location,
                    'title': f'Traffic Increase Predicted - {location}',
                    'message': f'Traffic expected to increase in {location} within the next hour',
                    'current_density': density,
                    'predicted_density': predicted_next_density,
                    'confidence': confidence,
                    'time_window': '1 hour',
                    'suggestions': [
                        'Consider traveling now to avoid upcoming congestion',
                        'Plan alternative routes',
                        'Monitor traffic updates'
                    ],
                    'timestamp': datetime.now().isoformat(),
                    'expires_at': (datetime.now() + timedelta(hours=1)).isoformat(),
                    'priority': 2
                })
        
        return alerts
    
    def _generate_route_alerts(self, predictions, preferences):
        """Generate route-specific alerts"""
        alerts = []
        preferred_routes = preferences.get('preferred_routes', [])
        
        for route in preferred_routes:
            if route in predictions:
                prediction_data = predictions[route]
                density = prediction_data.get('prediction', 0.5) if isinstance(prediction_data, dict) else prediction_data
                
                if density > 0.6:
                    alerts.append({
                        'id': f"route_alert_{route}_{int(datetime.now().timestamp())}",
                        'type': 'preferred_route_traffic',
                        'severity': 'info',
                        'location': route,
                        'title': f'Your Preferred Route - {route}',
                        'message': f'Higher than usual traffic on your preferred route through {route}',
                        'density': density,
                        'suggestions': [
                            'Consider alternative routes',
                            'Delay travel if possible',
                            'Check route alternatives'
                        ],
                        'timestamp': datetime.now().isoformat(),
                        'expires_at': (datetime.now() + timedelta(hours=2)).isoformat(),
                        'priority': 3
                    })
        
        return alerts
    
    def _calculate_eta_impact(self, density):
        """Calculate ETA impact based on traffic density"""
        if density > 0.8:
            return '+20-35 minutes'
        elif density > 0.6:
            return '+10-20 minutes'
        elif density > 0.4:
            return '+5-10 minutes'
        else:
            return 'Minimal impact'
    
    def _get_traffic_suggestions(self, location, density):
        """Get traffic-specific suggestions"""
        if density > 0.8:
            return [
                'Avoid this area if possible',
                'Use public transportation if available',
                'Delay travel by 30-60 minutes if not urgent',
                'Consider working from home if feasible'
            ]
        elif density > 0.6:
            return [
                'Allow extra 15-20 minutes travel time',
                'Consider alternative routes',
                'Monitor real-time traffic updates',
                'Leave earlier than planned'
            ]
        elif density > 0.4:
            return [
                'Allow extra 5-10 minutes travel time',
                'Normal precautions advised',
                'Monitor traffic conditions'
            ]
        else:
            return ['Normal traffic conditions', 'No special precautions needed']
    
    def _get_weather_suggestions(self, weather_condition):
        """Get weather-specific suggestions"""
        suggestions = {
            'Very Sunny': [
                'Normal driving conditions',
                'Stay hydrated during travel',
                'Use sunglasses for better visibility'
            ],
            'Very Cold': [
                'Allow extra time for vehicle warm-up',
                'Drive carefully on potentially icy roads',
                'Keep emergency supplies in vehicle'
            ],
            'Rain': [
                'Reduce speed and increase following distance',
                'Use headlights even during daytime',
                'Avoid sudden braking or steering',
                'Check tire tread for better grip'
            ],
            'Stormy': [
                'Avoid unnecessary travel if possible',
                'If travel is necessary, drive very slowly',
                'Stay updated with weather alerts',
                'Keep emergency contact numbers handy',
                'Consider public transportation'
            ]
        }
        return suggestions.get(weather_condition, ['Drive with caution'])
    
    def _calculate_priority(self, alert_type, impact_factor, confidence):
        """Calculate alert priority (1-5, higher is more urgent)"""
        base_priorities = {
            'high_traffic': 4,
            'medium_traffic': 2,
            'weather': 3,
            'event': 4,
            'predictive': 2
        }
        
        base_priority = base_priorities.get(alert_type, 3)
        
        # Adjust based on impact and confidence
        if impact_factor > 0.8:
            base_priority += 1
        elif impact_factor < 0.3:
            base_priority -= 1
        
        if confidence > 0.9:
            base_priority += 0.5
        elif confidence < 0.7:
            base_priority -= 0.5
        
        return max(1, min(5, int(base_priority)))
    
    def _filter_and_prioritize_alerts(self, alerts, preferences):
        """Filter duplicate alerts and prioritize by importance"""
        # Remove expired alerts
        current_time = datetime.now()
        active_alerts = []
        
        for alert in alerts:
            try:
                expires_at = datetime.fromisoformat(alert['expires_at'].replace('Z', '+00:00'))
                if expires_at.replace(tzinfo=None) > current_time:
                    active_alerts.append(alert)
            except:
                # If parsing fails, include the alert
                active_alerts.append(alert)
        
        # Remove duplicates based on location and type
        unique_alerts = []
        seen_combinations = set()
        
        for alert in active_alerts:
            key = (alert['type'], alert['location'])
            if key not in seen_combinations:
                seen_combinations.add(key)
                unique_alerts.append(alert)
        
        # Sort by priority (higher first)
        unique_alerts.sort(key=lambda x: x.get('priority', 3), reverse=True)
        
        # Limit number of alerts based on user preference
        sensitivity = preferences.get('alert_sensitivity', 'medium')
        max_alerts = {'low': 3, 'medium': 5, 'high': 8}.get(sensitivity, 5)
        
        return unique_alerts[:max_alerts]
    
    def _create_alert_summary(self, alerts):
        """Create a summary of all active alerts"""
        if not alerts:
            return {
                'total_alerts': 0,
                'severity_breakdown': {'critical': 0, 'warning': 0, 'info': 0},
                'main_concerns': [],
                'overall_status': 'All clear'
            }
        
        severity_count = {'critical': 0, 'warning': 0, 'info': 0}
        alert_types = {}
        
        for alert in alerts:
            severity = alert.get('severity', 'info')
            severity_count[severity] += 1
            
            alert_type = alert.get('type', 'unknown')
            alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
        
        # Determine overall status
        if severity_count['critical'] > 0:
            overall_status = 'Critical conditions detected'
        elif severity_count['warning'] > 2:
            overall_status = 'Multiple traffic concerns'
        elif severity_count['warning'] > 0:
            overall_status = 'Traffic concerns detected'
        else:
            overall_status = 'Normal conditions with minor alerts'
        
        # Identify main concerns
        main_concerns = []
        if alert_types.get('high_traffic', 0) > 0:
            main_concerns.append('Heavy traffic in multiple areas')
        if alert_types.get('weather_impact', 0) > 0:
            main_concerns.append('Weather affecting traffic')
        if alert_types.get('random_event', 0) > 0:
            main_concerns.append('Incidents affecting traffic flow')
        
        return {
            'total_alerts': len(alerts),
            'severity_breakdown': severity_count,
            'alert_type_breakdown': alert_types,
            'main_concerns': main_concerns,
            'overall_status': overall_status
        }
    
    def _generate_recommendations(self, alerts, predictions):
        """Generate actionable recommendations based on alerts"""
        recommendations = {
            'immediate_actions': [],
            'travel_planning': [],
            'route_suggestions': [],
            'timing_advice': []
        }
        
        high_traffic_locations = []
        weather_issues = False
        events_detected = False
        
        # Analyze alerts to generate recommendations
        for alert in alerts:
            if alert['type'] in ['high_traffic', 'medium_traffic']:
                high_traffic_locations.append(alert['location'])
            elif alert['type'] == 'weather_impact':
                weather_issues = True
            elif alert['type'] in ['random_event', 'rush_hour']:
                events_detected = True
        
        # Generate immediate actions
        if high_traffic_locations:
            recommendations['immediate_actions'].append(
                f"Avoid heavy traffic areas: {', '.join(set(high_traffic_locations))}"
            )
        
        if weather_issues:
            recommendations['immediate_actions'].append(
                "Take weather precautions - reduce speed and increase following distance"
            )
        
        # Generate travel planning advice
        if len(alerts) > 3:
            recommendations['travel_planning'].append(
                "Consider postponing non-essential travel"
            )
        
        recommendations['travel_planning'].append(
            "Allow 20-30% extra time for all journeys"
        )
        
        # Generate route suggestions
        safe_locations = [loc for loc in predictions.keys() if loc not in high_traffic_locations]
        if safe_locations:
            recommendations['route_suggestions'].append(
                f"Consider routes through: {', '.join(safe_locations[:2])}"
            )
        
        # Generate timing advice
        current_hour = datetime.now().hour
        if current_hour in [7, 8, 16, 17, 18]:
            recommendations['timing_advice'].append(
                "Peak hours detected - consider traveling earlier or later"
            )
        else:
            recommendations['timing_advice'].append(
                "Current time is generally good for travel"
            )
        
        return recommendations
    
    def _calculate_alert_statistics(self, alerts):
        """Calculate statistics about current alerts"""
        if not alerts:
            return {'avg_priority': 0, 'coverage_areas': 0, 'estimated_duration': '0 minutes'}
        
        priorities = [alert.get('priority', 3) for alert in alerts]
        avg_priority = sum(priorities) / len(priorities)
        
        unique_locations = set(alert['location'] for alert in alerts if alert['location'] != 'all')
        coverage_areas = len(unique_locations)
        
        # Estimate how long alerts will remain active
        current_time = datetime.now()
        durations = []
        
        for alert in alerts:
            try:
                expires_at = datetime.fromisoformat(alert['expires_at'].replace('Z', '+00:00'))
                duration = (expires_at.replace(tzinfo=None) - current_time).total_seconds() / 60
                durations.append(max(0, duration))
            except:
                durations.append(60)  # Default 1 hour
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'avg_priority': round(avg_priority, 1),
            'coverage_areas': coverage_areas,
            'estimated_duration': f"{int(avg_duration)} minutes",
            'total_locations_affected': len(unique_locations)
        }
    
    def _calculate_next_update_time(self):
        """Calculate when the next alert update should occur"""
        next_update = datetime.now() + timedelta(minutes=5)
        return next_update.isoformat()
    
    def _get_fallback_alerts(self):
        """Provide fallback alerts if main generation fails"""
        return {
            'active_alerts': [{
                'id': 'fallback_info',
                'type': 'system_info',
                'severity': 'info',
                'location': 'all',
                'title': 'Traffic Monitoring Active',
                'message': 'Traffic monitoring system is active and collecting data',
                'timestamp': datetime.now().isoformat(),
                'priority': 1
            }],
            'alert_summary': {
                'total_alerts': 1,
                'severity_breakdown': {'critical': 0, 'warning': 0, 'info': 1},
                'main_concerns': [],
                'overall_status': 'System operational'
            },
            'recommendations': {
                'immediate_actions': ['Monitor traffic conditions'],
                'travel_planning': ['Plan routes in advance'],
                'route_suggestions': ['Use real-time navigation'],
                'timing_advice': ['Check traffic before departure']
            },
            'alert_statistics': {
                'avg_priority': 1,
                'coverage_areas': 0,
                'estimated_duration': '5 minutes'
            },
            'next_update': self._calculate_next_update_time()
        }
