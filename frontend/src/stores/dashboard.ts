import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import {
  getAlunos,
  getPerformanceData,
  getAlunoSummary,
  getExerciciosPorAluno,
  getCalendarData
} from '@/services/ApiService'

// Função auxiliar para obter o número da semana no formato 'Ano-WXX'
const getWeekNumber = (d: Date): string => {
  d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  return `${d.getUTCFullYear()}-W${String(weekNo).padStart(2, '0')}`;
};

// Definimos nosso "store" do dashboard
export const useDashboardStore = defineStore('dashboard', () => {
  // --- STATE (Os dados que vamos armazenar) ---
  const alunos = ref<any[]>([])
  const exercicios = ref<any[]>([])
  const selectedAlunoId = ref<number | null>(null)
  const selectedExercicioId = ref<number | null>(null)
  const performanceData = ref<any>(null) // Dados para os gráficos de performance (do DWH)
  const calendarData = ref<any[]>([])    // Dados para o calendário (do OLTP)
  const summaryData = ref<any>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const frequency = ref<'semanal' | 'mensal' | 'anual'>('mensal')
  const calendarDate = ref(new Date())

  // --- GETTERS (Dados computados a partir do state) ---
  const filteredPerformanceData = computed(() => {
    if (!performanceData.value?.performance) return [];

    let data = performanceData.value.performance;

    if (selectedExercicioId.value) {
      data = data.filter((item: any) => item.id_exercicio === selectedExercicioId.value);
    }
    
    const refDate = calendarDate.value;
    return data.filter((item: any) => {
      const itemDate = new Date(item.data_treino);
      if (frequency.value === 'semanal') return getWeekNumber(itemDate) === getWeekNumber(refDate);
      if (frequency.value === 'mensal') return itemDate.getMonth() === refDate.getMonth() && itemDate.getFullYear() === refDate.getFullYear();
      if (frequency.value === 'anual') return itemDate.getFullYear() === refDate.getFullYear();
      return false;
    });
  });

  // --- ACTIONS (As funções que modificam o state) ---
  async function fetchAlunos() {
    try {
      const response = await getAlunos();
      alunos.value = response.data;
      if (alunos.value.length > 0) {
        await selectAluno(alunos.value[0].id_usuario);
      }
    } catch (e) {
      error.value = 'Erro ao carregar a lista de alunos.';
      console.error(e);
    }
  }

  async function selectAluno(alunoId: number) {
    if (!alunoId) return;
    selectedAlunoId.value = alunoId;
    isLoading.value = true;
    error.value = null;
    performanceData.value = null;
    summaryData.value = null;
    exercicios.value = [];
    selectedExercicioId.value = null;
    calendarData.value = [];

    try {
      const [performanceResponse, summaryResponse, exerciciosResponse, calendarResponse] = await Promise.all([
        getPerformanceData(alunoId, null),
        getAlunoSummary(alunoId),
        getExerciciosPorAluno(alunoId),
        getCalendarData(alunoId)
      ]);
      
      performanceData.value = performanceResponse.data;
      summaryData.value = summaryResponse.data;
      exercicios.value = exerciciosResponse.data;
      calendarData.value = calendarResponse.data.eventos;
      
      if (exercicios.value.length > 0) {
        selectedExercicioId.value = exercicios.value[0].id_exercicio;
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Ocorreu um erro ao buscar os dados do aluno.';
      console.error(err);
    } finally {
      isLoading.value = false;
    }
  }

  function setFrequency(newFrequency: 'semanal' | 'mensal' | 'anual') {
    frequency.value = newFrequency;
    calendarDate.value = new Date();
  }

  function selectExercicio(exercicioId: number) {
    selectedExercicioId.value = exercicioId;
  }

  function nextPeriod() {
    const newDate = new Date(calendarDate.value);
    if (frequency.value === 'semanal') newDate.setDate(newDate.getDate() + 7);
    if (frequency.value === 'mensal') newDate.setMonth(newDate.getMonth() + 1);
    if (frequency.value === 'anual') newDate.setFullYear(newDate.getFullYear() + 1);
    calendarDate.value = newDate;
  }

  function previousPeriod() {
    const newDate = new Date(calendarDate.value);
    if (frequency.value === 'semanal') newDate.setDate(newDate.getDate() - 7);
    if (frequency.value === 'mensal') newDate.setMonth(newDate.getMonth() - 1);
    if (frequency.value === 'anual') newDate.setFullYear(newDate.getFullYear() - 1);
    calendarDate.value = newDate;
  }

  // Expomos tudo que os componentes precisarão usar
  return {
    // State
    alunos, exercicios, selectedAlunoId, selectedExercicioId, performanceData,
    summaryData, isLoading, error, frequency, calendarDate, calendarData,
    // Getters
    filteredPerformanceData,
    // Actions
    fetchAlunos, selectAluno, setFrequency, selectExercicio, nextPeriod, previousPeriod
  }
})