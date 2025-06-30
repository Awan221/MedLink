<template>
  <div class="p-6 max-w-4xl mx-auto">
    <h2 class="text-2xl font-bold mb-4">Gestion des stocks de sang</h2>
    <div class="mb-6 flex flex-wrap gap-4">
      <select v-model="form.center" class="border rounded px-2 py-1">
        <option value="" disabled>Choisir un centre</option>
        <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }} ({{ center.region }})</option>
      </select>
      <select v-model="form.blood_group" class="border rounded px-2 py-1">
        <option value="" disabled>Groupe sanguin</option>
        <option v-for="g in bloodGroups" :key="g" :value="g">{{ g }}</option>
      </select>
      <input v-model.number="form.units_available" type="number" min="0" class="border rounded px-2 py-1 w-32" placeholder="Quantité" />
      <button @click="saveStock" class="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700">{{ editing ? 'Mettre à jour' : 'Ajouter' }}</button>
      <button v-if="editing" @click="resetForm" class="ml-2 px-4 py-1 rounded border">Annuler</button>
    </div>
    <table class="min-w-full bg-white border">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 border">Centre</th>
          <th class="p-2 border">Groupe</th>
          <th class="p-2 border">Quantité</th>
          <th class="p-2 border">Dernière mise à jour</th>
          <th class="p-2 border">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in stocks" :key="stock.id">
          <td class="p-2 border">{{ getCenterName(stock.center) }}</td>
          <td class="p-2 border">{{ stock.blood_group }}</td>
          <td class="p-2 border">{{ stock.units_available }}</td>
          <td class="p-2 border">{{ formatDate(stock.last_updated) }}</td>
          <td class="p-2 border">
            <button @click="editStock(stock)" class="text-blue-600 hover:underline">Éditer</button>
            <button @click="deleteStock(stock.id)" class="ml-2 text-red-600 hover:underline">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'

const stocks = ref([])
const centers = ref([])
const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
const form = ref({ id: null, center: '', blood_group: '', units_available: 0 })
const editing = ref(false)
const toast = useToast()

function fetchCenters() {
  axios.get('/api/blood-bank/centers/')
    .then(res => { centers.value = res.data })
    .catch(() => toast.error('Erreur lors du chargement des centres'))
}

function fetchStocks() {
  axios.get('/api/blood-bank/inventory/')
    .then(res => { stocks.value = res.data })
    .catch(() => toast.error('Erreur lors du chargement des stocks'))
}

function saveStock() {
  if (!form.value.center || !form.value.blood_group) {
    toast.error('Centre et groupe sanguin obligatoires')
    return
  }
  const payload = {
    center: form.value.center,
    blood_type: form.value.blood_group,
    quantity_ml: form.value.units_available * 450 // Convertir en ml (1 unité = ~450ml)
  }
  if (editing.value && form.value.id) {
    axios.put(`/api/blood-bank/inventory/${form.value.id}/`, payload)
      .then(() => {
        toast.success('Stock mis à jour')
        fetchStocks()
        resetForm()
      })
      .catch(() => toast.error('Erreur lors de la mise à jour'))
  } else {
    axios.post('/api/blood-bank/inventory/', payload)
      .then(() => {
        toast.success('Stock ajouté')
        fetchStocks()
        resetForm()
      })
      .catch(() => toast.error('Erreur lors de l\'ajout'))
  }
}

function editStock(stock) {
  form.value = { ...stock }
  editing.value = true
}

function deleteStock(id) {
  if (confirm('Supprimer ce stock ?')) {
    axios.delete(`/api/blood-bank/inventory/${id}/`)
      .then(() => {
        toast.success('Stock supprimé')
        fetchStocks()
      })
      .catch(() => toast.error('Erreur lors de la suppression'))
  }
}

function resetForm() {
  form.value = { id: null, center: '', blood_group: '', units_available: 0 }
  editing.value = false
}

function getCenterName(centerId) {
  const c = centers.value.find(c => c.id === centerId)
  return c ? c.name : ''
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('fr-FR')
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
