<template>
  <nav class="bg-white border-b border-gray-200 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo et titre -->
        <div class="flex items-center">
          <router-link to="/" class="flex-shrink-0 flex items-center">
            <img class="h-8 w-auto" src="@/assets/logo-medlink.svg" alt="MedLink Logo">
            <span class="ml-3 text-xl font-semibold text-gray-800">MedLink</span>
          </router-link>
          
          <!-- Navigation principale -->
          <div class="hidden md:ml-10 md:flex md:space-x-6">
            <router-link 
              v-for="item in navItems" 
              :key="item.name" 
              :to="item.path" 
              v-permission="item.roles"
              class="inline-flex items-center px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors duration-200"
              active-class="text-blue-600 bg-blue-50"
            >
              {{ item.name }}
            </router-link>
          </div>
        </div>

        <!-- Menu utilisateur -->
        <div class="hidden md:ml-4 md:flex md:items-center">
          <div class="relative" v-if="user">
            <div>
              <button 
                @click="userMenuOpen = !userMenuOpen" 
                class="flex items-center max-w-xs text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                id="user-menu" 
                aria-expanded="false" 
                aria-haspopup="true"
              >
                <span class="sr-only">Ouvrir le menu utilisateur</span>
                <div class="flex items-center">
                  <div class="text-right mr-3">
                    <p class="text-sm font-medium text-gray-700">{{ user.first_name }} {{ user.last_name }}</p>
                    <p class="text-xs text-gray-500">{{ getUserRoleLabel(user.role) }}</p>
                  </div>
                  <div class="h-9 w-9 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 border border-gray-200">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                    </svg>
                  </div>
                </div>
              </button>
            </div>
            
            <!-- Menu déroulant utilisateur -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div 
                v-if="userMenuOpen"
                class="origin-top-right absolute right-0 mt-2 w-56 rounded-lg shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-50 py-1.5"
                role="menu"
                aria-orientation="vertical"
                aria-labelledby="user-menu"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <p class="text-sm font-medium text-gray-900">{{ user.first_name }} {{ user.last_name }}</p>
                  <p class="text-xs text-gray-500">{{ user.email }}</p>
                </div>
                <div class="py-1">
                  <router-link 
                    to="/profile" 
                    class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                    role="menuitem"
                    @click="userMenuOpen = false"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    Mon profil
                  </router-link>
                  <router-link 
                    to="/settings" 
                    class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-colors"
                    role="menuitem"
                    @click="userMenuOpen = false"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    Paramètres
                  </router-link>
                </div>
                <div class="border-t border-gray-100 my-1"></div>
                <div class="py-1">
                  <button 
                    @click="logout" 
                    class="w-full flex items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    role="menuitem"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-3 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Déconnexion
                  </button>
                </div>
              </div>
            </transition>
          </div>
        </div>

        <!-- Bouton menu mobile -->
        <div class="flex items-center md:hidden">
          <button 
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-600 hover:text-gray-900 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            aria-expanded="false"
          >
            <span class="sr-only">Ouvrir le menu principal</span>
            <svg v-if="!mobileMenuOpen" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Menu mobile -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div v-if="mobileMenuOpen" class="md:hidden bg-white shadow-xl ring-1 ring-black ring-opacity-5">
        <!-- En-tête du menu mobile -->
        <div class="px-4 pt-4 pb-3 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <img class="h-8 w-auto" src="@/assets/logo-medlink.svg" alt="MedLink">
              <span class="ml-2 text-xl font-semibold text-gray-800">Menu</span>
            </div>
            <button 
              @click="mobileMenuOpen = false"
              class="rounded-md p-2 text-gray-500 hover:bg-gray-100 focus:outline-none"
            >
              <span class="sr-only">Fermer le menu</span>
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Navigation mobile -->
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            v-for="item in navItems" 
            :key="item.name" 
            :to="item.path" 
            v-permission="item.roles"
            class="mx-4 my-1 block rounded-md px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
            active-class="bg-blue-50 text-blue-600"
            @click="mobileMenuOpen = false"
          >
            {{ item.name }}
          </router-link>
        </div>
        
        <!-- Menu utilisateur mobile -->
        <div v-if="user" class="border-t border-gray-200 pt-4 pb-3">
          <div class="flex items-center px-4">
            <div class="h-10 w-10 flex-shrink-0 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <div class="text-base font-medium text-gray-800">{{ user.first_name }} {{ user.last_name }}</div>
              <div class="text-sm font-medium text-gray-500">{{ user.email }}</div>
            </div>
          </div>
          <div class="mt-3 space-y-1">
            <router-link 
              to="/profile" 
              class="mx-4 my-1 block rounded-md px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
              @click="mobileMenuOpen = false"
            >
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                Mon profil
              </div>
            </router-link>
            <router-link 
              to="/settings" 
              class="mx-4 my-1 block rounded-md px-3 py-2 text-base font-medium text-gray-700 hover:bg-gray-50 hover:text-blue-600"
              @click="mobileMenuOpen = false"
            >
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Paramètres
              </div>
            </router-link>
            <button 
              @click="logout" 
              class="w-full text-left mx-4 my-1 block rounded-md px-3 py-2 text-base font-medium text-red-600 hover:bg-red-50"
            >
              <div class="flex items-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-3 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Déconnexion
              </div>
            </button>
          </div>
        </div>
      </div>
    </transition>
  </nav>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'NavbarView',
  
  data() {
    return {
      userMenuOpen: false,
      mobileMenuOpen: false,
      navItems: [
        { name: 'Tableau de bord', path: '/dashboard', roles: ['ADMIN', 'MEDECIN', 'INFIRMIER', 'BANQUE_SANG'] },
        { name: 'Patients', path: '/patients', roles: ['ADMIN', 'MEDECIN', 'INFIRMIER'] },
        { name: 'Rendez-vous', path: '/appointments', roles: ['ADMIN', 'MEDECIN', 'INFIRMIER'] },
        { name: 'Dossiers médicaux', path: '/medical-records', roles: ['ADMIN', 'MEDECIN', 'INFIRMIER'] },
        { name: 'Ordonnances', path: '/prescriptions', roles: ['ADMIN', 'MEDECIN'] },
        { name: 'Demandes', path: '/registration-requests', roles: ['ADMIN'] },
        { name: 'Utilisateurs', path: '/users', roles: ['ADMIN'] },
        { name: 'Stocks de sang', path: '/blood-stocks', roles: ['ADMIN', 'BANQUE_SANG'] },
        { name: 'Rapports', path: '/reports', roles: ['ADMIN'] }
      ]
    }
  },

  computed: {
    ...mapGetters('auth', ['user', 'userRole'])
  },
  methods: {
    ...mapActions('auth', ['logout']),
    toggleUserMenu() {
      console.log('toggleUserMenu called, current:', this.userMenuOpen);
      this.userMenuOpen = !this.userMenuOpen;
      // DEBUG: force ouverture
      // this.userMenuOpen = true;
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMenus() {
      this.userMenuOpen = false
      this.mobileMenuOpen = false
    },
    getUserRoleLabel(role) {
      const roles = {
        'ADMIN': 'Administrateur',
        'MEDECIN': 'Médecin',
        'INFIRMIER': 'Infirmier',
        'BANQUE_SANG': 'Banque de sang',
        'PATIENT': 'Patient'
      };
      return roles[role] || role;
    }
  },
  mounted() {
    this._onClickOutside = (e) => {
      if (!this.$el.contains(e.target)) {
        this.closeMenus()
      }
    }
    document.addEventListener('click', this._onClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this._onClickOutside)
  }
}
</script>