from crewai import Agent
import math
import random
from datetime import datetime

class RouteOptimizerAgent:
    def __init__(self):
        self.junction_coordinates = {
            'Kukatpally': {'lat': 17.493338, 'lng': 78.402547},
            'Ameerpet': {'lat': 17.434275, 'lng': 78.445403},
            'Miyapur': {'lat': 17.496653, 'lng': 78.361809},
            'Bowenpally': {'lat': 17.463865, 'lng': 78.472837},
            'Secunderabad': {'lat': 17.434962, 'lng': 78.500812},
            'Madhapur': {'lat': 17.451399, 'lng': 78.381218}
        }
        
        # Define road connections and their characteristics
        self.road_network = {
            'Kukatpally': ['Miyapur', 'Ameerpet', 'Bowenpally'],
            'Ameerpet': ['Kukatpally', 'Secunderabad', 'Madhapur'],
            'Miyapur': ['Kukatpally', 'Madhapur'],
            'Bowenpally': ['Kukatpally', 'Secunderabad'],
            'Secunderabad': ['Ameerpet', 'Bowenpally', 'Madhapur'],
            'Madhapur': ['Ameerpet', 'Miyapur', 'Secunderabad']
        }
        
        # Road quality and speed factors
        self.road_characteristics = {
            ('Kukatpally', 'Miyapur'): {'speed_factor': 1.2, 'quality': 'excellent', 'lanes': 6},
            ('Ameerpet', 'Secunderabad'): {'speed_factor': 1.0, 'quality': 'good', 'lanes': 4},
            ('Madhapur', 'Miyapur'): {'speed_factor': 1.1, 'quality': 'good', 'lanes': 4},
            ('Ameerpet', 'Madhapur'): {'speed_factor': 0.9, 'quality': 'average', 'lanes': 4},
            ('Kukatpally', 'Ameerpet'): {'speed_factor': 0.8, 'quality': 'average', 'lanes': 4},
            ('Bowenpally', 'Secunderabad'): {'speed_factor': 1.0, 'quality': 'good', 'lanes': 4},
            ('Kukatpally', 'Bowenpally'): {'speed_factor': 0.9, 'quality': 'average', 'lanes': 3},
            ('Secunderabad', 'Madhapur'): {'speed_factor': 1.0, 'quality': 'good', 'lanes': 4}
        }
        
        self.agent = Agent(
            role='Route Optimization Expert',
            goal='Calculate optimal routes based on traffic predictions, road conditions, and provide intelligent alternative paths with real-time adaptation',
            backstory='Navigation specialist with expertise in graph algorithms, real-time route optimization, and urban traffic flow dynamics. Experienced in multi-criteria optimization including distance, time, fuel efficiency, and user preferences.',
            verbose=True,
            allow_delegation=False
        )
    
    def calculate_optimal_routes(self, origin, destination, current_traffic, user_preferences=None):
        """Calculate optimal routes with multiple optimization criteria"""
        try:
            if origin == destination:
                return {
                    'error': 'Origin and destination cannot be the same',
                    'recommended_route': None,
                    'alternatives': []
                }
            
            # Set default preferences
            if user_preferences is None:
                user_preferences = {
                    'priority': 'time',  # 'time', 'distance', 'fuel'
                    'avoid_tolls': False,
                    'avoid_highways': False,
                    'vehicle_type': 'Four-Wheeler'
                }
            
            # Find all possible routes
            all_routes = self._find_all_routes(origin, destination, max_hops=3)
            
            if not all_routes:
                return self._get_fallback_route_response(origin, destination)
            
            # Evaluate each route
            evaluated_routes = []
            for route in all_routes:
                evaluation = self._evaluate_route(route, current_traffic, user_preferences)
                evaluated_routes.append(evaluation)
            
            # Sort routes by optimization score
            evaluated_routes.sort(key=lambda x: x['optimization_score'])
            
            # Select best route and alternatives
            recommended_route = evaluated_routes[0]
            alternatives = evaluated_routes[1:4]  # Top 3 alternatives
            
            return {
                'recommended_route': recommended_route,
                'alternatives': alternatives,
                'route_comparison': self._compare_routes(evaluated_routes[:4]),
                'traffic_aware_eta': recommended_route.get('estimated_time', 30),
                'optimization_criteria': user_preferences,
                'real_time_updates': self._generate_real_time_updates(recommended_route, current_traffic)
            }
            
        except Exception as e:
            print(f"Route optimization error: {str(e)}")
            return self._get_fallback_route_response(origin, destination)
    
    def _find_all_routes(self, origin, destination, max_hops=3):
        """Find all possible routes between origin and destination"""
        routes = []
        
        # Direct route
        if destination in self.road_network.get(origin, []):
            routes.append([origin, destination])
        
        # Routes with 1 intermediate stop
        for intermediate in self.road_network.get(origin, []):
            if intermediate != destination and destination in self.road_network.get(intermediate, []):
                routes.append([origin, intermediate, destination])
        
        # Routes with 2 intermediate stops (if needed)
        if len(routes) < 3 and max_hops >= 3:
            for first_stop in self.road_network.get(origin, []):
                if first_stop == destination:
                    continue
                for second_stop in self.road_network.get(first_stop, []):
                    if second_stop in [origin, first_stop, destination]:
                        continue
                    if destination in self.road_network.get(second_stop, []):
                        route = [origin, first_stop, second_stop, destination]
                        if route not in routes:
                            routes.append(route)
        
        return routes
    
    def _evaluate_route(self, route, current_traffic, preferences):
        """Evaluate a route based on multiple criteria"""
        total_distance = 0
        total_time = 0
        total_traffic_impact = 0
        road_quality_score = 0
        
        # Calculate route metrics
        for i in range(len(route) - 1):
            start = route[i]
            end = route[i + 1]
            
            # Distance calculation
            segment_distance = self.calculate_distance(start, end)
            total_distance += segment_distance
            
            # Traffic impact
            traffic_density = current_traffic.get(end, 0.5)
            total_traffic_impact += traffic_density
            
            # Road characteristics
            road_key = tuple(sorted([start, end]))
            road_char = self.road_characteristics.get(road_key, {
                'speed_factor': 0.8, 'quality': 'average', 'lanes': 3
            })
            
            # Time calculation
            base_speed = 30  # km/h base speed
            adjusted_speed = base_speed * road_char['speed_factor'] * (1 - traffic_density * 0.5)
            segment_time = (segment_distance / adjusted_speed) * 60  # Convert to minutes
            total_time += segment_time
            
            # Road quality score (higher is better)
            quality_scores = {'excellent': 1.0, 'good': 0.8, 'average': 0.6, 'poor': 0.4}
            road_quality_score += quality_scores.get(road_char['quality'], 0.6)
        
        # Normalize scores
        avg_traffic_impact = total_traffic_impact / (len(route) - 1)
        avg_road_quality = road_quality_score / (len(route) - 1)
        
        # Calculate optimization score based on preferences
        optimization_score = self._calculate_optimization_score(
            total_distance, total_time, avg_traffic_impact, avg_road_quality, preferences
        )
        
        # Generate route description
        route_description = self._generate_route_description(route, total_distance, total_time)
        
        return {
            'path': route,
            'distance': round(total_distance, 2),
            'estimated_time': round(total_time, 1),
            'traffic_impact': round(avg_traffic_impact, 2),
            'road_quality': avg_road_quality,
            'optimization_score': optimization_score,
            'route_type': self._classify_route_type(route),
            'description': route_description,
            'traffic_hotspots': self._identify_traffic_hotspots(route, current_traffic),
            'fuel_efficiency': self._estimate_fuel_efficiency(total_distance, avg_traffic_impact),
            'difficulty_level': self._assess_route_difficulty(route, avg_traffic_impact)
        }
    
    def _calculate_optimization_score(self, distance, time, traffic, quality, preferences):
        """Calculate optimization score based on user preferences"""
        priority = preferences.get('priority', 'time')
        
        # Normalize values (lower is better for score)
        distance_score = distance / 50  # Normalize by max expected distance
        time_score = time / 120  # Normalize by max expected time
        traffic_score = traffic  # Already normalized 0-1
        quality_score = 1 - quality  # Invert quality (lower score is better)
        
        # Weight based on priority
        if priority == 'time':
            weights = {'time': 0.5, 'traffic': 0.3, 'distance': 0.1, 'quality': 0.1}
        elif priority == 'distance':
            weights = {'distance': 0.5, 'time': 0.2, 'traffic': 0.2, 'quality': 0.1}
        elif priority == 'fuel':
            weights = {'traffic': 0.4, 'distance': 0.3, 'time': 0.2, 'quality': 0.1}
        else:  # balanced
            weights = {'time': 0.3, 'distance': 0.25, 'traffic': 0.25, 'quality': 0.2}
        
        score = (weights['time'] * time_score +
                weights['distance'] * distance_score +
                weights['traffic'] * traffic_score +
                weights['quality'] * quality_score)
        
        return round(score, 3)
    
    def _classify_route_type(self, route):
        """Classify the type of route"""
        if len(route) == 2:
            return 'direct'
        elif len(route) == 3:
            return f'via_{route[1]}'
        else:
            return f'multi_stop_via_{route[1]}'
    
    def _generate_route_description(self, route, distance, time):
        """Generate human-readable route description"""
        if len(route) == 2:
            return f"Direct route from {route[0]} to {route[1]} ({distance:.1f} km, ~{time:.0f} min)"
        else:
            intermediate_stops = ' → '.join(route[1:-1])
            return f"Route via {intermediate_stops} ({distance:.1f} km, ~{time:.0f} min)"
    
    def _identify_traffic_hotspots(self, route, current_traffic):
        """Identify traffic hotspots along the route"""
        hotspots = []
        for location in route:
            traffic_level = current_traffic.get(location, 0.5)
            if traffic_level > 0.7:
                hotspots.append({
                    'location': location,
                    'traffic_level': traffic_level,
                    'severity': 'high' if traffic_level > 0.8 else 'medium'
                })
        return hotspots
    
    def _estimate_fuel_efficiency(self, distance, traffic_impact):
        """Estimate fuel efficiency for the route"""
        base_efficiency = 15  # km per liter
        traffic_penalty = traffic_impact * 0.3  # 30% reduction at maximum traffic
        efficiency = base_efficiency * (1 - traffic_penalty)
        fuel_needed = distance / efficiency
        return {
            'efficiency_kmpl': round(efficiency, 2),
            'estimated_fuel_liters': round(fuel_needed, 2),
            'traffic_impact_on_fuel': f"{traffic_penalty * 100:.1f}% reduction"
        }
    
    def _assess_route_difficulty(self, route, traffic_impact):
        """Assess the driving difficulty of the route"""
        difficulty_factors = {
            'traffic_stress': traffic_impact,
            'route_complexity': min((len(route) - 2) * 0.2, 0.6),  # More turns = more complex
            'navigation_difficulty': 0.1 if len(route) == 2 else 0.3
        }
        
        total_difficulty = sum(difficulty_factors.values()) / len(difficulty_factors)
        
        if total_difficulty < 0.3:
            level = 'Easy'
        elif total_difficulty < 0.6:
            level = 'Moderate'
        else:
            level = 'Challenging'
        
        return {
            'level': level,
            'score': round(total_difficulty, 2),
            'factors': difficulty_factors
        }
    
    def _compare_routes(self, routes):
        """Compare multiple routes and provide insights"""
        if not routes:
            return {}
        
        comparison = {
            'fastest_route': min(routes, key=lambda x: x['estimated_time']),
            'shortest_route': min(routes, key=lambda x: x['distance']),
            'least_traffic_route': min(routes, key=lambda x: x['traffic_impact']),
            'time_difference_range': {
                'min': min(route['estimated_time'] for route in routes),
                'max': max(route['estimated_time'] for route in routes)
            },
            'distance_difference_range': {
                'min': min(route['distance'] for route in routes),
                'max': max(route['distance'] for route in routes)
            }
        }
        
        return comparison
    
    def _generate_real_time_updates(self, route, current_traffic):
        """Generate real-time updates for the recommended route"""
        updates = []
        
        # Check for traffic alerts along the route
        for location in route['path']:
            traffic_level = current_traffic.get(location, 0.5)
            
            if traffic_level > 0.7:
                updates.append({
                    'type': 'traffic_alert',
                    'location': location,
                    'message': f"Heavy traffic ahead at {location}",
                    'impact': 'Expect 5-10 minute delay'
                })
            elif traffic_level < 0.3:
                updates.append({
                    'type': 'clear_road',
                    'location': location,
                    'message': f"Clear roads at {location}",
                    'impact': 'Good travel conditions'
                })
        
        # Add timing recommendations
        current_hour = datetime.now().hour
        if current_hour in [8, 9, 17, 18, 19]:
            updates.append({
                'type': 'timing_advice',
                'message': 'Currently peak hours - consider delaying travel if possible',
                'impact': 'Traffic may be heavier than usual'
            })
        
        return updates
    
    def calculate_distance(self, loc1, loc2):
        """Calculate distance between two locations using Haversine formula"""
        if loc1 not in self.junction_coordinates or loc2 not in self.junction_coordinates:
            return 10  # Default distance for unknown locations
        
        coords1 = self.junction_coordinates[loc1]
        coords2 = self.junction_coordinates[loc2]
        
        R = 6371  # Earth's radius in kilometers
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = math.radians(coords1['lat']), math.radians(coords1['lng'])
        lat2, lon2 = math.radians(coords2['lat']), math.radians(coords2['lng'])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return round(distance, 2)
    
    def _get_fallback_route_response(self, origin, destination):
        """Provide fallback response when route calculation fails"""
        fallback_distance = 15  # Assume 15km average distance
        fallback_time = 45  # Assume 45 minutes average time
        
        return {
            'recommended_route': {
                'path': [origin, destination],
                'distance': fallback_distance,
                'estimated_time': fallback_time,
                'traffic_impact': 0.5,
                'route_type': 'direct',
                'description': f"Direct route from {origin} to {destination} (estimated)",
                'optimization_score': 0.5
            },
            'alternatives': [],
            'route_comparison': {},
            'traffic_aware_eta': fallback_time,
            'real_time_updates': [{
                'type': 'info',
                'message': 'Using estimated route data',
                'impact': 'Actual conditions may vary'
            }]
        }
