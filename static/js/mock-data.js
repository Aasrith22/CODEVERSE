/**
 * Mock Data Generator for Frontend - Provides sample data for testing and demo
 */
class MockDataGenerator {
    constructor() {
        this.locations = ['Ameerpet', 'Kukatpally', 'Madhapur', 'Bowenpally', 'Miyapur', 'Secunderabad'];
        this.weatherConditions = ['Very Cold', 'Very Sunny', 'Rain', 'Stormy'];
        this.vehicleTypes = ['Heavy vehicles', 'Two-Wheeler', 'Three-Wheeler', 'Four-Wheeler'];
        
        this.baseTrafficPatterns = {
            'Ameerpet': 0.4,
            'Kukatpally': 0.5,
            'Madhapur': 0.6,
            'Bowenpally': 0.3,
            'Miyapur': 0.4,
            'Secunderabad': 0.5
        };
    }
    
    generateSamplePredictionData() {
        return {
            density: Math.random() * 0.6 + 0.2, // 0.2 to 0.8
            confidence: Math.random() * 0.3 + 0.7, // 0.7 to 1.0
            mae: 0.118,
            rmse: 0.166,
            agent_analysis: {
                current_conditions: this.generateCurrentConditions(),
                prediction_breakdown: this.generatePredictionBreakdown(),
                confidence_scores: this.generateConfidenceScores(),
                alerts: this.generateSampleAlerts(),
                alert_summary: this.generateAlertSummary(),
                recommendations: this.generateRecommendations(),
                route_suggestions: this.generateRouteSuggestions(),
                insights: this.generateAgentInsights(),
                crew_metadata: this.generateCrewMetadata()
            },
            analysis_duration: Math.random() * 2 + 0.5, // 0.5 to 2.5 seconds
            timestamp: new Date().toISOString()
        };
    }
    
    generateCurrentConditions() {
        const location = this.getRandomLocation();
        return {
            timestamp: new Date().toISOString(),
            location: location,
            current_density: Math.random() * 0.8 + 0.1,
            trend_analysis: {
                weekly_pattern: 'High traffic on weekdays during rush hours',
                hourly_pattern: this.getCurrentHourPattern(),
                seasonal_trend: 'Normal seasonal traffic patterns',
                growth_rate: `+${Math.floor(Math.random() * 10 + 1)}% compared to last month`,
                confidence_score: Math.random() * 0.3 + 0.7
            },
            anomaly_detection: {
                current_anomaly: Math.random() < 0.2, // 20% chance
                anomaly_details: Math.random() < 0.2 ? ['Unusual traffic spike detected'] : [],
                event_correlations: this.getEventCorrelations(),
                severity: this.getRandomSeverity()
            },
            peak_hour_prediction: this.generatePeakHourPrediction(),
            weather_impact: this.generateWeatherImpact(),
            event_impact: this.generateEventImpact(),
            historical_comparison: this.generateHistoricalComparison()
        };
    }
    
    getCurrentHourPattern() {
        const hour = new Date().getHours();
        if (hour >= 7 && hour <= 9) return 'Morning rush hour - peak traffic expected';
        if (hour >= 17 && hour <= 19) return 'Evening rush hour - heavy traffic anticipated';
        if (hour >= 12 && hour <= 14) return 'Lunch hour - moderate traffic increase';
        if (hour >= 22 || hour <= 5) return 'Night hours - minimal traffic expected';
        return 'Normal traffic flow expected';
    }
    
    generatePredictionBreakdown() {
        return {
            linear_regression: Math.random() * 0.6 + 0.2,
            random_forest: Math.random() * 0.6 + 0.2,
            neural_network: Math.random() * 0.6 + 0.2,
            legacy_model: Math.random() * 0.6 + 0.2
        };
    }
    
    generateConfidenceScores() {
        return {
            linear_regression: Math.random() * 0.3 + 0.7,
            random_forest: Math.random() * 0.2 + 0.8,
            neural_network: Math.random() * 0.3 + 0.7,
            legacy_model: Math.random() * 0.2 + 0.8
        };
    }
    
    generateSampleAlerts() {
        const alerts = [];
        const alertTypes = [
            {
                type: 'high_traffic',
                severity: 'warning',
                title: 'Heavy Traffic Alert',
                message: 'Heavy traffic detected in Madhapur area',
                location: 'Madhapur'
            },
            {
                type: 'weather_impact',
                severity: 'info',
                title: 'Weather Advisory',
                message: 'Rain expected - drive with caution',
                location: 'all'
            },
            {
                type: 'rush_hour',
                severity: 'info',
                title: 'Rush Hour Traffic',
                message: 'Peak hours - expect delays',
                location: 'all'
            },
            {
                type: 'random_event',
                severity: 'warning',
                title: 'Traffic Incident',
                message: 'Accident reported on main route',
                location: this.getRandomLocation()
            }
        ];
        
        // Generate 0-3 random alerts
        const alertCount = Math.floor(Math.random() * 4);
        for (let i = 0; i < alertCount; i++) {
            const alertTemplate = alertTypes[Math.floor(Math.random() * alertTypes.length)];
            alerts.push({
                ...alertTemplate,
                id: `alert_${Date.now()}_${i}`,
                timestamp: new Date().toISOString(),
                expires_at: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(), // 2 hours from now
                priority: Math.floor(Math.random() * 5) + 1,
                eta_impact: this.getRandomETAImpact(),
                suggestions: this.getAlertSuggestions(alertTemplate.type)
            });
        }
        
        return alerts;
    }
    
    generateAlertSummary() {
        const totalAlerts = Math.floor(Math.random() * 6);
        const critical = Math.floor(Math.random() * 2);
        const warning = Math.floor(Math.random() * 3);
        const info = Math.max(0, totalAlerts - critical - warning);
        
        return {
            total_alerts: totalAlerts,
            severity_breakdown: { critical, warning, info },
            alert_type_breakdown: {
                high_traffic: Math.floor(Math.random() * 3),
                weather_impact: Math.floor(Math.random() * 2),
                random_event: Math.floor(Math.random() * 2)
            },
            main_concerns: this.getMainConcerns(totalAlerts),
            overall_status: this.getOverallStatus(critical, warning)
        };
    }
    
    generateRecommendations() {
        return {
            immediate_actions: [
                'Monitor traffic conditions regularly',
                'Allow extra travel time during peak hours',
                'Consider alternative routes when available'
            ],
            travel_planning: [
                'Plan journeys outside peak hours when possible',
                'Check weather conditions before departure',
                'Keep alternative routes in mind'
            ],
            route_suggestions: [
                'Use real-time navigation apps',
                'Consider public transportation during heavy traffic',
                'Avoid construction zones'
            ],
            timing_advice: [
                'Best travel times: 10 AM - 4 PM',
                'Avoid: 8-10 AM and 5-7 PM on weekdays',
                'Weekend mornings typically have lighter traffic'
            ]
        };
    }
    
    generateRouteSuggestions() {
        if (Math.random() < 0.3) return null; // 30% chance of no route suggestions
        
        const origin = this.getRandomLocation();
        let destination = this.getRandomLocation();
        while (destination === origin) {
            destination = this.getRandomLocation();
        }
        
        return {
            recommended_route: {
                path: [origin, destination],
                distance: Math.random() * 20 + 5, // 5-25 km
                estimated_time: Math.random() * 40 + 10, // 10-50 minutes
                traffic_impact: Math.random() * 0.6 + 0.1,
                route_type: 'direct',
                description: `Direct route from ${origin} to ${destination}`,
                optimization_score: Math.random() * 0.5 + 0.5
            },
            alternatives: this.generateAlternativeRoutes(origin, destination),
            route_comparison: this.generateRouteComparison(),
            traffic_aware_eta: Math.random() * 40 + 15
        };
    }
    
    generateAlternativeRoutes(origin, destination) {
        const alternatives = [];
        const intermediateStops = this.locations.filter(loc => loc !== origin && loc !== destination);
        
        for (let i = 0; i < Math.min(2, intermediateStops.length); i++) {
            const intermediate = intermediateStops[i];
            alternatives.push({
                path: [origin, intermediate, destination],
                distance: Math.random() * 25 + 8,
                estimated_time: Math.random() * 50 + 15,
                traffic_impact: Math.random() * 0.8 + 0.1,
                route_type: `via_${intermediate}`,
                description: `Route via ${intermediate}`,
                optimization_score: Math.random() * 0.8 + 0.2
            });
        }
        
        return alternatives;
    }
    
    generateRouteComparison() {
        return {
            fastest_route: { estimated_time: Math.random() * 30 + 10 },
            shortest_route: { distance: Math.random() * 15 + 5 },
            least_traffic_route: { traffic_impact: Math.random() * 0.4 + 0.1 },
            time_difference_range: {
                min: Math.random() * 20 + 10,
                max: Math.random() * 20 + 30
            },
            distance_difference_range: {
                min: Math.random() * 10 + 5,
                max: Math.random() * 15 + 15
            }
        };
    }
    
    generateAgentInsights() {
        return {
            data_analyst_insight: 'Traffic patterns show typical weekday rush hour behavior with 85% confidence',
            prediction_insight: `Model confidence is ${(Math.random() * 0.3 + 0.7).toFixed(0)}% using 4 models. Primary factors: time of day, weather conditions`,
            route_insight: 'Optimal route identified with moderate traffic density and good road conditions',
            alert_insight: `Generated ${Math.floor(Math.random() * 5)} alerts with ${Math.floor(Math.random() * 3)} requiring immediate attention`,
            crew_summary: `${this.getTrafficStatus()} with high confidence prediction from AI agent collaboration`
        };
    }
    
    generateCrewMetadata() {
        return {
            agents_used: ['data_analyst', 'predictor', 'route_optimizer', 'alert_manager'],
            analysis_version: '2.0',
            crew_type: 'comprehensive_traffic_analysis',
            capabilities: [
                'real_time_analysis',
                'multi_model_prediction',
                'route_optimization',
                'intelligent_alerting'
            ],
            timestamp: new Date().toISOString()
        };
    }
    
    generatePeakHourPrediction() {
        const currentHour = new Date().getHours();
        const nextPeakHours = [8, 9, 17, 18, 19];
        const nextPeak = nextPeakHours.find(hour => hour > currentHour) || nextPeakHours[0];
        
        return {
            next_peak_hour: nextPeak,
            peak_periods: { morning: [8, 9], evening: [17, 18, 19] },
            current_status: nextPeakHours.includes(currentHour) ? 'peak' : 'normal',
            time_to_next_peak: nextPeak > currentHour ? nextPeak - currentHour : 24 - currentHour + nextPeak
        };
    }
    
    generateWeatherImpact() {
        const condition = this.weatherConditions[Math.floor(Math.random() * this.weatherConditions.length)];
        const impacts = {
            'Very Sunny': { factor: 0.1, description: 'Minimal weather impact on traffic flow' },
            'Very Cold': { factor: 0.15, description: 'Slight increase in traffic due to reduced visibility' },
            'Rain': { factor: 0.4, description: 'Moderate traffic impact - slower speeds expected' },
            'Stormy': { factor: 0.6, description: 'Significant traffic disruption expected' }
        };
        
        return {
            condition: condition,
            impact_factor: impacts[condition].factor,
            description: impacts[condition].description,
            recommendations: this.getWeatherRecommendations(condition)
        };
    }
    
    generateEventImpact() {
        const events = [];
        if (Math.random() < 0.3) { // 30% chance of events
            events.push({
                name: 'Road Construction',
                location: this.getRandomLocation(),
                traffic_impact: Math.random() * 0.4 + 0.1
            });
        }
        
        return {
            active_events: events,
            total_impact_score: events.reduce((sum, event) => sum + event.traffic_impact, 0),
            event_count: events.length,
            severity: events.length > 0 ? 'medium' : 'low'
        };
    }
    
    generateHistoricalComparison() {
        const currentDensity = Math.random() * 0.6 + 0.2;
        const historicalAverage = 0.4;
        
        return {
            historical_average: historicalAverage,
            current_vs_average: currentDensity > historicalAverage ? 'above average' : 'below average',
            percentage_difference: `${((currentDensity - historicalAverage) / historicalAverage * 100).toFixed(1)}%`,
            trend_direction: Math.random() > 0.5 ? 'increasing' : 'stable'
        };
    }
    
    // Utility methods
    getRandomLocation() {
        return this.locations[Math.floor(Math.random() * this.locations.length)];
    }
    
    getRandomSeverity() {
        const severities = ['low', 'medium', 'high'];
        return severities[Math.floor(Math.random() * severities.length)];
    }
    
    getRandomETAImpact() {
        const impacts = ['+5-10 minutes', '+10-15 minutes', '+15-25 minutes', 'Minimal impact'];
        return impacts[Math.floor(Math.random() * impacts.length)];
    }
    
    getAlertSuggestions(alertType) {
        const suggestions = {
            high_traffic: ['Avoid this area if possible', 'Use alternative routes', 'Allow extra travel time'],
            weather_impact: ['Drive carefully', 'Reduce speed', 'Use headlights'],
            rush_hour: ['Consider public transport', 'Leave earlier or later', 'Allow extra time'],
            random_event: ['Use alternative routes', 'Monitor traffic updates', 'Be patient']
        };
        return suggestions[alertType] || ['Drive safely'];
    }
    
    getMainConcerns(totalAlerts) {
        if (totalAlerts === 0) return [];
        
        const concerns = [
            'Heavy traffic in multiple areas',
            'Weather affecting traffic conditions',
            'Incidents affecting traffic flow',
            'Peak hour congestion'
        ];
        
        return concerns.slice(0, Math.min(totalAlerts, 3));
    }
    
    getOverallStatus(critical, warning) {
        if (critical > 0) return 'Critical conditions detected';
        if (warning > 2) return 'Multiple traffic concerns';
        if (warning > 0) return 'Traffic concerns detected';
        return 'Normal conditions';
    }
    
    getEventCorrelations() {
        const events = [
            'IT Conference in Madhapur affecting nearby areas',
            'Shopping mall events increasing traffic',
            'School hours affecting local traffic',
            'Construction work causing delays'
        ];
        
        return Math.random() < 0.4 ? [events[Math.floor(Math.random() * events.length)]] : [];
    }
    
    getWeatherRecommendations(condition) {
        const recommendations = {
            'Very Sunny': ['Normal driving conditions', 'Stay hydrated'],
            'Very Cold': ['Allow extra warm-up time', 'Drive carefully'],
            'Rain': ['Reduce speed', 'Increase following distance', 'Use headlights'],
            'Stormy': ['Avoid unnecessary travel', 'Drive very slowly', 'Stay updated']
        };
        return recommendations[condition] || ['Drive with caution'];
    }
    
    getTrafficStatus() {
        const statuses = [
            'Light traffic conditions',
            'Moderate traffic conditions',
            'Heavy traffic conditions',
            'Peak traffic conditions'
        ];
        return statuses[Math.floor(Math.random() * statuses.length)];
    }
    
    // Method to generate real-time traffic updates
    generateRealTimeUpdate() {
        const trafficUpdates = {};
        this.locations.forEach(location => {
            trafficUpdates[location] = {
                density: Math.random() * 0.8 + 0.1,
                trend: ['increasing', 'decreasing', 'stable'][Math.floor(Math.random() * 3)],
                confidence: Math.random() * 0.3 + 0.7
            };
        });
        
        return {
            timestamp: new Date().toISOString(),
            traffic_updates: trafficUpdates,
            weather_conditions: this.generateWeatherImpact(),
            events: Math.random() < 0.2 ? [{ // 20% chance of events
                name: 'Traffic Update',
                location: this.getRandomLocation(),
                impact: Math.random() * 0.3 + 0.1
            }] : []
        };
    }
    
    // Method to generate sample location traffic data
    generateLocationTrafficData() {
        const data = {};
        this.locations.forEach(location => {
            data[location] = Math.random() * 0.8 + 0.1;
        });
        return data;
    }
    
    // Method to generate hourly trend data
    generateHourlyTrendData() {
        const hours = Array.from({length: 24}, (_, i) => i);
        return hours.map(hour => {
            // Simulate realistic traffic patterns
            if (hour >= 7 && hour <= 9) return Math.random() * 0.3 + 0.6; // Morning rush
            if (hour >= 17 && hour <= 19) return Math.random() * 0.3 + 0.7; // Evening rush
            if (hour >= 12 && hour <= 14) return Math.random() * 0.2 + 0.4; // Lunch
            if (hour >= 22 || hour <= 5) return Math.random() * 0.2 + 0.1; // Night
            return Math.random() * 0.3 + 0.3; // Normal
        });
    }
}

// Make it globally available
window.MockDataGenerator = MockDataGenerator;

// Create a global instance
window.mockDataGenerator = new MockDataGenerator();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MockDataGenerator;
}
