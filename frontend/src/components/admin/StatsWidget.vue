<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <div v-for="stat in stats" :key="stat.name" class="bg-white shadow rounded-lg p-6 flex items-center">
      <component :is="stat.icon" class="h-8 w-8 text-blue-600 mr-4" />
      <div>
        <div class="text-lg font-semibold">{{ stat.value }}</div>
        <div class="text-sm text-gray-500">{{ stat.name }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Composant de widget de statistiques pour le tableau de bord admin
defineProps({ stats: Array });
</script>
