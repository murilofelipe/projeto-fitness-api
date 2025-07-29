<script setup lang="ts">
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { computed } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const store = useDashboardStore(); // Conecta ao store

// Função auxiliar para obter o número da semana
const getWeekNumber = (d: Date) => {
  d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  return `${d.getUTCFullYear()}-W${String(weekNo).padStart(2, '0')}`;
};

const chartData = computed(() => {
  if (!store.performanceData?.performance) return { labels: [], datasets: [] };

  const frequencyMap: { [key: string]: number } = {};
  
  // A lógica agora lê a frequência diretamente do store
  store.performanceData.performance.forEach((item: any) => {
    const date = new Date(item.data_treino);
    let key = '';

    if (store.frequency === 'semanal') {
      key = getWeekNumber(date);
    } else if (store.frequency === 'mensal') {
      key = date.toLocaleString('pt-BR', { month: 'long', year: 'numeric' });
    } else if (store.frequency === 'anual') {
      key = String(date.getFullYear());
    }

    if (!frequencyMap[key]) frequencyMap[key] = 0;
    frequencyMap[key]++;
  });

  const labels = Object.keys(frequencyMap).sort();
  const data = labels.map(label => frequencyMap[label]);
  
  return {
    labels,
    datasets: [{
      label: `Frequência de Treinos (${store.frequency})`,
      backgroundColor: '#8e44ad',
      data
    }]
  };
});

const chartOptions = { /* ... (suas opções de gráfico aqui) ... */ };
</script>

<template>
  <div class="card">
    <h3>Frequência de Treinos</h3>
    <div style="height: 300px; position: relative;">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
/* O estilo agora é mais simples */
.card {
  background-color: #2c2c2c;
  padding: 1.5rem;
  border-radius: 8px;
}
h3 {
  margin-top: 0;
}
</style>