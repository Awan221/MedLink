<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h3 class="text-lg font-bold mb-4">Alertes</h3>
    <ul>
      <li v-for="alert in alerts" :key="alert.id" class="mb-2">
        <span class="font-medium text-red-600">{{ alert.title }}</span> — <span class="text-gray-500">{{ alert.message }}</span>
      </li>
      <li v-if="alerts.length === 0" class="text-gray-400">Aucune alerte</li>
    </ul>
  </div>
</template>

<script setup>
defineProps({ alerts: Array })
</script>
