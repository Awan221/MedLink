<template>
  <div>
    <h2>Créer un rendez-vous</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="patient">Patient :</label>
        <input v-model="form.patient" id="patient" required />
      </div>
      <div>
        <label for="doctor">Médecin :</label>
        <input v-model="form.doctor" id="doctor" required />
      </div>
      <div>
        <label for="scheduled_datetime">Date/Heure :</label>
        <input v-model="form.scheduled_datetime" id="scheduled_datetime" type="datetime-local" required />
      </div>
      <div>
        <label for="reason">Motif :</label>
        <textarea v-model="form.reason" id="reason"></textarea>
      </div>
      <button type="submit" :disabled="loading">Créer</button>
    </form>
    <div v-if="error" class="error">Erreur : {{ error.message || error }}</div>
    <div v-if="success" class="success">Rendez-vous créé avec succès !</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "AppointmentForm",
  data() {
    return {
      form: {
        patient: '',
        doctor: '',
        scheduled_datetime: '',
        reason: ''
      },
      loading: false,
      error: null,
      success: false
    };
  },
  methods: {
    async submitForm() {
      this.loading = true;
      this.error = null;
      this.success = false;
      try {
        await axios.post('/api/patients/appointments/', this.form);
        this.success = true;
        this.form = { patient: '', doctor: '', scheduled_datetime: '', reason: '' };
      } catch (err) {
        this.error = err.response ? err.response.data : err;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
form > div {
  margin-bottom: 1em;
}
label {
  display: block;
  margin-bottom: 0.3em;
}
input, textarea {
  width: 100%;
  padding: 0.5em;
  box-sizing: border-box;
}
button {
  padding: 0.6em 1.2em;
  font-size: 1em;
}
.error {
  color: red;
  margin-top: 1em;
}
.success {
  color: green;
  margin-top: 1em;
}
</style>
