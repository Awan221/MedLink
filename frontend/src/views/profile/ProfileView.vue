<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- En-tête de la page -->
    <div class="md:flex md:items-center md:justify-between mb-8">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Mon Profil</h2>
        <p class="mt-1 text-sm text-gray-500">Gérez vos informations personnelles et vos préférences.</p>
      </div>
    </div>

    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 class="text-lg leading-6 font-medium text-gray-900">Informations personnelles</h3>
        <p class="mt-1 max-w-2xl text-sm text-gray-500">Ces informations seront visibles par les autres membres de l'équipe.</p>
      </div>
      
      <div class="px-4 py-5 sm:p-6">
        <form @submit.prevent="updateProfile">
          <div class="space-y-6">
            <!-- Photo de profil -->
            <div class="flex items-center">
              <div class="flex-shrink-0 h-16 w-16 rounded-full bg-gray-200 flex items-center justify-center overflow-hidden">
                <svg v-if="!user.profile_picture" class="h-10 w-10 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
                <img v-else :src="user.profile_picture" :alt="`Photo de ${user.first_name}`" class="h-full w-full object-cover">
              </div>
              <div class="ml-4">
                <button type="button" class="text-sm font-medium text-blue-600 hover:text-blue-500 focus:outline-none">
                  Changer
                </button>
                <input type="file" class="hidden" accept="image/*" @change="handleFileUpload">
              </div>
            </div>

            <!-- Champs du formulaire -->
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div class="sm:col-span-3">
                <label for="first_name" class="block text-sm font-medium text-gray-700">Prénom</label>
                <input type="text" id="first_name" v-model="form.first_name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              </div>

              <div class="sm:col-span-3">
                <label for="last_name" class="block text-sm font-medium text-gray-700">Nom</label>
                <input type="text" id="last_name" v-model="form.last_name" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              </div>

              <div class="sm:col-span-4">
                <label for="email" class="block text-sm font-medium text-gray-700">Adresse email</label>
                <input type="email" id="email" v-model="form.email" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              </div>

              <div class="sm:col-span-4">
                <label for="phone" class="block text-sm font-medium text-gray-700">Téléphone</label>
                <input type="tel" id="phone" v-model="form.phone" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
              </div>

              <div class="sm:col-span-6">
                <label for="bio" class="block text-sm font-medium text-gray-700">À propos de moi</label>
                <div class="mt-1">
                  <textarea id="bio" v-model="form.bio" rows="3" class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border border-gray-300 rounded-md"></textarea>
                </div>
                <p class="mt-2 text-sm text-gray-500">Quelques mots pour vous décrire.</p>
              </div>
            </div>
          </div>

          <div class="pt-5">
            <div class="flex justify-end">
              <button type="button" class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Annuler
              </button>
              <button type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Enregistrer les modifications
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'ProfileView',
  
  data() {
    return {
      form: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        bio: ''
      },
      isLoading: false
    };
  },
  
  computed: {
    ...mapGetters('auth', ['user'])
  },
  
  created() {
    this.initializeForm();
  },
  
  methods: {
    initializeForm() {
      if (this.user) {
        this.form = {
          first_name: this.user.first_name || '',
          last_name: this.user.last_name || '',
          email: this.user.email || '',
          phone: this.user.phone || '',
          bio: this.user.bio || ''
        };
      }
    },
    
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Ici, vous pourriez ajouter la logique pour télécharger l'image
        console.log('Fichier sélectionné:', file);
      }
    },
    
    async updateProfile() {
      this.isLoading = true;
      try {
        // Ici, vous pourriez appeler une action Vuex pour mettre à jour le profil
        // await this.$store.dispatch('auth/updateProfile', this.form);
        this.$toast.success('Profil mis à jour avec succès');
      } catch (error) {
        console.error('Erreur lors de la mise à jour du profil:', error);
        this.$toast.error('Une erreur est survenue lors de la mise à jour du profil');
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Styles spécifiques à la page de profil si nécessaire */
</style>
