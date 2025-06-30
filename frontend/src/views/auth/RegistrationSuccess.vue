<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <div class="text-center">
        <div class="inline-block p-3 rounded-full bg-green-100 mb-4">
          <svg class="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="text-4xl font-extrabold text-gray-900 sm:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-green-600 to-blue-600">
          Demande d'inscription envoyée !
        </h2>
        <p class="mt-4 text-xl text-gray-600">
          Votre demande d'inscription a été envoyée avec succès.
        </p>
      </div>

      <div class="mt-12 bg-white shadow-xl rounded-2xl overflow-hidden">
        <div class="px-8 py-6 border-b border-gray-200 bg-gradient-to-r from-green-50 to-blue-50">
          <h3 class="text-2xl font-semibold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Prochaines étapes
          </h3>
        </div>

        <div class="px-8 py-6 space-y-6">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="ml-3">
              <h4 class="text-lg font-medium text-gray-900">Vérifiez votre email</h4>
              <p class="mt-1 text-gray-600">
                Un email de confirmation a été envoyé à votre adresse. Veuillez vérifier votre boîte de réception et votre dossier spam.
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="ml-3">
              <h4 class="text-lg font-medium text-gray-900">Validation de votre compte</h4>
              <p class="mt-1 text-gray-600">
                Notre équipe va examiner votre demande et valider vos informations. Ce processus peut prendre jusqu'à 48 heures.
              </p>
            </div>
          </div>

          <div class="flex items-start">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <div class="ml-3">
              <h4 class="text-lg font-medium text-gray-900">Accès à la plateforme</h4>
              <p class="mt-1 text-gray-600">
                Une fois votre compte validé, vous recevrez un email avec les instructions pour vous connecter à la plateforme.
              </p>
            </div>
          </div>
        </div>

        <div class="px-8 py-6 bg-gray-50 border-t border-gray-200">
          <div class="flex justify-center space-x-4">
            <router-link 
              to="/login" 
              class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Retour à la connexion
            </router-link>
            <a 
              href="/contact" 
              class="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Nous contacter
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegistrationSuccess',
  mounted() {
    // Rediriger vers la page de connexion après 30 secondes
    setTimeout(() => {
      this.$router.push('/login')
    }, 30000)
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