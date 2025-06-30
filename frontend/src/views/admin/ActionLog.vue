<template>
  <div class="container mx-auto py-8">
    <h2 class="text-2xl font-bold mb-6">Audit / Logs d'actions</h2>
    <div class="mb-4 flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-sm font-semibold">Utilisateur</label>
        <input v-model="filters.user" @input="fetchLogs" class="border px-2 py-1 rounded" placeholder="ID utilisateur" />
      </div>
      <div>
        <label class="block text-sm font-semibold">Action</label>
        <input v-model="filters.action" @input="fetchLogs" class="border px-2 py-1 rounded" placeholder="Ex: DICOM_UPLOAD" />
      </div>
      <div>
        <label class="block text-sm font-semibold">Statut</label>
        <select v-model="filters.status" @change="fetchLogs" class="border px-2 py-1 rounded">
          <option value="">Tous</option>
          <option value="SUCCESS">Succès</option>
          <option value="FAIL">Échec</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-semibold">Recherche</label>
        <input v-model="filters.search" @input="fetchLogs" class="border px-2 py-1 rounded" placeholder="Message..." />
      </div>
      <button @click="resetFilters" class="ml-2 bg-gray-200 px-3 py-1 rounded">Réinitialiser</button>
    </div>
    <div v-if="loading" class="my-8 text-gray-500">Chargement...</div>
    <table v-else class="min-w-full bg-white border rounded shadow text-sm">
      <thead>
        <tr class="bg-gray-100">
          <th class="p-2 border">Date</th>
          <th class="p-2 border">Utilisateur</th>
          <th class="p-2 border">Action</th>
          <th class="p-2 border">Cible</th>
          <th class="p-2 border">Statut</th>
          <th class="p-2 border">Message</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="log in logs" :key="log.id">
          <td class="p-2 border whitespace-nowrap">{{ formatDate(log.timestamp) }}</td>
          <td class="p-2 border">{{ log.user_name || log.user }}</td>
          <td class="p-2 border">{{ log.action }}</td>
          <td class="p-2 border">{{ log.target_type }}<span v-if="log.target_id"> ({{ log.target_id }})</span></td>
          <td class="p-2 border">
            <span :class="log.status === 'SUCCESS' ? 'text-green-700' : 'text-red-700'">
              {{ log.status === 'SUCCESS' ? 'Succès' : 'Échec' }}
            </span>
          </td>
          <td class="p-2 border">{{ log.message }}</td>
        </tr>
        <tr v-if="logs.length === 0">
          <td class="p-2 border text-gray-500 text-center" colspan="6">Aucun log trouvé.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ActionLog',
  data() {
    return {
      logs: [],
      loading: false,
      filters: {
        user: '',
        action: '',
        status: '',
        search: ''
      }
    };
  },
  methods: {
    fetchLogs() {
      this.loading = true;
      let params = {};
      if (this.filters.user) params.user = this.filters.user;
      if (this.filters.action) params.action = this.filters.action;
      if (this.filters.status) params.status = this.filters.status;
      if (this.filters.search) params.search = this.filters.search;
      axios.get('/api/action-logs/', { params })
        .then(res => {
          this.logs = res.data;
        })
        .catch(() => {
          this.logs = [];
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetFilters() {
      this.filters = { user: '', action: '', status: '', search: '' };
      this.fetchLogs();
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
table th, table td { text-align: left; }
</style>
