import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'
import { ROLES,hasRole, hasRoleGroup } from '@/constants/roles'

// Vues d'authentification
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import ForgotPassword from '@/views/auth/ForgotPassword.vue'
import RegistrationSuccess from '@/views/auth/RegistrationSuccess.vue'

// Vues du tableau de bord
import DashboardView from '@/views/dashboard/Dashboard.vue'

// Vues des patients
import PatientList from '@/views/patients/PatientList.vue'
import PatientDetail from '@/views/patients/PatientDetail.vue'
import PatientForm from '@/views/patients/PatientForm.vue'
import MedicalRecordForm from '@/views/patients/MedicalRecordForm.vue'
import PrescriptionForm from '@/views/patients/PrescriptionForm.vue'

// Vues des rendez-vous
import AppointmentList from '@/views/appointments/AppointmentList.vue'
import AppointmentDetail from '@/views/appointments/AppointmentDetail.vue'
import AppointmentForm from '@/views/appointments/AppointmentForm.vue'

// Import des routes d'imagerie
import imagingRoutes from './imaging'

// Import des composants d'imagerie restants
import ImportDICOM from '@/views/imaging/ImportDICOM.vue'
import ImportLog from '@/views/imaging/ImportLog.vue'

// Vues du chatbot
import ChatInterface from '@/views/chatbot/ChatInterface.vue'

// Vues de l'IA
import AIDiagnostic from '@/views/ai/AIDiagnostic.vue'
import AIAlerts from '@/views/ai/AIAlerts.vue'

// Vues d'administration
import UserManagement from '@/views/admin/UserManagement.vue'
import UserAdmin from '@/views/admin/UserAdmin.vue'
import Settings from '@/views/admin/Settings.vue'
import RegistrationRequests from '@/views/admin/RegistrationRequests.vue'
import AdminRegistrationDashboard from '@/views/admin/AdminRegistrationDashboard.vue'
import ActionLog from '@/views/admin/ActionLog.vue'
import BloodStock from '@/views/admin/BloodStock.vue'
import BloodStockList from '@/views/BloodStockList.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import PermissionManagement from '@/views/admin/PermissionManagement.vue'
import AdminAlerts from '@/views/admin/AdminAlerts.vue'

// Vues du médecin
import DashboardMedecin from '@/views/medecin/DashboardMedecin.vue'

// Vues de profil et paramètres
import ProfileView from '@/views/profile/ProfileView.vue'
import SettingsView from '@/views/settings/SettingsView.vue'

// Vues du portail public
import DiseaseDocumentation from '@/views/DiseaseDocumentation.vue'
import DiseaseDetail from '@/views/DiseaseDetail.vue'
import NearbyHospitals from '@/views/NearbyHospitals.vue'
import PublicPortal from '@/views/PublicPortal.vue'
import StatisticsPage from '@/views/public/Statistics.vue'
// Vues banque de sang
import BloodStockForm from '@/views/blood/BloodStockForm.vue'
import BloodStockTable from '@/views/blood/BloodStockTable.vue'
import BloodDonationMap from '@/views/blood/BloodDonationMap.vue'

const routes = [
  // Tableau de bord médecin
  {
    path: '/medecin/dashboard',
    name: 'DashboardMedecin',
    component: DashboardMedecin,
    meta: { 
      requiresAuth: true,
      roles: ['doctor', 'DOCTOR', ROLES.DOCTOR, ROLES.ADMIN, ROLES.SUPER_ADMIN],
      title: 'Tableau de bord médecin'
    }
  },

  // Profil utilisateur
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { 
      requiresAuth: true,
      title: 'Mon Profil'
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView,
    meta: { 
      requiresAuth: true,
      title: 'Paramètres'
    }
  },

  // Banque de sang
  {
    path: '/blood/stock-form',
    name: 'BloodStockForm',
    component: BloodStockForm,
    meta: { 
      requiresAuth: true, 
      roles: ['blood_bank_manager', 'BLOOD_BANK_MANAGER', ROLES.BLOOD_BANK_MANAGER, ROLES.ADMIN],
      title: 'Gestion des stocks de sang'
    }
  },
  {
    path: '/blood/stocks',
    name: 'BloodStockTable',
    component: BloodStockTable,
    meta: { 
      requiresAuth: true, 
      roles: ['doctor','blood_bank_manager', 'BLOOD_BANK_MANAGER', ROLES.BLOOD_BANK_MANAGER, ROLES.ADMIN, ROLES.NURSE],
      title: 'Stocks de sang'
    }
  },
  {
    path: '/donner-sang',
    name: 'BloodDonationMap',
    component: BloodDonationMap,
    meta: { 
      requiresAuth: false,
      title: 'Don de sang - Points de collecte'
    }
  },
  // Routes publiques (portail)
  {
    path: '/public',
    name: 'PublicPortal',
    component: PublicPortal,
    meta: { requiresAuth: false }
  },
  {
    path: '/public/statistiques',
    name: 'StatisticsPage',
    component: StatisticsPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/public/don',
    name: 'PublicBecomeDonor',
    component: () => import('@/views/public/BecomeDonor.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/public/contact',
    name: 'PublicContact',
    component: () => import('@/views/public/Contact.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/public/maladies',
    name: 'DiseaseDocumentation',
    component: DiseaseDocumentation,
    meta: { requiresAuth: false }
  },
  {
    path: '/public/maladies/:slug',
    name: 'DiseaseDetail',
    component: DiseaseDetail,
    meta: { requiresAuth: false },
    props: true
  },
  {
    path: '/public/hopitaux',
    name: 'NearbyHospitals',
    component: NearbyHospitals,
    meta: { requiresAuth: false }
  },
  // --- routes existantes ---
  {
    path: '/imaging/import-log',
    name: 'ImportLog',
    component: ImportLog,
    meta: { requiresAuth: true, technicienOnly: true }
  },
  {
    path: '/imaging/import',
    name: 'ImportDICOM',
    component: ImportDICOM,
    meta: { requiresAuth: true, technicienOnly: true }
  },
  // Routes publiques
  {
    path: '/blood-stocks',
    name: 'BloodStockList',
    component: BloodStockList,
    meta: { requiresAuth: true, medecinOnly: true }
  },
  {
    path: '/admin/blood-stock',
    name: 'BloodStock',
    component: BloodStock,
    meta: { requiresAuth: true, adminOrBloodBankOnly: true }
  },
  {
    path: '/admin/action-logs',
    name: 'ActionLog',
    component: ActionLog,
    meta: { requiresAuth: true, adminOnly: true }
  },
  {
    path: '/admin/inscriptions',
    name: 'AdminRegistrationDashboard',
    component: AdminRegistrationDashboard,
    meta: { requiresAuth: true, adminOnly: true }
  },
  {
    path: '/admin/alerts',
    name: 'AdminAlerts',
    component: AdminAlerts,
    meta: { requiresAuth: true, adminOnly: true }
  },  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN', 'ADMIN'] }
  },
  {
    path: '/admin/permissions',
    name: 'PermissionManagement',
    component: PermissionManagement,
    meta: { requiresAuth: true, roles: ['SUPER_ADMIN'] }
  },
  {
    path: '/admin/users',
    name: 'UserAdmin',
    component: UserAdmin,
    meta: { requiresAuth: true, adminOnly: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { guest: true }
  },
  {
    path: '/register/success',
    name: 'RegistrationSuccess',
    component: RegistrationSuccess,
    props: true,
    meta: { guest: true }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { guest: true }
  },
  
  // Routes protégées
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true }
  },
  
  // Routes des patients
  {
    path: '/patients',
    name: 'PatientList',
    component: PatientList,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/new',
    name: 'PatientCreate',
    component: PatientForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id',
    name: 'PatientDetail',
    component: PatientDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/edit',
    name: 'PatientEdit',
    component: PatientForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/medical-records/new',
    name: 'MedicalRecordCreate',
    component: MedicalRecordForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/medical-records/:recordId/edit',
    name: 'MedicalRecordEdit',
    component: MedicalRecordForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/prescriptions/new',
    name: 'PrescriptionCreate',
    component: PrescriptionForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/patients/:id/prescriptions/:prescId/edit',
    name: 'PrescriptionEdit',
    component: PrescriptionForm,
    meta: { requiresAuth: true }
  },
  
  // Routes des rendez-vous
  {
    path: '/appointments',
    name: 'AppointmentList',
    component: AppointmentList,
    meta: { requiresAuth: true }
  },
  {
    path: '/appointments/new',
    name: 'AppointmentCreate',
    component: AppointmentForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/appointments/:id',
    name: 'AppointmentDetail',
    component: AppointmentDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/appointments/:id/edit',
    name: 'AppointmentEdit',
    component: AppointmentForm,
    meta: { requiresAuth: true }
  },
  
  // Routes d'imagerie
  ...imagingRoutes,
  
  // Routes du chatbot
  {
    path: '/chat',
    name: 'ChatInterface',
    component: ChatInterface,
    meta: { requiresAuth: false } // Accessible sans authentification
  },
  
  // Routes de l'IA
  {
    path: '/ai/diagnostic',
    name: 'AIDiagnostic',
    component: AIDiagnostic,
    meta: { requiresAuth: true, roles: ['MEDECIN', 'RADIOLOGUE', 'SPECIALISTE'] }
  },
  {
    path: '/ai/alerts',
    name: 'AIAlerts',
    component: AIAlerts,
    meta: { requiresAuth: true, roles: ['MEDECIN', 'RADIOLOGUE'] }
  },
  
  // Routes de la banque de sang
  {
    path: '/blood/dashboard',
    name: 'BloodBankDashboard',
    component: () => import('@/views/blood/DashboardBloodBank.vue'),
    meta: { 
      requiresAuth: true, 
      roles: ['blood_bank_manager','BLOOD_BANK_MANAGER']
    }
  },
  
  // Routes d'administration
  {
    path: '/admin/user-management',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true, admin: true }
  },
  {
    path: '/admin/registration-requests',
    name: 'RegistrationRequests',
    component: RegistrationRequests,
    meta: { requiresAuth: true, admin: true }
  },
  {
    path: '/admin/settings',
    name: 'AdminSettings',
    component: Settings,
    meta: { requiresAuth: true, admin: true, title: 'Paramètres administrateur' }
  },
  
  // Route 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  try {
    const isAuthenticated = store.getters['auth/isAuthenticated']
    const userRoles = store.getters['auth/userRoles'] || []
    
    // Définir le titre de la page si spécifié dans la route
    if (to.meta.title) {
      document.title = `${to.meta.title} | MedLink`
    }

    // Si l'utilisateur est authentifié mais que les rôles ne sont pas encore chargés
    if (isAuthenticated && (!userRoles || userRoles.length === 0)) {
      try {
        await store.dispatch('auth/fetchUserInfo')
        const updatedUserRoles = store.getters['auth/userRoles'] || []
        
        // Redirection personnalisée selon le rôle
        if (hasRole(updatedUserRoles, ROLES.SUPER_ADMIN)) {
          if (!to.path.startsWith('/admin')) {
            next({ path: '/admin/dashboard' })
            return
          }
        } else if (hasRole(updatedUserRoles, ROLES.ADMIN)) {
          if (!to.path.startsWith('/admin')) {
            next({ path: '/admin/inscriptions' })
            return
          }
        } else if (hasRole(updatedUserRoles, ROLES.BLOOD_BANK_MANAGER)) {
          if (!to.path.startsWith('/blood')) {
            next({ path: '/blood/dashboard' })
            return
          }
        } else if (to.path.startsWith('/admin')) {
          // Empêcher l'accès aux routes admin pour les non-admins
          next({ path: '/dashboard' })
          return
        }
      } catch (error) {
        console.error('Erreur lors du chargement des informations utilisateur:', error)
        store.dispatch('auth/logout')
        next({ name: 'Login' })
        return
      }
    }

    // Rediriger vers la page de connexion si l'authentification est requise
    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
      console.warn('Accès refusé: authentification requise', { path: to.fullPath })
      next({ 
        name: 'Login', 
        query: { 
          redirect: to.fullPath,
          message: 'Veuillez vous connecter pour accéder à cette page.'
        } 
      })
      return
    }

    // Rediriger les utilisateurs connectés qui essaient d'accéder aux pages de connexion
    if (to.matched.some(record => record.meta.guest) && isAuthenticated) {
      console.info('Utilisateur déjà connecté, redirection vers le tableau de bord')
      next({ name: 'Dashboard' })
      return
    }

    // Vérifier les rôles requis pour la route
    if (to.meta.roles) {
      const hasRequiredRole = hasRole(userRoles, to.meta.roles)
      if (!hasRequiredRole) {
        console.warn('Accès refusé: rôles insuffisants', { 
          path: to.fullPath, 
          userRoles,
          requiredRoles: to.meta.roles 
        })
        next({ 
          name: 'Dashboard',
          query: { 
            error: 'unauthorized',
            message: 'Vous n\'avez pas les droits nécessaires pour accéder à cette page.'
          } 
        })
        return
      }
    }

    // Vérifier les groupes de rôles requis
    if (to.meta.roleGroups) {
      const hasRequiredGroup = hasRoleGroup(userRoles, to.meta.roleGroups)
      if (!hasRequiredGroup) {
        console.warn('Accès refusé: groupes de rôles insuffisants', { 
          path: to.fullPath, 
          userRoles,
          requiredGroups: to.meta.roleGroups 
        })
        next({ 
          name: 'Dashboard',
          query: { 
            error: 'unauthorized',
            message: 'Vous n\'avez pas les droits nécessaires pour accéder à cette page.'
          } 
        })
        return
      }
    }

    // Vérifier l'accès adminOnly (pour la rétrocompatibilité)
    if (to.matched.some(record => record.meta.adminOnly)) {
      const isAdmin = hasRole(userRoles, [ROLES.ADMIN, ROLES.SUPER_ADMIN])
      if (!isAdmin) {
        next({ 
          name: 'Dashboard',
          query: { 
            error: 'unauthorized',
            message: 'Accès réservé aux administrateurs.'
          } 
        })
        return
      }
    }

    // Tout est bon, on peut continuer
    next()
  } catch (error) {
    console.error('Erreur dans le navigation guard:', error);
    next(false); // Annule la navigation en cas d'erreur
  }
})

export default router