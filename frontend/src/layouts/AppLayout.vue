<script setup lang="ts">
import { ref } from 'vue';
import Sidebar from '@/layouts/Sidebar.vue';
import Header from '@/layouts/Header.vue';

const isSidebarCollapsed = ref(false);
</script>

<template>
  <div class="app-layout" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
    <Sidebar :collapsed="isSidebarCollapsed" @toggle="isSidebarCollapsed = !isSidebarCollapsed" />
    <div class="main-content">
      <Header />
      <main class="content-area">
        <slot></slot> </main>
    </div>
  </div>
</template>

<style scoped>
.app-layout {
  display: grid;
  grid-template-columns: 250px 1fr; /* Largura do sidebar e o resto */
  transition: grid-template-columns 0.3s ease;
}
.app-layout.sidebar-collapsed {
  grid-template-columns: 60px 1fr; /* Largura do sidebar quando oculto */
}
.main-content {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow-y: auto;
}
.content-area {
  padding: 2rem;
  flex-grow: 1;
}
</style>