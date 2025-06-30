<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100 py-8">
    <div class="container mx-auto px-4">
      <!-- En-tête amélioré -->
      <div class="bg-white rounded-3xl shadow-2xl p-8 mb-10 flex flex-col md:flex-row items-center justify-between gap-6 border-b-4 border-indigo-200">
        <div class="flex items-center gap-5">
          <div class="p-4 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl shadow-lg flex items-center justify-center">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div>
            <h2 class="text-3xl font-extrabold text-slate-800 tracking-tight">Demandes d'inscription du personnel médical</h2>
            <p class="text-slate-500 text-lg mt-1">Gérez les demandes d'inscription des nouveaux utilisateurs</p>
          </div>
        </div>
        <div class="flex flex-col items-end">
          <div class="text-sm text-slate-500">Total des demandes</div>
          <div class="text-3xl font-extrabold text-blue-700">{{ requests.length }}</div>
        </div>
      </div>

      <!-- Contenu principal sous forme de cartes -->
      <div class="bg-transparent">
        <div v-if="loading" class="flex justify-center items-center py-20">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent"></div>
        </div>
        <div v-else>
          <div v-if="requests.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <div v-for="req in requests.filter(r => r)" :key="req.id" class="bg-white rounded-2xl shadow-xl p-6 flex flex-col gap-4 border-t-4 border-indigo-200 hover:shadow-2xl transition-shadow">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center text-white text-2xl font-bold shadow">
                  <span>{{ req.first_name.charAt(0) }}{{ req.last_name.charAt(0) }}</span>
                </div>
                <div>
                  <div class="text-lg font-bold text-slate-800">{{ req.first_name }} {{ req.last_name }}</div>
                  <div class="text-sm text-slate-500">{{ req.email }}</div>
                </div>
              </div>
              <div class="flex flex-wrap gap-2 mt-2">
                <span class="inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full" :class="{
                  'bg-blue-100 text-blue-800': req.role === 'MEDECIN',
                  'bg-purple-100 text-purple-800': req.role === 'SPECIALISTE',
                  'bg-green-100 text-green-800': req.role === 'RADIOLOGUE',
                  'bg-yellow-100 text-yellow-800': req.role === 'TECHNICIEN',
                  'bg-red-100 text-red-800': req.role === 'BANQUE_SANG',
                  'bg-slate-100 text-slate-800': req.role === 'AUTRE'
                }">
                  <svg v-if="req.role === 'MEDECIN'" class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"/></svg>
                  {{ req.role }}
                </span>
                <span v-if="req.specialite" class="inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 17l4-4 4 4m0-8H8"/></svg>
                  {{ req.specialite }}
                </span>
                <span class="inline-flex items-center px-3 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-600">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                  {{ formatDate(req.created_at) }}
                </span>
              </div>
              <!-- Champs supplémentaires -->
              <div class="flex flex-col gap-1 text-sm text-slate-700 mt-2">
                <div><span class="font-semibold">Téléphone:</span> {{ req.phone }}</div>
                <div><span class="font-semibold">Hôpital:</span> {{ req.hopital }}</div>
                <div><span class="font-semibold">Région:</span> {{ req.region }}</div>
                <div><span class="font-semibold">N° Licence:</span> {{ req.numero_licence }}</div>
                <div><span class="font-semibold">Date licence:</span> {{ req.date_licence }}</div>
              </div>
              <!-- Affichage du justificatif (un seul fichier) -->
              <div class="flex flex-col gap-1 mt-2">
                <div v-if="req.documents">
                  <a :href="getDocUrl(req.documents)" target="_blank" class="inline-flex items-center gap-1 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                    </svg>
                    Télécharger le justificatif
                  </a>
                </div>
                <span v-else class="text-slate-400 text-sm">Aucun justificatif</span>
              </div>
              <div class="flex gap-3 mt-4">
                <button @click="processRequest(req.id, 'approve')"
                        class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-semibold shadow hover:from-green-600 hover:to-emerald-700 hover:scale-105 transition-all">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M5 13l4 4L19 7"/>
                  </svg>
                  Valider
                </button>
                <button @click="processRequest(req.id, 'reject')"
                        class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-red-500 to-rose-600 text-white rounded-xl font-semibold shadow hover:from-red-600 hover:to-rose-700 hover:scale-105 transition-all">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M6 18L18 6M6 6l12 12"/>
                  </svg>
                  Refuser
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-20">
            <div class="text-slate-400 text-xl font-semibold">Aucune demande en attente</div>
          </div>
        </div>
      </div>

      <!-- Messages de notification améliorés -->
      <transition name="fade">
        <div v-if="message" class="fixed bottom-6 right-6 bg-green-100 border-l-4 border-green-500 text-green-700 p-5 rounded-2xl shadow-2xl flex items-center gap-3 animate-bounce-in">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="font-semibold">{{ message }}</span>
        </div>
      </transition>
      <transition name="fade">
        <div v-if="error" class="fixed bottom-6 right-6 bg-red-100 border-l-4 border-red-500 text-red-700 p-5 rounded-2xl shadow-2xl flex items-center gap-3 animate-bounce-in">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <span class="font-semibold">{{ error }}</span>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminRegistrationDashboard',
  data() {
    return {
      requests: [],
      loading: true,
      message: '',
      error: '',
      messageType: 'success'
    };
  },
  methods: {
    fetchRequests() {
      this.loading = true;
      axios.get(`${process.env.VUE_APP_API_URL}auth/registration-requests/pending/`, { 
        headers: this.authHeader() 
      })
        .then(res => {
          this.requests = Array.isArray(res.data.results) ? res.data.results : (Array.isArray(res.data) ? res.data : []);
          console.log('Réponses API demandes:', this.requests);
        })
        .catch(() => {
          this.error = "Erreur lors du chargement des demandes.";
          this.messageType = 'error';
        })
        .finally(() => this.loading = false);
    },
    processRequest(id, action) {
      const note = prompt(action === 'approve' ? 'Note de validation (optionnel)' : 'Motif du refus (optionnel)');
      this.loading = true;
      axios.patch(`${process.env.VUE_APP_API_URL}auth/registration-requests/${id}/process/`, 
        { status: action === 'approve' ? 'approved' : 'rejected', note }, 
        { headers: this.authHeader() }
      )
        .then(() => {
          this.message = action === 'approve' ? 'Demande validée avec succès !' : 'Demande refusée.';
          this.messageType = 'success';
          this.error = '';
          this.fetchRequests();
        })
        .catch(() => {
          this.error = "Erreur lors du traitement de la demande.";
          this.messageType = 'error';
          this.message = '';
        })
        .finally(() => this.loading = false);
    },
    getDocUrl(path) {
      return `${process.env.VUE_APP_API_URL}media/${path}`;
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleString('fr-FR');
    },
    authHeader() {
      const token = localStorage.getItem('access');
      return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
  },
  mounted() {
    this.fetchRequests();
  }
};
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

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

@keyframes bounce-in {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  60% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(1);
  }
}
.animate-bounce-in {
  animation: bounce-in 0.6s;
}
</style>
