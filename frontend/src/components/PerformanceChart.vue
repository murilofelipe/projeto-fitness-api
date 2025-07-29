<script setup lang="ts">
import { Line as LineChart } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  TimeScale,
  TimeSeriesScale
} from 'chart.js'
import 'chartjs-adapter-date-fns';
import { computed } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

// Registra todos os componentes necessários do Chart.js, incluindo a escala de tempo
ChartJS.register(
    Title, Tooltip, Legend, LineElement, PointElement,
    CategoryScale, LinearScale, TimeScale, TimeSeriesScale
);

// Conecta o componente ao nosso "cérebro" central, o Pinia store
const store = useDashboardStore();

// 'computed' cria uma propriedade que se recalcula automaticamente sempre que os dados no store mudam.
const chartData = computed(() => {
  // Usamos o getter 'filteredPerformanceData' que já filtra os dados pelo exercício e frequência selecionados
  const dataToDisplay = store.performanceData?.performance;

  if (!dataToDisplay || dataToDisplay.length === 0) {
    return { labels: [], datasets: [] };
  }

  // Ordena os dados por data para que a linha do tempo seja exibida corretamente
  const sortedData = [...dataToDisplay].sort((a: any, b: any) => new Date(a.data_treino).getTime() - new Date(b.data_treino).getTime());

  const labels = sortedData.map((item: any) => item.data_treino);
  const volumeData = dataToDisplay.map((item: any) => item.volume_total_diario);
  const maxCargaData = dataToDisplay.map((item: any) => item.maior_carga_kg);

  return {
    labels: labels,
    datasets: [
      {
        label: 'Volume Total de Carga (kg)',
        backgroundColor: '#42b983', // Verde Vue
        borderColor: '#42b983',
        data: volumeData,
        tension: 0.2, // Deixa a linha levemente curvada
        yAxisID: 'yVolume' // Associa este dataset ao eixo Y da esquerda
      },
      {
        label: 'Maior Carga (kg)',
        backgroundColor: '#3498db', // Um azul para diferenciar
        borderColor: '#3498db',
        data: maxCargaData,
        tension: 0.2,
        yAxisID: 'yCarga' // Associa este dataset ao eixo Y da direita
      }
    ]
  };
});

// Opções de configuração aprimoradas para o gráfico com dois eixos Y e eixo de tempo
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index' as const,
    intersect: false,
  },
  plugins: {
    legend: {
      position: 'top' as const,
      labels: {
        color: '#e0e0e0'
      }
    },
    title: {
      display: false, // O título já está no card pai
    }
  },
  scales: {
    x: {
      type: 'time' as const, // Diz ao Chart.js para tratar o eixo X como uma linha do tempo
      time: {
        unit: 'day' as const,
        tooltipFormat: 'dd MMM yyyy',
        displayFormats: {
          day: 'dd/MM'
        }
      },
      ticks: { color: '#e0e0e0' },
      grid: { color: '#444' }
    },
    // Eixo Y da esquerda para o Volume Total
    yVolume: {
      type: 'linear' as const,
      display: true,
      position: 'left' as const,
      beginAtZero: true,
      ticks: { color: '#42b983' }, // Cor verde para o eixo
      grid: { color: '#444' }
    },
    // Eixo Y da direita para a Maior Carga
    yCarga: {
      type: 'linear' as const,
      display: true,
      position: 'right' as const,
      beginAtZero: true,
      ticks: { color: '#3498db' }, // Cor azul para o eixo
      grid: {
        drawOnChartArea: false, // Evita que as linhas de grade se sobreponham
      },
    }
  }
};
</script>

<template>
  <div style="height: 400px; position: relative;">
    <LineChart :data="chartData" :options="chartOptions" />
  </div>
</template>