import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/css/tailwind.css'
import 'leaflet/dist/leaflet.css'  // CSS de Leaflet
import 'animate.css/animate.min.css'  // CSS pour les animations
import axios from 'axios'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import Swal from 'sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

// Configuration d'Axios
axios.defaults.baseURL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api'

// Intercepteur pour ajouter le token JWT aux requêtes
axios.interceptors.request.use(
  config => {
    const token = store.getters['auth/token']
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Intercepteur pour gérer les erreurs d'authentification
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      store.dispatch('auth/logout')
      router.push('/login')
    } else if (error.response && error.response.status === 403) {
      if (typeof window !== 'undefined') {
        Swal.fire({
          title: 'Accès refusé',
          text: 'Vous n\'avez pas les droits suffisants pour accéder à cette ressource.',
          icon: 'error',
          confirmButtonColor: '#3b82f6'
        })
      }
      router.push('/dashboard')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

// Configuration de vue-toastification
app.use(Toast, {
  position: 'top-right',
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false
})

// Ajouter SweetAlert2 aux propriétés globales de l'application
app.config.globalProperties.$swal = Swal

app.use(router)
app.use(store)

// Directive pour gérer les permissions
app.directive('permission', {
  mounted(el, binding) {
    const { value } = binding
    const userRole = store.getters['auth/userRole']
    
    if (!userRole || (Array.isArray(value) && !value.includes(userRole))) {
      el.style.display = 'none'
    }
  }
})

app.mount('#app')