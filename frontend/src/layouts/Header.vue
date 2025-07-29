<script setup lang="ts">
import { useDashboardStore } from '@/stores/dashboard';
import ProfileCard from '../components/ProfileCard.vue';
import ProfileMenu from '../components/ProfileMenu.vue'; // 1. Importa nosso novo componente de menu

const store = useDashboardStore();
</script>

<template>
  <header class="app-header">
    <div class="platform-title">
      </div>

    <ProfileMenu>
      <ProfileCard :summaryData="store.summaryData" />
    </ProfileMenu>
  </header>
</template>

<style scoped>
/* O estilo do header permanece o mesmo */
.app-header {
  height: 70px;
  background-color: #2c2c2c;
  padding: 0 2rem;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  border-bottom: 1px solid #444;
}
</style>