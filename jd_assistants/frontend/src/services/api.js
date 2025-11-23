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

// ===== RECRUITMENT APIs =====

// Candidate API
export const candidateAPI = {
    uploadCV: (files) => {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file));
        return api.post('/api/v1/candidates/upload-cv', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },
    list: () => api.get('/api/v1/candidates'),
    get: (id) => api.get(`/api/v1/candidates/${id}`),
    delete: (id) => api.delete(`/api/v1/candidates/${id}`),
};

// Job Description API
export const jobDescriptionAPI = {
    list: () => api.get('/api/v1/job-descriptions'),
    get: (id) => api.get(`/api/v1/job-descriptions/${id}`),
    create: (data) => {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('description', data.description);
        formData.append('skills', data.skills);
        return api.post('/api/v1/job-descriptions', formData);
    },
    update: (id, data) => {
        const formData = new FormData();
        formData.append('title', data.title);
        formData.append('description', data.description);
        formData.append('skills', data.skills);
        return api.put(`/api/v1/job-descriptions/${id}`, formData);
    },
    delete: (id) => api.delete(`/api/v1/job-descriptions/${id}`),
    activate: (id) => api.put(`/api/v1/job-descriptions/${id}/activate`),
};

// Scoring API
export const scoringAPI = {
    scoreAll: () => api.post('/api/v1/scoring/score-all'),
    getScores: (jdId) => api.get('/api/v1/scoring/scores', { params: { jd_id: jdId } }),
};

// JD AI API
export const jdAIAPI = {
    analyze: (jdText) => {
        const formData = new FormData();
        formData.append('jd_text', jdText);
        return api.post('/api/v1/jd-ai/analyze', formData);
    },
    rewrite: (jdText) => {
        const formData = new FormData();
        formData.append('jd_text', jdText);
        return api.post('/api/v1/jd-ai/rewrite', formData);
    },
    generate: (requirements) => {
        const formData = new FormData();
        Object.keys(requirements).forEach(key => {
            formData.append(key, requirements[key]);
        });
        return api.post('/api/v1/jd-ai/generate', formData);
    },
    assessSalary: (data) => {
        const formData = new FormData();
        Object.keys(data).forEach(key => {
            formData.append(key, data[key]);
        });
        return api.post('/api/v1/jd-ai/assess-salary', formData);
    },
};

export default api;
