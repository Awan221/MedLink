<template>
  <div class="container mx-auto py-8">
    <h2 class="text-2xl font-bold mb-4">Études DICOM</h2>
    <form @submit.prevent="handleUpload" class="mb-6 flex flex-col md:flex-row items-center gap-4">
      <div class="relative w-64">
        <label class="block mb-1">Patient (recherche nom ou ID)</label>
        <input v-model="patientSearch" @input="searchPatients" @focus="showSuggestions=true" @blur="onBlur" placeholder="Nom, prénom ou ID médical" class="border px-2 py-1 rounded w-full" autocomplete="off" />
        <ul v-if="showSuggestions && patientSuggestions.length > 0" class="absolute z-10 bg-white border w-full max-h-40 overflow-auto rounded shadow">
          <li v-for="patient in patientSuggestions" :key="patient.id" @mousedown.prevent="selectPatient(patient)" class="px-3 py-2 hover:bg-blue-100 cursor-pointer">
            {{ patient.full_name }} ({{ patient.medical_id }})
          </li>
        </ul>
        <div v-if="showSuggestions && patientSearch && patientSuggestions.length === 0" class="absolute z-10 bg-white border w-full px-3 py-2 text-gray-500 rounded shadow">Aucun patient trouvé</div>
      </div>
      <div>
        <label class="block mb-1">Fichier DICOM</label>
        <input type="file" @change="onFileChange" accept=".dcm,application/dicom" required />
      </div>
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Uploader</button>
    </form>
    <transition name="fade">
      <div v-if="successMessage" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded relative mb-4" role="alert">
        <span class="block sm:inline">{{ successMessage }}</span>
      </div>
    </transition>
    <transition name="fade">
      <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
        <span class="block sm:inline">{{ errorMessage }}</span>
      </div>
    </transition>
    <h3 class="text-xl font-semibold mb-2">Liste des études</h3>
    <ul>
      <li v-for="study in studies" :key="study?.id || Math.random()">
        <template v-if="study">
          <router-link :to="`/imaging/studies/${study.id}`">{{ study.study_description || study.id }}</router-link>
        </template>
      </li>
    </ul>
    <div v-if="studies.length === 0" class="mt-4 text-gray-500">Aucune étude trouvée.</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "StudyList",
  data() {
    return {
      studies: [],
      patientId: '',
      patientSearch: '',
      patientSuggestions: [],
      showSuggestions: false,
      file: null,
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    fetchStudies() {
      axios.get('/imaging/studies/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          // Filtrer les études nulles ou non valides
          this.studies = Array.isArray(res.data) 
            ? res.data.filter(study => study && study.id) 
            : [];
          
          // Journalisation pour le débogage
          if (this.studies.length === 0) {
            console.log('Aucune étude valide trouvée dans la réponse:', res.data);
          }
        })
        .catch((error) => {
          console.error('Erreur lors de la récupération des études:', error);
          this.studies = [];
          this.errorMessage = 'Impossible de charger les études. Veuillez réessayer.';
        });
    },
    onFileChange(event) {
      this.file = event.target.files[0];
    },
    handleUpload() {
      if (!this.patientId || !this.file) return;
      this.successMessage = '';
      this.errorMessage = '';
      const formData = new FormData();
      formData.append('patient_medical_id', this.patientId);
      formData.append('file', this.file);
      axios.post('/imaging/studies/direct_upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('access')}`
        }
      })
        .then(() => {
          this.successMessage = 'Image DICOM uploadée avec succès.';
          this.errorMessage = '';
          this.fetchStudies();
          this.patientId = '';
          this.patientSearch = '';
          this.patientSuggestions = [];
        })
        .catch(err => {
          this.errorMessage = err.response?.data?.detail || "Erreur lors de l'upload DICOM.";
          this.successMessage = '';
        });
    },
    searchPatients() {
      if (!this.patientSearch) {
        this.patientSuggestions = [];
        this.patientId = '';
        return;
      }
      axios.get(`/patients/?search=${encodeURIComponent(this.patientSearch)}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.patientSuggestions = res.data;
        })
        .catch(() => {
          this.patientSuggestions = [];
        });
    },
    selectPatient(patient) {
      this.patientId = patient.medical_id;
      this.patientSearch = `${patient.full_name} (${patient.medical_id})`;
      this.patientSuggestions = [];
      this.showSuggestions = false;
    },
    onBlur() {
      setTimeout(() => { this.showSuggestions = false; }, 150);
    }
  },
  mounted() {
    this.fetchStudies();
  }
};
</script>
