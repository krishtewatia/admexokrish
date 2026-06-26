import axios from 'axios';

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

export const createLead = (data) => API.post('/api/leads', data);
export const getDashboard = () => API.get('/api/dashboard');

export default API;
