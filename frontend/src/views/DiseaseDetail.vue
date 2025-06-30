<template>
  <div class="min-h-screen bg-gradient-to-b from-blue-50 to-white">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="mb-8">
        <router-link
          to="/public/maladies"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 transition-colors duration-200"
        >
          <svg class="w-5 h-5 mr-2 -ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Retour à la liste des maladies
        </router-link>
      </div>

      <!-- État de chargement -->
      <div v-if="loading" class="text-center py-20">
        <div class="flex justify-center mb-4">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
        <p class="text-gray-600 text-lg">Chargement des informations sur la maladie...</p>
        <p class="text-sm text-gray-400 mt-2">Veuillez patienter un instant</p>
      </div>

      <!-- État d'erreur -->
      <div v-else-if="error" class="text-center py-20 px-4">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-red-100 mb-4">
          <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">Oups, une erreur est survenue</h3>
        <p class="text-gray-600 max-w-md mx-auto mb-6">{{ error }}</p>
        <button 
          @click="loadDiseaseData" 
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Réessayer
        </button>
      </div>

      <!-- Affichage des données de la maladie -->
      <div v-else-if="disease" class="bg-white rounded-xl shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl">
        <!-- En-tête avec image de fond -->
        <div class="relative bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-10 sm:py-16 text-white overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-blue-700/30"></div>
          <div class="relative z-10 max-w-3xl">
            <div class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white/20 backdrop-blur-sm mb-4">
              <span class="w-2 h-2 rounded-full bg-white/80 mr-2"></span>
              {{ disease.category }}
            </div>
            <h1 class="text-3xl md:text-4xl lg:text-5xl font-extrabold tracking-tight mb-4">{{ disease.name }}</h1>
            <p v-if="disease.short_description" class="text-lg text-blue-100 max-w-3xl">{{ disease.short_description }}</p>
          </div>
          <div class="absolute -bottom-10 -right-10 w-64 h-64 bg-blue-400 rounded-full opacity-20"></div>
          <div class="absolute -top-20 -right-20 w-80 h-80 bg-blue-300 rounded-full opacity-10"></div>
        </div>
        
        <!-- Contenu principal -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 p-8">
          <!-- Colonne principale (2/3) -->
          <div class="lg:col-span-2 space-y-10">
            <!-- Description -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-6">
                <div class="p-2 rounded-lg bg-blue-50 text-blue-600 mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-gray-900">Description</h2>
              </div>
              <p class="text-gray-700 leading-relaxed">{{ disease.description }}</p>
            </div>

            <!-- Symptômes -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-6">
                <div class="p-2 rounded-lg bg-red-50 text-red-600 mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-gray-900">Symptômes</h2>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="(symptom, index) in disease.symptoms" :key="index" class="flex items-start">
                  <svg class="flex-shrink-0 h-5 w-5 text-red-500 mt-0.5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="text-gray-700">{{ symptom }}</span>
                </div>
              </div>
            </div>

            <!-- Causes -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-6">
                <div class="p-2 rounded-lg bg-amber-50 text-amber-600 mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-gray-900">Causes</h2>
              </div>
              <ul class="space-y-3">
                <li v-for="(cause, index) in disease.causes" :key="index" class="flex items-start">
                  <div class="flex-shrink-0 h-2 w-2 mt-2.5 rounded-full bg-amber-500 mr-3"></div>
                  <p class="text-gray-700">{{ cause }}</p>
                </li>
              </ul>
            </div>

            <!-- Traitements -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-6">
                <div class="p-2 rounded-lg bg-emerald-50 text-emerald-600 mr-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 class="text-2xl font-bold text-gray-900">Traitements</h2>
              </div>
              <div class="space-y-6">
                <div v-for="(treatment, index) in disease.treatments" :key="index" class="bg-emerald-50/50 p-4 rounded-lg border border-emerald-100">
                  <h3 class="font-semibold text-emerald-800 mb-2 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    {{ treatment.title }}
                  </h3>
                  <p class="text-gray-700">{{ treatment.description }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Barre latérale (1/3) -->
          <div class="space-y-6">
            <!-- Prévention -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-4">
                <div class="p-2 rounded-lg bg-blue-50 text-blue-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900">Prévention</h3>
              </div>
              <ul class="space-y-3">
                <li v-for="(prevention, index) in disease.prevention" :key="index" class="flex items-start">
                  <div class="flex-shrink-0 h-2 w-2 mt-2 rounded-full bg-blue-500 mr-3"></div>
                  <p class="text-gray-700">{{ prevention }}</p>
                </li>
              </ul>
            </div>

            <!-- Complications -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-4">
                <div class="p-2 rounded-lg bg-red-50 text-red-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900">Complications possibles</h3>
              </div>
              <ul class="space-y-3">
                <li v-for="(complication, index) in disease.complications" :key="index" class="flex items-start">
                  <div class="flex-shrink-0 h-2 w-2 mt-2 rounded-full bg-red-500 mr-3"></div>
                  <p class="text-gray-700">{{ complication }}</p>
                </li>
              </ul>
            </div>

            <!-- Quand consulter -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-amber-50 bg-amber-50/30">
              <div class="flex items-center mb-4">
                <div class="p-2 rounded-lg bg-amber-100 text-amber-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-amber-900">Quand consulter un médecin ?</h3>
              </div>
              <ul class="space-y-3">
                <li v-for="(indication, index) in disease.whenToSeeDoctor" :key="index" class="flex items-start">
                  <div class="flex-shrink-0 h-2 w-2 mt-2 rounded-full bg-amber-500 mr-3"></div>
                  <p class="text-amber-800">{{ indication }}</p>
                </li>
              </ul>
            </div>

            <!-- Ressources -->
            <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
              <div class="flex items-center mb-4">
                <div class="p-2 rounded-lg bg-indigo-50 text-indigo-600 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <h3 class="text-xl font-bold text-gray-900">Ressources utiles</h3>
              </div>
              <div class="space-y-4">
                <a
                  v-for="resource in disease.resources"
                  :key="resource.title"
                  :href="resource.url"
                  target="_blank"
                  class="block p-4 bg-indigo-50/50 rounded-lg border border-indigo-100 hover:border-indigo-200 transition-colors group"
                >
                  <h4 class="font-semibold text-indigo-700 group-hover:text-indigo-800 transition-colors">
                    {{ resource.title }}
                  </h4>
                  <p class="text-sm text-indigo-600 mt-1">{{ resource.description }}</p>
                  <div class="mt-2 inline-flex items-center text-xs text-indigo-500 group-hover:text-indigo-600">
                    En savoir plus
                    <svg class="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DiseaseDetail',
  data() {
    return {
      disease: null,
      loading: true,
      error: null
    };
  },
  created() {
    this.loadDiseaseData();
  },
  methods: {
    async loadDiseaseData() {
      this.loading = true;
      this.error = null;
      
      try {
        const slug = this.$route.params.slug;
        const response = await axios.get(`/public/diseases/${slug}/`);
        
        // Formater les données pour correspondre à la structure attendue par le template
        this.disease = {
          ...response.data,
          // Extraire le nom de la catégorie si c'est un objet
          category: response.data.category && typeof response.data.category === 'object' 
            ? response.data.category.name 
            : response.data.category,
          // Convertir les chaînes séparées par des retours à la ligne en tableaux
          symptoms: response.data.main_symptoms ? 
            (Array.isArray(response.data.main_symptoms) ? 
              response.data.main_symptoms : 
              String(response.data.main_symptoms || '').split('\n').filter(s => s.trim())
            ) : [],
            
          causes: response.data.causes ? 
            (Array.isArray(response.data.causes) ? 
              response.data.causes : 
              String(response.data.causes || '').split('\n').filter(s => s.trim())
            ) : [],
            
          prevention: response.data.prevention ? 
            (Array.isArray(response.data.prevention) ? 
              response.data.prevention : 
              String(response.data.prevention || '').split('\n').filter(s => s.trim())
            ) : [],
            
          complications: response.data.prognosis ? 
            (Array.isArray(response.data.prognosis) ? 
              response.data.prognosis : 
              String(response.data.prognosis || '').split('\n').filter(s => s.trim())
            ) : [],
            
          whenToSeeDoctor: response.data.when_to_see_doctor ? 
            (Array.isArray(response.data.when_to_see_doctor) ? 
              response.data.when_to_see_doctor : 
              String(response.data.when_to_see_doctor || '').split('\n').filter(s => s.trim())
            ) : [],
            
          // Formater les traitements
          treatments: [
            {
              title: 'Traitement médical',
              description: response.data.treatment || 'Aucun traitement spécifique mentionné.'
            }
          ],
          // Formater les ressources
          resources: response.data.resources ? (
            Array.isArray(response.data.resources) ? 
              response.data.resources : 
              []
          ).map(resource => ({
            title: resource.title || '',
            description: resource.description || '',
            url: resource.url || '#'
          })) : []
        };
      } catch (error) {
        console.error('Erreur lors du chargement de la maladie:', error);
        this.error = 'Impossible de charger les détails de la maladie. Veuillez réessayer plus tard.';
      } finally {
        this.loading = false;
      }
    }
  },
  watch: {
    // Recharger les données si le slug change
    '$route.params.slug': {
      handler() {
        this.loadDiseaseData();
      },
      immediate: true
    }
  }
};
</script>