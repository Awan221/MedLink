<template>
  <div class="space-y-6">
    <!-- En-tête avec bienvenue et actions rapides -->
    <div class="bg-gradient-to-r from-blue-600 to-blue-800 rounded-2xl shadow-xl p-6 text-white">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between">
        <div class="mb-4 md:mb-0">
          <h1 class="text-3xl font-bold">Tableau de bord médical</h1>
          <p class="mt-2 text-blue-100 flex items-center">
            <UserCircleIcon class="h-5 w-5 mr-2" />
            Bonjour, Dr. {{ currentUser?.last_name || '' }} | {{ currentDate }}
          </p>
        </div>
        <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
          <router-link 
            to="/patients/new"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400 transition-all duration-200 transform hover:-translate-y-0.5"
          >
            <UserPlusIcon class="-ml-1 mr-2 h-5 w-5" />
            Nouveau patient
          </router-link>
          <router-link 
            to="/appointments/new"
            class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-sm text-white bg-emerald-500 hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-400 transition-all duration-200 transform hover:-translate-y-0.5"
          >
            <PlusIcon class="-ml-1 mr-2 h-5 w-5" />
            Nouveau rendez-vous
          </router-link>
        </div>
      </div>
    </div>

    <!-- Cartes de statistiques améliorées -->
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

    <!-- Grille principale avec les fonctionnalités -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Colonne de gauche : Rendez-vous et patients -->
      <div class="space-y-6">
        <!-- Section Rendez-vous -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                <CalendarIcon class="h-5 w-5 mr-2 text-blue-500" />
                Rendez-vous d'aujourd'hui
              </h3>
              <router-link to="/appointments" class="text-sm font-medium text-blue-600 hover:text-blue-500">
                Voir tout
              </router-link>
            </div>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="appointment in appointments" :key="appointment.id" class="p-4 hover:bg-gray-50">
              <div class="flex items-center">
                <div class="flex-shrink-0 bg-blue-100 p-2 rounded-lg">
                  <ClockIcon class="h-5 w-5 text-blue-600" />
                </div>
                <div class="ml-4 flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ appointment.patientName }}</p>
                  <div class="flex items-center mt-1">
                    <span class="text-sm text-gray-500">{{ appointment.time }}</span>
                    <span class="mx-2 text-gray-300">•</span>
                    <span class="text-sm text-gray-500">{{ appointment.duration }} min</span>
                  </div>
                </div>
                <div>
                  <span class="px-2 py-1 text-xs rounded-full" :class="getAppointmentStatusClass(appointment.status)">
                    {{ appointment.status === 'confirmed' ? 'Confirmé' : 'En attente' }}
                  </span>
                </div>
              </div>
            </div>
            <div v-if="appointments.length === 0" class="p-6 text-center text-sm text-gray-500">
              Aucun rendez-vous prévu aujourd'hui
            </div>
          </div>
        </div>

        <!-- Section Patients récents -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-gray-900 flex items-center">
                <UserGroupIcon class="h-5 w-5 mr-2 text-blue-500" />
                Patients récents
              </h3>
              <router-link to="/patients" class="text-sm font-medium text-blue-600 hover:text-blue-500">
                Voir tout
              </router-link>
            </div>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="patient in recentPatients" :key="patient.id" class="p-4 hover:bg-gray-50">
              <div class="flex items-center">
                <div class="flex-shrink-0">
                  <UserCircleIcon class="h-10 w-10 text-gray-400" />
                </div>
                <div class="ml-4 flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ patient.name }}</p>
                  <div class="flex items-center mt-1">
                    <span class="text-sm text-gray-500">ID: {{ patient.id }}</span>
                    <span class="mx-2 text-gray-300">•</span>
                    <span class="text-sm text-gray-500">{{ patient.age }} ans</span>
                  </div>
                </div>
                <div>
                  <span class="px-2 py-1 text-xs rounded-full" :class="patient.alert ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'">
                    {{ patient.alert ? 'Alerte' : 'Stable' }}
                  </span>
                </div>
              </div>
            </div>
            <div v-if="recentPatients.length === 0" class="p-6 text-center text-sm text-gray-500">
              Aucun patient récent
            </div>
          </div>
        </div>
      </div>

      <!-- Colonne de droite : Accès rapide par catégorie -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Section Gestion des patients -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <UserGroupIcon class="h-5 w-5 mr-2 text-blue-500" />
              Gestion des patients
            </h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-6">
            <router-link 
              v-for="action in patientActions" 
              :key="action.title"
              :to="action.href"
              class="group p-4 border border-gray-200 rounded-lg hover:bg-blue-50 transition-colors duration-200"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                  <component :is="action.icon" class="h-5 w-5" />
                </div>
                <div class="ml-4">
                  <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                    {{ action.title }}
                  </h4>
                  <p class="mt-1 text-xs text-gray-500">{{ action.description }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Section Imagerie médicale -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <CameraIcon class="h-5 w-5 mr-2 text-blue-500" />
              Imagerie médicale
            </h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-6">
            <router-link 
              v-for="action in imagingActions" 
              :key="action.title"
              :to="action.href"
              class="group p-4 border border-gray-200 rounded-lg hover:bg-blue-50 transition-colors duration-200"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                  <component :is="action.icon" class="h-5 w-5" />
                </div>
                <div class="ml-4">
                  <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                    {{ action.title }}
                  </h4>
                  <p class="mt-1 text-xs text-gray-500">{{ action.description }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Section Outils médicaux -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <WrenchScrewdriverIcon class="h-5 w-5 mr-2 text-blue-500" />
              Outils médicaux
            </h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-6">
            <router-link 
              v-for="action in medicalTools" 
              :key="action.title"
              :to="action.href"
              class="group p-4 border border-gray-200 rounded-lg hover:bg-blue-50 transition-colors duration-200"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                  <component :is="action.icon" class="h-5 w-5" />
                </div>
                <div class="ml-4">
                  <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600">
                    {{ action.title }}
                  </h4>
                  <p class="mt-1 text-xs text-gray-500">{{ action.description }}</p>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- Section Administration -->
        <div v-if="currentUser?.role === 'admin' || currentUser?.role === 'super_admin'" class="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
          <div class="px-6 py-4 bg-gradient-to-r from-blue-50 to-white border-b border-gray-100">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <WrenchScrewdriverIcon class="h-5 w-5 mr-2 text-blue-500" />
              Administration
            </h3>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 p-6">
            <router-link 
              v-for="action in adminTools" 
              :key="action.title"
              :to="action.href"
              class="group p-4 border border-gray-200 rounded-lg hover:bg-blue-50 transition-colors duration-200"
            >
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
                  <component :is="action.icon" class="h-5 w-5" />
                </div>
                <div class="ml-4">
                  <h4 class="text-sm font-medium text-gray-900 group-hover:text-blue-600">
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
import { 
  UserCircleIcon, 
  ClockIcon, 
  PlusIcon, 
  ArrowTrendingUpIcon, 
  ArrowTrendingDownIcon,
  UserGroupIcon,
  UserPlusIcon,
  ClipboardDocumentCheckIcon,
  CalendarIcon,
  BellAlertIcon,
  CameraIcon,
  WrenchScrewdriverIcon
} from '@heroicons/vue/24/outline';

// Composant StatCard
const StatCard = {
  props: ['title', 'value', 'icon', 'trend', 'trendText', 'trendType'],
  template: `
    <div class="bg-white overflow-hidden shadow rounded-lg">
      <div class="p-5">
        <div class="flex items-center">
          <div class="flex-shrink-0 bg-primary-100 rounded-md p-3">
            <component :is="icon" class="h-6 w-6 text-primary-600" />
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
                <div v-if="trend" :class="[
                  trendType === 'up' ? 'text-green-600' : 'text-red-600',
                  'ml-2 flex items-baseline text-sm font-semibold'
                ]">
                  {{ trend }}
                  <span class="sr-only">{{ trendType === 'up' ? 'Increased' : 'Decreased' }} by</span>
                  {{ trendText }}
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
      <div class="bg-gray-50 px-5 py-3">
        <div class="text-sm">
          <a href="#" class="font-medium text-primary-600 hover:text-primary-500">
            Voir tout <span class="sr-only">{{ title }} stats</span>
          </a>
        </div>
      </div>
    </div>
  `
};

export default {
  name: 'DashboardMedecin',
  components: {
    UserCircleIcon,
    ClockIcon,
    PlusIcon,
    ArrowTrendingUpIcon,
    ArrowTrendingDownIcon,
    UserGroupIcon,
    UserPlusIcon,
    ClipboardDocumentCheckIcon,
    CalendarIcon,
    BellAlertIcon,
    CameraIcon,
    WrenchScrewdriverIcon,
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

    // Statistiques principales
    const stats = ref([
      { title: 'Patients aujourd\'hui', value: '24', trend: '+12%', trendText: 'vs hier', trendType: 'up', icon: 'UserGroupIcon', bgColor: 'bg-blue-100' },
      { title: 'Rendez-vous', value: '18', trend: '+3', trendText: 'non confirmés', trendType: 'down', icon: 'CalendarIcon', bgColor: 'bg-green-100' },
      { title: 'Examens en attente', value: '7', trend: '-2', trendText: 'en attente', trendType: 'down', icon: 'ClipboardDocumentCheckIcon', bgColor: 'bg-yellow-100' },
      { title: 'Alertes', value: '3', trend: '+1', trendText: 'non lues', trendType: 'up', icon: 'BellAlertIcon', bgColor: 'bg-red-100' }
    ]);

    // Rendez-vous du jour
    const appointments = ref([
      { id: 1, time: '09:00', duration: 30, patientName: 'Jean Dupont', patientId: 'PAT-001', reason: 'Consultation de routine', status: 'confirmed' },
      { id: 2, time: '10:30', duration: 15, patientName: 'Marie Martin', patientId: 'PAT-042', reason: 'Suivi traitement', status: 'confirmed' },
      { id: 3, time: '11:00', duration: 30, patientName: 'Pierre Durand', patientId: 'PAT-017', reason: 'Première visite', status: 'pending' },
      { id: 4, time: '14:30', duration: 15, patientName: 'Sophie Bernard', patientId: 'PAT-028', reason: 'Contrôle', status: 'confirmed' },
      { id: 5, time: '16:00', duration: 30, patientName: 'Thomas Moreau', patientId: 'PAT-035', reason: 'Consultation urgente', status: 'pending' }
    ]);

    // Patients récents
    const recentPatients = ref([
      { id: 'PAT-001', name: 'Jean Dupont', age: 45, alert: false },
      { id: 'PAT-042', name: 'Marie Martin', age: 32, alert: true },
      { id: 'PAT-017', name: 'Pierre Durand', age: 58, alert: false },
      { id: 'PAT-028', name: 'Sophie Bernard', age: 29, alert: false },
      { id: 'PAT-035', name: 'Thomas Moreau', age: 41, alert: true }
    ]);

    // Actions par catégorie
    const patientActions = [
      { 
        title: 'Nouveau patient', 
        description: 'Créer un nouveau dossier patient', 
        href: '/patients/new', 
        icon: 'UserPlusIcon' 
      },
      { 
        title: 'Rechercher', 
        description: 'Rechercher un patient existant', 
        href: '/patients', 
        icon: 'DocumentMagnifyingGlassIcon' 
      },
      { 
        title: 'Dossiers médicaux', 
        description: 'Accéder aux dossiers complets', 
        href: '/dossiers', 
        icon: 'FolderIcon' 
      },
      { 
        title: 'Ordonnances', 
        description: 'Gérer les ordonnances', 
        href: '/ordonnances', 
        icon: 'DocumentTextIcon' 
      }
    ];

    const imagingActions = [
      { 
        title: 'Examens d\'imagerie', 
        description: 'Voir tous les examens', 
        href: '/imaging/studies', 
        icon: 'ViewfinderCircleIcon' 
      },
      { 
        title: 'Envoyer une image', 
        description: 'Importer des images médicales', 
        href: '/imaging/upload', 
        icon: 'CloudArrowUpIcon' 
      },
      { 
        title: 'Rapports', 
        description: 'Consulter les rapports', 
        href: '/imaging/reports', 
        icon: 'DocumentChartBarIcon' 
      },
      { 
        title: 'Archives', 
        description: 'Accéder aux archives', 
        href: '/imaging/archive', 
        icon: 'QueueListIcon' 
      }
    ];

    const medicalTools = [
      { 
        title: 'Téléconsultation', 
        description: 'Démarrer une visio', 
        href: '/teleconsultation', 
        icon: 'VideoCameraIcon' 
      },
      { 
        title: 'Chat médical', 
        description: 'Discuter avec un patient', 
        href: '/chat', 
        icon: 'ChatBubbleLeftRightIcon' 
      },
      { 
        title: 'Banque de sang', 
        description: 'Vérifier les stocks', 
        href: '/blood/stocks', 
        icon: 'HeartIcon' 
      },
      { 
        title: 'Laboratoire', 
        description: 'Résultats d\'analyses', 
        href: '/laboratory', 
        icon: 'BeakerIcon' 
      }
    ];

    const adminTools = [
      { 
        title: 'Statistiques', 
        description: 'Tableaux de bord', 
        href: '/admin/stats', 
        icon: 'ChartBarIcon' 
      },
      { 
        title: 'Utilisateurs', 
        description: 'Gérer les accès', 
        href: '/admin/users', 
        icon: 'UserGroupIcon' 
      },
      { 
        title: 'Paramètres', 
        description: 'Configuration', 
        href: '/admin/settings', 
        icon: 'WrenchScrewdriverIcon' 
      },
      { 
        title: 'Support', 
        description: 'Aide et assistance', 
        href: '/support', 
        icon: 'QuestionMarkCircleIcon' 
      }
    ];

    const getAppointmentStatusClass = (status) => {
      switch (status) {
        case 'confirmed':
          return 'bg-green-100 text-green-800';
        case 'pending':
          return 'bg-yellow-100 text-yellow-800';
        case 'cancelled':
          return 'bg-red-100 text-red-800';
        default:
          return 'bg-gray-100 text-gray-800';
      }
    };

    const loadDashboardData = async () => {
      try {
        // Ici, vous pourriez charger les données depuis l'API
        // const response = await api.get('/api/dashboard/medecin');
        // stats.value = response.data.stats;
        // appointments.value = response.data.appointments;
        // recentPatients.value = response.data.recentPatients;
      } catch (error) {
        console.error('Erreur lors du chargement des données du tableau de bord:', error);
      }
    };

    onMounted(() => {
      loadDashboardData();
    });

    // Exposer les données au template
    return {
      currentUser,
      currentDate,
      stats,
      appointments,
      recentPatients,
      patientActions,
      imagingActions,
      medicalTools,
      adminTools,
      getAppointmentStatusClass
    };
  }
};
</script>

<style scoped>
/* Styles spécifiques au tableau de bord médecin */
</style>
