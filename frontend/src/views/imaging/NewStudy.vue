<template>
  <div class="container mx-auto py-8 max-w-4xl">
    <!-- En-tête -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold">Nouvel examen DICOM</h1>
      <router-link 
        :to="patientId ? `/patients/${patientId}` : '/patients'" 
        class="text-gray-600 hover:text-gray-800"
      >
        &larr; Retour
      </router-link>
    </div>

    <!-- Formulaire -->
    <div class="bg-white rounded-lg shadow overflow-hidden">
      <div class="p-6">
        <!-- Informations patient -->
        <div v-if="patient" class="mb-6 p-4 bg-blue-50 rounded-lg">
          <h3 class="font-semibold text-lg mb-2">Patient</h3>
          <p class="text-gray-700">
            {{ patient.full_name }} ({{ patient.medical_id }})
            <span v-if="patient.date_of_birth" class="text-gray-500">
              • {{ calculateAge(patient.date_of_birth) }} ans
            </span>
          </p>
        </div>
        
        <!-- Formulaire d'upload -->
        <form @submit.prevent="submitForm">
          <!-- Type d'examen -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="study_type">
              Type d'examen *
            </label>
            <select 
              v-model="formData.study_type"
              id="study_type"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            >
              <option value="">Sélectionnez un type d'examen</option>
              <option value="CT">Tomodensitométrie (CT)</option>
              <option value="MR">Imagerie par Résonance Magnétique (IRM)</option>
              <option value="XRAY">Radiographie (X-Ray)</option>
              <option value="US">Échographie (US)</option>
              <option value="PET">TEP (PET)</option>
              <option value="OTHER">Autre</option>
            </select>
          </div>
          
          <!-- Modalité -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="modality">
              Modalité *
            </label>
            <select 
              v-model="formData.modality"
              id="modality"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            >
              <option value="">Sélectionnez une modalité</option>
              <option value="CT">CT - Tomodensitométrie</option>
              <option value="MR">MR - Imagerie par Résonance Magnétique</option>
              <option value="US">US - Échographie</option>
              <option value="PT">PT - Tomographie par émission de positons</option>
              <option value="XA">XA - Angiographie</option>
              <option value="MG">MG - Mammographie</option>
              <option value="CR">CR - Radiographie numérique</option>
              <option value="DX">DX - Radiographie numérique</option>
              <option value="OT">OT - Autre</option>
            </select>
          </div>
          
          <!-- Date de l'étude -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="study_date">
              Date de l'étude *
            </label>
            <input
              type="date"
              v-model="formData.study_date"
              id="study_date"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            >
          </div>
          
          <!-- Description de l'étude -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="study_description">
              Description de l'étude
            </label>
            <input
              type="text"
              v-model="formData.study_description"
              id="study_description"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Ex: Scanner cérébral sans injection"
            >
          </div>

          <!-- Fichiers DICOM -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2">
              Fichiers DICOM *
            </label>
            <div 
              @dragover.prevent="dragOver = true"
              @dragleave="dragOver = false"
              @drop.prevent="handleDrop"
              :class="{'border-blue-500 bg-blue-50': dragOver}"
              class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer"
              @click="$refs.fileInput.click()"
            >
              <input 
                type="file" 
                ref="fileInput" 
                class="hidden" 
                multiple
                accept=".dcm,application/dicom"
                @change="handleFileSelect"
              >
              <svg 
                class="mx-auto h-12 w-12 text-gray-400" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <p class="mt-1 text-sm text-gray-600">
                Glissez-déposez vos fichiers DICOM ici, ou cliquez pour sélectionner
              </p>
              <p class="mt-1 text-xs text-gray-500">
                Formats acceptés: .dcm (taille maximale: 100MB)
              </p>
            </div>
            
            <!-- Liste des fichiers sélectionnés -->
            <div v-if="files.length > 0" class="mt-4 space-y-2">
              <div 
                v-for="(file, index) in files" 
                :key="index"
                class="flex items-center justify-between p-2 bg-gray-50 rounded"
              >
                <div class="flex items-center">
                  <DocumentTextIcon class="h-5 w-5 text-gray-400 mr-2" />
                  <span class="text-sm text-gray-700">{{ file.name }}</span>
                  <span class="text-xs text-gray-500 ml-2">({{ formatFileSize(file.size) }})</span>
                </div>
                <button 
                  type="button" 
                  @click="removeFile(index)"
                  class="text-red-500 hover:text-red-700"
                >
                  <XIcon class="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>

          <!-- Notes -->
          <div class="mb-6">
            <label class="block text-gray-700 text-sm font-bold mb-2" for="notes">
              Notes (optionnel)
            </label>
            <textarea
              v-model="formData.notes"
              id="notes"
              rows="3"
              class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              placeholder="Ajoutez des notes ou des instructions pour cet examen..."
            ></textarea>
          </div>

          <!-- Boutons d'action -->
          <div class="flex justify-end space-x-4 pt-4 border-t">
            <button
              type="button"
              @click="$router.go(-1)"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
            >
              Annuler
            </button>
            <button
              type="submit"
              :disabled="uploading || files.length === 0"
              :class="{
                'bg-blue-600 hover:bg-blue-700': !uploading && files.length > 0,
                'bg-blue-300 cursor-not-allowed': uploading || files.length === 0
              }"
              class="px-4 py-2 border border-transparent rounded-md text-white focus:outline-none transition-colors"
            >
              <span v-if="uploading">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Téléversement...
              </span>
              <span v-else>
                {{ files.length > 0 ? `Téléverser ${files.length} fichier(s)` : 'Sélectionnez des fichiers' }}
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de succès -->
    <div v-if="showSuccess" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <div class="flex items-center justify-center mb-4">
          <div class="bg-green-100 rounded-full p-2">
            <CheckIcon class="h-8 w-8 text-green-600" />
          </div>
        </div>
        <h3 class="text-lg font-medium text-gray-900 text-center mb-2">Examen créé avec succès</h3>
        <p class="text-sm text-gray-500 text-center mb-6">
          Votre examen a été correctement enregistré et est en cours de traitement.
        </p>
        <div class="flex justify-center space-x-4">
          <button
            @click="goToStudy"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none"
          >
            Voir l'examen
          </button>
          <button
            @click="resetForm"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
          >
            Ajouter un autre examen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import { 
  DocumentTextIcon, 
  XMarkIcon as XIcon, 
  CheckIcon 
} from '@heroicons/vue/24/outline';

export default {
  name: 'NewStudy',
  components: {
    DocumentTextIcon,
    XIcon,
    CheckIcon
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useStore();
    
    // État du composant
    const patientId = ref(route.query.patient_id || '');
    const patient = ref(null);
    const files = ref([]);
    const dragOver = ref(false);
    const uploading = ref(false);
    const showSuccess = ref(false);
    const createdStudyId = ref(null);
    
    const formData = ref({
      study_type: '',
      modality: '',
      study_date: new Date().toISOString().split('T')[0],
      study_description: '',
      body_part: '',
      notes: '',
      patient_id: patientId.value
    });
    
    // Générer un UID unique pour l'étude
    const generateStudyUid = () => {
      return '2.25.' + Math.random().toString().substring(2, 15) + 
             Math.random().toString().substring(2, 15);
    };

    // Récupérer les informations du patient
    const fetchPatient = async () => {
      if (!patientId.value) return;
      try {
        const response = await store.dispatch('patients/fetchPatient', patientId.value);
        patient.value = response;
      } catch (error) {
        console.error('Erreur lors du chargement du patient:', error);
      }
    };

    // Gestion des fichiers
    const handleFileSelect = (event) => {
      const newFiles = Array.from(event.target.files);
      addFiles(newFiles);
    };

    const handleDrop = (event) => {
      dragOver.value = false;
      const newFiles = Array.from(event.dataTransfer.files);
      addFiles(newFiles);
    };

    const addFiles = (newFiles) => {
      // Vérifier la taille totale maximale (100MB)
      const MAX_SIZE = 100 * 1024 * 1024; // 100MB
      const totalSize = [...files.value, ...newFiles].reduce((total, file) => total + file.size, 0);
      
      if (totalSize > MAX_SIZE) {
        alert('La taille totale des fichiers ne doit pas dépasser 100MB');
        return;
      }
      
      // Ajouter uniquement les fichiers DICOM
      const dicomFiles = newFiles.filter(file => 
        file.name.toLowerCase().endsWith('.dcm') || 
        file.type === 'application/dicom'
      );
      
      if (dicomFiles.length !== newFiles.length) {
        alert('Seuls les fichiers DICOM (.dcm) sont acceptés');
      }
      
      files.value = [...files.value, ...dicomFiles];
    };

    const removeFile = (index) => {
      files.value.splice(index, 1);
    };

    // Soumission du formulaire
    const submitForm = async () => {
      if (files.value.length === 0 || !formData.value.study_type || uploading.value) return;
      
      uploading.value = true;
      
      try {
        // Créer un nouvel objet FormData pour l'envoi
        const formDataToSend = new FormData();
        
        // Ajouter le premier fichier (on ne supporte qu'un seul fichier pour l'instant)
        if (files.value.length > 0) {
          formDataToSend.append('dicom_file', files.value[0]);
        }
        
        // Ajouter les autres données du formulaire
        const studyData = {
          patient: formData.value.patient_id,  // Doit être l'ID du patient
          study_instance_uid: generateStudyUid(),
          modality: formData.value.modality,  // Champ obligatoire
          study_date: formData.value.study_date,
          study_description: formData.value.study_description || '',
          body_part: formData.value.body_part || '',
          notes: formData.value.notes || ''
        };
        
        // Supprimer les champs vides
        Object.keys(studyData).forEach(key => {
          if (studyData[key] === null || studyData[key] === undefined || studyData[key] === '') {
            delete studyData[key];
          }
        });
        
        // Ajouter les données de l'étude au FormData
        Object.entries(studyData).forEach(([key, value]) => {
          if (value !== null && value !== undefined) {
            formDataToSend.append(key, value);
          }
        });
        
        // Utiliser l'action createStudy du store
        const response = await store.dispatch('imaging/createStudy', formDataToSend);
        
        // Afficher le message de succès
        createdStudyId.value = response.id;
        showSuccess.value = true;
        
      } catch (error) {
        console.error('Erreur lors de l\'upload de l\'examen:', error);
        alert('Une erreur est survenue lors du téléversement des fichiers.');
      } finally {
        uploading.value = false;
      }
    };

    // Utilitaires
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes';
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const calculateAge = (birthDate) => {
      if (!birthDate) return '';
      const today = new Date();
      const birthDateObj = new Date(birthDate);
      let age = today.getFullYear() - birthDateObj.getFullYear();
      const monthDiff = today.getMonth() - birthDateObj.getMonth();
      
      if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDateObj.getDate())) {
        age--;
      }
      
      return age;
    };

    // Navigation
    const goToStudy = () => {
      if (createdStudyId.value) {
        router.push(`/imaging/studies/${createdStudyId.value}`);
      } else {
        resetForm();
      }
    };

    const resetForm = () => {
      showSuccess.value = false;
      files.value = [];
      formData.value = {
        study_type: '',
        notes: '',
        patient_id: patientId.value
      };
      if (createdStudyId.value) {
        createdStudyId.value = null;
      }
    };

    // Initialisation
    onMounted(() => {
      if (patientId.value) {
        fetchPatient();
      }
    });

    return {
      patientId,
      patient,
      files,
      dragOver,
      uploading,
      showSuccess,
      formData,
      handleFileSelect,
      handleDrop,
      removeFile,
      submitForm,
      formatFileSize,
      calculateAge,
      goToStudy,
      resetForm
    };
  }
};
</script>

<style scoped>
/* Styles spécifiques au composant */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* Animation pour le glisser-déposer */
@keyframes pulse {
  0% { opacity: 0.5; }
  50% { opacity: 1; }
  100% { opacity: 0.5; }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
