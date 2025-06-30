<template>
  <div>
    <h4 class="text-md font-bold mt-4 mb-2">Historique des modifications</h4>
    <div v-if="loading">Chargement...</div>
    <div v-else-if="error" class="text-red-600">{{ error }}</div>
    <ul v-else-if="history.length > 0">
      <li v-for="item in history" :key="item.id" class="mb-2 border p-2 rounded">
        <div>
          <strong>Action :</strong>
          <span :class="badgeClass(item.action)">{{ actionLabel(item.action) }}</span>
        </div>
        <div><strong>Par :</strong> {{ item.performed_by || 'Inconnu' }}</div>
        <div><strong>Date :</strong> {{ new Date(item.performed_at).toLocaleString('fr-FR') }}</div>
        <div><strong>État du dossier :</strong>
          <ul class="bg-gray-50 rounded p-2 text-xs">
            <li><strong>Date :</strong> {{ new Date(item.snapshot.date).toLocaleString('fr-FR') }}</li>
            <li><strong>Médecin :</strong> {{ item.snapshot.doctor }}</li>
            <li><strong>Motif :</strong> {{ item.snapshot.reason }}</li>
            <li><strong>Diagnostic :</strong> {{ item.snapshot.diagnosis }}</li>
            <li><strong>Traitement :</strong> {{ item.snapshot.treatment }}</li>
            <li v-if="item.snapshot.notes"><strong>Notes :</strong> {{ item.snapshot.notes }}</li>
          </ul>
        </div>
      </li>
    </ul>
    <div v-else class="text-gray-500">Aucun historique trouvé.</div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'MedicalRecordHistory',
  props: {
    recordId: {
      type: [Number, String],
      required: true
    }
  },
  computed: {
    ...mapGetters('medicalRecords', ['allMedicalRecords', 'medicalRecordsLoading', 'medicalRecordsError']),
    history() { return this.allMedicalRecords; },
    loading() { return this.medicalRecordsLoading; },
    error() { return this.medicalRecordsError; },
  },
  methods: {
    ...mapActions('medicalRecords', ['fetchMedicalRecords']),
    fetchHistory() {
      this.fetchMedicalRecords(this.recordId);
    },
    actionLabel(action) {
      switch(action) {
        case 'create': return 'Création';
        case 'update': return 'Modification';
        case 'delete': return 'Suppression';
        default: return action;
      }
    },
    badgeClass(action) {
      switch(action) {
        case 'create': return 'inline-block px-2 py-0.5 rounded bg-green-100 text-green-700 text-xs';
        case 'update': return 'inline-block px-2 py-0.5 rounded bg-yellow-100 text-yellow-700 text-xs';
        case 'delete': return 'inline-block px-2 py-0.5 rounded bg-red-100 text-red-700 text-xs';
        default: return '';
      }
    },
  },
  mounted() {
    this.fetchHistory();
  }
}
</script>

<style scoped>
pre { white-space: pre-wrap; word-break: break-all; }
</style>
