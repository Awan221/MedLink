<template>
  <div class="container mx-auto py-8 max-w-xl">
    <h2 class="text-2xl font-bold mb-4">Ajouter un dossier médical</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label>Motif</label>
        <input v-model="form.reason" required class="border px-2 py-1 rounded w-full" />
      </div>
      <div>
        <label>Symptômes</label>
        <textarea v-model="form.symptoms" class="border px-2 py-1 rounded w-full"></textarea>
      </div>
      <div>
        <label>Diagnostic</label>
        <textarea v-model="form.diagnosis" class="border px-2 py-1 rounded w-full"></textarea>
      </div>
      <div>
        <label>Traitement</label>
        <textarea v-model="form.treatment" class="border px-2 py-1 rounded w-full"></textarea>
      </div>
      <div>
        <label>Notes</label>
        <textarea v-model="form.notes" class="border px-2 py-1 rounded w-full"></textarea>
      </div>
      <div class="flex gap-2">
        <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">Enregistrer</button>
        <router-link :to="`/patients/${patientId}`" class="bg-gray-400 text-white px-4 py-2 rounded">Annuler</router-link>
      </div>
      <div v-if="error" class="text-red-600">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "MedicalRecordForm",
  data() {
    return {
      form: {
        reason: '',
        symptoms: '',
        diagnosis: '',
        treatment: '',
        notes: ''
      },
      error: '',
      patientId: this.$route.params.id,
      recordId: this.$route.params.recordId,
      isEdit: !!this.$route.params.recordId
    }
  },
  created() {
    if (this.isEdit) {
      this.fetchMedicalRecord();
    }
  },
  methods: {
    fetchMedicalRecord() {
      axios.get(`${process.env.VUE_APP_API_URL}patients/${this.patientId}/medical-records/${this.recordId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.form = res.data;
        })
        .catch(() => {
          this.error = "Erreur lors du chargement du dossier médical.";
        });
    },
    handleSubmit() {
      const url = this.isEdit
        ? `${process.env.VUE_APP_API_URL}patients/${this.patientId}/medical-records/${this.recordId}/`
        : `${process.env.VUE_APP_API_URL}patients/${this.patientId}/medical-records/`;
      const method = this.isEdit ? 'put' : 'post';
      axios[method](url, this.form, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(() => {
          this.$router.push(`/patients/${this.patientId}`);
        })
        .catch(err => {
          this.error = err.response?.data?.detail || "Erreur lors de l'enregistrement.";
        });
    }
  }
}
</script>

<style scoped>
form > div {
  margin-bottom: 1rem;
}
</style>
