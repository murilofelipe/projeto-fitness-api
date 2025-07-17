<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getPerformanceData } from './../services/ApiService.js';

// Variáveis reativas para armazenar os dados, o estado de carregamento e os erros
const performanceData = ref<any>(null);
const isLoading = ref(true);
const error = ref<string | null>(null);

// ID do aluno para o qual queremos buscar os dados.
const alunoId = 1;

// A função onMounted é executada assim que o componente é "montado" na tela
onMounted(async () => {
    try {
        // Chama nossa função do serviço de API
        const response = await getPerformanceData(alunoId);
        // Armazena os dados na nossa variável reativa
        performanceData.value = response.data;
    } catch (err: any) {
        // Se der erro (ex: API fora do ar, aluno não encontrado), armazena a mensagem
        error.value = err.response?.data?.detail || 'Ocorreu um erro ao buscar os dados.';
    } finally {
        // Independentemente de sucesso ou erro, marca o carregamento como concluído
        isLoading.value = false;
    }
});
</script>

<template>
    <div class="dashboard">
        <h1>Dashboard de Performance</h1>

        <div v-if="isLoading">
            <p>Carregando dados...</p>
        </div>

        <div v-else-if="error">
            <p class="error">Erro: {{ error }}</p>
        </div>

        <div v-else-if="performanceData">
            <h2>Performance de: {{ performanceData.nome_aluno }} (ID: {{ performanceData.id_aluno }})</h2>
            <table>
                <thead>
                    <tr>
                        <th>Data</th>
                        <th>Exercício</th>
                        <th>Grupo Muscular</th>
                        <th>Séries</th>
                        <th>Repetições</th>
                        <th>Maior Carga (kg)</th>
                        <th>Volume Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in performanceData.performance" :key="item.data_treino + item.nome_exercicio">
                        <td>{{ item.data_treino }}</td>
                        <td>{{ item.nome_exercicio }}</td>
                        <td>{{ item.grupo_muscular }}</td>
                        <td>{{ item.total_series }}</td>
                        <td>{{ item.total_repeticoes }}</td>
                        <td>{{ item.maior_carga_kg }}</td>
                        <td>{{ item.volume_total_carga }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<style scoped>
.dashboard {
    font-family: sans-serif;
    padding: 20px;
}
.error {
    color: red;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
th {
    background-color: #f2f2f2;
}
</style>