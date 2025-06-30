<template>
  <div>
    <h2>Visualisation DICOM</h2>
    <select v-model="selectedStudy" @change="fetchSeries">
      <option disabled value="">Sélectionner une étude</option>
      <option v-for="study in studies" :key="study.id" :value="study.id">
        {{ study.patient_name }} - {{ study.study_date }}
      </option>
    </select>

    <div v-if="seriesList.length">
      <label for="seriesSelect">Série :</label>
      <select id="seriesSelect" v-model="selectedSeries" @change="fetchInstances">
        <option disabled value="">Sélectionner une série</option>
        <option v-for="series in seriesList" :key="series.id" :value="series.id">
          {{ series.modality }} - {{ series.series_description || 'Sans description' }}
        </option>
      </select>
    </div>

    <DICOMViewer v-if="imageUrls.length" :imageUrls="imageUrls" />
    <div v-else class="empty">Aucune image à afficher</div>

    <!-- Préparation pour outils d'annotation (cornerstone-tools) -->
    <!-- <div class="annotation-tools">Outils d'annotation à venir...</div> -->
  </div>
</template>

<script>
import DICOMViewer from '@/components/DICOMViewer.vue';

export default {
  name: 'DICOMViewerPage',
  components: { DICOMViewer },
  data() {
    return {
      studies: [],
      selectedStudy: '',
      seriesList: [],
      selectedSeries: '',
      imageUrls: [],
    };
  },
  created() {
    this.fetchStudies();
  },
  methods: {
    async fetchStudies() {
      const res = await fetch('/api/dicom/studies');
      this.studies = await res.json();
    },
    async fetchSeries() {
      this.selectedSeries = '';
      this.imageUrls = [];
      if (!this.selectedStudy) {
        this.seriesList = [];
        return;
      }
      const res = await fetch(`/api/dicom/studies/${this.selectedStudy}/series`);
      this.seriesList = await res.json();
    },
    async fetchInstances() {
      this.imageUrls = [];
      if (!this.selectedSeries) return;
      const res = await fetch(`/api/dicom/series/${this.selectedSeries}/instances`);
      const instances = await res.json();
      this.imageUrls = instances.map(inst => `/api/dicom/instances/${inst.id}/file`);
    },
  },
};
</script>

<style scoped>
.empty {
  color: #888;
  margin-top: 2em;
}
</style>


<style scoped>
.empty {
  color: #888;
  margin-top: 2em;
}
</style>
