<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md mx-auto">
      <div class="text-center">
        <div class="inline-block p-3 rounded-full bg-white shadow-lg mb-4">
          <svg class="w-12 h-12 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
          </svg>
        </div>
        <h2 class="text-3xl font-extrabold text-gray-900 sm:text-4xl bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-indigo-600">
          Réinitialisation du mot de passe
        </h2>
        <p class="mt-4 text-lg text-gray-600">
          Entrez votre nouveau mot de passe
        </p>
      </div>

      <div class="mt-8 bg-white shadow-xl rounded-2xl overflow-hidden">
        <div class="px-8 py-6 border-b border-gray-200 bg-gradient-to-r from-primary-50 to-indigo-50">
          <h3 class="text-xl font-semibold text-gray-900">
            Créer un nouveau mot de passe
          </h3>
        </div>

        <form class="space-y-6 p-8" @submit.prevent="handleResetPassword">
          <transition name="fade" mode="out-in">
            <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg" role="alert">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium">{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </transition>

          <div class="form-group">
            <label for="password" class="block text-sm font-medium text-gray-700">
              Nouveau mot de passe
            </label>
            <div class="mt-1 relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input 
                id="password" 
                name="password" 
                type="password" 
                required 
                v-model="formData.password"
                pattern="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
                title="Le mot de passe doit contenir au moins 8 caractères, une lettre, un chiffre et un caractère spécial"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
            <p class="mt-1 text-sm text-gray-500">
              Le mot de passe doit contenir au moins 8 caractères, une lettre, un chiffre et un caractère spécial
            </p>
          </div>

          <div class="form-group">
            <label for="password_confirmation" class="block text-sm font-medium text-gray-700">
              Confirmer le mot de passe
            </label>
            <div class="mt-1 relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input 
                id="password_confirmation" 
                name="password_confirmation" 
                type="password" 
                required 
                v-model="formData.password_confirmation"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
              />
            </div>
          </div>

          <div class="flex justify-end">
            <button 
              type="submit" 
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? 'Réinitialisation en cours...' : 'Réinitialiser le mot de passe' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  data() {
    return {
      formData: {
        password: '',
        password_confirmation: '',
        token: ''
      },
      loading: false,
      errorMessage: ''
    }
  },
  created() {
    // Récupérer le token depuis l'URL
    const urlParams = new URLSearchParams(window.location.search)
    this.formData.token = urlParams.get('token')
    
    if (!this.formData.token) {
      this.errorMessage = 'Token de réinitialisation invalide ou manquant'
    }
  },
  methods: {
    async handleResetPassword() {
      this.loading = true
      this.errorMessage = ''

      try {
        // Validation des données
        if (this.formData.password !== this.formData.password_confirmation) {
          throw new Error('Les mots de passe ne correspondent pas')
        }

        // Envoi de la requête
        const response = await fetch('/api/auth/reset-password', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.formData)
        })

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.message || 'Une erreur est survenue lors de la réinitialisation du mot de passe')
        }

        // Redirection vers la page de connexion avec un message de succès
        this.$router.push({
          path: '/login',
          query: { message: 'Votre mot de passe a été réinitialisé avec succès' }
        })
      } catch (error) {
        this.errorMessage = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
