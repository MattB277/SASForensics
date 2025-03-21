import axios from 'axios';

const axiosInstance = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api/',
    headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
    },
    timeout: 10000, // 10-second timeout
});

// Request Interceptor to add auth token
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken'); // Example for adding auth token
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response Interceptor
axiosInstance.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response) {
            // Handling 401 Unauthorized
            if (error.response.status === 401) {
                console.error('Unauthorized - Invalid or expired token');
                // Optionally, redirect to login page
                window.location.href = '/login';
            }
            // Handling timeout error
            if (error.code === 'ECONNABORTED') {
                console.error('API call timed out');
                alert('The request timed out. Please try again later.');
            }
        } else {
            // No response, likely a network error
            alert('Network error! Please check your internet connection.');
        }
        return Promise.reject(error);
    }
);

export default axiosInstance;