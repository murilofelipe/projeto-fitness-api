<script setup lang="ts">
import { useDashboardStore } from '@/stores/dashboard';
import { onMounted } from 'vue';
import TrainingCalendar from '@/components/TrainingCalendar.vue';

const store = useDashboardStore();

onMounted(() => {
  if (store.alunos.length === 0) {
    store.fetchAlunos();
  }
});

function onAlunoChange(event: Event) {
  const target = event.target;
  if (target instanceof HTMLSelectElement) {
    store.selectAluno(Number(target.value));
  }
}
</script>

<template>
  <div class="view-container">
    <header class="view-header">
      <h1>Calendário de Treinos</h1>
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
          <label>Período:</label>
          <div class="period-selector">
            <button @click="store.setFrequency('semanal')" :class="{ active: store.frequency === 'semanal' }">Semanal</button>
            <button @click="store.setFrequency('mensal')" :class="{ active: store.frequency === 'mensal' }">Mensal</button>
            <button @click="store.setFrequency('anual')" :class="{ active: store.frequency === 'anual' }">Anual</button>
          </div>
        </div>
      </div>
    </header>
    
    <main>
      <div v-if="store.isLoading" class="state-message">Carregando dados...</div>
      <div v-else-if="store.error" class="state-message error">{{ store.error }}</div>
      <div v-else-if="store.performanceData">
        <TrainingCalendar />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* Estilos para manter a consistência visual entre as páginas */
.view-container {
  width: 100%;
}
.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #444;
}
.view-header h1 {
  margin: 0;
  color: #e0e0e0;
}
.state-message { text-align: center; font-size: 1.2rem; margin-top: 4rem; }
.error { color: #ff5252; }

/* Estilos para os controles */
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
.control-group label {
  font-size: 1rem;
}
.control-group select {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: #2c2c2c;
  color: #e0e0e0;
  border: 1px solid #444;
  font-size: 1rem;
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