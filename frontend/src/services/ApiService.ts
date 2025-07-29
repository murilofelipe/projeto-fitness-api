// /frontend/src/services/ApiService.ts
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000', // A URL da nossa API Python
    headers: { 'Content-Type': 'application/json' }
});

export const getPerformanceData = (alunoId: number, exercicioId: number | null) => {
    let url = `/analytics/performance/${alunoId}`;
    if (exercicioId) {
        url += `?exercicio_id=${exercicioId}`;
    }
    return apiClient.get(url);
};

export const getAlunos = () => {
    return apiClient.get('/alunos/');
};

export const getAlunoSummary = (alunoId: number) => {
    return apiClient.get(`/alunos/${alunoId}/summary`);
};

export const getExerciciosPorAluno = (alunoId: number) => {
    return apiClient.get(`/alunos/${alunoId}/exercicios`);
};

export const getFrequenciaData = (alunoId: number, periodo: string) => {
    return apiClient.get(`/analytics/frequencia/${alunoId}?periodo=${periodo}`);
};

export const getCalendarData = (alunoId: number) => {
    return apiClient.get(`/calendario/${alunoId}`);
};

