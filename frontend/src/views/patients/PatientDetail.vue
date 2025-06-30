<template>
  <div class="container mx-auto py-8 max-w-5xl">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold">Fiche patient</h2>
      <div class="flex space-x-2">
        <router-link 
          v-if="patient" 
          :to="`/patients/${patient.id}/edit`" 
          class="bg-yellow-500 hover:bg-yellow-600 text-white px-3 py-1 rounded text-sm"
        >
          <i class="fas fa-edit mr-1"></i> Modifier
        </router-link>
        <router-link 
          to="/patients" 
          class="bg-gray-400 hover:bg-gray-500 text-white px-3 py-1 rounded text-sm"
        >
          <i class="fas fa-arrow-left mr-1"></i> Retour
        </router-link>
      </div>
    </div>
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
      <p class="mt-2 text-gray-600">Chargement des données du patient...</p>
    </div>
    <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <p class="text-sm text-red-700">{{ error }}</p>
        </div>
      </div>
    </div>
    <div v-else-if="!patient" class="text-center py-8">
      <p class="text-gray-500">Aucune donnée patient trouvée.</p>
      <router-link to="/patients" class="text-blue-600 hover:underline mt-2 inline-block">
        Retour à la liste des patients
      </router-link>
    </div>
    <div v-else>
      <!-- Onglets de navigation -->
      <div class="border-b border-gray-200 mb-6">
        <nav class="-mb-px flex space-x-8">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id 
                ? 'border-blue-500 text-blue-600' 
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            {{ tab.label }}
          </button>
        </nav>
      </div>

      <!-- Contenu des onglets -->
      <div v-show="activeTab === 'info'" class="space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Colonne de gauche - Informations personnelles -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6 bg-gray-50">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Informations personnelles
              </h3>
            </div>
            <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
              <dl class="grid grid-cols-1 gap-x-4 gap-y-4">
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Nom complet</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.full_name || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">ID médical</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.medical_id || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">NIN</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.national_id || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Date de naissance</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.date_of_birth || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Sexe</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ formatGender(patient?.gender) }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Âge</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.age || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Groupe sanguin</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.blood_group || '-' }}</dd>
                </div>
              </dl>
            </div>
          </div>

          <!-- Colonne de droite - Coordonnées -->
          <div class="bg-white shadow overflow-hidden sm:rounded-lg">
            <div class="px-4 py-5 sm:px-6 bg-gray-50">
              <h3 class="text-lg leading-6 font-medium text-gray-900">
                Coordonnées
              </h3>
            </div>
            <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
              <dl class="grid grid-cols-1 gap-x-4 gap-y-4">
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Email</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.email || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Téléphone</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.phone || '-' }}</dd>
                </div>
                <div class="sm:col-span-2">
                  <dt class="text-sm font-medium text-gray-500">Adresse</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.address || '-' }}</dd>
                </div>
                <div class="sm:col-span-1">
                  <dt class="text-sm font-medium text-gray-500">Région</dt>
                  <dd class="mt-1 text-sm text-gray-900">{{ patient?.region || '-' }}</dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        <!-- Informations médicales -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 bg-gray-50">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              Informations médicales
            </h3>
          </div>
          <div class="border-t border-gray-200 px-4 py-5 sm:p-6">
            <dl class="grid grid-cols-1 gap-x-4 gap-y-4">
              <div class="sm:col-span-2">
                <dt class="text-sm font-medium text-gray-500">Allergies</dt>
                <dd class="mt-1 text-sm text-gray-900 whitespace-pre-line">{{ patient?.allergies || 'Aucune connue' }}</dd>
              </div>
              <div class="sm:col-span-2">
                <dt class="text-sm font-medium text-gray-500">Maladies chroniques</dt>
                <dd class="mt-1 text-sm text-gray-900 whitespace-pre-line">{{ patient?.chronic_diseases || 'Aucune connue' }}</dd>
              </div>
              <div class="sm:col-span-2">
                <dt class="text-sm font-medium text-gray-500">Médicaments en cours</dt>
                <dd class="mt-1 text-sm text-gray-900 whitespace-pre-line">{{ patient?.current_medications || 'Aucun' }}</dd>
              </div>
            </dl>
          </div>
        </div>
      </div>

      <!-- Onglet Imagerie -->
      <div v-show="activeTab === 'imaging'">
        <PatientImagingTab 
          v-if="patient" 
          :patient-id="patient.id" 
          class="mt-4"
        />
      </div>
      <h3 class="text-lg font-bold mt-8 mb-2">Historique médical</h3>
      <div v-if="medicalRecords.length === 0" class="text-gray-500">Aucun dossier médical.</div>
      <ul v-else class="mb-4">
        <li v-for="record in medicalRecords" :key="record.id" class="mb-2 border p-2 rounded">
          <div><strong>Date :</strong> {{ new Date(record.date).toLocaleString('fr-FR') }}</div>
          <div><strong>Médecin :</strong> {{ record.doctor_name }}</div>
          <div><strong>Motif :</strong> {{ record.reason }}</div>
          <div><strong>Diagnostic :</strong> {{ record.diagnosis }}</div>
          <div><strong>Traitement :</strong> {{ record.treatment }}</div>
          <div class="mt-2 flex gap-2">
            <router-link v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" :to="`/patients/${patient.id}/medical-records/${record.id}/edit`" class="bg-yellow-500 text-white px-2 py-1 rounded">Modifier</router-link>
            <button v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" @click="deleteMedicalRecord(record.id)" class="bg-red-600 text-white px-2 py-1 rounded">Supprimer</button>
          </div>
          <MedicalRecordHistory :recordId="record.id" />
        </li>
      </ul>
      <router-link v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" :to="`/patients/${patient.id}/medical-records/new`" class="bg-blue-600 text-white px-3 py-1 rounded">Ajouter un dossier médical</router-link>

      <h3 class="text-lg font-bold mt-8 mb-2">Prescriptions</h3>
      <div v-if="prescriptions.length === 0" class="text-gray-500">Aucune prescription.</div>
      <ul v-else>
        <li v-for="presc in prescriptions" :key="presc.id" class="mb-2 border p-2 rounded">
          <div><strong>Date :</strong> {{ new Date(presc.date).toLocaleString('fr-FR') }}</div>
          <div><strong>Médecin :</strong> {{ presc.doctor_name }}</div>
          <div><strong>Médicaments :</strong> {{ presc.medications }}</div>
          <div><strong>Dosage :</strong> {{ presc.dosage }}</div>
          <div><strong>Durée :</strong> {{ presc.duration }}</div>
          <div class="mt-2 flex gap-2">
            <router-link v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" :to="`/patients/${patient.id}/prescriptions/${presc.id}/edit`" class="bg-yellow-500 text-white px-2 py-1 rounded">Modifier</router-link>
            <button v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" @click="deletePrescription(presc.id)" class="bg-red-600 text-white px-2 py-1 rounded">Supprimer</button>
          </div>
          <PrescriptionHistory :prescriptionId="presc.id" />
        </li>
      </ul>
      <router-link v-if="['admin', 'medecin', 'specialiste'].includes(userRole)" :to="`/patients/${patient.id}/prescriptions/new`" class="bg-blue-600 text-white px-3 py-1 rounded mt-2">Ajouter une prescription</router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import MedicalRecordHistory from './MedicalRecordHistory.vue';
import PrescriptionHistory from './PrescriptionHistory.vue';
import PatientImagingTab from '@/components/patients/PatientImagingTab.vue';
export default {
  name: "PatientDetail",
  data() {
    return {
      activeTab: 'info',
      tabs: [
        { id: 'info', label: 'Informations' },
        { id: 'imaging', label: 'Imagerie' },
        { id: 'history', label: 'Historique' },
        { id: 'prescriptions', label: 'Prescriptions' }
      ],
      medicalRecords: [],
      prescriptions: [],
      userRole: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')).role.toLowerCase() : '',
    }
  },
  computed: {
    ...mapGetters('patients', ['patient', 'patientsLoading', 'patientsError']),
    loading() { return this.patientsLoading; },
    error() { return this.patientsError; },
  },
  methods: {
    ...mapActions('patients', ['fetchPatient']),
    fetchMedicalRecords() {
      // axios.get(`${process.env.VUE_APP_API_URL}patients/${this.$route.params.id}/medical-records/`, {
      //   headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      // })
      //   .then(res => {
      //     this.medicalRecords = res.data;
      //   })
      //   .catch(() => {
      //     this.medicalRecords = [];
      //   });
    },
    fetchPrescriptions() {
      // axios.get(`${process.env.VUE_APP_API_URL}patients/${this.$route.params.id}/prescriptions/`, {
      //   headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      // })
      //   .then(res => {
      //     this.prescriptions = res.data;
      //   })
      //   .catch(() => {
      //     this.prescriptions = [];
      //   });
    },
    // eslint-disable-next-line no-unused-vars
    deleteMedicalRecord(recordId) {
      // axios.delete(`${process.env.VUE_APP_API_URL}patients/${this.$route.params.id}/medical-records/${recordId}/`, {
      //   headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      // })
      //   .then(() => {
      //     this.fetchMedicalRecords();
      //   })
      //   .catch(() => {
      //     alert('Erreur lors de la suppression du dossier médical.');
      //   });
    },
    // eslint-disable-next-line no-unused-vars
    deletePrescription(prescId) {
      // axios.delete(`${process.env.VUE_APP_API_URL}patients/${this.$route.params.id}/prescriptions/${prescId}/`, {
      //   headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      // })
      //   .then(() => {
      //     this.fetchPrescriptions();
      //   })
      //   .catch(() => {
      //     alert('Erreur lors de la suppression de la prescription.');
      //   });
    },
    formatGender(g) {
      if (g === 'M') return 'Masculin';
      if (g === 'F') return 'Féminin';
      return 'Autre';
    }
  },
  async mounted() {
    try {
      const patientId = this.$route.params.id;
      if (!patientId) {
        throw new Error('ID patient manquant dans l\'URL');
      }
      
      // Charger les données du patient
      await this.fetchPatient(patientId);
      
      // Vérifier que les données du patient sont bien chargées
      if (!this.patient) {
        throw new Error('Impossible de charger les données du patient');
      }
      
      // Charger les données associées
      await Promise.all([
        this.fetchMedicalRecords(),
        this.fetchPrescriptions()
      ]);
      
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
      this.$store.commit('patients/setError', error.message || 'Une erreur est survenue lors du chargement des données');
    }
  },
  components: {
    MedicalRecordHistory,
    PrescriptionHistory,
    PatientImagingTab
  }
}
</script>

<style scoped>
.container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 2rem;
}
</style>
