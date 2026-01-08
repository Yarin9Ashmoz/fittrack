import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5005';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add token to all requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Intake Evaluations API
export const intakeEvaluationAPI = {
    create: (data) => api.post('/intake-evaluations/', data),
    getByMember: (memberId) => api.get(`/intake-evaluations/member/${memberId}`),
    getLatest: (memberId) => api.get(`/intake-evaluations/member/${memberId}/latest`),
    getById: (id) => api.get(`/intake-evaluations/${id}`),
    update: (id, data) => api.put(`/intake-evaluations/${id}`, data),
    checkClearance: (memberId) => api.get(`/intake-evaluations/member/${memberId}/clearance`),
};

// Personal Tracking API
export const personalTrackingAPI = {
    create: (data) => api.post('/personal-tracking/', data),
    getByMember: (memberId) => api.get(`/personal-tracking/member/${memberId}`),
    getSummary: (memberId, days = 30) => api.get(`/personal-tracking/member/${memberId}/summary`, { params: { days } }),
    getById: (id) => api.get(`/personal-tracking/${id}`),
    update: (id, data) => api.put(`/personal-tracking/${id}`, data),
};

// Error Reports API (Admin only)
export const errorReportAPI = {
    getAll: (filters = {}) => api.get('/error-reports/', { params: filters }),
    getUnresolved: () => api.get('/error-reports/unresolved'),
    getStats: () => api.get('/error-reports/stats'),
    getById: (id) => api.get(`/error-reports/${id}`),
    updateStatus: (id, data) => api.put(`/error-reports/${id}`, data),
};

// Extended Payment API
export const paymentAPI = {
    getAll: () => api.get('/payments/'),
    create: (data) => api.post('/payments/', data),
    getById: (id) => api.get(`/payments/${id}`),
    getByMember: (memberId) => api.get(`/payments/member/${memberId}`),
    cancelPayment: (id) => api.delete(`/payments/${id}`),

    // New endpoints
    calculateForClass: (classId, data) => api.post(`/payments/calculate-for-class/${classId}`, data),
    processSubscription: (subscriptionId, data) => api.post(`/payments/process-subscription/${subscriptionId}`, data),
    markAsPaid: (id) => api.post(`/payments/${id}/mark-paid`),
    getPending: () => api.get('/payments/pending'),
};

export default api;
