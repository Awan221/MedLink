import axios from 'axios'
import store from '@/store'
import router from '@/router'
import { getTokenExpiration } from '@/utils/auth'

// Créer une instance Axios avec la configuration de base
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Intercepteur de requêtes
api.interceptors.request.use(
  async config => {
    const token = localStorage.getItem('token')

    if (token) {
      const expiration = getTokenExpiration(token)
      const now = Date.now() / 1000

      if (expiration && now > expiration) {
        try {
          await store.dispatch('auth/refreshToken')
          const newToken = localStorage.getItem('token')
          config.headers.Authorization = `Bearer ${newToken}`
        } catch (error) {
          store.dispatch('auth/logout')
          router.push({ name: 'login' })
          return Promise.reject(error)
        }
      } else {
        config.headers.Authorization = `Bearer ${token}`
      }
    }

    return config
  },
  error => Promise.reject(error)
)

// Intercepteur de réponses
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        await store.dispatch('auth/refreshToken')
        const token = localStorage.getItem('token')

        api.defaults.headers.common['Authorization'] = `Bearer ${token}`
        originalRequest.headers['Authorization'] = `Bearer ${token}`

        return api(originalRequest)
      } catch (refreshError) {
        store.dispatch('auth/logout')
        router.push({ name: 'login' })
        return Promise.reject(refreshError)
      }
    }

    if (error.response) {
      if (error.response.status === 403) {
        router.push({ name: 'forbidden' })
      } else if (error.response.status === 404) {
        router.push({ name: 'not-found' })
      } else if (error.response.status >= 500) {
        store.dispatch('setError', {
          message: 'Une erreur serveur s\'est produite. Veuillez réessayer plus tard.',
          status: error.response.status
        })
      }
    }

    return Promise.reject(error)
  }
)

export default api