import axios from 'axios';

// Connect dynamically securely locally 
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
});

export const sendTelemetry = (payload) => api.post('/telemetry', payload);
export const calculateRoutes = () => api.post('/routes/calculate');
export const getRoute = (truckId, date) => api.get(`/routes/${truckId}?date=${date}`);
