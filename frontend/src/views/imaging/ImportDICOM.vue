<template>
  <div class="container mx-auto py-8">
    <h2 class="text-2xl font-bold mb-4">Import en masse DICOM (Technicien)</h2>
    <form @submit.prevent="handleBulkUpload" class="space-y-6">
      <div>
        <label class="block mb-1">Sélectionner les fichiers DICOM</label>
        <input type="file" multiple @change="onFilesChange" accept=".dcm,application/dicom" />
      </div>
      <div v-if="files.length > 0">
        <h3 class="text-lg font-semibold mb-2">Associer chaque fichier à un patient</h3>
        <div v-for="(file, idx) in files" :key="file.name + idx" class="mb-4 p-2 border rounded">
          <div class="mb-1 font-medium">{{ file.name }}</div>
          <div v-if="dicomError[idx]" class="text-red-600 text-sm mb-1">{{ dicomError[idx] }}</div>
          <div v-else-if="dicomMeta[idx]" class="bg-gray-50 rounded p-2 text-xs mb-1">
            <div><strong>Patient :</strong> {{ dicomMeta[idx].PatientName }} ({{ dicomMeta[idx].PatientID }})</div>
            <div><strong>Date étude :</strong> {{ dicomMeta[idx].StudyDate }}</div>
            <div><strong>Modalité :</strong> {{ dicomMeta[idx].Modality }}</div>
            <div><strong>Étude :</strong> {{ dicomMeta[idx].StudyDescription }}</div>
            <div><strong>Série :</strong> {{ dicomMeta[idx].SeriesDescription }}</div>
            <div><strong>Institution :</strong> {{ dicomMeta[idx].InstitutionName }}</div>
          </div>
          <div class="relative w-64">
            <input v-model="patientSearch[idx]" @input="searchPatients(idx)" @focus="showSuggestions[idx]=true" @blur="onBlur(idx)" placeholder="Nom, prénom ou ID médical" class="border px-2 py-1 rounded w-full" autocomplete="off" />
            <ul v-if="showSuggestions[idx] && patientSuggestions[idx] && patientSuggestions[idx].length > 0" class="absolute z-10 bg-white border w-full max-h-40 overflow-auto rounded shadow">
              <li v-for="patient in patientSuggestions[idx]" :key="patient.id" @mousedown.prevent="selectPatient(idx, patient)" class="px-3 py-2 hover:bg-blue-100 cursor-pointer">
                {{ patient.full_name }} ({{ patient.medical_id }})
              </li>
            </ul>
            <div v-if="showSuggestions[idx] && patientSearch[idx] && (!patientSuggestions[idx] || patientSuggestions[idx].length === 0)" class="absolute z-10 bg-white border w-full px-3 py-2 text-gray-500 rounded shadow">Aucun patient trouvé</div>
          </div>
        </div>
      </div>
      <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded" :disabled="loading">Importer</button>
    </form>

  </div>
</template>

<script>
import axios from 'axios';
import { extractDicomMetadata } from '@/utils/dicomMeta';
export default {
  name: 'ImportDICOM',
  data() {
    return {
      files: [],
      patientSearch: [],
      patientId: [],
      patientSuggestions: [],
      showSuggestions: [],
      dicomMeta: [], // tableau de métadonnées pour chaque fichier
      dicomError: [], // tableau d’erreurs pour chaque fichier
      loading: false,

    };
  },
  methods: {
    async onFilesChange(event) {
      this.files = Array.from(event.target.files);
      this.patientSearch = this.files.map(() => '');
      this.patientId = this.files.map(() => '');
      this.patientSuggestions = this.files.map(() => []);
      this.showSuggestions = this.files.map(() => false);
      this.dicomMeta = [];
      this.dicomError = [];
      // Extraction des métadonnées pour chaque fichier
      for (let i = 0; i < this.files.length; i++) {
        try {
          const meta = await extractDicomMetadata(this.files[i]);
          this.dicomMeta[i] = meta;
          this.dicomError[i] = '';
        } catch (err) {
          this.dicomMeta[i] = null;
          this.dicomError[i] = err;
        }
      }
    },
    searchPatients(idx) {
      if (!this.patientSearch[idx]) {
        this.patientSuggestions[idx] = [];
        this.patientId[idx] = '';
        return;
      }
      axios.get(`/api/patients/?search=${encodeURIComponent(this.patientSearch[idx])}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.$set(this.patientSuggestions, idx, res.data);
        })
        .catch(() => {
          this.$set(this.patientSuggestions, idx, []);
        });
    },
    selectPatient(idx, patient) {
      this.$set(this.patientId, idx, patient.medical_id);
      this.$set(this.patientSearch, idx, `${patient.full_name} (${patient.medical_id})`);
      this.$set(this.patientSuggestions, idx, []);
      this.$set(this.showSuggestions, idx, false);
    },
    onBlur(idx) {
      setTimeout(() => { this.$set(this.showSuggestions, idx, false); }, 150);
    },
    async handleBulkUpload() {
      if (this.files.length === 0) return;
      this.loading = true;
      let successCount = 0;
      let failCount = 0;
      for (let i = 0; i < this.files.length; i++) {
        if (!this.patientId[i] || !this.files[i]) {
          failCount++;
          continue;
        }
        const formData = new FormData();
        formData.append('patient_medical_id', this.patientId[i]);
        formData.append('file', this.files[i]);
        try {
          await axios.post('/api/imaging/studies/direct_upload/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${localStorage.getItem('access')}`
            }
          });
          successCount++;
        } catch (err) {
          failCount++;
        }
      }
      this.loading = false;
      if (successCount > 0 && failCount === 0) {
        this.$toast.success(`${successCount} fichier(s) importé(s) avec succès.`);
      } else if (successCount > 0 && failCount > 0) {
        this.$toast.success(`${successCount} import(s) réussi(s), ${failCount} échec(s).`);
        this.$toast.error(`${failCount} import(s) ont échoué.`);
      } else if (failCount > 0) {
        this.$toast.error(`Tous les imports ont échoué.`);
      }
      // Reset
      this.files = [];
      this.patientSearch = [];
      this.patientId = [];
      this.patientSuggestions = [];
      this.showSuggestions = [];
    }
  }
};
</script>

<style scoped>
input[type="file"] {
  margin-bottom: 1rem;
}
</style>
