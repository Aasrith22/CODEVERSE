/**
 * Charts Manager - Handles all chart creation and updates
 */
class ChartsManager {
    constructor() {
        this.charts = {};
        this.initializeCharts();
    }
    
    initializeCharts() {
        this.createConfidenceChart();
        this.createTrafficTrendChart();
        this.createModelComparisonChart();
    }
    
    createConfidenceChart() {
        const ctx = document.getElementById('confidenceChart');
        if (!ctx) return;
        
        this.charts.confidence = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 100],
                    backgroundColor: ['#4CAF50', '#e0e0e0'],
                    borderWidth: 0,
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                cutout: '75%',
                animation: {
                    animateRotate: true,
                    duration: 1000
                }
            },
            plugins: [{
                beforeDraw: (chart) => {
                    const { width, height, ctx } = chart;
                    ctx.restore();
                    
                    const fontSize = (height / 114).toFixed(2);
                    ctx.font = `bold ${fontSize}em Arial`;
                    ctx.textBaseline = 'middle';
                    ctx.fillStyle = '#333';
                    
                    const text = chart.data.datasets[0].data[0].toFixed(1) + '%';
                    const textX = Math.round((width - ctx.measureText(text).width) / 2);
                    const textY = height / 2;
                    
                    ctx.fillText(text, textX, textY);
                    ctx.save();
                }
            }]
        });
    }
    
    createTrafficTrendChart() {
        const ctx = document.getElementById('trafficTrendChart');
        if (!ctx) return;
        
        // Generate sample trend data
        const hours = Array.from({length: 24}, (_, i) => i);
        const trendData = hours.map(hour => {
            // Simulate traffic patterns throughout the day
            if (hour >= 7 && hour <= 9) return Math.random() * 0.3 + 0.6; // Morning rush
            if (hour >= 17 && hour <= 19) return Math.random() * 0.3 + 0.7; // Evening rush
            if (hour >= 12 && hour <= 14) return Math.random() * 0.2 + 0.4; // Lunch time
            if (hour >= 22 || hour <= 5) return Math.random() * 0.2 + 0.1; // Night
            return Math.random() * 0.3 + 0.3; // Normal hours
        });
        
        this.charts.trend = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: hours.map(h => `${h.toString().padStart(2, '0')}:00`),
                datasets: [{
                    label: 'Traffic Density',
                    data: trendData,
                    borderColor: '#2196F3',
                    backgroundColor: 'rgba(33, 150, 243, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#2196F3',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                return `Traffic: ${(context.parsed.y * 100).toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Time of Day'
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Traffic Density'
                        },
                        min: 0,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            }
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });
    }
    
    createModelComparisonChart() {
        const ctx = document.getElementById('modelComparisonChart');
        if (!ctx) return;
        
        this.charts.modelComparison = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['Linear Reg.', 'Random Forest', 'Neural Net', 'Ensemble'],
                datasets: [{
                    label: 'Prediction Accuracy',
                    data: [0, 0, 0, 0], // Will be updated with real data
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${(context.parsed.y * 100).toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Models'
                        },
                        grid: {
                            display: false
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Prediction Value'
                        },
                        min: 0,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            }
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    updateConfidenceChart(confidence) {
        if (!this.charts.confidence) return;
        
        const percentage = confidence * 100;
        this.charts.confidence.data.datasets[0].data = [percentage, 100 - percentage];
        
        // Update color based on confidence level
        let color;
        if (confidence > 0.8) {
            color = '#4CAF50'; // Green
        } else if (confidence > 0.6) {
            color = '#FF9800'; // Orange
        } else {
            color = '#f44336'; // Red
        }
        
        this.charts.confidence.data.datasets[0].backgroundColor = [color, '#e0e0e0'];
        this.charts.confidence.update('active');
    }
    
    updateModelComparison(modelData) {
        if (!this.charts.modelComparison || !modelData) return;
        
        const modelNames = ['linear_regression', 'random_forest', 'neural_network'];
        const predictions = modelNames.map(name => modelData[name] || 0);
        
        // Calculate ensemble average
        const ensemble = predictions.reduce((sum, pred) => sum + pred, 0) / predictions.length;
        predictions.push(ensemble);
        
        this.charts.modelComparison.data.datasets[0].data = predictions;
        this.charts.modelComparison.update('active');
    }
    
    updateTrafficTrend(hourlyData) {
        if (!this.charts.trend || !hourlyData) return;
        
        this.charts.trend.data.datasets[0].data = hourlyData;
        this.charts.trend.update('active');
    }
    
    createLocationComparisonChart(locationData) {
        const ctx = document.getElementById('locationComparisonChart');
        if (!ctx) return;
        
        const locations = Object.keys(locationData);
        const densities = Object.values(locationData);
        
        this.charts.locationComparison = new Chart(ctx.getContext('2d'), {
            type: 'radar',
            data: {
                labels: locations,
                datasets: [{
                    label: 'Traffic Density',
                    data: densities,
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgb(54, 162, 235)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgb(54, 162, 235)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            callback: function(value) {
                                return (value * 100).toFixed(0) + '%';
                            }
                        }
                    }
                }
            }
        });
    }
    
    createAlertTimelineChart(alertData) {
        const ctx = document.getElementById('alertTimelineChart');
        if (!ctx) return;
        
        // Process alert data for timeline display
        const timeLabels = [];
        const alertCounts = [];
        const severityData = { critical: [], warning: [], info: [] };
        
        // Generate last 24 hours
        for (let i = 23; i >= 0; i--) {
            const hour = new Date();
            hour.setHours(hour.getHours() - i);
            timeLabels.push(hour.getHours().toString().padStart(2, '0') + ':00');
            
            // Simulate alert counts (replace with real data)
            const critical = Math.floor(Math.random() * 3);
            const warning = Math.floor(Math.random() * 5);
            const info = Math.floor(Math.random() * 8);
            
            severityData.critical.push(critical);
            severityData.warning.push(warning);
            severityData.info.push(info);
            alertCounts.push(critical + warning + info);
        }
        
        this.charts.alertTimeline = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: timeLabels,
                datasets: [
                    {
                        label: 'Critical',
                        data: severityData.critical,
                        backgroundColor: 'rgba(244, 67, 54, 0.8)',
                        borderColor: 'rgba(244, 67, 54, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Warning',
                        data: severityData.warning,
                        backgroundColor: 'rgba(255, 152, 0, 0.8)',
                        borderColor: 'rgba(255, 152, 0, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Info',
                        data: severityData.info,
                        backgroundColor: 'rgba(33, 150, 243, 0.8)',
                        borderColor: 'rgba(33, 150, 243, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Alert Count'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    destroyChart(chartName) {
        if (this.charts[chartName]) {
            this.charts[chartName].destroy();
            delete this.charts[chartName];
        }
    }
    
    destroyAllCharts() {
        Object.keys(this.charts).forEach(chartName => {
            this.destroyChart(chartName);
        });
    }
    
    // Utility method to create dynamic charts
    createCustomChart(canvasId, config) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;
        
        const chart = new Chart(ctx.getContext('2d'), config);
        this.charts[canvasId] = chart;
        return chart;
    }
    
    // Method to update multiple charts at once
    updateAllCharts(data) {
        if (data.confidence !== undefined) {
            this.updateConfidenceChart(data.confidence);
        }
        
        if (data.modelBreakdown) {
            this.updateModelComparison(data.modelBreakdown);
        }
        
        if (data.hourlyTrend) {
            this.updateTrafficTrend(data.hourlyTrend);
        }
        
        if (data.locationData) {
            if (this.charts.locationComparison) {
                this.charts.locationComparison.destroy();
            }
            this.createLocationComparisonChart(data.locationData);
        }
    }
}

// Initialize charts manager
document.addEventListener('DOMContentLoaded', () => {
    window.chartsManager = new ChartsManager();
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChartsManager;
}
