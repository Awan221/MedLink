<template>
  <div class="h-full flex flex-col bg-white border-r border-gray-200">
    <!-- Logo -->
    <div class="flex items-center h-16 flex-shrink-0 px-4 border-b border-gray-200">
      <router-link to="/" class="text-primary-600 font-bold text-xl">
        Orthanc Telemedicine
      </router-link>
    </div>
    
    <!-- Navigation -->
    <nav class="mt-5 flex-1 px-2 bg-white space-y-1">
      <router-link 
        v-for="item in navigationItems" 
        :key="item.name" 
        :to="item.to" 
        :class="[
          $route.path.includes(item.to.path) 
            ? 'bg-primary-50 text-primary-600' 
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900',
          'group flex items-center px-2 py-2 text-sm font-medium rounded-md'
        ]"
      >
        <component 
          :is="item.icon" 
          :class="[
            $route.path.includes(item.to.path) 
              ? 'text-primary-500' 
              : 'text-gray-400 group-hover:text-gray-500',
            'mr-3 flex-shrink-0 h-6 w-6'
          ]" 
          aria-hidden="true" 
        />
        {{ item.name }}
      </router-link>
    </nav>
    
    <!-- User Info -->
    <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
      <div class="flex-shrink-0 w-full group block">
        <div class="flex items-center">
          <div class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 font-semibold">
            {{ userInitials }}
          </div>
          <div class="ml-3">
            <p class="text-sm font-medium text-gray-700 group-hover:text-gray-900">
              {{ currentUser.first_name }} {{ currentUser.last_name }}
            </p>
            <p class="text-xs font-medium text-gray-500 group-hover:text-gray-700">
              {{ userRoleDisplay }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

// Icônes (à remplacer par vos propres composants d'icônes)

const DashboardIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
      d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 
      0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
  </svg>`
}

const PatientsIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
      d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 
      20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 
      019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 
      0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
  </svg>`
}

const ImagingIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>`
}

const BloodBankIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
  </svg>`
}

const ChatbotIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
  </svg>`
}

const AIIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
  </svg>`
}

const AdminIcon = {
  template: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>`
}

export default {
  name: 'AppSidebar',
  components: {
    DashboardIcon,
    PatientsIcon,
    ImagingIcon,
    BloodBankIcon,
    ChatbotIcon,
    AIIcon,
    AdminIcon
  },
  setup() {
    const store = useStore()
    
    const currentUser = computed(() => store.getters['auth/currentUser'])
    const userRole = computed(() => store.getters['auth/userRole'])
    
    const userInitials = computed(() => {
      if (!currentUser.value) return ''
      
      const firstInitial = currentUser.value.first_name ? currentUser.value.first_name.charAt(0) : ''
      const lastInitial = currentUser.value.last_name ? currentUser.value.last_name.charAt(0) : ''
      
      return `\${firstInitial}\${lastInitial}`.toUpperCase()
    })
    
    const userRoleDisplay = computed(() => {
      const roleMap = {
        'ADMIN': 'Administrateur',
        'SUPER_ADMIN': 'Super Administrateur',
        'MEDECIN': 'Médecin Généraliste',
        'SPECIALISTE': 'Médecin Spécialiste',
        'RADIOLOGUE': 'Radiologue',
        'TECHNICIEN': 'Technicien en Imagerie',
        'BANQUE_SANG': 'Responsable Banque de Sang',
        'AUTRE': 'Autre Personnel Médical'
      }
      
      return roleMap[userRole.value] || userRole.value
    })
    
    const navigationItems = computed(() => {
      const items = [
        { name: 'Tableau de bord', to: { path: '/app/dashboard' }, icon: 'DashboardIcon' }
      ]
      
      // Ajouter les éléments de navigation en fonction du rôle
      if (['MEDECIN', 'SPECIALISTE', 'ADMIN', 'SUPER_ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Patients', to: { path: '/app/patients' }, icon: 'PatientsIcon' })
      }
      
      if (['MEDECIN', 'SPECIALISTE', 'RADIOLOGUE', 'TECHNICIEN'].includes(userRole.value)) {
        items.push({ name: 'Imagerie', to: { path: '/app/imaging/studies' }, icon: 'ImagingIcon' })
      }
      
      if (['MEDECIN', 'SPECIALISTE', 'BANQUE_SANG', 'ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Banque de Sang', to: { path: '/app/blood-bank' }, icon: 'BloodBankIcon' })
      }
      
      items.push({ name: 'Chatbot Médical', to: { path: '/app/chatbot' }, icon: 'ChatbotIcon' })
      
      if (['MEDECIN', 'SPECIALISTE', 'ADMIN'].includes(userRole.value)) {
        items.push({ name: 'IA Diagnostic', to: { path: '/app/ai-diagnostic' }, icon: 'AIIcon' })
      }
      
      if (['ADMIN', 'SUPER_ADMIN'].includes(userRole.value)) {
        items.push({ name: 'Administration', to: { path: '/app/admin/users' }, icon: 'AdminIcon' })
      }
      
      return items
    })
    
    return {
      currentUser,
      userInitials,
      userRoleDisplay,
      navigationItems
    }
  }
}
</script>