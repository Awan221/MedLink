<template>
  <div class="mt-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-bold">Examens d'imagerie</h3>
      <router-link 
        :to="`/imaging/studies/new?patient_id=${patientId}`" 
        class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm"
      >
        <i class="fas fa-plus mr-1"></i> Nouvel examen DICOM
      </router-link>
    </div>
    
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-2 text-gray-600">Chargement des examens...</p>
    </div>
    
    <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">{{ error }}</p>
        </div>
      </div>
    </div>
    
    <div v-else-if="studies.length === 0" class="bg-gray-50 p-4 rounded-lg border border-gray-200 text-center">
      <p class="text-gray-500">Aucun examen d'imagerie trouvé pour ce patient.</p>
      <router-link 
        :to="`/imaging/studies/new?patient_id=${patientId}`" 
        class="text-blue-600 hover:underline mt-2 inline-block"
      >
        Ajouter le premier examen
      </router-link>
    </div>
    
    <div v-else class="space-y-4">
      <!-- Barre de recherche et filtres -->
      <div class="bg-white p-4 rounded-lg shadow-sm border border-gray-200">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div class="relative flex-1">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <i class="fas fa-search text-gray-400"></i>
            </div>
            <input
              type="text"
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Rechercher un examen..."
              v-model="searchQuery"
              @keyup.enter="handleSearch"
            >
          </div>
          <div class="flex items-center space-x-2">
            <select 
              v-model="statusFilter"
              @change="handleFilterChange"
              class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="">Tous les statuts</option>
              <option value="UPLOADED">Téléchargé</option>
              <option value="PENDING">En attente</option>
              <option value="ANALYZED">Analysé</option>
              <option value="REPORTED">Rapporté</option>
            </select>
            
            <select 
              v-model="sortBy"
              @change="handleSortChange"
              class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="-study_date">Date (récent au + ancien)</option>
              <option value="study_date">Date (ancien au + récent)</option>
              <option value="study_description">Description (A-Z)</option>
              <option value="-study_description">Description (Z-A)</option>
            </select>
            
            <button 
              @click="resetFilters"
              class="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <i class="fas fa-sync-alt mr-1"></i> Réinitialiser
            </button>
          </div>
        </div>
      </div>
      <div v-for="study in studies" :key="study.id" class="border rounded-lg overflow-hidden">
        <div class="bg-gray-50 px-4 py-3 border-b flex justify-between items-center">
          <div>
            <h4 class="font-medium">
              {{ study.study_description || 'Examen sans description' }}
              <span class="text-sm text-gray-500 ml-2">({{ study.modality }})</span>
            </h4>
            <div class="text-xs text-gray-500 mt-1">
              {{ formatDate(study.study_date) }} • {{ study.series?.length || 0 }} séries
            </div>
          </div>
          <span 
            :class="{
              'bg-blue-100 text-blue-800': study.status === 'UPLOADED',
              'bg-yellow-100 text-yellow-800': study.status === 'PENDING',
              'bg-green-100 text-green-800': study.status === 'ANALYZED',
              'bg-purple-100 text-purple-800': study.status === 'REPORTED',
            }" 
            class="px-2 py-1 text-xs font-medium rounded-full"
          >
            {{ getStatusLabel(study.status) }}
          </span>
        </div>
        
        <div class="p-4">
          <div class="flex justify-between items-center">
            <div>
              <span class="text-sm text-gray-600">Ajouté le {{ formatDateTime(study.uploaded_at) }}</span>
              <span v-if="study.uploaded_by_name" class="text-sm text-gray-600 ml-2">par {{ study.uploaded_by_name }}</span>
            </div>
            <div class="space-x-2">
              <router-link 
                :to="`/imaging/studies/${study.id}/view`" 
                class="text-blue-600 hover:text-blue-800 text-sm font-medium"
              >
                <i class="fas fa-eye mr-1"></i> Visualiser
              </router-link>
              <router-link 
                v-if="study.report"
                :to="`/imaging/reports/${study.report.id}`" 
                class="text-green-600 hover:text-green-800 text-sm font-medium ml-3"
              >
                <i class="fas fa-file-alt mr-1"></i> Voir le rapport
              </router-link>
            </div>
          </div>
          
          <!-- Aperçu des séries si disponible -->
          <div v-if="study.series && study.series.length > 0" class="mt-3 pt-3 border-t">
            <h5 class="text-sm font-medium text-gray-700 mb-2">Séries disponibles :</h5>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
              <div 
                v-for="series in study.series.slice(0, 4)" 
                :key="series.id"
                class="border rounded p-2 text-center text-xs"
              >
                <div class="font-medium truncate">
                  {{ series.series_description || `Série ${series.series_number}` }}
                </div>
                <div class="text-gray-500 text-xs mt-1">
                  {{ series.instances?.length || 0 }} images
                </div>
              </div>
              <div 
                v-if="study.series.length > 4"
                class="border-2 border-dashed rounded p-2 text-center text-xs flex items-center justify-center text-gray-500"
              >
                +{{ study.series.length - 4 }} autres
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Pagination -->
      <div v-if="pagination && pagination.totalPages > 1" class="mt-6 flex items-center justify-between px-4 py-3 bg-white border-t border-gray-200 sm:px-6 rounded-b-lg">
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Affichage de <span class="font-medium">{{ (pagination.page - 1) * pagination.pageSize + 1 }}</span>
              à <span class="font-medium">{{ Math.min(pagination.page * pagination.pageSize, pagination.count) }}</span>
              sur <span class="font-medium">{{ pagination.count }}</span> résultats
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                @click="handlePageChange(pagination.page - 1)"
                :disabled="pagination.page === 1"
                :class="{
                  'opacity-50 cursor-not-allowed': pagination.page === 1,
                  'hover:bg-gray-50': pagination.page > 1
                }"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500"
              >
                <span class="sr-only">Précédent</span>
                <i class="fas fa-chevron-left"></i>
              </button>
              
              <!-- Pages -->
              <template v-for="page in pagination.totalPages" :key="page">
                <button
                  v-if="showPageButton(page)"
                  @click="handlePageChange(page)"
                  :class="{
                    'z-10 bg-blue-50 border-blue-500 text-blue-600': pagination.page === page,
                    'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': pagination.page !== page
                  }"
                  class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
                >
                  {{ page }}
                </button>
                <span 
                  v-else-if="showEllipsis(page)"
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                >
                  ...
                </span>
              </template>
              
              <button
                @click="handlePageChange(pagination.page + 1)"
                :disabled="pagination.page === pagination.totalPages"
                :class="{
                  'opacity-50 cursor-not-allowed': pagination.page === pagination.totalPages,
                  'hover:bg-gray-50': pagination.page < pagination.totalPages
                }"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500"
              >
                <span class="sr-only">Suivant</span>
                <i class="fas fa-chevron-right"></i>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';

export default {
  name: 'PatientImagingTab',
  props: {
    patientId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 10,
      searchQuery: '',
      statusFilter: '',
      sortBy: '-study_date',
      filters: {
        search: '',
        status: '',
        ordering: '-study_date'
      },
      debounceTimer: null
    };
  },
  computed: {
    ...mapState('imaging', {
      studies: state => state.studies,
      loading: state => state.loading,
      error: state => state.error,
      pagination: state => state.pagination
    })
  },
  watch: {
    patientId: {
      immediate: true,
      handler() {
        this.loadPatientStudies();
      }
    }
  },
  methods: {
    ...mapActions('imaging', ['fetchPatientStudies', 'clearError']),
    
    async loadPatientStudies() {
      if (!this.patientId) return;
      
      try {
        // Préparer les paramètres de requête
        const params = {
          patient: this.patientId,
          page: this.currentPage,
          page_size: this.pageSize,
          ...(this.filters.search && { search: this.filters.search }),
          ...(this.filters.status && { status: this.filters.status }),
          ...(this.filters.ordering && { ordering: this.filters.ordering })
        };
        
        await this.fetchPatientStudies(params);
      } catch (err) {
        console.error('Erreur lors du chargement des examens:', err);
        // L'erreur est déjà gérée par le store
      }
    },
    
    handlePageChange(page) {
      this.currentPage = page;
      this.loadPatientStudies();
    },
    
    handleSearch() {
      // Annuler le timer précédent s'il existe
      if (this.debounceTimer) {
        clearTimeout(this.debounceTimer);
      }
      
      // Définir un nouveau timer pour retarder la recherche
      this.debounceTimer = setTimeout(() => {
        this.filters.search = this.searchQuery;
        this.currentPage = 1; // Réinitialiser à la première page
        this.loadPatientStudies();
      }, 500); // Délai de 500ms
    },
    
    handleFilterChange() {
      this.filters.status = this.statusFilter;
      this.currentPage = 1; // Réinitialiser à la première page
      this.loadPatientStudies();
    },
    
    handleSortChange() {
      this.filters.ordering = this.sortBy;
      this.loadPatientStudies();
    },
    
    resetFilters() {
      this.searchQuery = '';
      this.statusFilter = '';
      this.sortBy = '-study_date';
      this.filters = {
        search: '',
        status: '',
        ordering: '-study_date'
      };
      this.currentPage = 1;
      this.loadPatientStudies();
    },
    
    showPageButton(page) {
      // Afficher les 2 premières pages, les 2 dernières, et les pages autour de la page courante
      return (
        page === 1 ||
        page === 2 ||
        page === this.pagination.totalPages - 1 ||
        page === this.pagination.totalPages ||
        (page >= this.currentPage - 1 && page <= this.currentPage + 1)
      );
    },
    
    showEllipsis(page) {
      // Afficher les points de suspension si nécessaire
      return (
        page === 3 && this.currentPage > 3 ||
        page === this.pagination.totalPages - 2 && this.currentPage < this.pagination.totalPages - 2
      );
    },
    
    formatDate(dateStr) {
      if (!dateStr) return 'Date inconnue';
      const date = new Date(dateStr);
      return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },
    
    formatDateTime(datetimeStr) {
      if (!datetimeStr) return 'Date inconnue';
      const date = new Date(datetimeStr);
      return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    
    getStatusLabel(status) {
      const statusMap = {
        'UPLOADED': 'Téléchargé',
        'PENDING': 'En attente',
        'ANALYZED': 'Analysé',
        'REPORTED': 'Rapporté'
      };
      return statusMap[status] || status;
    }
  }
};
</script>
