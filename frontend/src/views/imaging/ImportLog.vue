<template>
  <div class="container mx-auto py-8">
    <h2 class="text-2xl font-bold mb-4">Suivi des Imports DICOM</h2>
    <div class="mb-4 flex gap-2 flex-wrap items-end">
      <input v-model="search" @input="fetchLogs" placeholder="Recherche patient, technicien, fichier..." class="border px-2 py-1 rounded w-64" />
      <div>
        <label class="block text-xs text-gray-500 mb-1">Du</label>
        <input v-model="dateFrom" type="date" class="border px-2 py-1 rounded" @change="fetchLogs" />
      </div>
      <div>
        <label class="block text-xs text-gray-500 mb-1">Au</label>
        <input v-model="dateTo" type="date" class="border px-2 py-1 rounded" @change="fetchLogs" />
      </div>
      <div>
        <label class="block text-xs text-gray-500 mb-1">Statut</label>
        <select v-model="status" class="border px-2 py-1 rounded" @change="fetchLogs">
          <option value="">Tous</option>
          <option value="UPLOADED">Succès</option>
          <option value="PENDING">En attente</option>
          <option value="FAILED">Erreur</option>
        </select>
      </div>
      <button @click="fetchLogs" class="bg-blue-600 text-white px-4 py-1 rounded">Actualiser</button>
    </div>
    <table class="min-w-full bg-white border">
      <thead>
        <tr>
          <th class="px-4 py-2">Date</th>
          <th class="px-4 py-2">Patient</th>
          <th class="px-4 py-2">Fichier</th>
          <th class="px-4 py-2">Technicien</th>
          <th class="px-4 py-2">Statut</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td>{{ formatDate(log.uploaded_at) }}</td>
          <td>{{ log.patient_name }} ({{ log.patient_medical_id }})</td>
          <td>{{ log.file_name }}</td>
          <td>{{ log.uploaded_by_name }}</td>
          <td>
            <span v-if="log.status === 'UPLOADED'" class="text-blue-600 font-semibold">Succès</span>
            <span v-else class="text-red-600 font-semibold">Erreur</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="logs.length === 0" class="mt-4 text-gray-500">Aucun import trouvé.</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ImportLog',
  data() {
    return {
      logs: [],
      search: '',
      dateFrom: '',
      dateTo: '',
      status: ''
    };
  },
  methods: {
    fetchLogs() {
      let params = [];
      if (this.search) params.push(`search=${encodeURIComponent(this.search)}`);
      if (this.dateFrom) params.push(`date_from=${this.dateFrom}`);
      if (this.dateTo) params.push(`date_to=${this.dateTo}`);
      if (this.status) params.push(`status=${this.status}`);
      let url = '/api/imaging/import-logs/';
      if (params.length) url += '?' + params.join('&');
      axios.get(url, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.logs = res.data;
        })
        .catch(() => {
          this.logs = [];
        });
    },
    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleString();
    }
  },
  mounted() {
    this.fetchLogs();
  }
};
</script>

<style scoped>
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #e2e8f0;
  padding: 8px 12px;
}
th {
  background: #f7fafc;
}
</style>
