<template>
  <div class="user-management">
    <h2>Gestion des utilisateurs</h2>
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement...</span>
      </div>
      <p class="mt-2">Chargement des utilisateurs en cours...</p>
    </div>
    <div v-else>
      <table class="table table-bordered table-hover">
        <thead>
          <tr>
            <th>Email</th>
            <th>Nom</th>
            <th>Prénom</th>
            <th>Rôle</th>
<th>Spécialité</th>
            <th>Statut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.email }}</td>
            <td>{{ user.last_name }}</td>
            <td>{{ user.first_name }}</td>
            <td>
  <select v-model="user.role" @change="updateRole(user)" class="form-select form-select-sm">
    <option value="ADMIN">Administrateur</option>
    <option value="SUPER_ADMIN">Super Administrateur</option>
    <option value="DOCTOR">Médecin</option>
    <option value="RADIOLOGIST">Radiologue</option>
    <option value="TECHNICIAN">Technicien en Imagerie</option>
    <option value="BLOOD_BANK_MANAGER">Responsable Banque de Sang</option>
    <option value="NURSE">Infirmier(ère)</option>
    <option value="PATIENT">Patient</option>
    <option value="AUTRE">Autre Personnel Médical</option>
  </select>
</td>
<td>
  <select v-model="user.specialite" @change="updateRole(user)" class="form-select form-select-sm" v-if="user.role === 'SPECIALISTE' || user.role === 'MEDECIN'">
    <option value="">Aucune</option>
    <option value="CARDIOLOGUE">Cardiologue</option>
    <option value="DIABETOLOGUE">Diabétologue</option>
    <option value="PEDIATRE">Pédiatre</option>
    <option value="GYNECO">Gynécologue</option>
    <option value="AUTRE">Autre Spécialité</option>
  </select>
  <span v-else>-</span>
</td>
            <td>
              <span :class="user.is_active ? 'text-success' : 'text-danger'">
                {{ user.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm" :class="user.is_active ? 'btn-danger' : 'btn-success'" @click="toggleActive(user)">
                {{ user.is_active ? 'Désactiver' : 'Activer' }}
              </button>
              <button class="btn btn-warning btn-sm ms-2" @click="resetPassword(user)">Réinitialiser mot de passe</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="users.length === 0" class="text-center">Aucun utilisateur trouvé.</div>
    </div>
    <div v-if="message" class="alert mt-3" :class="{
      'alert-success': messageType === 'success',
      'alert-danger': messageType === 'error',
      'alert-warning': messageType === 'warning',
      'alert-info': messageType === 'info'
    }">
      {{ message }}
      <button v-if="messageType === 'error'" type="button" class="btn-close float-end" @click="message = ''" aria-label="Fermer"></button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { computed } from 'vue';
import { useStore } from 'vuex';

export default {
  name: "UserManagement",
  setup() {
    const store = useStore();
    const userRole = computed(() => store.getters['auth/userRole']);
    return { userRole };
  },
  data() {
    return {
      users: [],
      loading: false, // Commencer à false pour éviter les chargements inutiles
      message: '',
      messageType: 'info', // Type par défaut
    };
  },
  methods: {
    async updateRole(user) {
      try {
        // eslint-disable-next-line no-unused-vars
        const data = { role: user.role, specialite: user.specialite };
        // eslint-disable-next-line no-unused-vars
        const response = await axios.patch(`${process.env.VUE_APP_API_URL}auth/users/${user.id}/roles/`, data, { headers: this.authHeader() });
        this.message = 'Rôle et spécialité mis à jour.';
        this.messageType = 'success';
      } catch (error) {
        this.message = "Erreur lors de la mise à jour du rôle ou de la spécialité.";
        this.messageType = 'error';
      }
    },
    async fetchUsers() {
      this.loading = true;
      this.message = '';
      try {
        const url = `${process.env.VUE_APP_API_URL}auth/users/`;
        console.log('Tentative de chargement des utilisateurs depuis:', url);
        
        const response = await axios.get(url, { 
          headers: this.authHeader() 
        });
        
        console.log('Réponse reçue:', response);
        
        if (response && response.data) {
          // Vérifier si la réponse contient une propriété 'results' (format paginé)
          const usersData = response.data.results || response.data;
          this.users = Array.isArray(usersData) ? usersData : [];
          
          console.log(`${this.users.length} utilisateurs chargés`, this.users);
          
          if (this.users.length === 0) {
            this.message = 'Aucun utilisateur trouvé.';
            this.messageType = 'info';
          } else {
            // Mapper les rôles pour correspondre aux options du select
            this.users = this.users.map(user => ({
              ...user,
              // S'assurer que le rôle est en majuscules pour correspondre aux options
              role: user.role ? user.role.toUpperCase() : '',
              // Ajouter la spécialité si elle n'existe pas
              specialite: user.specialite || ''
            }));
          }
        } else {
          throw new Error('Réponse invalide du serveur');
        }
      } catch (error) {
        console.error('Erreur lors du chargement des utilisateurs:', error);
        this.message = `Erreur lors du chargement des utilisateurs: ${error.message || 'Erreur inconnue'}`;
        this.messageType = 'error';
        this.users = [];
      } finally {
        this.loading = false;
      }
    },
    toggleActive(user) {
      const action = user.is_active ? 'désactiver' : 'activer';
      if (!confirm(`Voulez-vous vraiment ${action} cet utilisateur ?`)) return;
      axios.patch(`${process.env.VUE_APP_API_URL}auth/users/${user.id}/`, { is_active: !user.is_active }, { headers: this.authHeader() })
        .then(() => {
          user.is_active = !user.is_active;
          this.message = `Utilisateur ${action} avec succès.`;
          this.messageType = 'success';
        })
        .catch(() => {
          this.message = `Erreur lors de la modification du statut.`;
          this.messageType = 'error';
        });
    },
    async resetPassword(user) {
      const email = user.email;
      if (!confirm(`Envoyer un email de réinitialisation à ${email} ?`)) return;
      
      this.loading = true;
      this.message = '';
      this.messageType = '';
      
      try {
        // Utiliser le nouvel endpoint de réinitialisation de mot de passe
        const url = '/auth/password-reset/';
        console.log('Envoi de la demande de réinitialisation à:', url);
        
        // Préparer les données de la requête
        const data = { email };
        console.log('Données de la requête:', JSON.stringify(data, null, 2));
        
        // Préparer les en-têtes
        const headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          ...this.authHeader()
        };
        
        console.log('En-têtes de la requête:', JSON.stringify({
          ...headers,
          'Authorization': headers.Authorization ? 'Bearer [TOKEN]' : 'Non fourni'
        }, null, 2));
        
        // Effectuer la requête via le proxy
        console.log('Envoi de la requête...');
        const response = await axios({
          method: 'post',
          url: url,
          data: data,
          headers: headers,
          withCredentials: true,
          validateStatus: (status) => status < 500 // Valider les réponses < 500 comme réussies
        });
        
        console.log('Réponse reçue:', {
          status: response.status,
          statusText: response.statusText,
          headers: response.headers,
          data: response.data
        });
        
        if (response.status === 200) {
          this.message = `Email de réinitialisation envoyé à ${email} s'il existe dans notre système.`;
          this.messageType = 'success';
        } else if (response.status === 400) {
          this.message = 'Requête invalide. Veuillez vérifier les informations fournies.';
          this.messageType = 'error';
        } else if (response.status === 404) {
          this.message = 'Utilisateur non trouvé.';
          this.messageType = 'error';
        } else {
          throw new Error(`Réponse inattendue du serveur: ${response.status} - ${response.statusText}`);
        }
      } catch (error) {
        console.error('Erreur lors de la réinitialisation du mot de passe:', error);
        
        let errorMessage = 'Erreur inconnue';
        
        if (error.response) {
          // La requête a été faite et le serveur a répondu avec un statut hors 2xx
          console.error('Détails de l\'erreur:', {
            status: error.response.status,
            headers: error.response.headers,
            data: error.response.data
          });
          
          errorMessage = error.response.data?.message || 
                        error.response.data?.detail || 
                        JSON.stringify(error.response.data) || 
                        `Erreur ${error.response.status}: ${error.response.statusText}`;
        } else if (error.request) {
          // La requête a été faite mais aucune réponse n'a été reçue
          console.error('Aucune réponse reçue:', error.request);
          errorMessage = 'Aucune réponse du serveur. Vérifiez votre connexion.';
        } else {
          // Une erreur s'est produite lors de la configuration de la requête
          console.error('Erreur de configuration de la requête:', error.message);
          errorMessage = `Erreur de configuration: ${error.message}`;
        }
        
        this.message = `Erreur lors de l'envoi de l'email: ${errorMessage}`;
        this.messageType = 'error';
      } finally {
        this.loading = false;
        // Cacher le message d'erreur après 10 secondes
        if (this.message) {
          setTimeout(() => {
            this.message = '';
            this.messageType = '';
          }, 10000);
        }
      }
    },
    authHeader() {
      const token = localStorage.getItem('token') || localStorage.getItem('access');
      return token ? { 'Authorization': `Bearer ${token}` } : {};
    }
  },
  mounted() {
    console.log('Composant UserManagement monté');
    console.log('Rôle utilisateur actuel:', this.userRole);
    
    // Vérification des rôles
    if (!this.userRole || !["ADMIN", "SUPER_ADMIN"].includes(this.userRole)) {
      console.warn('Accès refusé: rôle insuffisant');
      this.message = 'Accès non autorisé. Redirection...';
      this.messageType = 'warning';
      
      // Redirection après un court délai pour permettre à l'utilisateur de voir le message
      setTimeout(() => {
        this.$router.push('/dashboard');
      }, 2000);
      return;
    }
    
    // Chargement des utilisateurs
    console.log('Chargement des utilisateurs...');
    this.fetchUsers();
  }
};
</script>

<style scoped>
.user-management {
  max-width: 1100px;
  margin: 40px auto;
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
}
.table {
  background: #f8f9fa;
}
.btn {
  min-width: 90px;
}
.text-success { color: #198754; }
.text-danger { color: #dc3545; }
</style>