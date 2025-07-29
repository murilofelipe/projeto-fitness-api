<script setup lang="ts">
import { computed } from 'vue';

// Define as "props" que este componente espera receber
const props = defineProps<{
  summaryData: any;
}>();

// Cria uma propriedade computada para as iniciais do nome
const userInitials = computed(() => {
  if (props.summaryData?.nome) {
    const names = props.summaryData.nome.split(' ');
    if (names.length > 1) {
      return `${names[0][0]}${names[names.length - 1][0]}`.toUpperCase();
    }
    return props.summaryData.nome.substring(0, 2).toUpperCase();
  }
  return '...';
});
</script>

<template>
  <div class="profile" v-if="summaryData">
    <div class="profile-details">
      <span class="profile-name">{{ summaryData.nome }}</span>
      <span class="profile-info">
        Último Login: {{ summaryData.ultimo_login ? new Date(summaryData.ultimo_login).toLocaleString('pt-BR') : 'Nunca' }} | 
        Último Treino: {{ summaryData.ultimo_treino ? summaryData.ultimo_treino.data_treino : 'N/A' }}
      </span>
    </div>
    <div class="avatar" :title="summaryData.nome">
      {{ userInitials }}
    </div>
  </div>
</template>

<style scoped>
.profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #e0e0e0;
}
.profile-details {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.profile-name {
  font-weight: bold;
}
.profile-info {
  font-size: 0.8rem;
  color: #a0a0a0;
  white-space: nowrap;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #42b983;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1rem;
  text-transform: uppercase;
}
</style>