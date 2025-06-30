<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex justify-between h-16">
        <div class="flex">
          <!-- Logo -->
          <div class="flex-shrink-0 flex items-center">
            <router-link to="/" class="text-xl font-bold text-blue-600">
              MedLink
            </router-link>
          </div>

          <!-- Navigation Links -->
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              to="/public"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-900"
              active-class="border-b-2 border-blue-500"
            >
              Accueil
            </router-link>

            <router-link
              to="/public/maladies"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              active-class="border-b-2 border-blue-500 text-gray-900"
            >
              Documentation Médicale
            </router-link>

            <router-link
              to="/public/hopitaux"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              active-class="border-b-2 border-blue-500 text-gray-900"
            >
              Hôpitaux à Proximité
            </router-link>

            <router-link
              to="/public/rdv"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              active-class="border-b-2 border-blue-500 text-gray-900"
            >
              Prendre RDV
            </router-link>

            <router-link
              to="/public/don"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              active-class="border-b-2 border-blue-500 text-gray-900"
            >
              Don de Sang
            </router-link>

            <router-link
              to="/public/contact"
              class="inline-flex items-center px-1 pt-1 text-sm font-medium text-gray-500 hover:text-gray-900"
              active-class="border-b-2 border-blue-500 text-gray-900"
            >
              Contact
            </router-link>
          </div>
        </div>

        <!-- Boutons de connexion/inscription -->
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <router-link
            to="/login"
            class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50"
          >
            Connexion
          </router-link>
          <router-link
            to="/register"
            class="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Inscription
          </router-link>
        </div>

        <!-- Menu mobile -->
        <div class="flex items-center sm:hidden">
          <button
            @click="isOpen = !isOpen"
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
          >
            <span class="sr-only">Ouvrir le menu</span>
            <svg
              class="h-6 w-6"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                v-if="!isOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Menu mobile déroulant -->
    <div
      v-show="isOpen"
      class="sm:hidden"
    >
      <div class="pt-2 pb-3 space-y-1">
        <router-link
          to="/public"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Accueil
        </router-link>

        <router-link
          to="/public/maladies"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Documentation Médicale
        </router-link>

        <router-link
          to="/public/hopitaux"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Hôpitaux à Proximité
        </router-link>

        <router-link
          to="/public/rdv"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Prendre RDV
        </router-link>

        <router-link
          to="/public/don"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Don de Sang
        </router-link>

        <router-link
          to="/public/contact"
          class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          active-class="bg-blue-50 border-l-4 border-blue-500 text-blue-700"
        >
          Contact
        </router-link>
      </div>

      <div class="pt-4 pb-3 border-t border-gray-200">
        <div class="space-y-1">
          <router-link
            to="/login"
            class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          >
            Connexion
          </router-link>
          <router-link
            to="/register"
            class="block pl-3 pr-4 py-2 text-base font-medium text-gray-700 hover:bg-gray-50"
          >
            Inscription
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navigation',
  data() {
    return {
      isOpen: false
    }
  }
}
</script> 