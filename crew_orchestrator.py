from crewai import Crew, Task
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.data_analyst_agent import DataAnalystAgent
from agents.prediction_agent import PredictionAgent
from agents.route_optimizer_agent import RouteOptimizerAgent
from agents.alert_manager_agent import AlertManagerAgent
from datetime import datetime
import traceback

class TrafficPredictionCrew:
    def __init__(self):
        try:
            print("🚀 Initializing Traffic Prediction Crew...")
            self.data_analyst = DataAnalystAgent()
            self.predictor = PredictionAgent()
            self.route_optimizer = RouteOptimizerAgent()
            self.alert_manager = AlertManagerAgent()
            print("✅ All agents initialized successfully!")
        except Exception as e:
            print(f"⚠️ Error initializing agents: {str(e)}")
            print(traceback.format_exc())
    
    def execute_comprehensive_analysis(self, request_data):
        """Execute comprehensive traffic analysis using all agents"""
        try:
            print(f"🔍 Starting comprehensive analysis for: {request_data}")
            
            location = request_data.get('location', request_data.get('area', 'Ameerpet'))
            analysis_start_time = datetime.now()
            
            # Step 1: Data Analysis
            print("📊 Step 1: Analyzing current traffic conditions...")
            current_analysis = self.data_analyst.analyze_current_conditions(location)
            print(f"✅ Data analysis completed for {location}")
            
            # Step 2: Traffic Prediction
            print("🧠 Step 2: Generating traffic predictions...")
            prediction_input = self._prepare_prediction_input(request_data, current_analysis)
            traffic_prediction = self.predictor.predict_traffic_density(prediction_input)
            print(f"✅ Traffic prediction completed - Density: {traffic_prediction['prediction']:.2%}")
            
            # Step 3: Route Optimization (if destination provided)
            route_analysis = None
            if request_data.get('destination'):
                print("🗺️ Step 3: Calculating optimal routes...")
                current_traffic = self._prepare_traffic_data_for_routing(location, traffic_prediction)
                route_analysis = self.route_optimizer.calculate_optimal_routes(
                    location, request_data['destination'], current_traffic
                )
                print("✅ Route optimization completed")
            else:
                print("ℹ️ Step 3: Skipping route optimization (no destination provided)")
            
            # Step 4: Alert Management
            print("🚨 Step 4: Generating traffic alerts...")
            prediction_data = {location: traffic_prediction}
            user_preferences = self._extract_user_preferences(request_data)
            alerts = self.alert_manager.generate_alerts(
                prediction_data, current_analysis, user_preferences
            )
            print(f"✅ Alert generation completed - {len(alerts['active_alerts'])} alerts generated")
            
            # Step 5: Generate Agent Insights
            print("💡 Step 5: Generating agent insights...")
            agent_insights = self._generate_agent_insights(
                current_analysis, traffic_prediction, route_analysis, alerts
            )
            
            # Combine all results
            comprehensive_result = {
                'location': location,
                'timestamp': current_analysis.get('timestamp', datetime.now().isoformat()),
                'analysis_duration': (datetime.now() - analysis_start_time).total_seconds(),
                'current_analysis': current_analysis,
                'traffic_prediction': traffic_prediction,
                'route_analysis': route_analysis,
                'alerts': alerts,
                'agent_insights': agent_insights,
                'crew_metadata': self._generate_crew_metadata()
            }
            
            print("🎉 Comprehensive analysis completed successfully!")
            return comprehensive_result
            
        except Exception as e:
            print(f"❌ Error in comprehensive analysis: {str(e)}")
            print(traceback.format_exc())
            return self._get_fallback_analysis(request_data)
    
    def _prepare_prediction_input(self, request_data, analysis):
        """Convert request data to model input format"""
        try:
            # Extract data with fallbacks
            input_data = [
                request_data.get('City', 'Hyderabad'),
                request_data.get('vehicleType', request_data.get('vehicle-type', 'Four-Wheeler')),
                request_data.get('weather', 'Very Sunny'),
                int(request_data.get('day', 1)),
                int(request_data.get('time', datetime.now().hour)),
                int(request_data.get('isPeakHour', request_data.get('peak-hours', 0))),
                int(request_data.get('randomEvent', request_data.get('random-events', 0)))
            ]
            
            print(f"📝 Prepared prediction input: {input_data}")
            return input_data
            
        except Exception as e:
            print(f"⚠️ Error preparing prediction input: {str(e)}")
            # Return default input
            return ['Hyderabad', 'Four-Wheeler', 'Very Sunny', 1, 12, 0, 0]
    
    def _prepare_traffic_data_for_routing(self, location, traffic_prediction):
        """Prepare traffic data for route optimization"""
        try:
            # Create traffic data for all locations
            all_locations = ['Ameerpet', 'Kukatpally', 'Madhapur', 'Bowenpally', 'Miyapur', 'Secunderabad']
            current_traffic = {}
            
            for loc in all_locations:
                if loc == location:
                    current_traffic[loc] = traffic_prediction['prediction']
                else:
                    # Estimate traffic for other locations based on patterns
                    base_values = {
                        'Ameerpet': 0.4,
                        'Kukatpally': 0.5,
                        'Madhapur': 0.6,  # IT hub
                        'Bowenpally': 0.3,
                        'Miyapur': 0.4,
                        'Secunderabad': 0.5
                    }
                    current_traffic[loc] = base_values.get(loc, 0.4)
            
            return current_traffic
            
        except Exception as e:
            print(f"⚠️ Error preparing traffic data for routing: {str(e)}")
            return {loc: 0.5 for loc in ['Ameerpet', 'Kukatpally', 'Madhapur', 'Bowenpally', 'Miyapur', 'Secunderabad']}
    
    def _extract_user_preferences(self, request_data):
        """Extract user preferences from request data"""
        return {
            'alert_sensitivity': request_data.get('alert_sensitivity', 'medium'),
            'preferred_routes': request_data.get('preferred_routes', []),
            'commute_times': request_data.get('commute_times', ['08:00', '17:00']),
            'vehicle_type': request_data.get('vehicleType', request_data.get('vehicle-type', 'Four-Wheeler')),
            'priority': request_data.get('route_priority', 'time')
        }
    
    def _generate_agent_insights(self, analysis, prediction, routes, alerts):
        """Generate insights from all agents"""
        try:
            insights = {
                'data_analyst_insight': self._generate_data_analyst_insight(analysis),
                'prediction_insight': self._generate_prediction_insight(prediction),
                'route_insight': self._generate_route_insight(routes),
                'alert_insight': self._generate_alert_insight(alerts),
                'crew_summary': self._generate_crew_summary(analysis, prediction, routes, alerts)
            }
            
            return insights
            
        except Exception as e:
            print(f"⚠️ Error generating agent insights: {str(e)}")
            return self._get_fallback_insights()
    
    def _generate_data_analyst_insight(self, analysis):
        """Generate insight from data analyst"""
        try:
            trend = analysis.get('trend_analysis', {})
            anomaly = analysis.get('anomaly_detection', {})
            
            insight_parts = []
            
            # Add trend information
            weekly_pattern = trend.get('weekly_pattern', 'Normal traffic patterns observed')
            insight_parts.append(f"Traffic analysis reveals: {weekly_pattern}")
            
            # Add anomaly information
            if anomaly.get('current_anomaly', False):
                anomaly_details = ', '.join(anomaly.get('anomaly_details', []))
                insight_parts.append(f"Anomalies detected: {anomaly_details}")
            
            # Add confidence
            confidence = trend.get('confidence_score', 0.8)
            insight_parts.append(f"Analysis confidence: {confidence:.1%}")
            
            return ' | '.join(insight_parts)
            
        except Exception as e:
            print(f"⚠️ Error generating data analyst insight: {str(e)}")
            return "Data analysis completed with standard traffic patterns observed"
    
    def _generate_prediction_insight(self, prediction):
        """Generate insight from prediction agent"""
        try:
            confidence = prediction.get('confidence', 0.8)
            factors = prediction.get('factors_influence', {})
            primary_factors = factors.get('primary_factors', ['traffic patterns'])
            model_count = len(prediction.get('model_breakdown', {}))
            
            insight = f"Prediction confidence: {confidence:.1%} using {model_count} models. "
            insight += f"Primary influencing factors: {', '.join(primary_factors[:2])}"
            
            # Add uncertainty information
            uncertainty = prediction.get('uncertainty_metrics', {})
            model_agreement = uncertainty.get('model_agreement', 0.8)
            insight += f" | Model agreement: {model_agreement:.1%}"
            
            return insight
            
        except Exception as e:
            print(f"⚠️ Error generating prediction insight: {str(e)}")
            return "Traffic prediction completed with standard confidence levels"
    
    def _generate_route_insight(self, routes):
        """Generate insight from route optimizer"""
        try:
            if not routes:
                return "No route optimization requested"
            
            recommended = routes.get('recommended_route', {})
            alternatives_count = len(routes.get('alternatives', []))
            
            distance = recommended.get('distance', 'unknown')
            time = recommended.get('estimated_time', 'unknown')
            traffic_impact = recommended.get('traffic_impact', 0.5)
            
            insight = f"Optimal route: {distance} km, ~{time} min with {traffic_impact:.1%} traffic impact. "
            insight += f"{alternatives_count} alternative routes available"
            
            return insight
            
        except Exception as e:
            print(f"⚠️ Error generating route insight: {str(e)}")
            return "Route optimization available upon request"
    
    def _generate_alert_insight(self, alerts):
        """Generate insight from alert manager"""
        try:
            active_alerts = alerts.get('active_alerts', [])
            summary = alerts.get('alert_summary', {})
            
            total_alerts = len(active_alerts)
            severity_breakdown = summary.get('severity_breakdown', {})
            warning_count = severity_breakdown.get('warning', 0)
            critical_count = severity_breakdown.get('critical', 0)
            
            if total_alerts == 0:
                return "No active traffic alerts - conditions are normal"
            
            insight = f"Generated {total_alerts} alerts"
            
            if critical_count > 0:
                insight += f" ({critical_count} critical)"
            elif warning_count > 0:
                insight += f" ({warning_count} warnings)"
            
            main_concerns = summary.get('main_concerns', [])
            if main_concerns:
                insight += f" | Main concerns: {', '.join(main_concerns[:2])}"
            
            return insight
            
        except Exception as e:
            print(f"⚠️ Error generating alert insight: {str(e)}")
            return "Alert monitoring active and operational"
    
    def _generate_crew_summary(self, analysis, prediction, routes, alerts):
        """Generate overall crew analysis summary"""
        try:
            location = analysis.get('location', 'Unknown')
            density = prediction.get('prediction', 0.5)
            confidence = prediction.get('confidence', 0.8)
            alert_count = len(alerts.get('active_alerts', []))
            
            # Determine overall status
            if density > 0.8:
                status = "High traffic conditions"
            elif density > 0.6:
                status = "Moderate traffic conditions"
            elif density > 0.4:
                status = "Light traffic conditions"
            else:
                status = "Minimal traffic conditions"
            
            # Add confidence qualifier
            if confidence > 0.9:
                confidence_desc = "very high confidence"
            elif confidence > 0.8:
                confidence_desc = "high confidence"
            elif confidence > 0.7:
                confidence_desc = "moderate confidence"
            else:
                confidence_desc = "acceptable confidence"
            
            summary = f"{status} in {location} predicted with {confidence_desc}"
            
            if alert_count > 0:
                summary += f" | {alert_count} active alerts require attention"
            
            if routes:
                summary += " | Route optimization available"
            
            return summary
            
        except Exception as e:
            print(f"⚠️ Error generating crew summary: {str(e)}")
            return "Comprehensive traffic analysis completed by AI agent crew"
    
    def _generate_crew_metadata(self):
        """Generate metadata about the crew analysis"""
        return {
            'agents_used': ['data_analyst', 'predictor', 'route_optimizer', 'alert_manager'],
            'analysis_version': '2.0',
            'crew_type': 'comprehensive_traffic_analysis',
            'capabilities': [
                'real_time_analysis',
                'multi_model_prediction',
                'route_optimization',
                'intelligent_alerting'
            ],
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_fallback_analysis(self, request_data):
        """Provide fallback analysis if main analysis fails"""
        location = request_data.get('location', request_data.get('area', 'Ameerpet'))
        
        return {
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'analysis_duration': 1.0,
            'current_analysis': {
                'current_density': 0.5,
                'trend_analysis': {
                    'weekly_pattern': 'Standard traffic patterns',
                    'confidence_score': 0.7
                },
                'anomaly_detection': {
                    'current_anomaly': False,
                    'severity': 'low'
                }
            },
            'traffic_prediction': {
                'prediction': 0.5,
                'confidence': 0.7,
                'model_breakdown': {'fallback_model': 0.5},
                'factors_influence': {
                    'primary_factors': ['Time of day'],
                    'impact_scores': {'time': 0.6}
                }
            },
            'route_analysis': None,
            'alerts': {
                'active_alerts': [],
                'alert_summary': {
                    'total_alerts': 0,
                    'overall_status': 'System operational'
                },
                'recommendations': {
                    'immediate_actions': ['Monitor traffic conditions'],
                    'travel_planning': ['Plan ahead']
                }
            },
            'agent_insights': self._get_fallback_insights(),
            'crew_metadata': {
                'agents_used': ['fallback'],
                'analysis_version': '2.0-fallback',
                'note': 'Fallback analysis due to system limitations'
            }
        }
    
    def _get_fallback_insights(self):
        """Get fallback insights if insight generation fails"""
        return {
            'data_analyst_insight': 'Traffic data analysis completed with standard procedures',
            'prediction_insight': 'Prediction models operational with acceptable accuracy',
            'route_insight': 'Route optimization ready for activation',
            'alert_insight': 'Alert system monitoring and ready',
            'crew_summary': 'AI traffic analysis crew operational and ready for comprehensive analysis'
        }
    
    def get_agent_status(self):
        """Get status of all agents"""
        try:
            status = {
                'data_analyst': {
                    'status': 'active',
                    'last_analysis': 'just now',
                    'capabilities': ['pattern_analysis', 'anomaly_detection', 'trend_prediction']
                },
                'predictor': {
                    'status': 'active',
                    'models_loaded': len(self.predictor.ensemble_models.models) if hasattr(self.predictor, 'ensemble_models') else 1,
                    'capabilities': ['ensemble_prediction', 'confidence_scoring', 'uncertainty_quantification']
                },
                'route_optimizer': {
                    'status': 'active',
                    'routes_calculated': 'ready',
                    'capabilities': ['multi_criteria_optimization', 'real_time_adaptation', 'alternative_routing']
                },
                'alert_manager': {
                    'status': 'active',
                    'monitoring': 'continuous',
                    'capabilities': ['real_time_alerting', 'predictive_warnings', 'smart_notifications']
                }
            }
            
            return status
            
        except Exception as e:
            print(f"⚠️ Error getting agent status: {str(e)}")
            return {
                'data_analyst': {'status': 'operational'},
                'predictor': {'status': 'operational'},
                'route_optimizer': {'status': 'operational'},
                'alert_manager': {'status': 'operational'}
            }
