<template>
  <div class="statistics-page">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Statistiques de Santé</h1>

      <!-- Statistiques générales -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 text-blue-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Patients traités</p>
              <p class="text-2xl font-semibold text-gray-900">24,500</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 text-green-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Rendez-vous</p>
              <p class="text-2xl font-semibold text-gray-900">12,800</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Hôpitaux partenaires</p>
              <p class="text-2xl font-semibold text-gray-900">45</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-red-100 text-red-600">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">Donneurs de sang</p>
              <p class="text-2xl font-semibold text-gray-900">8,200</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Graphiques -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Maladies les plus fréquentes -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Maladies les plus fréquentes</h2>
          <div class="space-y-4">
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-blue-600 h-4 rounded-full" style="width: 75%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">COVID-19 (75%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-blue-600 h-4 rounded-full" style="width: 60%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Diabète (60%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-blue-600 h-4 rounded-full" style="width: 45%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Hypertension (45%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-blue-600 h-4 rounded-full" style="width: 30%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Asthme (30%)</span>
            </div>
          </div>
        </div>

        <!-- Taux de satisfaction -->
        <div class="bg-white rounded-lg shadow-lg p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">Taux de satisfaction</h2>
          <div class="space-y-4">
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-green-600 h-4 rounded-full" style="width: 90%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Service d'urgence (90%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-green-600 h-4 rounded-full" style="width: 85%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Consultations (85%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-green-600 h-4 rounded-full" style="width: 80%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Imagerie médicale (80%)</span>
            </div>
            <div class="flex items-center">
              <div class="w-full bg-gray-200 rounded-full h-4">
                <div class="bg-green-600 h-4 rounded-full" style="width: 75%"></div>
              </div>
              <span class="ml-4 text-sm text-gray-600">Laboratoire (75%)</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Informations supplémentaires -->
      <div class="mt-12 bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Points clés</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="p-4 bg-blue-50 rounded-lg">
            <h3 class="font-medium text-blue-900 mb-2">Temps d'attente moyen</h3>
            <p class="text-blue-700">15 minutes en consultation</p>
          </div>
          <div class="p-4 bg-green-50 rounded-lg">
            <h3 class="font-medium text-green-900 mb-2">Taux de guérison</h3>
            <p class="text-green-700">95% pour les cas traités</p>
          </div>
          <div class="p-4 bg-yellow-50 rounded-lg">
            <h3 class="font-medium text-yellow-900 mb-2">Disponibilité des lits</h3>
            <p class="text-yellow-700">85% en moyenne</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatisticsPage'
}
</script>

<style scoped>
.statistics-page {
  min-height: 100vh;
  background-color: #f8fafc;
}
</style> 