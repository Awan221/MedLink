<template>
  <div>
    <h2>Liste des rendez-vous</h2>
    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="error">Erreur : {{ error.message || error }}</div>
    <table v-else class="appointments-table">
      <thead>
        <tr>
          <th>Date/Heure</th>
          <th>Patient</th>
          <th>Médecin</th>
          <th>Statut</th>
          <th>Motif</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="appointment in appointments" :key="appointment.id">
          <td>{{ appointment.scheduled_datetime }}</td>
          <td>{{ appointment.patient_name }}</td>
          <td>{{ appointment.doctor_name }}</td>
          <td>{{ appointment.status }}</td>
          <td>{{ appointment.reason }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: "AppointmentList",
  computed: {
    ...mapGetters('appointments', ['allAppointments', 'appointmentsLoading', 'appointmentsError']),
    appointments() {
      return this.allAppointments;
    },
    loading() {
      return this.appointmentsLoading;
    },
    error() {
      return this.appointmentsError;
    }
  },
  created() {
    this.fetchAppointments();
  },
  methods: {
    ...mapActions('appointments', ['fetchAppointments'])
  }
}
</script>

<style scoped>
.appointments-table {
  width: 100%;
  border-collapse: collapse;
}
.appointments-table th, .appointments-table td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
.error {
  color: red;
  margin: 1em 0;
}
</style>
