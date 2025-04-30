import fs from 'fs';
import fetch from 'node-fetch';
import { createObjectCsvWriter } from 'csv-writer';

const TOMTOM_API_KEY = 'gZxAqQZgQv1wLw2sdjc5NjOmT2aJiGCD';

// Configure CSV writer
const csvWriter = createObjectCsvWriter({
    path: 'tomtom_traffic_data.csv',
    header: [
        {id: 'timestamp', title: 'Timestamp'},
        {id: 'origin_lat', title: 'OriginLatitude'},
        {id: 'origin_lon', title: 'OriginLongitude'},
        {id: 'dest_lat', title: 'DestinationLatitude'},
        {id: 'dest_lon', title: 'DestinationLongitude'},
        {id: 'duration', title: 'Duration'},
        {id: 'distance', title: 'Distance'},
        {id: 'trafficDelay', title: 'TrafficDelay'},
        {id: 'liveTrafficIncidents', title: 'LiveTrafficIncidents'},
        {id: 'avgSpeed', title: 'AverageSpeed'},
        {id: 'dayOfWeek', title: 'DayOfWeek'},
        {id: 'hourOfDay', title: 'HourOfDay'},
        {id: 'isWeekend', title: 'IsWeekend'},
        {id: 'isRushHour', title: 'IsRushHour'}
    ]
});

// Define sample routes
const sampleRoutes = [
    {
        origin: {lat: 17.4875, lon: 78.3953}, // Hyderabad City
        destination: {lat: 17.4487, lon: 78.3908}, // Hyderabad Airport
        name: 'Hyderabad City to Airport'
    },
    {
        origin: {lat: 12.9716, lon: 77.5946}, // Bangalore City
        destination: {lat: 13.1989, lon: 77.7068}, // Bangalore Airport
        name: 'Bangalore City to Airport'
    }
];

// Helper function to check if current time is rush hour
function isRushHour(hour) {
    return (hour >= 8 && hour <= 10) || (hour >= 16 && hour <= 19);
}

// Function to fetch traffic incidents along the route
async function getTrafficIncidents(bbox) {
    try {
        const response = await fetch(
            `https://api.tomtom.com/traffic/services/4/incidentDetails/s3/${bbox}/10/-1/json?key=${TOMTOM_API_KEY}`
        );
        const data = await response.json();
        return data.incidents ? data.incidents.length : 0;
    } catch (error) {
        console.error('Error fetching traffic incidents:', error.message);
        return 0;
    }
}

// Function to fetch traffic data from TomTom
async function getTrafficData(origin, destination) {
    try {
        // Calculate route with traffic
        const routeResponse = await fetch(
            `https://api.tomtom.com/routing/1/calculateRoute/${origin.lat},${origin.lon}:${destination.lat},${destination.lon}/json?` +
            `traffic=true&travelMode=car&key=${TOMTOM_API_KEY}`
        );
        const routeData = await routeResponse.json();
        
        if (!routeData.routes || !routeData.routes[0]) {
            throw new Error('No route data available');
        }

        const route = routeData.routes[0];
        const summary = route.summary;
        
        // Get traffic incidents for the route area
        // Use a simple bounding box based on origin and destination
        const minLat = Math.min(origin.lat, destination.lat);
        const maxLat = Math.max(origin.lat, destination.lat);
        const minLon = Math.min(origin.lon, destination.lon);
        const maxLon = Math.max(origin.lon, destination.lon);
        const bbox = `${minLat},${minLon},${maxLat},${maxLon}`;
        
        // Get traffic incidents
        const incidents = await getTrafficIncidents(bbox);
        
        return {
            duration: summary.travelTimeInSeconds,
            distance: summary.lengthInMeters,
            trafficDelay: summary.trafficDelayInSeconds || 0,
            liveTrafficIncidents: incidents,
            avgSpeed: (summary.lengthInMeters / summary.travelTimeInSeconds) * 3.6 // Convert to km/h
        };
    } catch (error) {
        console.error(`Error fetching data for route: ${error.message}`);
        return null;
    }
}

// Main function to collect data
async function collectData(numSamples = 10) {
    const records = [];
    
    for (let i = 0; i < numSamples; i++) {
        for (const route of sampleRoutes) {
            const now = new Date();
            const trafficData = await getTrafficData(route.origin, route.destination);
            
            if (trafficData) {
                records.push({
                    timestamp: now.toISOString(),
                    origin_lat: route.origin.lat,
                    origin_lon: route.origin.lon,
                    dest_lat: route.destination.lat,
                    dest_lon: route.destination.lon,
                    duration: trafficData.duration,
                    distance: trafficData.distance,
                    trafficDelay: trafficData.trafficDelay,
                    liveTrafficIncidents: trafficData.liveTrafficIncidents,
                    avgSpeed: trafficData.avgSpeed,
                    dayOfWeek: now.getDay(),
                    hourOfDay: now.getHours(),
                    isWeekend: [0, 6].includes(now.getDay()),
                    isRushHour: isRushHour(now.getHours())
                });
                
                console.log(`Collected sample ${i + 1}/${numSamples} for route: ${route.name}`);
                console.log(`Current traffic delay: ${trafficData.trafficDelay} seconds`);
                console.log(`Number of incidents: ${trafficData.liveTrafficIncidents}`);
            }
            
            // Add delay to avoid overwhelming the API
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    }
    
    // Write to CSV
    try {
        await csvWriter.writeRecords(records);
        console.log(`Successfully wrote ${records.length} records to tomtom_traffic_data.csv`);
    } catch (error) {
        console.error('Error writing to CSV:', error);
    }
}

// Start data collection
collectData(10).then(() => {
    console.log('Data collection completed!');
}).catch(error => {
    console.error('Error in data collection:', error);
});
