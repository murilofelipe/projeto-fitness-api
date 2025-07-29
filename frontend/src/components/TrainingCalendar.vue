<script setup lang="ts">
import { computed } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

const store = useDashboardStore();

// --- LÓGICA DE GERAÇÃO DO CALENDÁRIO ---

// Gera a grade de dias para a visualização selecionada
const calendarGrid = computed(() => {
  const refDate = store.calendarDate;
  const year = refDate.getFullYear();
  const month = refDate.getMonth();

  if (store.frequency === 'semanal') {
    const startOfWeek = new Date(refDate);
    startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay()); // Inicia no Domingo
    return Array.from({ length: 7 }).map((_, i) => {
      const day = new Date(startOfWeek);
      day.setDate(day.getDate() + i);
      return { date: day, isCurrentMonth: true };
    });
  }

  if (store.frequency === 'mensal') {
    const firstDayOfMonth = new Date(year, month, 1);
    const startDate = new Date(firstDayOfMonth);
    startDate.setDate(startDate.getDate() - startDate.getDay()); // Encontra o domingo anterior ao início do mês

    const days = [];
    let currentDate = new Date(startDate);
    // Gera 6 semanas (42 dias) para cobrir todos os layouts de mês possíveis
    for (let i = 0; i < 42; i++) {
      days.push({
        date: new Date(currentDate),
        isCurrentMonth: currentDate.getMonth() === month // Marca se o dia pertence ao mês atual
      });
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return days;
  }
  
  // Para a visualização ANUAL, não geramos uma grade de dias
  return null;
});

// Agrupa os treinos por data, usando a fonte de dados dedicada do calendário
const trainingsByDate = computed(() => {
  if (!store.calendarData) return {};
  
  const map: { [key: string]: { exercicios: string[], status: string } } = {};
  
  store.calendarData.forEach((item: any) => {
    // A chave do mapa é a data no formato 'YYYY-MM-DD'
    const dateKey = new Date(item.data_treino).toISOString().split('T')[0];
    
    // Agrupa todos os exercícios e o status para um único dia
    if (!map[dateKey]) {
      map[dateKey] = {
        exercicios: [],
        status: item.status
      };
    }
    map[dateKey].exercicios.push(...item.exercicios);
  });

  return map;
});


// Agrupa a contagem de treinos por mês para a visualização anual
const trainingsByMonth = computed(() => {
    if (!store.calendarData) return {};
    const map: { [key: string]: number } = {};
    const uniqueDays = new Set();
    
    store.calendarData.forEach((item: any) => {
        // Conta apenas treinos executados para a frequência
        if (item.status === 'executado') {
            const dateKey = new Date(item.data_treino).toISOString().split('T')[0];
            if (!uniqueDays.has(dateKey)) {
                const monthKey = new Date(item.data_treino).getMonth();
                if (!map[monthKey]) map[monthKey] = 0;
                map[monthKey]++;
                uniqueDays.add(dateKey);
            }
        }
    });
    return map;
});

const monthsOfYear = [
    "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
];

// Gera o título dinâmico para o calendário
const currentViewLabel = computed(() => {
  const refDate = store.calendarDate;
  if (store.frequency === 'semanal') {
    const endOfWeek = new Date(refDate);
    endOfWeek.setDate(refDate.getDate() - refDate.getDay() + 6);
    return `Semana de ${refDate.toLocaleDateString('pt-BR', {day: '2-digit', month: 'short'})} a ${endOfWeek.toLocaleDateString('pt-BR', {day: '2-digit', month: 'short'})}`;
  }
  if (store.frequency === 'anual') {
    return `Ano de ${refDate.getFullYear()}`;
  }
  return refDate.toLocaleString('pt-BR', { month: 'long', year: 'numeric' });
})
</script>

<template>
  <div class="card">
    <div class="calendar-header">
      <button @click="store.previousPeriod()">&lt;</button>
      <h3>{{ currentViewLabel }}</h3>
      <button @click="store.nextPeriod()">&gt;</button>
    </div>

    <div class="calendar-grid annual" v-if="store.frequency === 'anual'">
        <div v-for="(month, index) in monthsOfYear" :key="month" class="month-cell">
            <div class="month-name">{{ month }}</div>
            <div class="month-count">{{ trainingsByMonth[index] || 0 }} treinos</div>
        </div>
    </div>

    <div class="calendar-grid daily" v-else>
      <div class="weekday-header" v-for="day in ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']" :key="day">{{ day }}</div>
      <div v-for="dayInfo in calendarGrid" :key="dayInfo.date.toISOString()" class="day-cell" :class="{ 'not-current-month': !dayInfo.isCurrentMonth }">
        <div class="day-number">{{ dayInfo.date.getDate() }}</div>
        <div class="day-content">
            <div v-for="(exercicio, index) in trainingsByDate[dayInfo.date.toISOString().split('T')[0]]?.exercicios" 
                 :key="index" 
                 class="training-tag"
                 :class="trainingsByDate[dayInfo.date.toISOString().split('T')[0]]?.status">
                {{ exercicio }}
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card { background-color: #2c2c2c; padding: 1.5rem; border-radius: 8px; }
.calendar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.calendar-header h3 { margin: 0; text-transform: capitalize; }
.calendar-header button { background: #444; border: none; color: white; cursor: pointer; padding: 0.5rem; border-radius: 4px; font-size: 1rem; }
.calendar-grid { 
  display: grid; 
  gap: 0.5rem;
}
.daily { 
  grid-template-columns: repeat(7, 1fr);
}
.annual {
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
}
.month-cell { background-color: #3e3e3e; border-radius: 8px; padding: 1rem; text-align: center; }
.month-name { font-weight: bold; color: #a0a0a0; }
.month-count { font-size: 1.5rem; font-weight: bold; color: #42b983; margin-top: 0.5rem; }
.weekday-header { text-align: center; font-weight: bold; color: #a0a0a0; padding-bottom: 0.5rem; }
.day-cell { background-color: #3e3e3e; border-radius: 4px; padding: 0.5rem; min-height: 100px; display: flex; flex-direction: column; }
.not-current-month { background-color: #252525; color: #666; }
.day-number { font-weight: bold; margin-bottom: 0.5rem; }
.day-content { display: flex; flex-direction: column; gap: 0.25rem; flex-grow: 1; }
.training-tag { 
  color: #1a1a1a; 
  font-size: 0.7rem; 
  padding: 0.2rem 0.4rem; 
  border-radius: 4px; 
  font-weight: bold;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
/* Cores baseadas no status */
.training-tag.executado { background-color: #42b983; /* Verde */ }
.training-tag.planejado { background-color: #3498db; /* Azul */ }
.training-tag.nao_executado { background-color: #e74c3c; /* Vermelho */ }
</style>