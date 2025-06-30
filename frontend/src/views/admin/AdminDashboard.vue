<template>
  <div class="min-h-screen flex flex-col relative overflow-hidden bg-gradient-to-br from-blue-200 via-indigo-200 to-purple-200">
    <!-- Effet fond animé SVG - plus dynamique -->
    <svg class="absolute left-0 top-0 w-full h-full opacity-30 pointer-events-none z-0" style="filter: blur(48px);" aria-hidden="true">
      <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#2563eb" />
          <stop offset="100%" stop-color="#7c3aed" />
        </linearGradient>
      </defs>
      <circle cx="20%" cy="30%" r="180" fill="url(#grad1)" />
      <circle cx="80%" cy="70%" r="220" fill="url(#grad1)" />
    </svg>

    <!-- Header avec nouveau style -->
    <header class="sticky top-0 z-20 bg-white/95 backdrop-blur-lg text-slate-800 py-4 shadow-lg border-b border-blue-400">
      <div class="container mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-4">
          <div class="p-2.5 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl shadow-lg shadow-blue-500/40">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
          </div>
          <div>
            <h1 class="text-2xl md:text-3xl font-bold tracking-tight mb-1 flex items-center gap-2">
              <span>Bienvenue</span>
              <span v-if="userInfo && userInfo.first_name" class="text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700">{{ userInfo.first_name }} {{ userInfo.last_name }}</span>
              <span v-else class="text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-700">Administrateur</span>
            </h1>
            <div class="text-slate-600 text-sm font-medium">Gestion centralisée de la plateforme MedLink</div>
          </div>
        </div>

        <!-- Navigation principale avec nouveau style -->
        <nav class="flex flex-wrap justify-center gap-6">
          <router-link to="/admin/users" class="flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-indigo-700 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17 20h5v-2a4 4 0 0 0-3-3.87"/><path d="M9 20H4v-2a4 4 0 0 1 3-3.87"/><circle cx="9" cy="7" r="4"/><circle cx="17" cy="7" r="4"/></svg>
            Utilisateurs
          </router-link>
          <router-link to="/admin/inscriptions" class="flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-indigo-700 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M12 4v16m8-8H4"/></svg>
            Inscriptions
          </router-link>
          <router-link to="/admin/alerts" class="flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-indigo-700 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 13V8a6 6 0 1 0-12 0v5a2 2 0 0 1-2 2h16a2 2 0 0 1-2-2z"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            Alertes
          </router-link>
          <router-link to="/admin/roles" class="flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-indigo-700 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M8 12h8"/></svg>
            Rôles
          </router-link>
          <router-link v-if="userRole === 'SUPER_ADMIN'" to="/admin/permissions" class="flex items-center gap-2 text-sm font-medium text-blue-700 hover:text-indigo-700 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M8 12h8"/></svg>
            Permissions
          </router-link>
        </nav>


      </div>
    </header>

    <main class="flex-1 container mx-auto px-6 py-8">
      <!-- Widgets principaux avec nouvelle disposition -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
        <!-- Widget Stats -->
        <router-link to="/admin/inscriptions" class="col-span-1 group">
          <div class="widget-card bg-gradient-to-br from-blue-600 to-indigo-700 h-full">
            <div class="flex items-center gap-3 mb-4">
              <div class="p-2.5 bg-white/20 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"/></svg>
              </div>
              <span class="text-lg font-semibold text-white">Statistiques</span>
            </div>
            <div v-if="loadingStats" class="flex justify-center py-8"><span class="loader"></span></div>
            <StatsWidget v-else-if="stats && stats.length" :stats="stats" />
          </div>
        </router-link>

        <!-- Widget Alertes -->
        <router-link to="/admin/alerts" class="col-span-1 group">
          <div class="widget-card bg-gradient-to-br from-red-600 to-pink-700 h-full">
            <div class="flex items-center gap-3 mb-4">
              <div class="p-2.5 bg-white/20 rounded-xl">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 13V8a6 6 0 1 0-12 0v5a2 2 0 0 1-2 2h16a2 2 0 0 1-2-2z"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
              </div>
              <span class="text-lg font-semibold text-white">Alertes</span>
            </div>
            <div v-if="loadingAlerts" class="flex justify-center py-8"><span class="loader"></span></div>
            <AlertsWidget v-else-if="alerts" :alerts="alerts.slice(0,3)" />
          </div>
        </router-link>
      </div>

      <!-- Widgets détaillés avec nouvelle disposition -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Inscriptions en attente -->
        <section class="widget-card bg-white">
          <h3 class="text-lg font-bold mb-4 flex items-center gap-2 text-slate-800">
            <div class="p-2.5 bg-blue-200 rounded-xl">
              <svg class="w-5 h-5 text-blue-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/></svg>
            </div>
            Inscriptions en attente
            <router-link to="/admin/inscriptions" class="ml-auto text-blue-700 hover:text-indigo-700 text-sm font-medium">Gérer</router-link>
          </h3>
          <div v-if="loadingPending" class="flex justify-center py-8"><span class="loader"></span></div>
          <PendingRegistrations v-else-if="pendingRequests" :requests="pendingRequests" />
        </section>

        <!-- Alertes médicales -->
        <section class="widget-card bg-white">
          <h3 class="text-lg font-bold mb-4 flex items-center gap-2 text-slate-800">
            <div class="p-2.5 bg-red-200 rounded-xl">
              <svg class="w-5 h-5 text-red-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 13V8a6 6 0 1 0-12 0v5a2 2 0 0 1-2 2h16a2 2 0 0 1-2-2z"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
            </div>
            Alertes médicales
            <router-link to="/admin/alerts" class="ml-auto text-blue-700 hover:text-indigo-700 text-sm font-medium">Tout voir</router-link>
          </h3>
          <div v-if="loadingAlerts" class="flex justify-center py-8"><span class="loader"></span></div>
          <AlertsWidget v-else-if="alerts" :alerts="alerts" />
        </section>
      </div>
    </main>

    <!-- Footer avec nouveau style -->
    <footer class="bg-gradient-to-r from-blue-800 to-indigo-900 text-white text-center py-6 mt-12">
      <span>&copy; 2025 MedLink - Dashboard Administrateur</span>
    </footer>
  </div>
</template>

<style scoped>
.widget-card {
  border-radius: 1.25rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(226, 232, 240, 0.5);
  padding: 1.75rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(12px);
}

.widget-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  transform: translateY(-0.25rem);
}

.loader {
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid #ffffff;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

<script setup>
import PendingRegistrations from './PendingRegistrations.vue'
import { ref, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import axios from 'axios'
import StatsWidget from '@/components/admin/StatsWidget.vue'
import AlertsWidget from '@/components/admin/AlertsWidget.vue'

const store = useStore()
const userInfo = computed(() => store.getters['auth/userInfo'])
const userRole = computed(() => store.getters['auth/role'])

const stats = ref([])
const loadingStats = ref(true)
const loadingPending = ref(true)
const loadingAlerts = ref(true)
const loadingActivity = ref(true)
const pendingRequests = ref([])
const alerts = ref([])
const recentActivity = ref([])

async function fetchStats() {
  loadingStats.value = true
  try {
    const res = await axios.get(`${process.env.VUE_APP_API_URL}auth/admin/stats/`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    stats.value = [
      { name: 'Demandes totales', value: res.data.total, icon: 'UserIcon' },
      { name: 'En attente', value: res.data.pending, icon: 'ClockIcon' },
      { name: 'Approuvées', value: res.data.approved, icon: 'CheckIcon' },
      { name: 'Rejetées', value: res.data.rejected, icon: 'XIcon' },
    ]
  } catch (error) {
    console.error('Error fetching stats:', error)
  } finally {
    loadingStats.value = false
  }
}

async function fetchPendingRequests() {
  loadingPending.value = true
  try {
    const res = await axios.get(`${process.env.VUE_APP_API_URL}auth/registration-requests/pending/`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    pendingRequests.value = res.data
  } catch (error) {
    console.error('Error fetching pending requests:', error)
  } finally {
    loadingPending.value = false
  }
}

async function fetchAlerts() {
  loadingAlerts.value = true
  try {
    const res = await axios.get(`${process.env.VUE_APP_API_URL}auth/admin/alerts/`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    alerts.value = res.data.alerts || []
  } catch (error) {
    console.error('Error fetching alerts:', error)
  } finally {
    loadingAlerts.value = false
  }
}

async function fetchRecentActivity() {
  loadingActivity.value = true
  try {
    const res = await axios.get(`${process.env.VUE_APP_API_URL}auth/admin/recent-activity/`, { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
    recentActivity.value = res.data
  } catch (error) {
    console.error('Error fetching recent activity:', error)
  } finally {
    loadingActivity.value = false
  }
}

onMounted(async () => {
  await Promise.all([
    fetchStats(),
    fetchPendingRequests(),
    fetchAlerts(),
    fetchRecentActivity()
  ])
})
</script>
