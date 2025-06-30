<template>
  <div class="container mx-auto py-8">
    <h2 class="text-2xl font-bold mb-4">Liste des patients</h2>
    <div class="mb-4 flex items-center">
      <input v-model="search" @input="handleSearch" placeholder="Recherche... nom, ID, NIN" class="border px-2 py-1 rounded w-64 mr-2" />
      <router-link to="/patients/new" class="ml-auto bg-green-600 text-white px-3 py-1 rounded">Nouveau patient</router-link>
    </div>
    <table class="min-w-full bg-white border">
      <thead>
        <tr>
          <th class="px-4 py-2">Nom</th>
          <th class="px-4 py-2">ID médical</th>
          <th class="px-4 py-2">NIN</th>
          <th class="px-4 py-2">Sexe</th>
          <th class="px-4 py-2">Âge</th>
          <th class="px-4 py-2">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="patient in patients" :key="patient.id">
          <td>{{ patient.full_name }}</td>
          <td>{{ patient.medical_id }}</td>
          <td>{{ patient.national_id }}</td>
          <td>{{ formatGender(patient.gender) }}</td>
          <td>{{ patient.age }}</td>
          <td>
            <router-link :to="`/patients/${patient.id}`" class="text-blue-600 hover:underline">Voir</router-link>
            <router-link :to="`/patients/${patient.id}/edit`" class="ml-2 text-yellow-600 hover:underline">Modifier</router-link>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="patients.length === 0" class="mt-4 text-gray-500">Aucun patient trouvé.</div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
  name: "PatientList",
  data() {
    return {
      search: '',
    }
  },
  computed: {
    ...mapGetters('patients', ['allPatients', 'patientsLoading', 'patientsError']),
    patients() { return this.allPatients; },
    loading() { return this.patientsLoading; },
    error() { return this.patientsError; },
  },
  methods: {
    ...mapActions('patients', ['fetchPatients']),
    handleSearch() {
      this.fetchPatients(this.search);
    },
    formatGender(g) {
      if (g === 'M') return 'Masculin';
      if (g === 'F') return 'Féminin';
      return 'Autre';
    },
  },
  mounted() {
    this.fetchPatients();
  }
}
</script>

<style scoped>
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #e5e7eb;
  padding: 0.5rem;
  text-align: left;
}
</style>
