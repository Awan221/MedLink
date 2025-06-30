<template>
  <div>
    <div v-if="!emailSent">
      <div class="mb-4 text-sm text-gray-600">
        <p>Veuillez entrer votre adresse email et nous vous enverrons un lien pour réinitialiser votre mot de passe.</p>
      </div>
      
      <form class="space-y-6" @submit.prevent="handleSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Adresse email
          </label>
          <div class="mt-1">
            <input 
              id="email" 
              name="email" 
              type="email" 
              autocomplete="email" 
              required 
              v-model="email"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
          </div>
        </div>

        <div>
          <button 
            type="submit" 
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            :disabled="loading"
          >
            <svg 
              v-if="loading" 
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Envoyer le lien de réinitialisation
          </button>
        </div>
        
        <div v-if="error" class="rounded-md bg-red-50 p-4">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">
                Erreur
              </h3>
              <div class="mt-2 text-sm text-red-700">
                <p>{{ error }}</p>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
    
    <div v-else class="text-center">
      <svg class="mx-auto h-12 w-12 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="mt-2 text-lg font-medium text-gray-900">Email envoyé</h3>
      <p class="mt-1 text-sm text-gray-600">
        Un email contenant les instructions pour réinitialiser votre mot de passe a été envoyé à {{ email }}.
      </p>
      <div class="mt-6">
        <router-link 
          to="/auth/login" 
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          Retour à la connexion
        </router-link>
      </div>
    </div>
    
    <div class="text-center mt-6">
      <router-link to="/auth/login" class="font-medium text-primary-600 hover:text-primary-500">
        Retour à la connexion
      </router-link>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
//import axios from 'axios'

export default {
  name: 'ForgotPasswordView',
  setup() {
    const email = ref('')
    const loading = ref(false)
    const error = ref(null)
    const emailSent = ref(false)
    
    const handleSubmit = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Simuler une requête API pour la réinitialisation du mot de passe
        // Dans un environnement réel, vous feriez une requête à votre API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // Simuler une réponse réussie
        emailSent.value = true
      } catch (err) {
        error.value = err.response?.data?.detail || 'Une erreur s\'est produite. Veuillez réessayer.'
      } finally {
        loading.value = false
      }
    }
    
    return {
      email,
      loading,
      error,
      emailSent,
      handleSubmit
    }
  }
}
</script>