<script setup lang="ts">
import { RouterLink } from 'vue-router'; // Importe o RouterLink
defineProps<{ collapsed: boolean }>();
const emit = defineEmits(['toggle']);
</script>
<template>
    <aside class="sidebar">
      <div class="logo-area">
        <span v-if="!collapsed">FitnessData</span>
      </div>
      <nav>
        <ul>
          <li>
            <RouterLink to="/">
              <svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M13 3v6h8V3m-8 18h8V11h-8M3 21h8v-6H3m0-2V3h8v10Z"/></svg>
              <span v-if="!collapsed">Dashboard</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink to="/calendario">
              <svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M19 19H5V8h14m-3-7v2H8V1H6v2H5c-1.11 0-2 .89-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2h-1V1m-1 11h-5v5h5z"/></svg>
              <span v-if="!collapsed">Calendário</span>
            </RouterLink>
          </li>
        </ul>
      </nav>
      <button @click="emit('toggle')" class="toggle-btn">
        <svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="m14 7l-5 5l5 5V7Z"/></svg>
      </button>
    </aside>
  </template>
<style scoped>
/* Estilos para um menu lateral bonito */
.sidebar {
  background-color: #2c2c2c;
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: 1rem 0;
  transition: width 0.3s ease;
}
.logo-area { text-align: center; font-size: 1.5rem; font-weight: bold; padding: 1rem 0; color: #42b983; }
nav ul { list-style: none; padding: 0; margin: 0; }
nav a {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  color: #e0e0e0;
  text-decoration: none;
  transition: background-color 0.2s;
  white-space: nowrap;
  overflow: hidden;
}
nav a.active, nav a:hover { background-color: #3e3e3e; }
.toggle-btn {
  margin-top: auto;
  background: none;
  border: none;
  color: #e0e0e0;
  cursor: pointer;
  padding: 1rem;
}
</style>