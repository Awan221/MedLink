<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white">
    <!-- Contenu principal -->
    <main class="pb-12">
      <!-- En-tête avec image de fond -->
      <div class="bg-blue-700 text-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <h1 class="text-4xl font-extrabold tracking-tight sm:text-5xl lg:text-6xl">
            Documentation Médicale
          </h1>
          <p class="mt-3 max-w-3xl text-xl text-blue-100">
            Accédez à des informations médicales fiables et détaillées sur les principales maladies
          </p>
        </div>
      </div>
      
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    
        <!-- Barre de recherche et filtres -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div class="flex flex-col md:flex-row gap-4">
            <div class="relative flex-1">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
                </svg>
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Rechercher une maladie, un symptôme..."
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition duration-150"
                @input="onSearchInput"
              />
              <div v-if="loading" class="absolute right-3 top-3.5">
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
              </div>
            </div>
            <div class="w-full md:w-64">
              <select
                v-model="selectedCategory"
                class="block w-full pl-3 pr-10 py-3 text-base border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent rounded-lg bg-white"
                @change="onCategoryChange"
              >
                <option value="">Toutes les catégories</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>
          </div>
          <div v-if="selectedCategory || searchQuery" class="mt-4 flex justify-end">
            <button
              @click="resetFilters"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
            >
              <svg class="-ml-1 mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Réinitialiser les filtres
            </button>
          </div>
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm">{{ error }}</p>
            </div>
          </div>
        </div>

        <!-- Chargement -->
        <div v-if="loading && diseases.length === 0" class="flex justify-center py-16">
          <div class="text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
            <p class="text-gray-600">Chargement des maladies...</p>
          </div>
        </div>

        <!-- Aucun résultat -->
        <div v-else-if="showNoResults" class="text-center py-12">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="mt-2 text-lg font-medium text-gray-900">Aucun résultat trouvé</h3>
          <p class="mt-1 text-gray-500">Essayez de modifier vos critères de recherche ou de réinitialiser les filtres.</p>
          <div class="mt-6">
            <button
              @click="resetFilters"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Réinitialiser les filtres
            </button>
          </div>
        </div>

        <!-- Liste des maladies -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <router-link
            v-for="disease in diseases"
            :key="disease.id"
            :to="{ name: 'DiseaseDetail', params: { slug: disease.slug } }"
            class="group bg-white rounded-xl shadow-sm border border-gray-100 hover:shadow-md hover:border-blue-100 transition-all duration-300 overflow-hidden transform hover:-translate-y-1 flex flex-col h-full"
          >
            <div class="p-6 flex-1 flex flex-col">
              <div class="flex items-start justify-between mb-4">
                <h2 class="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors duration-200">
                  {{ disease.name }}
                  <span v-if="disease.is_emergency" class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                    Urgence
                  </span>
                </h2>
                <span 
                  v-if="disease.category" 
                  class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium" 
                  :class="getCategoryClass(disease.category.name)"
                >
                  {{ disease.category.name }}
                </span>
              </div>
              
              <p class="text-gray-600 mb-4 flex-grow">{{ disease.short_description }}</p>
              
              <div class="mt-4 space-y-3">
                <div>
                  <h3 class="text-sm font-medium text-gray-900 flex items-center">
                    <svg class="flex-shrink-0 mr-1.5 h-4 w-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Symptômes principaux
                  </h3>
                  <ul class="mt-1 space-y-1">
                    <li v-for="(symptom, index) in disease.symptoms.slice(0, 3)" :key="index" class="flex items-start">
                      <svg class="flex-shrink-0 h-4 w-4 text-blue-500 mt-0.5 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span class="text-sm text-gray-600">{{ symptom }}</span>
                    </li>
                    <li v-if="disease.symptoms.length > 3" class="text-xs text-gray-500 mt-1">
                      + {{ disease.symptoms.length - 3 }} autre(s) symptôme(s)
                    </li>
                  </ul>
                </div>
                
                <div v-if="disease.severity" class="mt-2">
                  <div class="flex items-center justify-between text-xs text-gray-500 mb-1">
                    <span>Niveau de gravité</span>
                    <span class="font-medium" :class="{
                      'text-green-600': disease.severity === 'L',
                      'text-yellow-600': disease.severity === 'M',
                      'text-red-600': disease.severity === 'S'
                    }">
                      {{ getSeverityText(disease.severity) }}
                    </span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-1.5">
                    <div 
                      class="h-1.5 rounded-full" 
                      :class="{
                        'bg-green-500 w-1/3': disease.severity === 'L',
                        'bg-yellow-500 w-2/3': disease.severity === 'M',
                        'bg-red-500 w-full': disease.severity === 'S'
                      }"
                    ></div>
                  </div>
                </div>
              </div>
              
              <div class="mt-4 pt-4 border-t border-gray-100">
                <div class="flex items-center justify-between">
                  <span class="text-sm text-gray-500">En savoir plus</span>
                  <svg class="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </router-link>
        </div>

        <!-- Pagination -->
        <div v-if="showPagination" class="mt-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="flex flex-col sm:flex-row justify-between items-center space-y-4 sm:space-y-0">
            <div class="text-sm text-gray-600">
              Page {{ pagination.current }} sur {{ pagination.last_page }}
            </div>
            <div class="flex space-x-1">
              <button
                v-for="page in paginationButtons"
                :key="page"
                @click="changePage(page)"
                :disabled="page === '...'"
                :class="{
                  'px-3 py-1 rounded-md': true,
                  'bg-blue-600 text-white': page === pagination.current,
                  'text-gray-700 hover:bg-gray-100': page !== pagination.current && page !== '...',
                  'text-gray-400 cursor-default': page === '...'
                }"
              >
                {{ page }}
              </button>
            </div>
            <div class="flex space-x-2">
              <button
                @click="changePage(pagination.current - 1)"
                :disabled="pagination.current === 1"
                class="px-3 py-1 rounded-md text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Précédent
              </button>
              <button
                @click="changePage(pagination.current + 1)"
                :disabled="pagination.current === pagination.last_page"
                class="px-3 py-1 rounded-md text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Suivant
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DiseaseDocumentation',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      categories: [],
      diseases: [],
      loading: false,
      initialLoading: true,
      error: null,
      pagination: {
        current: 1,
        total: 0,
        perPage: 10,
        lastPage: 1
      },
      debounce: null,
      maxVisiblePages: 5
    };
  },
  computed: {
    hasResults() {
      return this.diseases.length > 0;
    },
    showPagination() {
      return this.pagination.total > this.pagination.perPage;
    },
    showNoResults() {
      return !this.loading && !this.error && !this.initialLoading && this.diseases.length === 0;
    },
    paginationButtons() {
      const current = this.pagination.current;
      const last = this.pagination.lastPage;
      const delta = Math.floor(this.maxVisiblePages / 2);
      const range = [];

      if (last <= 1) return [1];
      
      range.push(1);
      
      if (current - delta > 2) {
        range.push('...');
      }

      for (let i = Math.max(2, current - delta); i <= Math.min(last - 1, current + delta); i++) {
        range.push(i);
      }

      if (current + delta < last - 1) {
        range.push('...');
      }

      if (last > 1) {
        range.push(last);
      }

      return range;
    }
  },
  created() {
    this.fetchCategories();
    this.fetchDiseases();
  },
  methods: {
    getSeverityText(severity) {
      const severityMap = {
        'L': 'Faible',
        'M': 'Modéré',
        'S': 'Sévère'
      };
      return severityMap[severity] || 'Non spécifié';
    },
    
    async fetchCategories() {
      try {
        const response = await axios.get('/public/diseases/categories/');
        this.categories = response.data;
      } catch (error) {
        console.error('Erreur lors du chargement des catégories:', error);
        this.error = 'Impossible de charger les catégories. Veuillez réessayer plus tard.';
        if (this.$toast) {
          this.$toast.error(this.error);
        }
      }
    },
    async fetchDiseases(page = 1) {
      this.loading = true;
      this.error = null;
      
      try {
        const params = {
          page: page,
          search: this.searchQuery || undefined,
          category: this.selectedCategory || undefined,
          ordering: 'name' // Tri par défaut par nom
        };
        
        const response = await axios.get('/public/diseases/', { 
          params,
          timeout: 10000 // Timeout de 10 secondes
        });
        
        this.diseases = response.data.results || [];
        this.pagination = {
          current: page,
          total: response.data.count || 0,
          perPage: response.data.results?.length || 10,
          lastPage: Math.ceil((response.data.count || 0) / 10)
        };
      } catch (error) {
        console.error('Erreur lors du chargement des maladies:', error);
        this.error = this.getErrorMessage(error);
        if (this.$toast) {
          this.$toast.error(this.error);
        }
      } finally {
        this.loading = false;
        this.initialLoading = false;
      }
    },
    getErrorMessage(error) {
      if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
        return 'La requête a pris trop de temps. Veuillez vérifier votre connexion et réessayer.';
      } else if (error.response?.status === 404) {
        return 'Aucune maladie trouvée avec les critères sélectionnés.';
      } else if (error.response?.status >= 500) {
        return 'Une erreur est survenue côté serveur. Veuillez réessayer plus tard.';
      } else {
        return 'Une erreur est survenue lors du chargement des données. Veuillez réessayer.';
      }
    },
    onSearch() {
      clearTimeout(this.debounce);
      this.debounce = setTimeout(() => {
        this.fetchDiseases(1);
      }, 500);
    },
    onCategoryChange() {
      this.fetchDiseases(1);
    },
    changePage(page) {
      if (page < 1 || page > this.pagination.lastPage || page === this.pagination.current) return;
      this.pagination.current = page;
      this.fetchDiseases(page);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    fetchPage(url) {
      if (!url) return;
      try {
        const page = new URL(url).searchParams.get('page') || 1;
        this.changePage(parseInt(page));
      } catch (error) {
        console.error('Erreur lors de la récupération de la page:', error);
        if (this.$toast) {
          this.$toast.error('Erreur lors du chargement de la page');
        }
      }
    },
    getCategoryClass(categoryName) {
      if (!categoryName) return 'bg-gray-100 text-gray-800';
      
      const colors = {
        'Cardiologie': 'bg-red-100 text-red-800',
        'Neurologie': 'bg-blue-100 text-blue-800',
        'Pneumologie': 'bg-green-100 text-green-800',
        'Gastro-entérologie': 'bg-yellow-100 text-yellow-800',
        'Dermatologie': 'bg-purple-100 text-purple-800',
        'Endocrinologie': 'bg-pink-100 text-pink-800',
        'Infectiologie': 'bg-indigo-100 text-indigo-800',
        'Autre': 'bg-gray-100 text-gray-800'
      };
      
      // Vérifier si le nom de la catégorie correspond exactement ou partiellement
      const matchedCategory = Object.keys(colors).find(key => 
        categoryName.toLowerCase().includes(key.toLowerCase())
      );
      
      return matchedCategory ? colors[matchedCategory] : 'bg-gray-100 text-gray-800';
    },
    resetFilters() {
      this.searchQuery = '';
      this.selectedCategory = '';
      this.fetchDiseases(1);
    }
  },
  watch: {
    // Réinitialiser la pagination lors d'une nouvelle recherche
    searchQuery() {
      this.pagination.current = 1;
    },
    selectedCategory() {
      this.pagination.current = 1;
    }
  }
};
</script> 