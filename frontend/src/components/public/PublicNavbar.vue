<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-2xl font-bold text-green-600">
              MedLink
            </router-link>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link 
              to="/" 
              class="inline-flex items-center px-1 pt-1 border-b-2"
              :class="[$route.path === '/' ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']"
            >
              Accueil
            </router-link>
            <router-link 
              to="/appointment" 
              class="inline-flex items-center px-1 pt-1 border-b-2"
              :class="[$route.path === '/appointment' ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']"
            >
              Rendez-vous
            </router-link>
            <router-link 
              to="/donor" 
              class="inline-flex items-center px-1 pt-1 border-b-2"
              :class="[$route.path === '/donor' ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']"
            >
              Don de sang
            </router-link>
            <router-link 
              to="/contact" 
              class="inline-flex items-center px-1 pt-1 border-b-2"
              :class="[$route.path === '/contact' ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']"
            >
              Contact
            </router-link>
          </div>
        </div>
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <router-link 
            to="/login" 
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
          >
            Espace personnel
          </router-link>
        </div>
        <div class="-mr-2 flex items-center sm:hidden">
          <button 
            @click="isOpen = !isOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-green-500"
          >
            <span class="sr-only">Ouvrir le menu</span>
            <svg 
              class="h-6 w-6" 
              :class="{'hidden': isOpen, 'block': !isOpen}"
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg 
              class="h-6 w-6" 
              :class="{'block': isOpen, 'hidden': !isOpen}"
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Menu mobile -->
    <div class="sm:hidden" :class="{'block': isOpen, 'hidden': !isOpen}">
      <div class="pt-2 pb-3 space-y-1">
        <router-link 
          to="/" 
          class="block pl-3 pr-4 py-2 border-l-4"
          :class="[$route.path === '/' ? 'border-green-500 text-green-700 bg-green-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
        >
          Accueil
        </router-link>
        <router-link 
          to="/appointment" 
          class="block pl-3 pr-4 py-2 border-l-4"
          :class="[$route.path === '/appointment' ? 'border-green-500 text-green-700 bg-green-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
        >
          Rendez-vous
        </router-link>
        <router-link 
          to="/donor" 
          class="block pl-3 pr-4 py-2 border-l-4"
          :class="[$route.path === '/donor' ? 'border-green-500 text-green-700 bg-green-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
        >
          Don de sang
        </router-link>
        <router-link 
          to="/contact" 
          class="block pl-3 pr-4 py-2 border-l-4"
          :class="[$route.path === '/contact' ? 'border-green-500 text-green-700 bg-green-50' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']"
        >
          Contact
        </router-link>
        <router-link 
          to="/login" 
          class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700"
        >
          Espace personnel
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

defineOptions({
  name: 'PublicNavbar'
});

const isOpen = ref(false);
</script> 