<template>
  <div class="study-detail">
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-2 text-gray-600">Chargement de l'étude...</p>
    </div>

    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Erreur !</strong>
      <span class="block sm:inline">{{ error }}</span>
    </div>

    <div v-else>
      <!-- En-tête avec les informations de base -->
      <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
        <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              {{ study.study_description || 'Étude DICOM' }}
            </h3>
            <p class="mt-1 max-w-2xl text-sm text-gray-500">
              ID: {{ study.id }}
            </p>
          </div>
          <div class="flex space-x-2">
            <router-link 
              :to="{ name: 'StudyViewer', params: { id: study.id } }" 
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <EyeIcon class="-ml-1 mr-2 h-5 w-5" />
              Visualiser
            </router-link>
            <button 
              @click="downloadStudy"
              class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <ArrowDownTrayIcon class="-ml-1 mr-2 h-5 w-5 text-gray-500" />
              Télécharger
            </button>
          </div>
        </div>
        <div class="border-t border-gray-200 px-4 py-5 sm:px-6">
          <dl class="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Patient</dt>
              <dd class="mt-1 text-sm text-gray-900">
                <router-link 
                  :to="{ name: 'PatientDetail', params: { id: study.patient } }"
                  class="text-blue-600 hover:text-blue-800 hover:underline"
                >
                  {{ study.patient_name }}
                </router-link>
              </dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Date d'étude</dt>
              <dd class="mt-1 text-sm text-gray-900">
                {{ formatDate(study.study_date) }}
                <span v-if="study.study_time"> à {{ formatTime(study.study_time) }}</span>
              </dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Modalité</dt>
              <dd class="mt-1 text-sm text-gray-900">{{ study.modality }}</dd>
            </div>
            <div class="sm:col-span-1">
              <dt class="text-sm font-medium text-gray-500">Statut</dt>
              <dd class="mt-1">
                <span 
                  :class="{
                    'px-2 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                    'bg-green-100 text-green-800': study.status === 'COMPLETED',
                    'bg-yellow-100 text-yellow-800': study.status === 'IN_PROGRESS',
                    'bg-blue-100 text-blue-800': study.status === 'UPLOADED',
                    'bg-gray-100 text-gray-800': !study.status
                  }"
                >
                  {{ getStatusLabel(study.status) }}
                </span>
              </dd>
            </div>
            <div v-if="study.study_instance_uid" class="sm:col-span-2">
              <dt class="text-sm font-medium text-gray-500">Study Instance UID</dt>
              <dd class="mt-1 text-sm text-gray-900 font-mono break-all">{{ study.study_instance_uid }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Liste des séries -->
      <div class="bg-white shadow overflow-hidden sm:rounded-lg mb-6">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Séries DICOM
          </h3>
        </div>
        
        <div v-if="seriesLoading" class="p-4 text-center">
          <div class="animate-pulse flex space-x-4">
            <div class="flex-1 space-y-4 py-1">
              <div class="h-4 bg-gray-200 rounded w-3/4"></div>
              <div class="space-y-2">
                <div class="h-4 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-else-if="seriesError" class="bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" aria-hidden="true" />
            </div>
            <div class="ml-3">
              <p class="text-sm text-yellow-700">
                Impossible de charger les séries: {{ seriesError }}
              </p>
            </div>
          </div>
        </div>
        
        <ul v-else-if="Array.isArray(series) && series.length > 0" class="divide-y divide-gray-200">
          <li v-for="serie in series" :key="serie.id" class="px-4 py-4 sm:px-6 hover:bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                  <span class="text-blue-600 font-medium">{{ serie.modality || 'SR' }}</span>
                </div>
                <div class="ml-4">
                  <div class="text-sm font-medium text-gray-900">
                    {{ serie.series_description || 'Sans description' }}
                  </div>
                  <div class="text-sm text-gray-500">
                    {{ serie.instances_count || 0 }} instances
                  </div>
                </div>
              </div>
              <div class="ml-2 flex-shrink-0 flex">
                <router-link 
                  :to="{ name: 'StudyViewer', query: { series: serie.id } }" 
                  class="ml-2 inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Voir
                </router-link>
              </div>
            </div>
          </li>
        </ul>
        
        <div v-else class="text-center py-4 text-gray-500">
          Aucune série trouvée pour cette étude.
        </div>
      </div>
      
      <!-- Rapports associés -->
      <div v-if="report" class="bg-white shadow overflow-hidden sm:rounded-lg">
        <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
          <h3 class="text-lg leading-6 font-medium text-gray-900">
            Rapport radiologique
          </h3>
        </div>
        <div class="px-4 py-5 sm:p-6">
          <div class="prose max-w-none">
            <h4>Trouvées:</h4>
            <p class="whitespace-pre-line">{{ report.findings }}</p>
            
            <h4 class="mt-4">Impression:</h4>
            <p class="whitespace-pre-line">{{ report.impression }}</p>
            
            <div v-if="report.recommendations" class="mt-4">
              <h4>Recommandations:</h4>
              <p class="whitespace-pre-line">{{ report.recommendations }}</p>
            </div>
            
            <div class="mt-6 pt-6 border-t border-gray-200 text-sm text-gray-500">
              <p>Rapport créé le {{ formatDate(report.created_at) }}</p>
              <p v-if="report.updated_at !== report.created_at">
                Dernière mise à jour le {{ formatDate(report.updated_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { 
  EyeIcon, 
  ArrowDownTrayIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'StudyDetail',
  
  components: {
    EyeIcon,
    ArrowDownTrayIcon,
    ExclamationTriangleIcon
  },
  
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    
    const loading = ref(true);
    const error = ref(null);
    const study = ref({});
    const series = ref([]);
    const seriesLoading = ref(false);
    const seriesError = ref(null);
    const report = ref(null);
    
    const fetchStudy = async () => {
      try {
        loading.value = true;
        error.value = null;
        
        const response = await store.dispatch('imaging/fetchStudy', route.params.id);
        study.value = response.data || {};
        
        // Charger les séries après avoir récupéré l'étude
        await fetchSeries();
        
        // Vérifier s'il y a un rapport associé
        if (response.data?.report) {
          report.value = response.data.report;
        }
      } catch (err) {
        console.error('Erreur lors du chargement de l\'étude:', err);
        error.value = 'Impossible de charger les détails de l\'étude. Veuillez réessayer.';
        // Réinitialiser les séries en cas d'erreur
        series.value = [];
      } finally {
        loading.value = false;
      }
    };
    
    const fetchSeries = async () => {
      try {
        seriesLoading.value = true;
        seriesError.value = null;
        
        const response = await store.dispatch('imaging/fetchStudySeries', route.params.id);
        series.value = response.data;
      } catch (err) {
        console.error('Erreur lors du chargement des séries:', err);
        seriesError.value = 'Impossible de charger les séries DICOM.';
      } finally {
        seriesLoading.value = false;
      }
    };
    
    const downloadStudy = async () => {
      try {
        await store.dispatch('imaging/downloadStudy', {
          studyId: route.params.id,
          fileName: `etude-${route.params.id}.zip`
        });
      } catch (err) {
        console.error('Erreur lors du téléchargement:', err);
        // Gérer l'erreur (par exemple, afficher un message à l'utilisateur)
      }
    };
    
    const formatDate = (dateString) => {
      if (!dateString) return 'Non spécifié';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    };
    
    const formatTime = (timeString) => {
      if (!timeString) return '';
      return new Date(`1970-01-01T${timeString}`).toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    };
    
    const getStatusLabel = (status) => {
      const statusMap = {
        'UPLOADED': 'Téléchargé',
        'IN_PROGRESS': 'En cours',
        'COMPLETED': 'Terminé',
        'REVIEWED': 'Révisé',
        'ARCHIVED': 'Archivé'
      };
      return statusMap[status] || status || 'Inconnu';
    };
    
    onMounted(() => {
      fetchStudy();
    });
    
    return {
      loading,
      error,
      study,
      series,
      seriesLoading,
      seriesError,
      report,
      downloadStudy,
      formatDate,
      formatTime,
      getStatusLabel,
      router
    };
  }
};
</script>

<style scoped>
.study-detail {
  @apply bg-gray-50 min-h-screen py-6 px-4 sm:px-6 lg:px-8;
}

.prose h4 {
  @apply text-sm font-medium text-gray-900 mt-4 mb-2;
}

.prose p {
  @apply text-gray-600;
}

/* Animation de chargement */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Animation de pulsation pour le chargement */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: .5; }
}

.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
