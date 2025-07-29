<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppLayout from './layouts/AppLayout.vue';
</script>

<template>
  <AppLayout>
    <RouterView />
  </AppLayout>
</template>

<style>
/* Estilos globais (sem 'scoped') */
body {
  margin: 0;
  background-color: #1a1a1a;
  color: #e0e0e0;
  font-family: sans-serif;
}
</style>