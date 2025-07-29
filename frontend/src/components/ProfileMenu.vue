<script setup lang="ts">
import { ref } from 'vue';
import { useDashboardStore } from '@/stores/dashboard';

// Conecta o componente ao nosso store central
const store = useDashboardStore();

// Variável reativa para controlar se o menu está visível ou não
const isMenuOpen = ref(false);

// Função para lidar com a seleção de um novo arquivo de foto
function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    const file = target.files[0];
    console.log("Arquivo de foto selecionado:", file.name);
    // Aqui, no futuro, você chamaria uma função do ApiService para fazer o upload do arquivo
    // Ex: await uploadProfilePicture(store.selectedAlunoId, file);
    isMenuOpen.value = false; // Fecha o menu após a seleção
  }
}
</script>

<template>
  <div class="profile-menu-container">
    <div @click="isMenuOpen = !isMenuOpen" class="menu-trigger">
      <slot></slot>
    </div>

    <transition name="fade">
      <div v-if="isMenuOpen" class="menu-dropdown">
        <div class="menu-header">
          <strong>{{ store.summaryData?.nome }}</strong>
          <span class="email">{{ store.summaryData?.email || 'email@exemplo.com' }}</span>
        </div>
        <ul class="menu-options">
          <li>
            <label for="photo-upload">Editar Foto</label>
            <input type="file" id="photo-upload" @change="handleFileSelect" accept="image/*" style="display: none;" />
          </li>
          <li>
            <a href="#">Sair (Logout)</a>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.profile-menu-container {
  position: relative; /* Essencial para o posicionamento do dropdown */
}

.menu-trigger {
  cursor: pointer;
}

.menu-dropdown {
  position: absolute;
  top: 110%; /* Posiciona o menu um pouco abaixo do header */
  right: 0;
  width: 250px;
  background-color: #3e3e3e;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
  z-index: 10;
}

.menu-header {
  padding: 1rem;
  border-bottom: 1px solid #555;
  display: flex;
  flex-direction: column;
}

.menu-header .email {
  font-size: 0.8rem;
  color: #a0a0a0;
}

.menu-options {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu-options li label,
.menu-options li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #e0e0e0;
  text-decoration: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.menu-options li label:hover,
.menu-options li a:hover {
  background-color: #4f4f4f;
}

/* Animação de transição para o menu aparecer suavemente */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>