<template>
  <div class="h-screen flex overflow-hidden bg-gray-100">
    &lt;!-- Sidebar mobile -->
    <div 
      v-if="sidebarOpen" 
      class="fixed inset-0 flex z-40 md:hidden" 
      role="dialog" 
      aria-modal="true"
    >
      <div 
        class="fixed inset-0 bg-gray-600 bg-opacity-75" 
        aria-hidden="true"
        @click="sidebarOpen = false"
      ></div>
      
      <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white">
        <div class="absolute top-0 right-0 -mr-12 pt-2">
          <button 
            type="button" 
            class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            @click="sidebarOpen = false"
          >
            <span class="sr-only">Fermer la barre latérale</span>
            <svg class="h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <AppSidebar />
      </div>
      
      <div class="flex-shrink-0 w-14">
        <!-- Force sidebar to shrink to fit close icon -->
      </div>
    </div>
    
    <!-- Sidebar desktop -->
    <div class="hidden md:flex md:flex-shrink-0">
      <div class="flex flex-col w-64">
        <AppSidebar />
      </div>
    </div>
    
    <!-- Content area -->
    <div class="flex flex-col w-0 flex-1 overflow-hidden">
      <div class="md:hidden pl-1 pt-1 sm:pl-3 sm:pt-3">
        <button 
          type="button" 
          class="-ml-0.5 -mt-0.5 h-12 w-12 inline-flex items-center justify-center rounded-md text-gray-500 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
          @click="sidebarOpen = true"
        >
          <span class="sr-only">Ouvrir la barre latérale</span>
          <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
      
      <main class="flex-1 relative z-0 overflow-y-auto focus:outline-none">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <router-view />
          </div>
        </div>
      </main>
    </div>
    
    <!-- Notifications -->
    <AppNotification />
  </div>
</template>

<script>
import { ref } from 'vue'
import AppSidebar from '@/components/common/AppSidebar.vue'
import AppNotification from '@/components/common/AppNotification.vue'

export default {
  name: 'MainLayout',
  components: {
    AppSidebar,
    AppNotification
  },
  setup() {
    const sidebarOpen = ref(false)
    
    return {
      sidebarOpen
    }
  }
}
</script>