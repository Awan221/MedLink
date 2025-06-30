<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-8">
    <div class="container mx-auto px-4">
      <!-- En-tête -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl shadow-lg">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path d="M12 4v16m8-8H4"/>
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-slate-800">Demandes d'inscription en attente</h2>
              <p class="text-slate-600">Gérez les demandes d'inscription des nouveaux utilisateurs</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <div class="text-sm text-slate-600">Total des demandes</div>
              <div class="text-2xl font-bold text-blue-700">{{ requests.length }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenu principal -->
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
        </div>
    <div v-else>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-slate-200">
              <thead class="bg-slate-50">
          <tr>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Email</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Nom</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Prénom</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Rôle</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Spécialité</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Téléphone</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Hôpital</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Région</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">N° licence</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Date licence</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Date demande</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Justificatif</th>
                  <th class="px-6 py-4 text-left text-xs font-medium text-slate-600 uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
              <tbody class="bg-white divide-y divide-slate-200">
                <tr v-for="req in requests" :key="req.id" class="hover:bg-slate-50 transition-colors">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.email }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.last_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.first_name }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 py-1 text-xs font-medium rounded-full" :class="{
                      'bg-blue-100 text-blue-800': req.role === 'MEDECIN',
                      'bg-purple-100 text-purple-800': req.role === 'SPECIALISTE',
                      'bg-green-100 text-green-800': req.role === 'RADIOLOGUE',
                      'bg-yellow-100 text-yellow-800': req.role === 'TECHNICIEN',
                      'bg-red-100 text-red-800': req.role === 'BANQUE_SANG',
                      'bg-slate-100 text-slate-800': req.role === 'AUTRE'
                    }">{{ req.role }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.specialite || '-' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.phone }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.hopital }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.region }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.numero_licence }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.date_licence ? formatDate(req.date_licence) : '-' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">{{ req.created_at ? formatDate(req.created_at) : '-' }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <a v-if="req.justificatif" :href="req.justificatif" target="_blank" 
                       class="text-blue-600 hover:text-blue-800 flex items-center gap-1">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                      </svg>
                      Télécharger
                    </a>
                    <span v-else class="text-slate-400">-</span>
            </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <div class="flex items-center gap-2">
                      <button @click="processRequest(req.id, 'approve')" 
                              class="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all shadow-sm hover:shadow">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M5 13l4 4L19 7"/>
                        </svg>
                        Valider
                      </button>
                      <button @click="processRequest(req.id, 'reject')" 
                              class="inline-flex items-center px-3 py-1.5 bg-gradient-to-r from-red-500 to-rose-600 text-white rounded-lg hover:from-red-600 hover:to-rose-700 transition-all shadow-sm hover:shadow">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path d="M6 18L18 6M6 6l12 12"/>
                        </svg>
                        Refuser
                      </button>
                    </div>
            </td>
          </tr>
        </tbody>
      </table>
          </div>
          <div v-if="requests.length === 0" class="text-center py-12">
            <div class="text-slate-400 text-lg">Aucune demande en attente</div>
          </div>
        </div>
      </div>

      <!-- Messages de notification -->
      <div v-if="message" class="fixed bottom-4 right-4 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-lg shadow-lg">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ message }}
        </div>
      </div>
      <div v-if="error" class="fixed bottom-4 right-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-lg">
        <div class="flex items-center">
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegistrationRequests',
  data() {
    return {
      requests: [],
      loading: false,
      message: '',
      error: ''
    }
  },
  methods: {
    fetchRequests() {
      this.loading = true;
      axios.get(`${process.env.VUE_APP_API_URL}auth/registration-requests/pending/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.requests = res.data;
        })
        .catch(() => {
          this.error = "Erreur lors du chargement des demandes.";
        })
        .finally(() => {
          this.loading = false;
        })
    },
    processRequest(id, action) {
      this.loading = true;
      axios.patch(`${process.env.VUE_APP_API_URL}auth/process-request/${id}/`, { action }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.message = res.data.detail;
          this.error = '';
          this.fetchRequests();
        })
        .catch(err => {
          this.error = err.response?.data?.detail || "Erreur lors du traitement de la demande.";
        })
        .finally(() => {
          this.loading = false;
        })
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('fr-FR');
    }
  },
  mounted() {
    this.fetchRequests();
  }
}
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
