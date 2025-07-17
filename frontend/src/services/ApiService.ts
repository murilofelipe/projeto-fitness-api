// /frontend/src/services/ApiService.ts
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000', // A URL da nossa API Python
    headers: { 'Content-Type': 'application/json' }
});

export const getPerformanceData = (alunoId: number) => {
    return apiClient.get(`/analytics/performance/${alunoId}`);
};