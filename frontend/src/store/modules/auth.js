import axios from 'axios'
import router from '@/router'

const state = {
  token: localStorage.getItem('token') || null,
  refreshToken: localStorage.getItem('refreshToken') || null,
  user: JSON.parse(localStorage.getItem('user')) || null,
  loading: false,
  error: null,
  success: null
}

const getters = {
  isAuthenticated: state => !!state.token && !!state.user,
  user: state => state.user,
  userRole: state => state.user ? state.user.role : null,
  userRoles: state => state.user && state.user.roles ? state.user.roles : state.user && state.user.role ? [state.user.role] : [],
  token: state => state.token,
  loading: state => state.loading,
  error: state => state.error,
  success: state => state.success,
  currentUser: state => state.user
}

const actions = {
  async login({ commit,dispatch }, credentials) {
    commit('setLoading', true)
    commit('setError', null)
    
    try {
      const response = await axios.post('/auth/token/', credentials)
      
      const { access, refresh } = response.data
      
      // Stocker les tokens
      localStorage.setItem('token', access)
      localStorage.setItem('refreshToken', refresh)
      
      commit('setToken', access)
      commit('setRefreshToken', refresh)
      
      // Récupérer les informations de l'utilisateur
      await dispatch('fetchUserInfo')
      //router.replace({name:'Dashboard'})
      await router.replace({ path: router.currentRoute.value.query.redirect || '/dashboard' })
    } catch (error) {
      commit('setError', error.response ? error.response.data : 'Erreur de connexion')
    } finally {
      commit('setLoading', false)
    }
  },
  
  async register({ commit }, userData) {
    commit('setLoading', true)
    commit('setError', null)
    try {
      await axios.post('/api/auth/register/', userData)
      commit('setSuccess', "Votre demande d'inscription a bien été envoyée. Elle sera validée par un administrateur.")
      return true
    } catch (error) {
      commit('setError', error.response ? error.response.data : "Erreur d'inscription")
      return false
    } finally {
      commit('setLoading', false)
    }
  },
  
  async logout({ commit }) {
    try {
      const refreshToken = localStorage.getItem('refreshToken')
      if (refreshToken) {
        await axios.post('/auth/logout/', { refresh: refreshToken })
      }
    } catch (error) {
      console.error('Erreur lors de la déconnexion:', error)
    }
    
    // Supprimer les tokens et les informations utilisateur
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    
    commit('setToken', null)
    commit('setRefreshToken', null)
    commit('setUser', null)
    
    router.push('/login')
  },
  
  async fetchUserInfo({ commit }) {
    console.log('fetchUserInfo called');
    try {
      const response = await axios.get('/auth/me/')
      const user = response.data
      console.log('User info fetched:', user);
      console.log('User role:', user?.role);
      if (user) {
        localStorage.setItem('user', JSON.stringify(user))
        commit('setUser', user)
        if (user.email) {
          localStorage.setItem('userEmail', user.email);
        }
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des informations utilisateur:', error)
    }
  },
  
  async refreshToken({ commit, state }) {
    try {
      const response = await axios.post('/auth/token/refresh/', {
        refresh: state.refreshToken
      })
      
      const { access } = response.data
      
      localStorage.setItem('token', access)
      commit('setToken', access)
      
      return access
    } catch (error) {
      console.error('Erreur lors du rafraîchissement du token:', error)
      commit('setToken', null)
      commit('setRefreshToken', null)
      commit('setUser', null)
      
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('user')
      
      router.push('/login')
    }
  },
  
  checkAuth({state, dispatch }) {
    if (state.token && state.user) {
      // Vérifier si le token est expiré
      const tokenData = JSON.parse(atob(state.token.split('.')[1]))
      const expirationTime = tokenData.exp * 1000
      
      if (Date.now() >= expirationTime) {
        // Token expiré, essayer de le rafraîchir
        dispatch('refreshToken')
      }
    }
  }
}

const mutations = {
  setSuccess(state, success) {
    state.success = success
  },
  setToken(state, token) {
    state.token = token
  },
  setRefreshToken(state, refreshToken) {
    state.refreshToken = refreshToken
  },
  setUser(state, user) {
    state.user = user
  },
  setLoading(state, loading) {
    state.loading = loading
  },
  setError(state, error) {
    state.error = error
  }
}

// Fonction utilitaire pour décoder l'email du token JWT
//eslint-disable-next-line no-unused-vars
function getUserIdFromToken() {
  try {
    const token = localStorage.getItem('token');
    if (!token) return null;
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id || null;
  } catch (e) {
    return null;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}