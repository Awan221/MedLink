<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- En-tête de la page -->
    <div class="md:flex md:items-center md:justify-between mb-8">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">Paramètres</h2>
        <p class="mt-1 text-sm text-gray-500">Gérez les paramètres de votre compte et vos préférences.</p>
      </div>
    </div>

    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <!-- Navigation par onglets -->
      <div class="border-b border-gray-200">
        <nav class="flex -mb-px">
          <button 
            v-for="tab in tabs" 
            :key="tab.name"
            @click="currentTab = tab.id"
            :class="[
              currentTab === tab.id 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Contenu des onglets -->
      <div class="p-6">
        <!-- Onglet Compte -->
        <div v-if="currentTab === 'account'">
          <h3 class="text-lg font-medium text-gray-900 mb-6">Paramètres du compte</h3>
          
          <form @submit.prevent="updateAccount" class="space-y-6">
            <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
              <div class="sm:col-span-4">
                <label for="username" class="block text-sm font-medium text-gray-700">Nom d'utilisateur</label>
                <div class="mt-1 flex rounded-md shadow-sm">
                  <span class="inline-flex items-center px-3 rounded-l-md border border-r-0 border-gray-300 bg-gray-50 text-gray-500 sm:text-sm">
                    medlink.com/
                  </span>
                  <input type="text" id="username" v-model="accountForm.username" class="flex-1 min-w-0 block w-full px-3 py-2 rounded-none rounded-r-md border border-gray-300 focus:ring-blue-500 focus:border-blue-500 sm:text-sm">
                </div>
              </div>

              <div class="sm:col-span-4">
                <label for="language" class="block text-sm font-medium text-gray-700">Langue</label>
                <select id="language" v-model="accountForm.language" class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md">
                  <option value="fr">Français</option>
                  <option value="en">English</option>
                  <option value="es">Español</option>
                </select>
              </div>

              <div class="sm:col-span-6">
                <label class="flex items-center">
                  <input type="checkbox" v-model="accountForm.newsletter" class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded">
                  <span class="ml-2 block text-sm text-gray-700">Recevoir la newsletter</span>
                </label>
              </div>
            </div>

            <div class="pt-5">
              <div class="flex justify-end">
                <button type="submit" class="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  Enregistrer les modifications
                </button>
              </div>
            </div>
          </form>
        </div>

        <!-- Onglet Sécurité -->
        <div v-else-if="currentTab === 'security'">
          <h3 class="text-lg font-medium text-gray-900 mb-6">Sécurité</h3>
          
          <div class="space-y-6">
            <!-- Mot de passe actuel -->
            <div class="bg-blue-50 p-4 rounded-lg">
              <h4 class="text-sm font-medium text-blue-800">Changer de mot de passe</h4>
              <form @submit.prevent="updatePassword" class="mt-2 space-y-4">
                <div>
                  <label for="current_password" class="block text-sm font-medium text-gray-700">Mot de passe actuel</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      :type="showCurrentPassword ? 'text' : 'password'" 
                      id="current_password" 
                      v-model="passwordForm.current_password" 
                      class="block w-full pr-10 border-gray-300 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                      placeholder="••••••••"
                    >
                    <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <button type="button" @click="showCurrentPassword = !showCurrentPassword" class="text-gray-400 hover:text-gray-500 focus:outline-none">
                        <span class="sr-only">{{ showCurrentPassword ? 'Cacher' : 'Afficher' }} le mot de passe</span>
                        <svg v-if="!showCurrentPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <div>
                  <label for="new_password" class="block text-sm font-medium text-gray-700">Nouveau mot de passe</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      :type="showNewPassword ? 'text' : 'password'" 
                      id="new_password" 
                      v-model="passwordForm.new_password" 
                      class="block w-full pr-10 border-gray-300 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                      placeholder="••••••••"
                    >
                    <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <button type="button" @click="showNewPassword = !showNewPassword" class="text-gray-400 hover:text-gray-500 focus:outline-none">
                        <span class="sr-only">{{ showNewPassword ? 'Cacher' : 'Afficher' }} le mot de passe</span>
                        <svg v-if="!showNewPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <div>
                  <label for="confirm_password" class="block text-sm font-medium text-gray-700">Confirmer le nouveau mot de passe</label>
                  <div class="mt-1 relative rounded-md shadow-sm">
                    <input 
                      :type="showConfirmPassword ? 'text' : 'password'" 
                      id="confirm_password" 
                      v-model="passwordForm.confirm_password" 
                      class="block w-full pr-10 border-gray-300 focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                      placeholder="••••••••"
                    >
                    <div class="absolute inset-y-0 right-0 pr-3 flex items-center">
                      <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="text-gray-400 hover:text-gray-500 focus:outline-none">
                        <span class="sr-only">{{ showConfirmPassword ? 'Cacher' : 'Afficher' }} le mot de passe</span>
                        <svg v-if="!showConfirmPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                        </svg>
                        <svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>

                <div class="pt-2">
                  <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Mettre à jour le mot de passe
                  </button>
                </div>
              </form>
            </div>

            <!-- Authentification à deux facteurs -->
            <div class="border-t border-gray-200 pt-6">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="text-sm font-medium text-gray-900">Authentification à deux facteurs</h4>
                  <p class="text-sm text-gray-500">Ajoutez une couche de sécurité supplémentaire à votre compte.</p>
                </div>
                <button type="button" class="ml-4 relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent bg-gray-200 transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2" role="switch" aria-checked="false">
                  <span class="sr-only">Activer l'authentification à deux facteurs</span>
                  <span aria-hidden="true" class="translate-x-0 inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"></span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Onglet Notifications -->
        <div v-else-if="currentTab === 'notifications'">
          <h3 class="text-lg font-medium text-gray-900 mb-6">Préférences de notification</h3>
          
          <form @submit.prevent="updateNotificationSettings" class="space-y-6">
            <div class="space-y-4">
              <div class="flex items-start">
                <div class="flex items-center h-5">
                  <input id="email_notifications" v-model="notificationForm.email_notifications" type="checkbox" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded">
                </div>
                <div class="ml-3 text-sm">
                  <label for="email_notifications" class="font-medium text-gray-700">Notifications par email</label>
                  <p class="text-gray-500">Recevoir des mises à jour par email.</p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="flex items-center h-5">
                  <input id="push_notifications" v-model="notificationForm.push_notifications" type="checkbox" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded">
                </div>
                <div class="ml-3 text-sm">
                  <label for="push_notifications" class="font-medium text-gray-700">Notifications push</label>
                  <p class="text-gray-500">Recevoir des notifications sur cet appareil.</p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="flex items-center h-5">
                  <input id="appointment_reminders" v-model="notificationForm.appointment_reminders" type="checkbox" class="focus:ring-blue-500 h-4 w-4 text-blue-600 border-gray-300 rounded">
                </div>
                <div class="ml-3 text-sm">
                  <label for="appointment_reminders" class="font-medium text-gray-700">Rappels de rendez-vous</label>
                  <p class="text-gray-500">Recevoir des rappels avant les rendez-vous.</p>
                </div>
              </div>
            </div>

            <div class="pt-4">
              <button type="submit" class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                Enregistrer les préférences
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'SettingsView',
  
  data() {
    return {
      currentTab: 'account',
      tabs: [
        { id: 'account', name: 'Compte' },
        { id: 'security', name: 'Sécurité' },
        { id: 'notifications', name: 'Notifications' }
      ],
      
      // Données du formulaire de compte
      accountForm: {
        username: '',
        language: 'fr',
        newsletter: true
      },
      
      // Données du formulaire de mot de passe
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      showCurrentPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      
      // Données du formulaire de notifications
      notificationForm: {
        email_notifications: true,
        push_notifications: true,
        appointment_reminders: true
      }
    };
  },
  
  computed: {
    ...mapGetters('auth', ['user'])
  },
  
  created() {
    this.initializeForms();
  },
  
  methods: {
    initializeForms() {
      if (this.user) {
        this.accountForm = {
          username: this.user.username || '',
          language: this.user.language || 'fr',
          newsletter: this.user.newsletter !== false
        };
        
        this.notificationForm = {
          email_notifications: this.user.email_notifications !== false,
          push_notifications: this.user.push_notifications !== false,
          appointment_reminders: this.user.appointment_reminders !== false
        };
      }
    },
    
    async updateAccount() {
      try {
        // Ici, vous pourriez appeler une action Vuex pour mettre à jour le compte
        // await this.$store.dispatch('auth/updateAccount', this.accountForm);
        this.$toast.success('Paramètres du compte mis à jour avec succès');
      } catch (error) {
        console.error('Erreur lors de la mise à jour du compte:', error);
        this.$toast.error('Une erreur est survenue lors de la mise à jour du compte');
      }
    },
    
    async updatePassword() {
      if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        this.$toast.error('Les mots de passe ne correspondent pas');
        return;
      }
      
      try {
        // Ici, vous pourriez appeler une action Vuex pour mettre à jour le mot de passe
        // await this.$store.dispatch('auth/updatePassword', {
        //   current_password: this.passwordForm.current_password,
        //   new_password: this.passwordForm.new_password
        // });
        
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        };
        
        this.$toast.success('Mot de passe mis à jour avec succès');
      } catch (error) {
        console.error('Erreur lors de la mise à jour du mot de passe:', error);
        this.$toast.error('Une erreur est survenue lors de la mise à jour du mot de passe');
      }
    },
    
    async updateNotificationSettings() {
      try {
        // Ici, vous pourriez appeler une action Vuex pour mettre à jour les préférences de notification
        // await this.$store.dispatch('auth/updateNotificationSettings', this.notificationForm);
        this.$toast.success('Préférences de notification mises à jour avec succès');
      } catch (error) {
        console.error('Erreur lors de la mise à jour des préférences de notification:', error);
        this.$toast.error('Une erreur est survenue lors de la mise à jour des préférences de notification');
      }
    }
  }
};
</script>

<style scoped>
/* Styles spécifiques à la page des paramètres si nécessaire */
</style>
