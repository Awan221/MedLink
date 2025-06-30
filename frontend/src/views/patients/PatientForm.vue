<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <!-- En-tête du formulaire -->
      <div class="px-6 py-5 border-b border-gray-200 bg-gray-50">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-2xl font-semibold text-gray-900">
              {{ isEdit ? 'Modifier le patient' : 'Nouveau patient' }}
            </h2>
            <p class="mt-1 text-sm text-gray-500">
              {{ isEdit ? 'Mettez à jour les informations du patient' : 'Remplissez les informations pour créer un nouveau patient' }}
            </p>
          </div>
          <router-link 
            to="/patients" 
            class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 -ml-1" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
            </svg>
            Retour à la liste
          </router-link>
        </div>
      </div>

      <!-- Messages d'alerte -->
      <transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-400 p-4 mx-6 mt-6 rounded">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-green-700">{{ successMessage }}</p>
            </div>
          </div>
        </div>
      </transition>

      <transition enter-active-class="transition ease-out duration-300" enter-from-class="opacity-0" enter-to-class="opacity-100" leave-active-class="transition ease-in duration-200" leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-400 p-4 mx-6 mt-6 rounded">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm text-red-700">{{ errorMessage }}</p>
            </div>
          </div>
        </div>
      </transition>

      <form @submit.prevent="handleSubmit" class="px-6 py-6">
        <div class="space-y-6">
          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
            <!-- Prénom -->
            <div class="sm:col-span-3">
              <label for="first_name" class="block text-sm font-medium text-gray-700">Prénom <span class="text-red-500">*</span></label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="first_name" 
                  v-model="form.first_name" 
                  required
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Jean"
                >
              </div>
            </div>

            <!-- Nom -->
            <div class="sm:col-span-3">
              <label for="last_name" class="block text-sm font-medium text-gray-700">Nom <span class="text-red-500">*</span></label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="last_name" 
                  v-model="form.last_name" 
                  required
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Dupont"
                >
              </div>
            </div>

            <!-- ID médical (seulement en mode édition) -->
            <div v-if="isEdit" class="sm:col-span-3">
              <label for="medical_id" class="block text-sm font-medium text-gray-700">ID médical</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="medical_id" 
                  v-model="form.medical_id" 
                  readonly 
                  class="bg-gray-100 shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                >
              </div>
            </div>

            <!-- NIN -->
            <div class="sm:col-span-3">
              <label for="national_id" class="block text-sm font-medium text-gray-700">Numéro d'identification nationale (NIN)</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="national_id" 
                  v-model="form.national_id" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="1234567890123"
                >
              </div>
            </div>

            <!-- Date de naissance -->
            <div class="sm:col-span-3">
              <label for="date_of_birth" class="block text-sm font-medium text-gray-700">Date de naissance <span class="text-red-500">*</span></label>
              <div class="mt-1">
                <input 
                  type="date" 
                  id="date_of_birth" 
                  v-model="form.date_of_birth" 
                  required
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                >
              </div>
            </div>

            <!-- Sexe -->
            <div class="sm:col-span-3">
              <label for="gender" class="block text-sm font-medium text-gray-700">Sexe <span class="text-red-500">*</span></label>
              <div class="mt-1">
                <select 
                  id="gender" 
                  v-model="form.gender" 
                  required
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                >
                  <option value="">Sélectionnez un sexe</option>
                  <option value="M">Masculin</option>
                  <option value="F">Féminin</option>
                </select>
              </div>
            </div>

            <!-- Groupe sanguin -->
            <div class="sm:col-span-3">
              <label for="blood_group" class="block text-sm font-medium text-gray-700">Groupe sanguin</label>
              <div class="mt-1">
                <select 
                  id="blood_group" 
                  v-model="form.blood_group" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                >
                  <option value="">Sélectionnez un groupe sanguin</option>
                  <option v-for="g in bloodGroups" :key="g" :value="g">{{ g }}</option>
                </select>
              </div>
            </div>

            <!-- Email -->
            <div class="sm:col-span-3">
              <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
              <div class="mt-1">
                <input 
                  type="email" 
                  id="email" 
                  v-model="form.email" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="jean.dupont@example.com"
                >
              </div>
            </div>

            <!-- Téléphone -->
            <div class="sm:col-span-3">
              <label for="phone" class="block text-sm font-medium text-gray-700">Téléphone</label>
              <div class="mt-1">
                <input 
                  type="tel" 
                  id="phone" 
                  v-model="form.phone" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="+33 6 12 34 56 78"
                >
              </div>
            </div>

            <!-- Adresse -->
            <div class="sm:col-span-6">
              <label for="address" class="block text-sm font-medium text-gray-700">Adresse</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="address" 
                  v-model="form.address" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="123 Rue de l'Exemple"
                >
              </div>
            </div>

            <!-- Ville -->
            <div class="sm:col-span-2">
              <label for="city" class="block text-sm font-medium text-gray-700">Ville</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="city" 
                  v-model="form.city" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Paris"
                >
              </div>
            </div>

            <!-- Code postal -->
            <div class="sm:col-span-2">
              <label for="postal_code" class="block text-sm font-medium text-gray-700">Code postal</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="postal_code" 
                  v-model="form.postal_code" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="75000"
                >
              </div>
            </div>

            <!-- Pays -->
            <div class="sm:col-span-2">
              <label for="country" class="block text-sm font-medium text-gray-700">Pays</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="country" 
                  v-model="form.country" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="France"
                >
              </div>
            </div>

            <!-- Médecin traitant -->
            <div class="sm:col-span-6">
              <label for="primary_doctor" class="block text-sm font-medium text-gray-700">Médecin traitant</label>
              <div class="mt-1">
                <input 
                  type="text" 
                  id="primary_doctor" 
                  v-model="form.primary_doctor" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Dr. Martin Dupont"
                >
              </div>
            </div>

            <!-- Notes médicales -->
            <div class="sm:col-span-6">
              <label for="medical_notes" class="block text-sm font-medium text-gray-700">Notes médicales</label>
              <div class="mt-1">
                <textarea 
                  id="medical_notes" 
                  v-model="form.medical_notes" 
                  rows="3" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Antécédents médicaux, conditions particulières..."
                ></textarea>
              </div>
            </div>

            <!-- Allergies -->
            <div class="sm:col-span-3">
              <label for="allergies" class="block text-sm font-medium text-gray-700">Allergies connues</label>
              <div class="mt-1">
                <textarea 
                  id="allergies" 
                  v-model="form.allergies" 
                  rows="2" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Pollen, pénicilline, arachides..."
                ></textarea>
              </div>
            </div>

            <!-- Médicaments actuels -->
            <div class="sm:col-span-3">
              <label for="current_medications" class="block text-sm font-medium text-gray-700">Médicaments actuels</label>
              <div class="mt-1">
                <textarea 
                  id="current_medications" 
                  v-model="form.current_medications" 
                  rows="2" 
                  class="shadow-sm focus:ring-blue-500 focus:border-blue-500 block w-full sm:text-sm border-gray-300 rounded-md"
                  placeholder="Paracétamol, vitamine D..."
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Boutons d'action -->
          <div class="pt-6 border-t border-gray-200 mt-8 flex justify-end space-x-3">
            <button 
              type="button" 
              @click="$router.push('/patients')" 
              class="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Annuler
            </button>
            <button 
              type="submit" 
              class="inline-flex justify-center py-2 px-6 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              :disabled="loading"
              :class="{'opacity-50 cursor-not-allowed': loading}"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isEdit ? 'Mettre à jour' : 'Créer le patient' }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'PatientForm',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    
    const isEdit = ref(false);
    const patientId = ref(null);
    const loading = ref(false);
    const error = ref('');
    const successMessage = ref('');
    const errorMessage = ref('');
    
    const form = ref({
      first_name: '',
      last_name: '',
      medical_id: '',
      national_id: '',
      date_of_birth: '',
      gender: '',
      blood_group: '',
      email: '',
      phone: '',
      address: '',
      city: '',
      postal_code: '',
      country: 'France',
      primary_doctor: '',
      medical_notes: '',
      allergies: '',
      current_medications: ''
    });
    
    const bloodGroups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];
    
    onMounted(async () => {
      if (route.params.id) {
        isEdit.value = true;
        patientId.value = route.params.id;
        await fetchPatient();
      }
    });
    
    const fetchPatient = async () => {
      loading.value = true;
      try {
        await store.dispatch('patients/fetchPatient', patientId.value);
        const patient = store.getters['patients/currentPatient'];
        
        // Mapper les champs du patient au formulaire
        form.value = {
          first_name: patient.first_name || '',
          last_name: patient.last_name || '',
          medical_id: patient.medical_id || '',
          national_id: patient.national_id || '',
          date_of_birth: patient.date_of_birth ? formatDateForInput(patient.date_of_birth) : '',
          gender: patient.gender || '',
          blood_group: patient.blood_group || '',
          email: patient.email || '',
          phone: patient.phone || '',
          address: patient.address || '',
          city: patient.city || '',
          postal_code: patient.postal_code || '',
          country: patient.country || 'France',
          primary_doctor: patient.primary_doctor || '',
          medical_notes: patient.medical_notes || '',
          allergies: patient.allergies || '',
          current_medications: patient.current_medications || ''
        };
      } catch (err) {
        errorMessage.value = 'Échec du chargement des données du patient';
        console.error('Erreur lors du chargement du patient:', err);
      } finally {
        loading.value = false;
      }
    };

    // Formate la date pour l'input de type date (YYYY-MM-DD)
    const formatDateForInput = (dateString) => {
      if (!dateString) return '';
      const date = new Date(dateString);
      return date.toISOString().split('T')[0];
    };
    
    const handleSubmit = async () => {
      loading.value = true;
      errorMessage.value = '';
      successMessage.value = '';
      
      try {
        const patientData = {
          ...form.value,
          // S'assurer que les chums vides sont null pour l'API
          email: form.value.email || null,
          phone: form.value.phone || null,
          address: form.value.address || null,
          city: form.value.city || null,
          postal_code: form.value.postal_code || null,
          country: form.value.country || null,
          primary_doctor: form.value.primary_doctor || null,
          medical_notes: form.value.medical_notes || null,
          allergies: form.value.allergies || null,
          current_medications: form.value.current_medications || null
        };

        if (isEdit.value) {
          await store.dispatch('patients/updatePatient', {
            id: patientId.value,
            ...patientData
          });
          successMessage.value = 'Les informations du patient ont été mises à jour avec succès';
        } else {
          await store.dispatch('patients/createPatient', patientData);
          successMessage.value = 'Le patient a été créé avec succès';
          // Recharger la liste des patients
          await store.dispatch('patients/fetchPatients');
          // Rediriger vers la liste après un court délai
          setTimeout(() => {
            router.push('/patients');
          }, 1500);
        }
        
        // Effacer le message de succès après 5 secondes
        setTimeout(() => {
          successMessage.value = '';
        }, 5000);
      } catch (err) {
        console.error('Erreur lors de la soumission du formulaire:', err);
        errorMessage.value = err.response?.data?.message || 'Une erreur est survenue lors de la soumission du formulaire';
        
        // Faire défiler vers le haut pour afficher le message d'erreur
        window.scrollTo({ top: 0, behavior: 'smooth' });
      } finally {
        loading.value = false;
      }
    };
    
    return {
      isEdit,
      form,
      loading,
      error,
      successMessage,
      errorMessage,
      handleSubmit,
      bloodGroups
    };
  }
};
</script>

<style scoped>
/* Animation pour le bouton de chargement */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Transition pour les messages flash */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
form > div {
  margin-bottom: 1rem;
}
</style>
