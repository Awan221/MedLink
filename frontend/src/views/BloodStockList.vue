<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Consultation des stocks de sang</h2>
    <div class="mb-6 flex flex-wrap gap-4">
      <select v-model="filters.center" class="border rounded px-2 py-1">
        <option value="">Tous les centres</option>
        <option v-for="center in (centers || []).filter(c => c && c.id)" :key="center.id" :value="center.id">{{ center.name }} ({{ center.region }})</option>
      </select>
      <select v-model="filters.blood_group" class="border rounded px-2 py-1">
        <option value="">Tous groupes</option>
        <option v-for="g in bloodGroups" :key="g" :value="g">{{ g }}</option>
      </select>
      <button @click="fetchStocks" class="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">Filtrer</button>
    </div>
    <div class="mb-4 flex gap-2">
      <button @click="exportCSV" class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700">Exporter CSV</button>
      <button @click="exportPDF" class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700">Exporter PDF</button>
    </div>
    <div class="mb-8">
      <canvas id="bloodChart" height="80"></canvas>
      <div v-if="criticalGroups.length" class="alert alert-danger mt-2">
        <b>Attention :</b> Stock critique pour les groupes :
        <span v-for="g in criticalGroups" :key="g" class="font-bold text-red-700 mx-1">{{ g }}</span>
      </div>
    </div>
    <table class="min-w-full bg-white border">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 border">Centre</th>
          <th class="p-2 border">Groupe</th>
          <th class="p-2 border">Quantité</th>
          <th class="p-2 border">Dernière mise à jour</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in (stocks || []).filter(s => s && s.id)" :key="stock.id">
          <td class="p-2 border">{{ getCenterName(stock.center) }}</td>
          <td class="p-2 border">
            <span :class="['px-2 py-1 rounded text-white', badgeColor(stock.blood_group)]">
              {{ stock.blood_group }}
            </span>
          </td>
          <td class="p-2 border">
            <span :class="unitsBadge(stock.units_available)">
              {{ stock.units_available }}
            </span>
          </td>
          <td class="p-2 border">{{ formatDate(stock.last_updated) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import jsPDF from 'jspdf'
import 'jspdf-autotable'
import Chart from 'chart.js/auto'

const stocks = ref([])
const centers = ref([])
const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
const filters = ref({ center: '', blood_group: '' })
const criticalGroups = ref([])
let chartInstance = null;

function updateChart() {
  if (!stocks.value.length) return;
  const groupQuantities = bloodGroups.map(g => {
    return stocks.value.filter(s => s.blood_group === g).reduce((acc, s) => acc + (s.units_available || 0), 0);
  });
  const ctx = document.getElementById('bloodChart').getContext('2d');
  if (chartInstance) chartInstance.destroy();
  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: bloodGroups,
      datasets: [{
        label: 'Quantité par groupe',
        data: groupQuantities,
        backgroundColor: bloodGroups.map(g => badgeColor(g).replace('bg-', '').replace('-500','')),
      }]
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });
  // Détection des stocks critiques (ex: < 10 unités)
  criticalGroups.value = bloodGroups.filter((g, i) => groupQuantities[i] < 10);
}

watch(stocks, updateChart);
onMounted(() => {
  fetchCenters()
  fetchStocks()
  setTimeout(updateChart, 500)
})

function badgeColor(group) {
  switch(group) {
    case 'A+': return 'bg-red-500';
    case 'A-': return 'bg-red-700';
    case 'B+': return 'bg-yellow-500';
    case 'B-': return 'bg-yellow-700';
    case 'AB+': return 'bg-purple-500';
    case 'AB-': return 'bg-purple-700';
    case 'O+': return 'bg-green-500';
    case 'O-': return 'bg-green-700';
    default: return 'bg-gray-400';
  }
}

function unitsBadge(units) {
  if (units <= 5) return 'bg-red-600 text-white px-2 py-1 rounded font-bold animate-pulse';
  if (units <= 15) return 'bg-orange-400 text-white px-2 py-1 rounded';
  return 'bg-green-500 text-white px-2 py-1 rounded';
}

function fetchCenters() {
  axios.get('/api/blood-bank/centers/')
    .then(res => { centers.value = Array.isArray(res.data) ? res.data : (res.data && Array.isArray(res.data.results) ? res.data.results : []) })
}

function fetchStocks() {
  let url = '/api/blood-bank/inventory/?'
  if (filters.value.center) url += `center=${filters.value.center}&`
  if (filters.value.blood_group) url += `blood_type=${filters.value.blood_group}&`
  axios.get(url)
    .then(res => { stocks.value = Array.isArray(res.data) ? res.data : (res.data && Array.isArray(res.data.results) ? res.data.results : []) })
}

function getCenterName(centerId) {
  const c = centers.value.find(c => c.id === centerId)
  return c ? c.name : ''
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('fr-FR')
}

function exportCSV() {
  let csv = 'Centre,Groupe sanguin,Quantité (ml),Date mise à jour\n'
  stocks.value.forEach(stock => {
    const center = getCenterName(stock.center)
    csv += `${center},${stock.blood_type},${stock.quantity_ml},${formatDate(stock.last_updated)}\n`
  })
  const blob = new Blob([csv], { type: 'text/csv' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'stocks_sang.csv'
  link.click()
}

function exportPDF() {
  const doc = new jsPDF()
  doc.text('Stocks de sang', 10, 10)
  doc.autoTable({
    head: [['Centre', 'Groupe sanguin', 'Quantité', 'Date mise à jour']],
    body: stocks.value.map(stock => [
      getCenterName(stock.center),
      stock.blood_group,
      stock.units_available,
      formatDate(stock.last_updated)
    ])
  })
  doc.save('stocks_sang.pdf')
}

onMounted(() => {
  fetchCenters()
  fetchStocks()
})
</script>

<style scoped>
table { border-collapse: collapse; }
th, td { text-align: left; }
</style>
