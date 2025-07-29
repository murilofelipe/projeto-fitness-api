// /frontend/src/components/__tests__/PerformanceDashboard.spec.ts
import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PerformanceDashboard from '../PerformanceDashboard.vue';

// Teste simples para verificar se o componente renderiza o título corretamente
describe('PerformanceDashboard', () => {
  it('renderiza o título principal', () => {
    const wrapper = mount(PerformanceDashboard);
    // Verifica se o texto 'Dashboard de Performance' existe no componente
    expect(wrapper.text()).toContain('Dashboard de Performance');
  });
});