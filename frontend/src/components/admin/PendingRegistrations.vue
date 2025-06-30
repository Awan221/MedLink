<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h3 class="text-lg font-bold mb-4">Inscriptions en attente</h3>
    <ul>
      <li v-for="req in requests" :key="req.id" class="mb-2">
        <span class="font-medium">{{ req.name }}</span> — <span class="text-gray-500">{{ req.type }}</span> <span class="text-xs text-gray-400">({{ req.date }})</span>
      </li>
      <li v-if="requests.length === 0" class="text-gray-400">Aucune inscription en attente</li>
    </ul>
  </div>
</template>

<script setup>
defineProps({ requests: Array })
</script>
