<script setup>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps({
  chartData: { 
    type: Object,
    required: true,
    default: () => ({ labels: [], datasets: [] })
  },
  chartOptions: {
    type: Object,
    default: () => ({
      responsive: true,
      maintainAspectRatio: false, 
      plugins: {
        legend: {
          display: true 
        }
      }
    })
  },
  chartId: {
    type: String,
    default: 'bar-chart'
  },
  datasetIdKey: {
    type: String,
    default: 'label' 
  },
  width: {
    type: Number,
    default: 400
  },
  height: {
    type: Number,
    default: 200
  }
});
</script>

<template>
  <Bar
    :chart-options="chartOptions"
    :data="chartData" 
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :width="width"
    :height="height"
  />
</template>