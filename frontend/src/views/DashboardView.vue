<script setup lang="ts">
import { useDashboardStore } from '@/stores/dashboard';
import { onMounted } from 'vue';

// Importa os componentes visuais
import PerformanceChart from '@/components/PerformanceChart.vue';
import FrequencyChart from '@/components/FrequencyChart.vue';

// Pega a instância do nosso "cérebro"
const store = useDashboardStore();

// Quando o componente for montado, manda o cérebro buscar os dados iniciais
onMounted(() => {
  store.fetchAlunos();
});

function onAlunoChange(event: Event) {
  const target = event.target;
  if (target instanceof HTMLSelectElement) {
    const newId = Number(target.value);
    store.selectAluno(newId);
  }
}

function onExercicioChange(event: Event) {
  const target = event.target;
  if (target instanceof HTMLSelectElement) {
    store.selectExercicio(Number(target.value));
  }
}
</script>

<template>
  <div class="dashboard-container">
    <header>
      <h1>Plataforma de Performance</h1>
      <div class="controls">
        <div class="control-group">
          <label for="aluno-select">Analisando Aluno:</label>
          <select id="aluno-select" :value="store.selectedAlunoId" @change="onAlunoChange">
            <option v-for="aluno in store.alunos" :key="aluno.id_usuario" :value="aluno.id_usuario">
              {{ aluno.nome }}
            </option>
          </select>
        </div>

        <div class="control-group">
          <label>Período de Frequência:</label>
          <div class="period-selector">
            <button @click="store.setFrequency('semanal')" :class="{ active: store.frequency === 'semanal' }">Semanal</button>
            <button @click="store.setFrequency('mensal')" :class="{ active: store.frequency === 'mensal' }">Mensal</button>
            <button @click="store.setFrequency('anual')" :class="{ active: store.frequency === 'anual' }">Anual</button>
          </div>
        </div>

        <div class="control-group">
          <label for="exercicio-select">Analisando Exercício:</label>
          <select id="exercicio-select" :value="store.selectedExercicioId" @change="onExercicioChange">
            <option v-for="ex in store.exercicios" :key="ex.id_exercicio" :value="ex.id_exercicio">
              {{ ex.nome_exercicio }}
            </option>
          </select>
        </div>
      </div>
    </header>
    
    <main>
      <div v-if="store.isLoading" class="state-message">...</div>
      <div v-else-if="store.error" class="state-message error">{{ store.error }}</div>
      
      <div class="dashboard-grid" v-else-if="store.performanceData">
        
        <FrequencyChart />
        
        <div class="card full-width">
          <h3>Evolução da Performance ao Longo do Tempo</h3>
          <PerformanceChart />
        </div>
      </div>
    </main>
  </div>
</template>


<style scoped>
.dashboard-container {
  padding: 2rem;
  background-color: #1a1a1a;
  min-height: 100vh;
  color: #e0e0e0;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-bottom: 1px solid #444;
  padding-bottom: 1rem;
}

header h1 {
  margin: 0;
  color: #42b983; /* Verde Vue */
}

.controls label {
  margin-right: 1rem;
  font-size: 1rem;
}

.controls select {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #2c2c2c;
  color: #e0e0e0;
  border: 1px solid #444;
  font-size: 1rem;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.card {
  background-color: #2c2c2c;
  padding: 1.5rem;
  border-radius: 8px;
}

.full-width {
  grid-column: 1 / -1; /* Ocupa a largura inteira */
}

.state-message {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 4rem;
}

.error {
  color: #ff5252;
  background-color: rgba(255, 82, 82, 0.1);
  padding: 1rem;
  border-radius: 8px;
}

.controls {
  display: flex;
  gap: 2rem;
  align-items: center;
}
.control-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.period-selector button {
  background-color: #444;
  color: #e0e0e0;
  border: 1px solid #555;
  padding: 0.3rem 0.6rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.period-selector button:first-child { border-radius: 4px 0 0 4px; }
.period-selector button:last-child { border-radius: 0 4px 4px 0; }
.period-selector button:hover { background-color: #555; }
.period-selector button.active {
  background-color: #42b983;
  color: #1a1a1a;
  font-weight: bold;
}
</style>