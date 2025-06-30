<template>
  <header class="bg-white shadow">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
      <!-- Logo et navigation principale -->
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-primary-600 font-bold text-xl">
              Orthanc Telemedicine
            </router-link>
          </div>
          <nav v-if="isAuthenticated" class="hidden md:ml-6 md:flex md:space-x-8">
            <router-link 
              v-for="item in navigationItems" 
              :key="item.name" 
              :to="item.to" 
              :class="[
                $route.path.includes(item.to.path) 
                  ? 'border-primary-500 text-gray-900' 
                  : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
              ]"
            >
              {{ item.name }}
            </router-link>
          </nav>
        </div>
        
        <!-- Boutons d'action -->
        <div class="flex items-center">
          <div v-if="!isAuthenticated" class="flex-shrink-0">
            <router-link 
              to="/auth/login" 
              class="relative inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Connexion
            </router-link>
            <router-link 
              to="/auth/register" 
              class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Inscription
            </router-link>
          </div>
          
          <!-- Menu utilisateur -->
          <div v-else class="ml-3 relative">
            <div>
              <button 
                @click="toggleUserMenu" 
                class="max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <span class="sr-only">Ouvrir le menu utilisateur</span>
                <div class="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-semibold">
                  {{ userInitials }}
                </div>
              </button>
            </div>
            
            <div 
              v-if="showUserMenu" 
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
            >
              <div class="px-4 py-2 text-sm text-gray-700 border-b border-gray-200">
                <div class="font-medium">{{ currentUser.first_name }} {{ currentUser.last_name }}</div>
                <div class="text-gray-500">{{ currentUser.email }}</div>
              </div>
              <router-link 
                to="/app/dashboard" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                Tableau de bord
              </router-link>
              <router-link 
                to="/app/profile" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                @click="showUserMenu = false"
              >
                Profil
              </router-link>
              <button 
                @click="logout" 
                class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Déconnexion
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { computed, ref, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AppHeader',
  setup() {
    const store = useStore()
    const router = useRouter()
    const showUserMenu = ref(false)
    
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated'])
    const currentUser = computed(() => store.getters['auth/currentUser'])
    const userRole = computed(() => store.getters['auth/userRole'])
    
    const userInitials = computed(() => {
      if (!currentUser.value) return ''
      
      //const firstInitial = currentUser.value.first_name ? currentUser.value.first_name.charAt(0) : ''
      //const lastInitial = currentUser.value.last_name ? currentUser.value.last_name.charAt(0) : ''
      
      return '${firstInitial}${lastInitial}'.toUpperCase()
    })
    
    const navigationItems = computed(() => {
      const items = [
        { name: 'Tableau de bord', to: { path: '/app/dashboard' } }
      ]
      
      // Ajouter les éléments de navigation en fonction du rôle
      if (['MEDECIN', 'SPECIALISTE', 'ADMIN', 'SUPER_ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Patients', to: { path: '/app/patients' } })
      }
      
      if (['MEDECIN', 'SPECIALISTE', 'RADIOLOGUE', 'TECHNICIEN'].includes(userRole.value)) {
        items.push({ name: 'Imagerie', to: { path: '/app/imaging' } })
      }
      
      if (['MEDECIN', 'SPECIALISTE', 'BANQUE_SANG', 'ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Banque de Sang', to: { path: '/app/blood-bank' } })
      }
      
      if (['MEDECIN', 'SPECIALISTE', 'ADMIN'].includes(userRole.value)) {
        items.push({ name: 'IA Diagnostic', to: { path: '/app/ai-diagnostic' } })
      }
      
      if (['ADMIN', 'SUPER_ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Administration', to: { path: '/app/admin' } })
      }
      
      return items
    })
    
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const logout = () => {
      store.dispatch('auth/logout')
      showUserMenu.value = false
      router.push({ name: 'home' })
    }
    
    // Fermer le menu utilisateur lorsqu'on clique en dehors
    const handleClickOutside = (event) => {
      if (showUserMenu.value && !event.target.closest('.relative')) {
        showUserMenu.value = false
      }
    }
    
    // Ajouter l'écouteur d'événement lors du montage du composant
    window.addEventListener('click', handleClickOutside)
    
    // Nettoyer l'écouteur d'événement lors du démontage du composant
    onUnmounted(() => {
      window.removeEventListener('click', handleClickOutside)
    })
    
    return {
      isAuthenticated,
      currentUser,
      userInitials,
      navigationItems,
      showUserMenu,
      toggleUserMenu,
      logout
    }
  }
}
</script>