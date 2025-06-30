<template>
  <div class="bg-white shadow rounded-lg p-6">
    <h3 class="text-lg font-bold mb-4">Activité récente</h3>
    <ul>
      <li v-for="item in activity" :key="item.id" class="mb-2">
        <span class="font-medium">{{ item.title }}</span> — <span class="text-gray-500">{{ item.description }}</span> <span class="text-xs text-gray-400">({{ item.date }})</span>
      </li>
      <li v-if="activity.length === 0" class="text-gray-400">Aucune activité récente</li>
    </ul>
  </div>
</template>

<script setup>
defineProps({ activity: Array })
</script>
