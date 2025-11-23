import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auth API
export const authAPI = {
    login: (email, password) => {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        return api.post('/api/v1/auth/login', formData);
    },
    register: (email, password, role = 'employee') =>
        api.post('/api/v1/auth/register', { email, password, role }),
    getCurrentUser: () => api.get('/api/v1/auth/me'),
};

// Employee API
export const employeeAPI = {
    list: () => api.get('/api/v1/employees'),
    get: (id) => api.get(`/api/v1/employees/${id}`),
    create: (data) => api.post('/api/v1/employees', data),
    update: (id, data) => api.put(`/api/v1/employees/${id}`, data),
    delete: (id) => api.delete(`/api/v1/employees/${id}`),
};

// Department API
export const departmentAPI = {
    list: () => api.get('/api/v1/departments'),
    get: (id) => api.get(`/api/v1/departments/${id}`),
    create: (data) => api.post('/api/v1/departments', data),
};

// Position API
export const positionAPI = {
    list: () => api.get('/api/v1/positions'),
    get: (id) => api.get(`/api/v1/positions/${id}`),
    create: (data) => api.post('/api/v1/positions', data),
};

export default api;
