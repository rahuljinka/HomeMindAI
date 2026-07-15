import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const apiClient = axios.create({
  // Use the computer's local IP address so physical devices can connect
  baseURL: 'http://192.168.68.102:8000', 
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(async (config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
