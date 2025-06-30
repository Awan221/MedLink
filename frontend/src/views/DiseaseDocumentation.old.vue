<template>
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8">Documentation Médicale</h1>
    
    <!-- Barre de recherche et filtres -->
    <div class="mb-8 space-y-4">
      <div class="flex gap-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Rechercher une maladie..."
          class="flex-1 p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          @input="searchDiseases"
        />
        <select
          v-model="selectedCategory"
          class="p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="">Toutes les catégories</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>
    </div>

    <!-- Liste des maladies -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="disease in filteredDiseases"
        :key="disease.id"
        :to="'/public/maladies/' + disease.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold">{{ disease.name }}</h2>
            <span class="px-3 py-1 text-sm rounded-full" :class="getCategoryClass(disease.category)">
              {{ disease.category }}
            </span>
          </div>
          <p class="text-gray-600 mb-4">{{ disease.shortDescription }}</p>
          <div class="space-y-2">
            <div>
              <h3 class="font-medium text-gray-700">Symptômes principaux</h3>
              <p class="text-gray-600">{{ disease.mainSymptoms }}</p>
            </div>
          </div>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiseaseDocumentation',
  data() {
    return {
      searchQuery: '',
      selectedCategory: '',
      categories: [
        'Maladie infectieuse',
        'Maladie cardiovasculaire',
        'Maladie respiratoire',
        'Maladie neurologique',
        'Maladie digestive',
        'Maladie endocrinienne',
        'Maladie auto-immune',
        'Cancer'
      ],
      diseases: [
        {
          id: 1,
          name: 'COVID-19',
          category: 'Maladie infectieuse',
          shortDescription: 'Maladie infectieuse causée par le coronavirus SARS-CoV-2.',
          mainSymptoms: 'Fièvre, toux, fatigue, perte du goût et de l\'odorat'
        },
        {
          id: 2,
          name: 'Diabète',
          category: 'Maladie endocrinienne',
          shortDescription: 'Trouble du métabolisme caractérisé par un taux de sucre élevé dans le sang.',
          mainSymptoms: 'Soif excessive, mictions fréquentes, fatigue, vision floue'
        },
        {
          id: 3,
          name: 'Hypertension',
          category: 'Maladie cardiovasculaire',
          shortDescription: 'Pression artérielle anormalement élevée.',
          mainSymptoms: 'Souvent asymptomatique, maux de tête, vertiges'
        },
        {
          id: 4,
          name: 'Asthme',
          category: 'Maladie respiratoire',
          shortDescription: 'Maladie inflammatoire chronique des voies respiratoires.',
          mainSymptoms: 'Essoufflement, sifflements respiratoires, toux'
        },
        {
          id: 5,
          name: 'Maladie de Parkinson',
          category: 'Maladie neurologique',
          shortDescription: 'Trouble dégénératif du système nerveux central.',
          mainSymptoms: 'Tremblements, rigidité musculaire, lenteur des mouvements'
        },
        {
          id: 6,
          name: 'Maladie de Crohn',
          category: 'Maladie digestive',
          shortDescription: 'Maladie inflammatoire chronique du tube digestif.',
          mainSymptoms: 'Douleurs abdominales, diarrhée, perte de poids'
        },
        {
          id: 7,
          name: 'Lupus',
          category: 'Maladie auto-immune',
          shortDescription: 'Maladie auto-immune touchant plusieurs organes.',
          mainSymptoms: 'Fatigue, douleurs articulaires, éruptions cutanées'
        },
        {
          id: 8,
          name: 'Cancer du sein',
          category: 'Cancer',
          shortDescription: 'Tumeur maligne se développant dans le sein.',
          mainSymptoms: 'Masse dans le sein, modification de la peau, écoulement'
        },
        {
          id: 9,
          name: 'Grippe',
          category: 'Maladie infectieuse',
          shortDescription: 'Infection virale respiratoire aiguë.',
          mainSymptoms: 'Fièvre, courbatures, fatigue, toux'
        },
        {
          id: 10,
          name: 'Tremblement essentiel',
          category: 'Maladie neurologique',
          shortDescription: 'Trouble neurologique caractérisé par des tremblements involontaires et rythmiques.',
          mainSymptoms: 'Tremblements des mains, de la tête et de la voix'
        }
      ]
    }
  },
  computed: {
    filteredDiseases() {
      let filtered = this.diseases

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(disease => 
          disease.name.toLowerCase().includes(query) ||
          disease.shortDescription.toLowerCase().includes(query) ||
          disease.mainSymptoms.toLowerCase().includes(query)
        )
      }

      if (this.selectedCategory) {
        filtered = filtered.filter(disease => 
          disease.category === this.selectedCategory
        )
      }

      return filtered
    }
  },
  methods: {
    searchDiseases() {
      // La recherche est gérée par le computed property filteredDiseases
    },
    getCategoryClass(category) {
      const classes = {
        'Maladie infectieuse': 'bg-red-100 text-red-800',
        'Maladie cardiovasculaire': 'bg-blue-100 text-blue-800',
        'Maladie respiratoire': 'bg-green-100 text-green-800',
        'Maladie neurologique': 'bg-purple-100 text-purple-800',
        'Maladie digestive': 'bg-yellow-100 text-yellow-800',
        'Maladie endocrinienne': 'bg-pink-100 text-pink-800',
        'Maladie auto-immune': 'bg-indigo-100 text-indigo-800',
        'Cancer': 'bg-gray-100 text-gray-800'
      }
      return classes[category] || 'bg-gray-100 text-gray-800'
    }
  }
}
</script> 