<template>
  <div>
    <table v-if="requests && requests.length" class="min-w-full divide-y divide-slate-200 bg-white rounded-xl shadow overflow-hidden">
      <thead class="bg-blue-50">
        <tr>
          <th class="px-4 py-2 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Nom</th>
          <th class="px-4 py-2 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Email</th>
          <th class="px-4 py-2 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Rôle</th>
          <th class="px-4 py-2 text-left text-xs font-semibold text-blue-700 uppercase tracking-wider">Date</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-slate-100">
        <tr v-for="req in requests.slice(0, 5)" :key="req.id">
          <td class="px-4 py-2 whitespace-nowrap font-medium text-slate-900">{{ req.first_name }} {{ req.last_name }}</td>
          <td class="px-4 py-2 whitespace-nowrap text-slate-700">{{ req.email }}</td>
          <td class="px-4 py-2 whitespace-nowrap">
            <span class="inline-block px-2 py-1 rounded-full text-xs font-semibold"
                  :class="roleColor(req.role)">
              {{ req.role }}
            </span>
          </td>
          <td class="px-4 py-2 whitespace-nowrap text-slate-600">{{ formatDate(req.created_at) }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else class="text-center text-slate-400 py-8">Aucune demande en attente</div>
    <div class="flex justify-end mt-3" v-if="requests && requests.length">
      <router-link to="/admin/inscriptions" class="text-blue-600 hover:text-indigo-700 text-sm font-medium">Voir tout &rarr;</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "PendingRegistrations",
  props: {
    requests: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return '-';
      const d = new Date(date);
      return d.toLocaleDateString('fr-FR', { year: 'numeric', month: 'short', day: 'numeric' });
    },
    roleColor(role) {
      switch ((role || '').toUpperCase()) {
        case 'MEDECIN': return 'bg-blue-100 text-blue-800';
        case 'SPECIALISTE': return 'bg-purple-100 text-purple-800';
        case 'ADMIN': return 'bg-green-100 text-green-800';
        case 'SUPER_ADMIN': return 'bg-yellow-100 text-yellow-800';
        case 'TECHNICIEN': return 'bg-yellow-100 text-yellow-800';
        case 'BANQUE_SANG': return 'bg-red-100 text-red-800';
        case 'PATIENT': return 'bg-gray-100 text-gray-700';
        default: return 'bg-slate-100 text-slate-800';
      }
    }
  }
}
</script>

<style scoped>
table {
  border-radius: 1rem;
  overflow: hidden;
}
th, td {
  font-size: 0.95rem;
}
</style>