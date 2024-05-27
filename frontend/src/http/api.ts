import axios, { AxiosError } from "axios";

export const MEDIA_URL = 'http://localhost:8888';
const API_URL = 'http://localhost:8888/api/v1'
export const apiAuth = axios.create({
  withCredentials: true,
  baseURL: API_URL
});
export const api = axios.create({
  withCredentials: true,
  baseURL: API_URL
});

apiAuth.interceptors.request.use((config) => {
  config.headers.Authorization = `Bearer ${localStorage.getItem('access-token')}`;
  return config;
});

apiAuth.interceptors.response.use((config) => {
  return config;
}, async (error: AxiosError) => {
  const originalRequest = error.config;

  if (error.response?.status === 401 && originalRequest && !originalRequest.headers.get('Auth-retry')) {
    originalRequest.headers.set('Auth-retry', true);
    try {
      const response = await axios.get(`${API_URL}/auth/refresh`, {withCredentials: true});
      localStorage.setItem('access-token', response.data.accessToken);
      return apiAuth.request(originalRequest)
    } catch (e) {

    }
  }
});