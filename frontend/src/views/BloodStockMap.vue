<template>
  <div class="p-6 max-w-6xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Carte des stocks de sang</h2>
    <div class="mb-4 flex gap-2 items-center">
      <label for="filterGroup">Filtrer par groupe critique :</label>
      <select id="filterGroup" v-model="filterGroup" @change="applyFilter" class="border rounded px-2 py-1">
        <option value="">Tous</option>
        <option v-for="g in ['A+','A-','B+','B-','AB+','AB-','O+','O-']" :key="g" :value="g">{{ g }}</option>
      </select>
      <button @click="exportMap" class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700">Exporter la carte (PNG)</button>
    </div>
    <div id="map" class="w-full h-[500px] rounded shadow"></div>
    <div v-if="showToast" class="toast-alert">⚠️ Pénurie détectée dans au moins un centre !</div>
    <div v-if="selectedCenter" class="mt-4 p-4 bg-white rounded shadow max-w-md mx-auto">
      <h3 class="font-bold text-lg mb-2">{{ selectedCenter.name }}</h3>
      <p class="mb-2">Région : {{ selectedCenter.region }}</p>
      <div>
        <span v-for="stock in selectedCenter.blood_stocks" :key="stock.blood_group"
              :class="['inline-block mx-1 px-2 py-1 rounded text-white text-sm', badgeColor(stock.blood_group)]">
          {{ stock.blood_group }} :
          <span :class="unitsBadge(stock.units_available)">{{ stock.units_available }}</span>
        </span>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'
import html2canvas from 'html2canvas'


const centers = ref([])
const selectedCenter = ref(null)
const showToast = ref(false)
let map = null

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
  axios.get('/blood-bank/centers/?with_stocks=1')
    .then(res => {
      centers.value = res.data;
      plotMarkers();
      // Détection automatique de pénurie
      showToast.value = centers.value.some(center => (center.blood_stocks||[]).some(s => s.units_available <= 5));
      if (showToast.value) setTimeout(() => { showToast.value = false }, 5000);
    })
}

function plotMarkers(filterGroup = null) {
  if (!map) return;
  // Nettoyer les anciens marqueurs
  map.eachLayer(layer => {
    if (layer instanceof L.Marker) map.removeLayer(layer);
  });
  centers.value.forEach(center => {
    if (center.latitude && center.longitude) {
      // Calcul du stock global ou du groupe filtré
      let total = 0;
      if (filterGroup) {
        const stock = (center.blood_stocks || []).find(s => s.blood_group === filterGroup);
        total = stock ? stock.units_available : 0;
      } else {
        total = (center.blood_stocks || []).reduce((acc, s) => acc + (s.units_available || 0), 0);
      }
      let color = 'green';
      if (total <= 5) color = 'red';
      else if (total <= 15) color = 'orange';
      const icon = L.divIcon({
        className: `custom-marker ${color}${total<=5?' pulse':''}`,
        html: `<div style='background:${color};width:24px;height:24px;border-radius:50%;border:2px solid white;'></div>`
      });
      const marker = L.marker([center.latitude, center.longitude], {icon}).addTo(map);
      marker.on('click', () => { selectedCenter.value = center });
      marker.bindTooltip(center.name);
    }
  });
}


onMounted(() => {
  map = L.map('map').setView([14.6928, -17.4467], 7) // Dakar par défaut
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map)
  fetchCenters()
})

// Ajout d'un filtre rapide par groupe sanguin critique
const filterGroup = ref('');
function applyFilter() {
  plotMarkers(filterGroup.value || null);
}

async function exportMap() {
  const mapDiv = document.getElementById('map');
  if (!mapDiv) return;
  const canvas = await html2canvas(mapDiv);
  const link = document.createElement('a');
  link.download = 'carte_stocks_sang.png';
  link.href = canvas.toDataURL();
  link.click();
}

</script>

<style scoped>
#map {
  min-height: 400px;
}
.custom-marker.red > div {
  background: #dc2626 !important;
  box-shadow: 0 0 10px 2px #dc2626;
}
.custom-marker.orange > div {
  background: #f59e42 !important;
  box-shadow: 0 0 10px 2px #f59e42;
}
.custom-marker.green > div {
  background: #22c55e !important;
  box-shadow: 0 0 5px 1px #22c55e;
}
.pulse > div {
  animation: pulse 1.2s infinite;
}
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 #dc2626; }
  70% { box-shadow: 0 0 0 12px rgba(220,38,38,0); }
  100% { box-shadow: 0 0 0 0 #dc2626; }
}
.toast-alert {
  position: fixed;
  top: 2em;
  left: 50%;
  transform: translateX(-50%);
  background: #dc2626;
  color: #fff;
  padding: 1em 2em;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  z-index: 10000;
  font-weight: bold;
  font-size: 1.2em;
  animation: fadeInOut 5s linear;
}
@keyframes fadeInOut {
  0% { opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { opacity: 0; }
}
</style>
