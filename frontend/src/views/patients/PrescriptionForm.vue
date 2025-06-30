<template>
  <div class="container mx-auto py-8 max-w-xl">
    <h2 class="text-2xl font-bold mb-4">Ajouter une prescription</h2>
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div>
        <label>Médicaments</label>
        <textarea v-model="form.medications" required class="border px-2 py-1 rounded w-full"></textarea>
      </div>
      <div>
        <label>Dosage</label>
        <input v-model="form.dosage" required class="border px-2 py-1 rounded w-full" />
      </div>
      <div>
        <label>Durée</label>
        <input v-model="form.duration" required class="border px-2 py-1 rounded w-full" />
      </div>
      <div>
        <label>Instructions</label>
        <textarea v-model="form.instructions" class="border px-2 py-1 rounded w-full"></textarea>
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
  name: "PrescriptionForm",
  data() {
    return {
      form: {
        medications: '',
        dosage: '',
        duration: '',
        instructions: ''
      },
      error: '',
      patientId: this.$route.params.id,
      prescId: this.$route.params.prescId,
      isEdit: !!this.$route.params.prescId
    }
  },
  created() {
    if (this.isEdit) {
      this.fetchPrescription();
    }
  },
  methods: {
    fetchPrescription() {
      axios.get(`${process.env.VUE_APP_API_URL}patients/${this.patientId}/prescriptions/${this.prescId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      })
        .then(res => {
          this.form = res.data;
        })
        .catch(() => {
          this.error = "Erreur lors du chargement de la prescription.";
        });
    },
    handleSubmit() {
      const url = this.isEdit
        ? `${process.env.VUE_APP_API_URL}patients/${this.patientId}/prescriptions/${this.prescId}/`
        : `${process.env.VUE_APP_API_URL}patients/${this.patientId}/prescriptions/`;
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
