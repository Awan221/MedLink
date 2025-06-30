<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Gestion des utilisateurs</h1>
      <div class="flex space-x-4">
        <button 
          @click="fetchUsers" 
          class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd" />
          </svg>
          Actualiser
        </button>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm">{{ error.message || error }}</p>
        </div>
      </div>
    </div>

    <!-- Message de succès -->
    <div v-if="message" class="mb-6 p-4 rounded-md" :class="{
      'bg-green-100 border-l-4 border-green-500 text-green-700': messageType === 'success',
      'bg-red-100 border-l-4 border-red-500 text-red-700': messageType === 'error',
      'bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700': messageType === 'warning',
      'bg-blue-100 border-l-4 border-blue-500 text-blue-700': messageType === 'info'
    }">
      <div class="flex justify-between items-center">
        <p class="text-sm">{{ message }}</p>
        <button @click="message = ''" class="text-gray-500 hover:text-gray-700">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Tableau des utilisateurs -->
    <div class="bg-white shadow-md rounded-lg overflow-hidden">
      <!-- En-tête du tableau -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nom
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Prénom
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Email
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Rôle
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Statut
              </th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <!-- État de chargement -->
            <tr v-if="loading">
              <td colspan="6" class="px-6 py-4 text-center">
                <div class="flex justify-center items-center space-x-2">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                  <span class="text-gray-600">Chargement des utilisateurs...</span>
                </div>
              </td>
            </tr>
            
            <!-- Aucun utilisateur -->
            <tr v-else-if="!loading && users.length === 0">
              <td colspan="6" class="px-6 py-4 text-center text-gray-500">
                Aucun utilisateur trouvé.
              </td>
            </tr>

            <!-- Liste des utilisateurs -->
            <tr v-for="user in users" :key="user.id" class="hover:bg-gray-50">
              <!-- Nom -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ user.last_name || '-' }}</div>
              </td>
              
              <!-- Prénom -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ user.first_name || '-' }}</div>
              </td>
              
              <!-- Email -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ user.email }}</div>
              </td>
              
              <!-- Rôle -->
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="relative" v-if="isSuperAdmin">
                  <select 
                    v-model="user.role" 
                    @change="updateUserRole(user)" 
                    class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                  >
                    <option v-for="(roleLabel, roleValue) in roles" :key="roleValue" :value="roleValue">
                      {{ roleLabel }}
                    </option>
                  </select>
                </div>
                <div v-else class="text-sm text-gray-900">
                  {{ getRoleLabel(user.role) }}
                </div>
              </td>
              
              <!-- Statut -->
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="{
                    'bg-green-100 text-green-800': user.is_active,
                    'bg-red-100 text-red-800': !user.is_active
                  }"
                >
                  {{ user.is_active ? 'Actif' : 'Inactif' }}
                </span>
              </td>
              
              <!-- Actions -->
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex space-x-2">
                  <button 
                    @click="toggleUserStatus(user)" 
                    class="px-3 py-1 rounded-md text-sm"
                    :class="{
                      'bg-red-100 text-red-700 hover:bg-red-200': user.is_active,
                      'bg-green-100 text-green-700 hover:bg-green-200': !user.is_active
                    }"
                  >
                    {{ user.is_active ? 'Désactiver' : 'Activer' }}
                  </button>
                  <button 
                    @click="resetPassword(user)" 
                    class="px-3 py-1 bg-yellow-100 text-yellow-700 hover:bg-yellow-200 rounded-md text-sm"
                  >
                    Réinitialiser MDP
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div v-if="totalPages > 1" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="flex-1 flex justify-between sm:hidden">
          <button 
            @click="currentPage > 1 ? currentPage-- : null" 
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Précédent
          </button>
          <button 
            @click="currentPage < totalPages ? currentPage++ : null"
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Suivant
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Affichage de <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span> à 
              <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span> sur 
              <span class="font-medium">{{ totalItems }}</span> résultats
            </p>
          </div>
          <div>
            <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button 
                @click="currentPage > 1 ? currentPage-- : null" 
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                :class="{'opacity-50 cursor-not-allowed': currentPage === 1}"
              >
                <span class="sr-only">Précédent</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
              
              <button 
                v-for="page in pagesToShow" 
                :key="page"
                @click="currentPage = page"
                :class="{
                  'bg-blue-50 border-blue-500 text-blue-600': currentPage === page,
                  'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': currentPage !== page
                }"
                class="relative inline-flex items-center px-4 py-2 border text-sm font-medium"
              >
                {{ page }}
              </button>
              
              <button 
                @click="currentPage < totalPages ? currentPage++ : null"
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                :class="{'opacity-50 cursor-not-allowed': currentPage === totalPages}"
              >
                <span class="sr-only">Suivant</span>
                <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import axios from 'axios';

export default {
  name: 'UserAdmin',
  
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      totalItems: 0,
      message: '',
      messageType: 'info',
      // Liste des rôles avec leurs libellés en français
      // Inclut les variantes en majuscules et minuscules pour la rétrocompatibilité
      roles: {
        // Format attendu par l'API (en minuscules)
        'super_admin': 'Super Administrateur',
        'admin': 'Administrateur',
        'doctor': 'Médecin',
        'radiologist': 'Radiologue',
        'blood_bank_manager': 'Responsable Banque de Sang',
        'technician': 'Technicien',
        'nurse': 'Infirmier/Infirmière',
        'pharmacist': 'Pharmacien',
        'receptionist': 'Réceptionniste',
        'patient': 'Patient',
        // Format en majuscules pour la rétrocompatibilité
        'SUPER_ADMIN': 'Super Administrateur',
        'ADMIN': 'Administrateur',
        'DOCTOR': 'Médecin',
        'RADIOLOGIST': 'Radiologue',
        'BLOOD_BANK_MANAGER': 'Responsable Banque de Sang',
        'TECHNICIAN': 'Technicien',
        'NURSE': 'Infirmier/Infirmière',
        'PHARMACIST': 'Pharmacien',
        'RECEPTIONIST': 'Réceptionniste',
        'PATIENT': 'Patient'
      },
      statuses: {
        'ACTIF': { label: 'Actif', class: 'bg-green-100 text-green-800' },
        'INACTIF': { label: 'Inactif', class: 'bg-red-100 text-red-800' },
        'EN_ATTENTE': { label: 'En attente', class: 'bg-yellow-100 text-yellow-800' },
        'REFUSE': { label: 'Refusé', class: 'bg-gray-100 text-gray-800' }
      }
    };
  },
  
  computed: {
    ...mapGetters('users', ['allUsers', 'usersLoading', 'usersError']),
    
    users() {
      try {
        return (Array.isArray(this.allUsers) ? this.allUsers : [])
          .filter(u => u && typeof u === 'object' && 'id' in u)
          .map(user => ({
            ...user,
            // Conserver le rôle tel qu'il vient de l'API
            role: user.role || 'patient',
            is_active: !!user.is_active,
            first_name: user.first_name || '',
            last_name: user.last_name || '',
            email: user.email || ''
          }));
      } catch (e) {
        console.error('Erreur lors du traitement des utilisateurs:', e);
        return [];
      }
    },
    
    loading() { 
      return this.usersLoading; 
    },
    
    error() { 
      return this.usersError; 
    },
    
    isSuperAdmin() {
      try {
        const user = JSON.parse(localStorage.getItem('user'));
        // Vérifier si l'utilisateur a le rôle super_admin (insensible à la casse)
        return user && user.role && user.role.toLowerCase() === 'super_admin';
      } catch (e) {
        console.error('Erreur lors de la récupération du rôle utilisateur:', e);
        return false;
      }
    },
    
    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage);
    },
    
    pagesToShow() {
      const pages = [];
      const maxPagesToShow = 5;
      let startPage = Math.max(1, this.currentPage - Math.floor(maxPagesToShow / 2));
      let endPage = startPage + maxPagesToShow - 1;
      
      if (endPage > this.totalPages) {
        endPage = this.totalPages;
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }
      
      return pages;
    },
    
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.users.slice(start, end);
    }
  },
  
  methods: {
    ...mapActions('users', ['fetchUsers', 'updateUser', 'updateUserRole']),
    
    // Méthode pour normaliser et afficher un rôle
    getRoleLabel(role) {
      if (!role) return 'Non défini';
      // Essayer de trouver le rôle tel quel
      if (this.roles[role]) {
        return this.roles[role];
      }
      // Essayer en minuscules
      const lowerRole = role.toLowerCase();
      if (this.roles[lowerRole]) {
        return this.roles[lowerRole];
      }
      // Essayer en majuscules
      const upperRole = role.toUpperCase();
      if (this.roles[upperRole]) {
        return this.roles[upperRole];
      }
      // Si aucun ne correspond, retourner le rôle original
      return role;
    },
    
    
    async fetchUsersList() {
      try {
        this.loading = true;
        await this.fetchUsers();
        this.totalItems = this.users.length;
        
        // Afficher les rôles dans la console pour le débogage
        console.log('Utilisateurs chargés:', this.users.map(u => ({
          id: u.id,
          email: u.email,
          role: u.role,
          roleLabel: this.roles[u.role] || 'Non défini'
        })));
        
      } catch (error) {
        console.error('Erreur lors du chargement des utilisateurs:', error);
        this.showMessage('Erreur lors du chargement des utilisateurs', 'error');
      } finally {
        this.loading = false;
      }
    },
    
    async updateUserRole(user) {
      if (!this.isSuperAdmin) {
        this.showMessage('Action non autorisée. Droits administrateur requis.', 'error');
        return;
      }
      
      if (!user || !user.id) {
        console.error('Utilisateur invalide:', user);
        this.showMessage('Erreur: Utilisateur invalide', 'error');
        return;
      }
      
      // Sauvegarder l'ancien rôle pour pouvoir le restaurer en cas d'erreur
      const oldRole = user.role;
      const newRole = (user.role || 'PATIENT').toUpperCase();
      
      // Vérifier que le nouveau rôle est valide
      if (!this.roles[newRole]) {
        console.error('Rôle invalide:', newRole);
        this.showMessage(`Erreur: Le rôle "${newRole}" n'est pas valide`, 'error');
        return;
      }
      
      const loadingMessage = this.showMessage(
        `Mise à jour du rôle en cours...`,
        'info',
        false
      );
      
      try {
        // Mise à jour optimiste de l'interface
        const updatedUsers = this.users.map(u => 
          u.id === user.id ? { ...u, role: newRole } : u
        );
        
        // Mettre à jour le store immédiatement pour un retour visuel rapide
        if (this.$store && this.$store.commit) {
          this.$store.commit('users/SET_USERS', updatedUsers);
        }
        
        // Envoyer la requête de mise à jour
        await this.$store.dispatch('users/updateUserRole', { 
          id: user.id, 
          data: { role: newRole } 
        });
        
        this.showMessage('Rôle mis à jour avec succès', 'success');
      } catch (error) {
        console.error('Erreur lors de la mise à jour du rôle:', error);
        
        // Revenir à l'ancien rôle en cas d'erreur
        if (this.$store && this.$store.commit) {
          const revertedUsers = this.users.map(u => 
            u.id === user.id ? { ...u, role: oldRole } : u
          );
          this.$store.commit('users/SET_USERS', revertedUsers);
        }
        
        const errorMessage = error.response?.data?.message || 'Erreur lors de la mise à jour du rôle';
        this.showMessage(errorMessage, 'error');
      } finally {
        if (loadingMessage) {
          clearTimeout(loadingMessage);
        }
      }
    },
    
    async toggleUserStatus(user) {
      if (!user || !user.id) {
        console.error('Utilisateur invalide pour le changement de statut:', user);
        this.showMessage('Erreur: Utilisateur invalide', 'error');
        return;
      }
      
      // Sauvegarder l'ancien état pour pouvoir le restaurer en cas d'erreur
      const oldStatus = !!user.is_active;
      const newStatus = !oldStatus;
      
      console.log(`Changement de statut pour l'utilisateur ${user.id} de ${oldStatus} à ${newStatus}`);
      
      const loadingMessage = this.showMessage(
        `Mise à jour du statut en cours...`,
        'info',
        false // Ne pas cacher automatiquement
      );
      
      try {
        // Mise à jour optimiste de l'interface
        const updatedUsers = this.users.map(u => 
          u.id === user.id ? { ...u, is_active: newStatus } : u
        );
        
        // Mettre à jour le store immédiatement pour un retour visuel rapide
        if (this.$store && this.$store.commit) {
          this.$store.commit('users/SET_USERS', updatedUsers);
        }
        
        // Envoyer la requête de mise à jour
        const response = await this.$store.dispatch('users/updateUser', { 
          id: user.id, 
          data: { is_active: newStatus }
        });
        
        console.log('Réponse de la mise à jour:', response);
        
        this.showMessage(
          `Utilisateur ${newStatus ? 'activé' : 'désactivé'} avec succès`,
          'success'
        );
        
        // Recharger la liste des utilisateurs pour s'assurer que les données sont à jour
        await this.fetchUsersList();
        
      } catch (error) {
        console.error('Erreur lors du changement de statut:', error);
        
        // Revenir à l'état précédent en cas d'erreur
        if (this.$store && this.$store.commit) {
          const revertedUsers = this.users.map(u => 
            u.id === user.id ? { ...u, is_active: oldStatus } : u
          );
          this.$store.commit('users/SET_USERS', revertedUsers);
        }
        
        const errorMessage = error.response?.data?.message || 'Erreur lors du changement de statut';
        this.showMessage(errorMessage, 'error');
      } finally {
        if (loadingMessage) {
          clearTimeout(loadingMessage);
        }
      }
    },
    
    async resetPassword(user) {
      if (!confirm(`Êtes-vous sûr de vouloir réinitialiser le mot de passe de ${user.email} ?`)) {
        return;
      }
      
      try {
        // Remplacez cette URL par votre endpoint de réinitialisation de mot de passe
        await axios.post(`/api/auth/users/${user.id}/reset-password/`);
        this.showMessage('Email de réinitialisation envoyé avec succès', 'success');
      } catch (error) {
        console.error('Erreur lors de la réinitialisation du mot de passe:', error);
        this.showMessage('Erreur lors de la réinitialisation du mot de passe', 'error');
      }
    },
    
    showMessage(message, type = 'info', autoHide = true) {
      this.message = message;
      this.messageType = type;
      
      // Masquer le message après 5 secondes si autoHide est vrai
      if (autoHide) {
        return setTimeout(() => {
          this.message = '';
        }, 5000);
      }
      return null;
    },
    
    clearMessage() {
      this.message = '';
      this.messageType = 'info';
    }
  },
  
  created() {
    this.fetchUsersList();
  },
  
  watch: {
    currentPage() {
      // Faites défiler vers le haut lors du changement de page
      window.scrollTo(0, 0);
    }
  }
};
</script>

<style scoped>
/* Styles personnalisés si nécessaire */
</style>
