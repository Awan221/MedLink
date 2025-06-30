<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 via-orange-50 to-red-50 py-8">
    <div class="container mx-auto px-4">
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-gradient-to-br from-yellow-400 to-red-500 rounded-xl shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-2xl font-bold text-slate-800">Alertes & Notifications</h2>
            <p class="text-slate-600">Toutes les alertes importantes du système</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
        <div v-if="loading" class="flex justify-center items-center py-12">
          <div class="animate-spin rounded-full h-12 w-12 border-4 border-yellow-500 border-t-transparent"></div>
        </div>
        <div v-else>
          <div v-if="alerts.length === 0" class="text-center py-12">
            <div class="text-slate-400 text-lg">Aucune alerte pour le moment</div>
          </div>
          <ul v-else class="divide-y divide-slate-200">
            <li v-for="alert in alerts" :key="alert.id" class="p-6 hover:bg-yellow-50 transition-colors flex gap-4 items-center">
              <div>
                <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full"
                      :class="alert.level === 'critical' ? 'bg-red-100 text-red-800' : alert.level === 'warning' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'">
                  {{ alert.level.toUpperCase() }}
                </span>
              </div>
              <div class="flex-1">
                <div class="font-semibold text-slate-900">{{ alert.title }}</div>
                <div class="text-slate-700 text-sm mt-1">{{ alert.message }}</div>
                <div class="text-xs text-slate-400 mt-2">{{ formatDate(alert.created_at) }}</div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminAlerts',
  data() {
    return {
      alerts: [],
      loading: false
    }
  },
  mounted() {
    this.fetchAlerts();
  },
  methods: {
    fetchAlerts() {
      this.loading = true;
      // Remplacer l'URL par l'endpoint réel de vos alertes si disponible
      fetch(`${process.env.VUE_APP_API_URL}auth/admin/alerts/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(res => res.json())
        .then(data => {
          this.alerts = Array.isArray(data) ? data : (data.results || []);
        })
        .catch(() => {
          this.alerts = [];
        })
        .finally(() => {
          this.loading = false;
        })
    },
    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return date.toLocaleString('fr-FR', { dateStyle: 'medium', timeStyle: 'short' });
    }
  }
}
</script>

<style scoped>
</style>