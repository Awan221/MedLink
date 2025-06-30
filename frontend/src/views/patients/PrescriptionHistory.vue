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
        <div><strong>État de la prescription :</strong>
          <ul class="bg-gray-50 rounded p-2 text-xs">
            <li><strong>Date :</strong> {{ new Date(item.snapshot.date).toLocaleString('fr-FR') }}</li>
            <li><strong>Médecin :</strong> {{ item.snapshot.doctor }}</li>
            <li><strong>Médicaments :</strong> {{ item.snapshot.medications }}</li>
            <li><strong>Dosage :</strong> {{ item.snapshot.dosage }}</li>
            <li><strong>Durée :</strong> {{ item.snapshot.duration }}</li>
            <li v-if="item.snapshot.instructions"><strong>Instructions :</strong> {{ item.snapshot.instructions }}</li>
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
  name: 'PrescriptionHistory',
  props: {
    prescriptionId: {
      type: [Number, String],
      required: true
    }
  },
  data() {
    return {
      // plus de state local, tout passe par le store
    }
  },
  computed: {
    ...mapGetters('prescriptions', ['allPrescriptions', 'prescriptionsLoading', 'prescriptionsError']),
    history() { return this.allPrescriptions; },
    loading() { return this.prescriptionsLoading; },
    error() { return this.prescriptionsError; },
  },
  methods: {
    ...mapActions('prescriptions', ['fetchPrescriptions']),
    fetchHistory() {
      this.fetchPrescriptions();
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
   // this.fetchHistory();
  }
}
</script>

<style scoped>
pre { white-space: pre-wrap; word-break: break-all; }
</style>
