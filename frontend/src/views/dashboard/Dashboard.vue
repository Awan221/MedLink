<template>
  <div>
    <div class="pb-5 border-b border-gray-200 sm:flex sm:items-center sm:justify-between">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Tableau de bord
      </h3>
      <div class="mt-3 sm:mt-0 sm:ml-4">
        <span class="text-sm font-medium text-gray-500">
          Bienvenue, {{ currentUser && currentUser.first_name ? currentUser.first_name : '' }} {{ currentUser && currentUser.last_name ? currentUser.last_name : '' }}
        </span>
        <template v-if="hasRole([ROLES.ADMIN, ROLES.SUPER_ADMIN])">
          <router-link to="/admin/inscriptions" class="ml-4 btn btn-primary">Dashboard Admin</router-link>
          <router-link to="/admin/user-management" class="ml-2 btn btn-secondary">Gestion Utilisateurs</router-link>
        </template>
      </div>
    </div>
    
    <!-- Statistiques -->
    <div class="mt-6 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="(stat, index) in filteredStats" :key="index" class="bg-white overflow-hidden shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0 bg-primary-100 rounded-md p-3 relative">
              <component v-if="stat.icon && typeof stat.icon === 'string' && $options.components[stat.icon]" :is="stat.icon" class="h-6 w-6 text-primary-600" />
              <svg v-else class="h-6 w-6 text-primary-600" fill="none" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="2" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3" /></svg>
              <span v-if="stat.badge" class="absolute -top-2 -right-2 px-2 py-0.5 text-xs font-medium rounded-full" :class="stat.badge">
                {{ stat.value }}
              </span>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  {{ stat.name }}
                </dt>
                <dd>
                  <div class="text-lg font-medium text-gray-900">
                    {{ stat.name === 'Chatbot Médical' ? 'Assistant IA' : stat.value }}
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div class="bg-gray-50 px-4 py-4 sm:px-6">
          <div class="text-sm">
            <router-link :to="stat.href" class="font-medium text-primary-600 hover:text-primary-500">
              Voir plus<span class="sr-only"> {{ stat.name }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Activité récente -->
    <div class="mt-8">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Activité récente
      </h3>
      <div class="mt-2 bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="(activity, index) in recentActivity" :key="index">
            <div class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="flex-shrink-0">
                    <component v-if="activity.icon && typeof activity.icon === 'string' && $options.components[activity.icon]" :is="activity.icon" class="h-6 w-6 text-gray-400" />
<svg v-else class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="2" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3" /></svg>
                  </div>
                  <div class="ml-3">
                    <p class="text-sm font-medium text-gray-900">
                      {{ activity.title }}
                    </p>
                    <p class="text-sm text-gray-500">
                      {{ activity.description }}
                    </p>
                  </div>
                </div>
                <div class="ml-2 flex-shrink-0 flex">
                  <p class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="activityStatusClass(activity.status)">
                    {{ activity.status }}
                  </p>
                </div>
              </div>
              <div class="mt-2 sm:flex sm:justify-between">
                <div class="sm:flex">
                  <p class="flex items-center text-sm text-gray-500">
                    <component v-if="activity.typeIcon && typeof activity.typeIcon === 'string' && $options.components[activity.typeIcon]" :is="activity.typeIcon" class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
<svg v-else class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><circle cx="12" cy="12" r="10" stroke-width="2" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3" /></svg>
                    {{ activity.type }}
                  </p>
                </div>
                <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                  <svg class="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd" />
                  </svg>
                  <span>
                    {{ activity.date }}
                  </span>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
    
    <!-- Alertes -->
    <div v-if="alerts.length > 0" class="mt-8">
      <h3 class="text-lg leading-6 font-medium text-gray-900">
        Alertes
      </h3>
      <div class="mt-2 bg-white shadow overflow-hidden sm:rounded-md">
        <ul class="divide-y divide-gray-200">
          <li v-for="(alert, index) in alerts" :key="index" class="px-4 py-4 sm:px-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-gray-900">
                  {{ alert.title }}
                </h3>
                <div class="mt-1 text-sm text-gray-500">
                  <p>{{ alert.message }}</p>
                </div>
                <div class="mt-2">
                  <router-link :to="alert.href" class="text-sm font-medium text-primary-600 hover:text-primary-500">
                    Voir les détails
                  </router-link>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ref, computed, onMounted, watch } from 'vue'
import { ROLES } from '@/constants/roles'
//import { useStore } from 'vuex'
//import { useRouter } from 'vue-router'

// Icônes (à remplacers par vos propres composants d'icônes)
const UserIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>`
}

const ImageIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>`
}

const BloodIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
  </svg>`
}

const AIIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>`
}

const ChatIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
  </svg>`
}

const PatientIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
  </svg>`
}

const ReportIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
  </svg>`
}

export default {
  name: 'DashboardView',
  components: {
    UserIcon,
    ImageIcon,
    BloodIcon,
    AIIcon,
    ChatIcon,
    PatientIcon,
    ReportIcon
  },
  setup() {
    const store = useStore()
    const router = useRouter()
    const isLoading = ref(true)
    
    // Récupérer les informations de l'utilisateur de manière sécurisée
    const currentUser = computed(() => {
      const user = store.getters['auth/currentUser']
      return user || { first_name: '', last_name: '' }
    })
    
    const userRoles = computed(() => store.getters['auth/userRoles'] || [])
    
    // Debug: Afficher les informations de l'utilisateur et ses rôles
    onMounted(() => {
      console.log('Current User:', currentUser.value)
      console.log('User Roles:', userRoles.value)
      isLoading.value = false
    })

    // Vérifier si l'utilisateur a un rôle spécifique
    const hasRole = (roles) => {
      if (!userRoles.value || userRoles.value.length === 0) return false
      if (!Array.isArray(roles)) roles = [roles]
      return userRoles.value.some(role => roles.includes(role))
    }

    // Vérification des rôles et redirection si nécessaire
    const checkUserRoleAndRedirect = () => {
      if (isLoading.value || !userRoles.value) return
      
      const currentPath = router.currentRoute.value.path
      
      if (hasRole([ROLES.SUPER_ADMIN])) {
        if (!currentPath.startsWith('/admin')) {
          router.replace('/admin/dashboard')
          return
        }
      } else if (hasRole([ROLES.ADMIN])) {
        if (!currentPath.startsWith('/admin')) {
          router.replace('/admin/inscriptions')
          return
        }
      }
    }
    
    // Surveiller les changements de rôles pour déclencher la vérification
    watch(userRoles, () => {
      checkUserRoleAndRedirect()
    }, { immediate: true })

    // Statistiques
    const stats = ref([
      {
        name: 'Patients',
        value: '0',
        href: '/patients',
        icon: 'UserIcon',
        roles: [ROLES.DOCTOR, ROLES.SPECIALIST, ROLES.ADMIN, ROLES.NURSE],
        description: 'Gérez vos patients et leurs dossiers médicaux'
      },
      {
        name: 'Chatbot Médical',
        value: 'Nouveau',
        href: '/chat?session_type=MEDICAL',
        icon: 'ChatIcon',
        roles: [ROLES.DOCTOR, ROLES.SPECIALIST, ROLES.ADMIN, ROLES.NURSE],
        badge: 'bg-green-100 text-green-800',
        description: 'Obtenez une assistance médicale en temps réel'
      },
      {
        name: 'Imagerie DICOM',
        value: '0',
        href: '/imaging/studies',
        icon: 'ImageIcon',
        roles: [ROLES.DOCTOR, ROLES.RADIOLOGIST, ROLES.TECHNICIAN, ROLES.ADMIN],
        description: 'Consultez et analysez les études d\'imagerie médicale'
      },
      {
        name: 'Banque de Sang',
        value: '0',
        href: '/blood/stocks',
        icon: 'BloodIcon',
        roles: [ROLES.BLOOD_BANK_MANAGER, ROLES.ADMIN, ROLES.DOCTOR, ROLES.NURSE],
        description: 'Gérez les stocks de sang et les dons'
      },
      {
        name: 'Analyse IA',
        value: '0',
        href: '/ai/diagnostic',
        icon: 'AIIcon',
        roles: [ROLES.DOCTOR, ROLES.RADIOLOGIST, ROLES.SPECIALIST, ROLES.ADMIN],
        description: 'Outils d\'aide au diagnostic par intelligence artificielle'
      },
      {
        name: 'Rendez-vous',
        value: '0',
        href: '/appointments',
        icon: 'CalendarIcon',
        roles: [ROLES.DOCTOR, ROLES.SPECIALIST, ROLES.ADMIN, ROLES.NURSE, ROLES.PATIENT],
        description: 'Gérez les rendez-vous et les consultations'
      }
    ])

    // Filtrer les statistiques en fonction des rôles de l'utilisateur
    const filteredStats = computed(() => {
      if (!userRoles.value || userRoles.value.length === 0) {
        return []
      }
      
      return stats.value.filter(stat => {
        // Vérifier si l'utilisateur a au moins un des rôles requis
        return hasRole(stat.roles)
      })
    })

    // Activité récente
    const recentActivity = ref([
      {
        title: 'Nouveau patient enregistré',
        description: 'Patient: Jean Dupont',
        status: 'Complété',
        type: 'Patient',
        typeIcon: 'PatientIcon',
        icon: 'UserIcon',
        date: 'Aujourd\'hui à 10:30'
      },
      {
        title: 'Nouvelle étude DICOM',
        description: 'Patient: Marie Martin - Radiographie thoracique',
        status: 'En attente',
        type: 'Imagerie',
        typeIcon: 'ImageIcon',
        icon: 'ImageIcon',
        date: 'Aujourd\'hui à 09:15'
      },
      {
        title: 'Rapport de radiologie',
        description: 'Patient: Pierre Durand - IRM cérébrale',
        status: 'Finalisé',
        type: 'Rapport',
        typeIcon: 'ReportIcon',
        icon: 'ReportIcon',
        date: 'Hier à 16:45'
      }
    ])

    // Alertes
    const alerts = ref([
      {
        title: 'Alerte IA - Anomalie détectée',
        message: 'Le modèle de détection a identifié une anomalie potentielle pour le patient Pierre Durand.',
        href: '/app/ai-diagnostic/alerts'
      },
      {
        title: 'Stock de sang critique',
        message: 'Le stock de sang de type O- est en dessous du seuil critique. Veuillez vérifier la banque de sang.',
        href: '/app/blood-bank'
      }
    ])

    // Fonction pour déterminer la classe CSS en fonction du statut
    const activityStatusClass = (status) => {
      switch (status) {
        case 'Complété':
          return 'bg-green-100 text-green-800'
        case 'En attente':
          return 'bg-yellow-100 text-yellow-800'
        case 'Finalisé':
          return 'bg-blue-100 text-blue-800'
        default:
          return 'bg-gray-100 text-gray-800'
      }
    }

    // Charger les données du tableau de bord
    const loadDashboardData = () => {
      if (isLoading.value) return
      
      // Simuler le chargement des données
      setTimeout(() => {
        try {
          // Mettre à jour les statistiques avec des valeurs aléatoires
          stats.value = stats.value.map(stat => {
            if (!stat) return null
            return {
              ...stat,
              value: Math.floor(Math.random() * 100).toString()
            }
          }).filter(Boolean) // Filtrer les valeurs nulles
        } catch (error) {
          console.error('Erreur lors du chargement des données du tableau de bord:', error)
        }
      }, 1000)
    }
    
    // Charger les données lorsque les rôles sont disponibles
    watch(userRoles, () => {
      if (userRoles.value && userRoles.value.length > 0) {
        loadDashboardData()
      }
    }, { immediate: true })

    // Filtrer les activités récentes pour s'assurer qu'elles sont valides
    const safeRecentActivity = computed(() => {
      return (recentActivity.value || []).filter(activity => 
        activity && activity.title && activity.description
      )
    })
    
    // Filtrer les alertes pour s'assurer qu'elles sont valides
    const safeAlerts = computed(() => {
      return (alerts.value || []).filter(alert => 
        alert && alert.title && alert.message
      )
    })
    
    return {
      currentUser,
      userRoles,
      ROLES,
      hasRole,
      stats: stats.value || [],
      filteredStats: filteredStats.value || [],
      recentActivity: safeRecentActivity,
      alerts: safeAlerts,
      activityStatusClass,
      isLoading
    }
  }
}
</script>