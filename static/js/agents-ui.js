/**
 * Agent UI Manager - Handles all AI agent interactions and displays
 */
class AgentUIManager {
    constructor() {
        this.agentStatus = {};
        this.currentInsights = {};
        this.alertsContainer = document.getElementById('active-alerts');
        this.insightsContainer = document.getElementById('insights-container');
        this.modelPredictionsContainer = document.getElementById('model-predictions');
        this.confidenceChart = null;
        
        this.initializeAgentUI();
        this.startRealTimeUpdates();
        this.setupEventListeners();
    }
    
    initializeAgentUI() {
        console.log('🤖 Initializing Agent UI Manager...');
        
        // Initialize agent status indicators
        this.updateAgentStatus();
        
        // Initialize confidence chart
        this.initializeConfidenceChart();
        
        console.log('✅ Agent UI Manager initialized');
    }
    
    setupEventListeners() {
        // Agent indicator click handlers
        document.querySelectorAll('.agent-indicator').forEach(indicator => {
            indicator.addEventListener('click', (e) => {
                const agentType = e.currentTarget.dataset.agent;
                this.showAgentDetails(agentType);
            });
        });
        
        // Modal close handlers
        const modal = document.getElementById('insights-modal');
        const closeBtn = document.querySelector('.close');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.style.display = 'none';
            });
        }
        
        if (modal) {
            window.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }
    }
    
    updatePredictionResults(data) {
        console.log('📊 Updating prediction results with agent analysis...');
        
        // Update main prediction display
        const densityElement = document.querySelector('.density-value');
        if (densityElement) {
            densityElement.textContent = (data.density * 100).toFixed(1) + '%';
        }
        
        // Update confidence chart
        this.updateConfidenceChart(data.confidence);
        
        // Update model breakdown
        if (data.agent_analysis && data.agent_analysis.prediction_breakdown) {
            this.displayModelBreakdown(data.agent_analysis.prediction_breakdown);
        }
        
        // Update agent insights
        if (data.agent_analysis && data.agent_analysis.insights) {
            this.displayAgentInsights(data.agent_analysis.insights);
        }
        
        // Update alerts
        if (data.agent_analysis && data.agent_analysis.alerts) {
            this.displayAlerts(data.agent_analysis.alerts);
        }
        
        // Update route suggestions if available
        if (data.agent_analysis && data.agent_analysis.route_suggestions) {
            this.displayRouteSuggestions(data.agent_analysis.route_suggestions);
        }
        
        // Show analysis duration
        if (data.analysis_duration) {
            this.showAnalysisDuration(data.analysis_duration);
        }
        
        console.log('✅ Prediction results updated');
    }
    
    initializeConfidenceChart() {
        const ctx = document.getElementById('confidenceChart');
        if (!ctx) return;
        
        this.confidenceChart = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#4CAF50', '#e0e0e0'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                cutout: '70%'
            }
        });
    }
    
    updateConfidenceChart(confidence) {
        if (!this.confidenceChart) return;
        
        const percentage = confidence * 100;
        this.confidenceChart.data.datasets[0].data = [percentage, 100 - percentage];
        
        // Update color based on confidence level
        const color = confidence > 0.8 ? '#4CAF50' : confidence > 0.6 ? '#FF9800' : '#f44336';
        this.confidenceChart.data.datasets[0].backgroundColor = [color, '#e0e0e0'];
        
        this.confidenceChart.update('none');
        
        // Update confidence text
        const confidenceText = document.querySelector('.confidence-text');
        if (confidenceText) {
            confidenceText.textContent = `${percentage.toFixed(1)}%`;
        }
    }
    
    displayModelBreakdown(breakdown) {
        if (!breakdown || !this.modelPredictionsContainer) return;
        
        let html = '<div class="model-breakdown-header"><h4>🧠 Model Predictions</h4></div>';
        
        Object.entries(breakdown).forEach(([model, prediction]) => {
            const percentage = (prediction * 100).toFixed(1);
            const modelName = this.formatModelName(model);
            
            html += `
                <div class="model-prediction-item">
                    <div class="model-info">
                        <span class="model-name">${modelName}</span>
                        <span class="model-prediction">${percentage}%</span>
                    </div>
                    <div class="prediction-bar">
                        <div class="prediction-fill" style="width: ${percentage}%"></div>
                    </div>
                </div>
            `;
        });
        
        this.modelPredictionsContainer.innerHTML = html;
        
        // Animate the bars
        setTimeout(() => {
            document.querySelectorAll('.prediction-fill').forEach(fill => {
                fill.style.transition = 'width 1s ease-in-out';
            });
        }, 100);
    }
    
    formatModelName(modelName) {
        const nameMap = {
            'linear_regression': 'Linear Regression',
            'random_forest': 'Random Forest',
            'neural_network': 'Neural Network',
            'legacy_model': 'Legacy Model',
            'ensemble': 'Ensemble Model'
        };
        return nameMap[modelName] || modelName.replace(/_/g, ' ').toUpperCase();
    }
    
    displayAgentInsights(insights) {
        if (!insights || !this.insightsContainer) return;
        
        let html = '<div class="insights-header"><h4>💡 AI Agent Insights</h4></div>';
        
        Object.entries(insights).forEach(([agent, insight]) => {
            if (insight && agent !== 'crew_summary') {
                const agentName = this.formatAgentName(agent);
                const agentIcon = this.getAgentIcon(agent);
                
                html += `
                    <div class="insight-item" data-agent="${agent}">
                        <div class="insight-header">
                            <span class="agent-icon">${agentIcon}</span>
                            <span class="agent-name">${agentName}</span>
                        </div>
                        <div class="insight-text">${insight}</div>
                    </div>
                `;
            }
        });
        
        // Add crew summary if available
        if (insights.crew_summary) {
            html += `
                <div class="insight-item crew-summary">
                    <div class="insight-header">
                        <span class="agent-icon">👥</span>
                        <span class="agent-name">Crew Summary</span>
                    </div>
                    <div class="insight-text">${insights.crew_summary}</div>
                </div>
            `;
        }
        
        this.insightsContainer.innerHTML = html;
    }
    
    formatAgentName(agentKey) {
        const nameMap = {
            'data_analyst_insight': 'Data Analyst',
            'prediction_insight': 'Prediction Specialist',
            'route_insight': 'Route Optimizer',
            'alert_insight': 'Alert Manager'
        };
        return nameMap[agentKey] || agentKey.replace(/_/g, ' ').replace('insight', '').trim();
    }
    
    getAgentIcon(agentKey) {
        const iconMap = {
            'data_analyst_insight': '📊',
            'prediction_insight': '🧠',
            'route_insight': '🗺️',
            'alert_insight': '🚨'
        };
        return iconMap[agentKey] || '🤖';
    }
    
    displayAlerts(alerts) {
        if (!this.alertsContainer) return;
        
        if (!alerts || alerts.length === 0) {
            this.alertsContainer.innerHTML = `
                <div class="no-alerts">
                    <div class="no-alerts-icon">✅</div>
                    <div class="no-alerts-text">No active alerts</div>
                    <div class="no-alerts-subtext">Traffic conditions are normal</div>
                </div>
            `;
            return;
        }
        
        let html = '<div class="alerts-header"><h4>🚨 Active Alerts</h4></div>';
        
        alerts.forEach(alert => {
            const severityIcon = this.getSeverityIcon(alert.severity);
            const timeAgo = this.getTimeAgo(alert.timestamp);
            
            html += `
                <div class="alert-item ${alert.severity}" data-alert-type="${alert.type}">
                    <div class="alert-header">
                        <span class="alert-icon">${severityIcon}</span>
                        <div class="alert-title-area">
                            <span class="alert-title">${alert.title || alert.type}</span>
                            <span class="alert-time">${timeAgo}</span>
                        </div>
                    </div>
                    <div class="alert-content">
                        <div class="alert-message">${alert.message}</div>
                        ${alert.suggestions ? this.formatSuggestions(alert.suggestions) : ''}
                        ${alert.eta_impact ? `<div class="eta-impact">ETA Impact: ${alert.eta_impact}</div>` : ''}
                    </div>
                </div>
            `;
        });
        
        this.alertsContainer.innerHTML = html;
        
        // Show alert notification for high priority alerts
        const highPriorityAlerts = alerts.filter(alert => 
            alert.severity === 'warning' || alert.severity === 'critical'
        );
        
        if (highPriorityAlerts.length > 0) {
            this.showAlertNotification(highPriorityAlerts[0]);
        }
    }
    
    getSeverityIcon(severity) {
        const icons = {
            'critical': '🚨',
            'warning': '⚠️',
            'info': 'ℹ️',
            'success': '✅'
        };
        return icons[severity] || 'ℹ️';
    }
    
    getTimeAgo(timestamp) {
        try {
            const alertTime = new Date(timestamp);
            const now = new Date();
            const diffMinutes = Math.floor((now - alertTime) / (1000 * 60));
            
            if (diffMinutes < 1) return 'Just now';
            if (diffMinutes < 60) return `${diffMinutes}m ago`;
            if (diffMinutes < 1440) return `${Math.floor(diffMinutes / 60)}h ago`;
            return `${Math.floor(diffMinutes / 1440)}d ago`;
        } catch {
            return 'Recent';
        }
    }
    
    formatSuggestions(suggestions) {
        if (!Array.isArray(suggestions)) return '';
        
        return `
            <div class="alert-suggestions">
                <div class="suggestions-header">💡 Suggestions:</div>
                <ul class="suggestions-list">
                    ${suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                </ul>
            </div>
        `;
    }
    
    showAlertNotification(alert) {
        // Use SweetAlert2 if available, otherwise fallback to browser notification
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                icon: alert.severity === 'critical' ? 'error' : 'warning',
                title: alert.title || 'Traffic Alert',
                text: alert.message,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 5000,
                timerProgressBar: true,
                customClass: {
                    popup: 'traffic-alert-toast'
                }
            });
        } else {
            // Fallback to browser notification
            if (Notification.permission === 'granted') {
                new Notification(alert.title || 'Traffic Alert', {
                    body: alert.message,
                    icon: '/static/icons/traffic-icon.png'
                });
            }
        }
    }
    
    displayRouteSuggestions(routeAnalysis) {
        if (!routeAnalysis) return;
        
        const routeContainer = document.getElementById('route-suggestions');
        if (!routeContainer) return;
        
        const recommended = routeAnalysis.recommended_route;
        const alternatives = routeAnalysis.alternatives || [];
        
        let html = `
            <div class="route-suggestions-header">
                <h4>🗺️ Route Suggestions</h4>
            </div>
            <div class="recommended-route">
                <div class="route-label">✨ Recommended Route</div>
                <div class="route-details">
                    <div class="route-path">${recommended.path.join(' → ')}</div>
                    <div class="route-metrics">
                        <span class="metric">📏 ${recommended.distance} km</span>
                        <span class="metric">⏱️ ${recommended.estimated_time} min</span>
                        <span class="metric">🚗 ${(recommended.traffic_impact * 100).toFixed(0)}% traffic</span>
                    </div>
                </div>
            </div>
        `;
        
        if (alternatives.length > 0) {
            html += '<div class="alternative-routes"><div class="alternatives-label">Alternative Routes</div>';
            alternatives.forEach((route, index) => {
                html += `
                    <div class="alternative-route">
                        <div class="route-path">${route.path.join(' → ')}</div>
                        <div class="route-metrics">
                            <span class="metric">📏 ${route.distance} km</span>
                            <span class="metric">⏱️ ${route.estimated_time} min</span>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        routeContainer.innerHTML = html;
    }
    
    showAnalysisDuration(duration) {
        const durationElement = document.getElementById('analysis-duration');
        if (durationElement) {
            durationElement.textContent = `Analysis completed in ${duration.toFixed(2)}s`;
            durationElement.style.display = 'block';
            
            // Hide after 3 seconds
            setTimeout(() => {
                durationElement.style.display = 'none';
            }, 3000);
        }
    }
    
    startRealTimeUpdates() {
        // Update agent status every 30 seconds
        setInterval(() => {
            this.updateAgentStatus();
        }, 30000);
        
        // Update real-time traffic data every 60 seconds
        setInterval(() => {
            this.updateRealTimeTrafficData();
        }, 60000);
    }
    
    updateAgentStatus() {
        fetch('/agent_status')
            .then(response => response.json())
            .then(data => {
                Object.entries(data).forEach(([agent, status]) => {
                    const indicator = document.querySelector(`[data-agent="${agent}"] .status-dot`);
                    if (indicator) {
                        indicator.className = `status-dot ${status.status}`;
                        
                        // Add pulse animation for active agents
                        if (status.status === 'active') {
                            indicator.classList.add('pulse');
                            setTimeout(() => indicator.classList.remove('pulse'), 1000);
                        }
                    }
                });
                
                this.agentStatus = data;
            })
            .catch(error => {
                console.warn('Could not update agent status:', error);
            });
    }
    
    updateRealTimeTrafficData() {
        fetch('/real_time_update')
            .then(response => response.json())
            .then(data => {
                // Update traffic indicators on map
                if (data.traffic_updates) {
                    this.updateMapTrafficIndicators(data.traffic_updates);
                }
                
                // Show weather updates
                if (data.weather_conditions) {
                    this.updateWeatherDisplay(data.weather_conditions);
                }
            })
            .catch(error => {
                console.warn('Could not update real-time data:', error);
            });
    }
    
    updateMapTrafficIndicators(trafficUpdates) {
        // Update traffic indicators on the map
        Object.entries(trafficUpdates).forEach(([location, data]) => {
            const marker = window.mapMarkers && window.mapMarkers[location];
            if (marker) {
                // Update marker color based on traffic density
                const density = data.density;
                const color = density > 0.7 ? '#f44336' : density > 0.4 ? '#ff9800' : '#4caf50';
                
                // Update marker style (implementation depends on map library)
                if (marker.setStyle) {
                    marker.setStyle({ fillColor: color });
                }
            }
        });
    }
    
    updateWeatherDisplay(weatherConditions) {
        const weatherElement = document.getElementById('current-weather');
        if (weatherElement) {
            const weatherIcons = {
                'Very Sunny': '☀️',
                'Very Cold': '🥶',
                'Rain': '🌧️',
                'Stormy': '⛈️'
            };
            
            const icon = weatherIcons[weatherConditions.condition] || '🌤️';
            weatherElement.innerHTML = `
                <span class="weather-icon">${icon}</span>
                <span class="weather-condition">${weatherConditions.condition}</span>
                <span class="weather-temp">${weatherConditions.temperature || 25}°C</span>
            `;
        }
    }
    
    showAgentDetails(agentType) {
        const modal = document.getElementById('insights-modal');
        const detailsContainer = document.getElementById('detailed-insights');
        
        if (!modal || !detailsContainer) return;
        
        const agentData = this.agentStatus[agentType];
        const insights = this.currentInsights[agentType];
        
        let html = `
            <div class="agent-details">
                <h3>${this.formatAgentName(agentType + '_insight')}</h3>
                <div class="agent-status-info">
                    <div class="status-item">
                        <label>Status:</label>
                        <span class="status-value ${agentData?.status || 'unknown'}">${agentData?.status || 'Unknown'}</span>
                    </div>
        `;
        
        // Add agent-specific details
        if (agentData) {
            Object.entries(agentData).forEach(([key, value]) => {
                if (key !== 'status' && key !== 'capabilities') {
                    html += `
                        <div class="status-item">
                            <label>${key.replace(/_/g, ' ')}:</label>
                            <span class="status-value">${value}</span>
                        </div>
                    `;
                }
            });
            
            // Add capabilities
            if (agentData.capabilities) {
                html += `
                    <div class="status-item">
                        <label>Capabilities:</label>
                        <div class="capabilities-list">
                            ${agentData.capabilities.map(cap => 
                                `<span class="capability-tag">${cap.replace(/_/g, ' ')}</span>`
                            ).join('')}
                        </div>
                    </div>
                `;
            }
        }
        
        html += '</div></div>';
        
        detailsContainer.innerHTML = html;
        modal.style.display = 'block';
    }
    
    // Method to trigger analysis for testing
    triggerTestAnalysis() {
        const testData = {
            location: 'Ameerpet',
            City: 'Hyderabad',
            vehicleType: 'Four-Wheeler',
            weather: 'Very Sunny',
            day: '1',
            time: '12',
            isPeakHour: '0',
            randomEvent: '0'
        };
        
        return fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(testData)
        })
        .then(response => response.json())
        .then(data => {
            this.updatePredictionResults(data);
            return data;
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Agent UI Manager...');
    window.agentUI = new AgentUIManager();
    
    // Make it globally available for debugging
    window.testAgentAnalysis = () => window.agentUI.triggerTestAnalysis();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AgentUIManager;
}
