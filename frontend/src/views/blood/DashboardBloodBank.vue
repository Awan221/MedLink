<template>
  <div class="space-y-6">
    <!-- En-tête avec bienvenue et actions rapides -->
    <div class="bg-gradient-to-r from-red-600 to-red-800 rounded-2xl shadow-xl p-6 text-white">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between">
        <div class="mb-4 md:mb-0">
          <h1 class="text-3xl font-bold">Tableau de bord Banque de Sang</h1>
          <p class="mt-2 text-red-100 flex items-center">
            <UserCircleIcon class="h-5 w-5 mr-2" />
            Bonjour, {{ currentUser?.last_name || '' }} | {{ currentDate }}
          </p>
        </div>
        <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
          <router-link 
            to="/donner-sang"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-red-500 hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-400 transition-all duration-200 transform hover:-translate-y-0.5"
          >
            <MapIcon class="-ml-1 mr-2 h-5 w-5" />
            Points de don
          </router-link>
          <router-link 
            to="/blood/stock-form"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-white hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400 transition-all duration-200 transform hover:-translate-y-0.5 text-red-700"
          >
            <PlusIcon class="-ml-1 mr-2 h-5 w-5" />
            Nouvelle entrée de stock
          </router-link>
        </div>
      </div>
    </div>

    <!-- Cartes de statistiques -->
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <div v-for="(stat, index) in stats" :key="index" 
           class="bg-white rounded-2xl shadow-lg overflow-hidden transition-all duration-300 transform hover:scale-105 hover:shadow-xl border border-gray-100">
        <div class="p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-500">{{ stat.title }}</p>
              <p class="mt-1 text-3xl font-semibold text-gray-900">{{ stat.value }}</p>
              <div class="mt-2 flex items-center" :class="{ 'text-green-600': stat.trendType === 'up', 'text-red-600': stat.trendType === 'down' }">
                <component :is="stat.trendType === 'up' ? 'ArrowTrendingUpIcon' : 'ArrowTrendingDownIcon'" class="h-5 w-5" />
                <span class="ml-1 text-sm font-medium">{{ stat.trend }}</span>
                <span class="ml-1 text-sm text-gray-500">{{ stat.trendText }}</span>
              </div>
            </div>
            <div class="p-3 rounded-full" :class="stat.bgColor">
              <component :is="stat.icon" class="h-8 w-8 text-white" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Grille principale -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Colonne de gauche : Stock par groupe sanguin -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-red-50 to-white border-b border-gray-100">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                <BeakerIcon class="h-5 w-5 mr-2 text-red-500" />
                Stock actuel par groupe sanguin
              </h3>
              <router-link to="/blood/stocks" class="text-sm font-medium text-red-600 hover:text-red-500">
                Voir tout
              </router-link>
            </div>
          </div>
          <div class="p-6">
            <BloodStockTable :show-actions="false" />
          </div>
        </div>

        <!-- Dernières opérations -->
        <div class="mt-6 bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-red-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <ClockIcon class="h-5 w-5 mr-2 text-red-500" />
              Dernières opérations
            </h3>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="(op, index) in recentOperations" :key="index" class="p-4 hover:bg-gray-50">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-red-100 p-2 rounded-lg">
                  <component :is="op.type === 'in' ? 'ArrowDownTrayIcon' : 'ArrowUpTrayIcon'" class="h-5 w-5 text-red-600" />
                </div>
                <div class="ml-4 flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900">{{ op.center }}</p>
                  <p class="text-sm text-gray-700">{{ op.description }}</p>
                  <div class="flex items-center mt-1 flex-wrap">
                    <span class="text-sm text-gray-500">{{ op.quantity }} unité{{ op.quantity > 1 ? 's' : '' }} de {{ op.bloodType }}</span>
                    <span class="mx-2 text-gray-300 hidden sm:inline">•</span>
                    <span class="text-sm text-gray-500">{{ op.city }}</span>
                    <span class="mx-2 text-gray-300">•</span>
                    <span class="text-sm text-gray-500">{{ op.time }}</span>
                  </div>
                </div>
                <span class="px-2 py-1 text-xs font-medium rounded-full" :class="op.type === 'in' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'">
                  {{ op.type === 'in' ? 'Entrée' : 'Sortie' }}
                </span>
              </div>
            </div>
            <div v-if="recentOperations.length === 0" class="p-6 text-center text-sm text-gray-500">
              Aucune opération récente
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne de droite : Carte et actions rapides -->
      <div class="space-y-6">
        <!-- Carte des dons -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-red-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <MapIcon class="h-5 w-5 mr-2 text-red-500" />
              Points de don à proximité
            </h3>
          </div>
          <div class="h-64">
            <BloodDonationMap />
          </div>
          <div class="p-4 bg-gray-50 text-center">
            <router-link to="/donner-sang" class="text-sm font-medium text-red-600 hover:text-red-500">
              Voir tous les points de don →
            </router-link>
          </div>
        </div>

        <!-- Actions rapides -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-red-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <BoltIcon class="h-5 w-5 mr-2 text-red-500" />
              Actions rapides
            </h3>
          </div>
          <div class="grid grid-cols-1 gap-4 p-6">
            <router-link 
              v-for="action in quickActions" 
              :key="action.title"
              :to="action.href"
              class="group p-4 border border-gray-200 rounded-lg hover:bg-red-50 transition-colors duration-200"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-red-100 flex items-center justify-center text-red-600">
                  <component :is="action.icon" class="h-5 w-5" />
                </div>
                <div class="ml-4">
                  <h4 class="text-sm font-medium text-gray-900 group-hover:text-red-600">
                    {{ action.title }}
                  </h4>
                  <p class="mt-1 text-xs text-gray-500">{{ action.description }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import axios from 'axios';
import { 
  UserCircleIcon, 
  ClockIcon, 
  PlusIcon, 
  ArrowTrendingUpIcon, 
  ArrowTrendingDownIcon,
  BeakerIcon,
  MapPinIcon as MapIcon,
  BoltIcon,
  ArrowDownTrayIcon,
  ArrowUpTrayIcon,
  DocumentTextIcon,
  /*UserGroupIcon,
  ChartBarIcon,
  DocumentReportIcon,
  UserPlusIcon*/
} from '@heroicons/vue/24/outline';
import BloodStockTable from './BloodStockTable.vue';
import BloodDonationMap from './BloodDonationMap.vue';

// Composant StatCard
const StatCard = {
  props: ['title', 'value', 'icon', 'trend', 'trendText', 'trendType'],
  template: `
    <div class="bg-white overflow-hidden shadow rounded-lg">
      <div class="p-5">
        <div class="flex items-center">
          <div class="flex-shrink-0 bg-red-100 rounded-md p-3">
            <component :is="icon" class="h-6 w-6 text-red-600" />
          </div>
          <div class="ml-5 w-0 flex-1">
            <dl>
              <dt class="text-sm font-medium text-gray-500 truncate">
                {{ title }}
              </dt>
              <dd class="flex items-baseline">
                <div class="text-2xl font-semibold text-gray-900">
                  {{ value }}
                </div>
                <div class="ml-2 flex items-baseline text-sm font-semibold" :class="trendType === 'up' ? 'text-green-600' : 'text-red-600'">
                  {{ trend }}
                  <span class="sr-only">{{ trendText }}</span>
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </div>
  `
};

export default {
  name: 'DashboardBloodBank',
  components: {
    UserCircleIcon,
    ClockIcon,
    PlusIcon,
    ArrowTrendingUpIcon,
    ArrowTrendingDownIcon,
    BeakerIcon,
    MapIcon,
    BoltIcon,
    ArrowDownTrayIcon,
    ArrowUpTrayIcon,
    DocumentTextIcon,
    BloodStockTable,
    BloodDonationMap,
    StatCard
  },
  setup() {
    const store = useStore();
    const currentUser = computed(() => store.state.auth.user);
    const currentDate = new Date().toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    // Données des statistiques
    const stats = ref([
      { 
        id: 'total-units',
        title: 'Unités disponibles', 
        value: '0', 
        trend: '0%', 
        trendText: 'chargement...', 
        trendType: 'up', 
        icon: 'BeakerIcon', 
        bgColor: 'bg-red-100' 
      },
      { 
        id: 'monthly-donations',
        title: 'Dons ce mois-ci', 
        value: '0', 
        trend: '0%', 
        trendText: 'chargement...', 
        trendType: 'up', 
        icon: 'UserGroupIcon', 
        bgColor: 'bg-blue-100' 
      },
      { 
        id: 'critical-groups',
        title: 'Groupes critiques', 
        value: '0', 
        trend: 'Chargement...', 
        trendText: 'niveaux bas', 
        trendType: 'down', 
        icon: 'ExclamationTriangleIcon', 
        bgColor: 'bg-yellow-100' 
      },
      { 
        id: 'pending-requests',
        title: 'Demandes en attente', 
        value: '0', 
        trend: '0', 
        trendText: 'chargement...', 
        trendType: 'down', 
        icon: 'DocumentTextIcon', 
        bgColor: 'bg-purple-100' 
      }
    ]);
    
    // Charger les données des stocks critiques
    const loadCriticalStocks = async () => {
      try {
        const response = await axios.get('/blood-bank/inventory/');
        const allStocks = response.data.results || [];
        
        // Calculer le total des unités disponibles
        const totalUnits = allStocks.reduce((sum, stock) => sum + (stock.quantity_ml || 0), 0);
        
        // Trouver les groupes critiques (quantité < minimum requis)
        const criticalStocks = allStocks.filter(stock => 
          stock.quantity_ml < stock.minimum_required_ml
        );
        
        // Mettre à jour les statistiques
        updateStat('total-units', {
          value: Math.round(totalUnits / 450).toLocaleString(), // Conversion ml en unités (~450ml/unité)
          trend: '+0%', // À remplacer par des données réelles si disponibles
          trendText: 'en temps réel'
        });
        
        updateStat('critical-groups', {
          value: criticalStocks.length.toString(),
          trend: criticalStocks.map(s => s.blood_type).join(', ') || 'Aucun',
          trendType: criticalStocks.length > 0 ? 'down' : 'up'
        });
        
      } catch (error) {
        console.error('Erreur lors du chargement des stocks critiques:', error);
        updateStat('critical-groups', {
          value: '?',
          trend: 'Erreur',
          trendText: 'données indisponibles',
          trendType: 'down'
        });
      }
    };
    
    // Mettre à jour une statistique spécifique
    const updateStat = (id, updates) => {
      const index = stats.value.findIndex(stat => stat.id === id);
      if (index !== -1) {
        stats.value[index] = { ...stats.value[index], ...updates };
      }
    };
    
    // Charger les données au montage du composant
    onMounted(() => {
      loadCriticalStocks();
    });

    // Dernières opérations
    const recentOperations = ref([
      { 
        id: 1, 
        type: 'in', 
        bloodType: 'O+', 
        quantity: 3, 
        description: 'Collecte mobile Fann', 
        time: 'Il y a 2 heures',
        center: 'Centre National de Transfusion Sanguine',
        city: 'Dakar'
      },
      { 
        id: 2, 
        type: 'out', 
        bloodType: 'A+', 
        quantity: 2, 
        description: 'Urgence CHU de Fann', 
        time: 'Il y a 5 heures',
        center: 'CHU de Fann',
        city: 'Dakar'
      },
      { 
        id: 3, 
        type: 'in', 
        bloodType: 'B+', 
        quantity: 4, 
        description: 'Don régulier', 
        time: 'Aujourd\'hui',
        center: 'Hôpital Principal',
        city: 'Dakar'
      },
      { 
        id: 4, 
        type: 'out', 
        bloodType: 'AB+', 
        quantity: 1, 
        description: 'Chirurgie programmee', 
        time: 'Hier',
        center: 'Hôpital Général de Grand Yoff',
        city: 'Dakar'
      },
      { 
        id: 5, 
        type: 'in', 
        bloodType: 'O-', 
        quantity: 5, 
        description: 'Collecte entreprise Sonatel', 
        time: 'Hier',
        center: 'Centre de Santé de Ouakam',
        city: 'Dakar'
      },
      { 
        id: 6, 
        type: 'out', 
        bloodType: 'A-', 
        quantity: 2, 
        description: 'Maternité de Pikine', 
        time: 'Il y a 2 jours',
        center: 'Centre de Santé de Pikine',
        city: 'Pikine'
      },
      { 
        id: 7, 
        type: 'in', 
        bloodType: 'B-', 
        quantity: 3, 
        description: 'Collecte universitaire', 
        time: 'Il y a 2 jours',
        center: 'UCAD',
        city: 'Dakar'
      }
    ]);

    // Actions rapides
    const quickActions = [
      { 
        title: 'Nouvelle entrée de stock', 
        description: 'Enregistrer des dons ou retours', 
        href: '/blood/stock-form',
        icon: 'PlusIcon'
      },
      { 
        title: 'Sortie de stock', 
        description: 'Enregistrer une distribution', 
        href: '/blood/distributions/new',
        icon: 'ArrowUpTrayIcon'
      },
      { 
        title: 'Rapport hebdomadaire', 
        description: 'Générer le rapport des stocks', 
        href: '/reports/blood-stocks',
        icon: 'DocumentTextIcon'
      },
      { 
        title: 'Nouveau donneur', 
        description: 'Enregistrer un nouveau donneur', 
        href: '/donors/new',
        icon: 'UserPlusIcon'
      },
      { 
        title: 'Statistiques', 
        description: 'Voir les analyses et tendances', 
        href: '/analytics/blood-usage',
        icon: 'ChartBarIcon'
      },
      { 
        title: 'Alertes de stock', 
        description: 'Configurer les seuils d\'alerte', 
        href: '/settings/blood-alerts',
        icon: 'BellIcon'
      }
    ];

    return {
      currentUser,
      currentDate,
      stats,
      recentOperations,
      quickActions
    };
  }
};
</script>

<style scoped>
/* Styles spécifiques au tableau de bord banque de sang */
</style>
