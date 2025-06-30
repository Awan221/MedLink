<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-12">
        <div class="inline-block p-3 rounded-full bg-white shadow-lg mb-4">
          <svg class="w-12 h-12 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
        </div>
        <h2 class="text-4xl font-extrabold text-gray-900 sm:text-5xl bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-indigo-600">
          Inscription à MedLink
        </h2>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          Rejoignez notre réseau de professionnels de santé et contribuez à améliorer les soins médicaux
        </p>
      </div>

      <div class="bg-white shadow-2xl rounded-2xl overflow-hidden transform transition-all duration-500 hover:shadow-primary-100">
        <div class="px-8 py-6 border-b border-gray-200 bg-gradient-to-r from-primary-50 to-indigo-50">
          <h3 class="text-2xl font-semibold text-gray-900 flex items-center">
            <svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Informations personnelles
          </h3>
        </div>

        <form class="space-y-8 p-8" @submit.prevent="handleRegister">
          <transition name="fade" mode="out-in">
            <div v-if="success" class="bg-green-50 border-l-4 border-green-500 text-green-700 p-4 rounded-lg mb-6 shadow-md" role="alert">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-green-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium">{{ success }}</p>
                </div>
              </div>
            </div>
          </transition>

          <transition name="fade" mode="out-in">
            <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg mb-6 shadow-md" role="alert">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-6 w-6 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium">{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </transition>

          <div class="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2">
            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="first_name" class="block text-sm font-medium text-gray-700 mb-2">
                Prénom
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  id="first_name" 
                  name="first_name" 
                  type="text" 
                  autocomplete="given-name" 
                  required 
                  v-model="formData.first_name"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>

            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="last_name" class="block text-sm font-medium text-gray-700 mb-2">
                Nom
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input 
                  id="last_name" 
                  name="last_name" 
                  type="text" 
                  autocomplete="family-name" 
                  required 
                  v-model="formData.last_name"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>
          </div>

          <div class="form-group transform transition-all duration-300 hover:scale-105">
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Adresse email
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <input 
                id="email" 
                name="email" 
                type="email" 
                autocomplete="email" 
                required 
                v-model="formData.email"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
              />
            </div>
          </div>

          <div class="form-group transform transition-all duration-300 hover:scale-105">
            <label for="role" class="block text-sm font-medium text-gray-700 mb-2">
              Rôle
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <select 
                id="role" 
                name="role" 
                required 
                v-model="formData.role"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                @change="handleRoleChange"
              >
                <option value="">Sélectionnez un rôle</option>
                <option value="doctor">Médecin Généraliste</option>
                <option value="specialist">Médecin Spécialiste</option>
                <option value="radiologist">Radiologue</option>
                <option value="lab_technician">Technicien en Imagerie</option>
                <option value="blood_bank_manager">Responsable Banque de Sang</option>
                <option value="nurse">Autre Personnel Médical</option>
              </select>
            </div>
          </div>

          <div v-if="formData.role === 'specialist'" class="form-group transform transition-all duration-300 hover:scale-105">
            <label for="specialist_type" class="block text-sm font-medium text-gray-700 mb-2">
              Spécialité
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <select 
                id="specialist_type" 
                name="specialist_type" 
                required 
                v-model="formData.specialist_type"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
              >
                <option value="">Sélectionnez une spécialité</option>
                <option value="cardiologist">Cardiologue</option>
                <option value="neurologist">Neurologue</option>
                <option value="pediatrician">Pédiatre</option>
                <option value="gynecologist">Gynécologue</option>
                <option value="dermatologist">Dermatologue</option>
                <option value="orthopedist">Orthopédiste</option>
                <option value="ophthalmologist">Ophtalmologue</option>
                <option value="other">Autre Spécialité</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2">
            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                Téléphone
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
                <input 
                  id="phone" 
                  name="phone" 
                  type="tel" 
                  autocomplete="tel" 
                  v-model="formData.phone"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>

            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="hopital" class="block text-sm font-medium text-gray-700 mb-2">
                Hôpital / Établissement
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <input 
                  id="hopital" 
                  name="hopital" 
                  type="text" 
                  v-model="formData.hopital"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>
          </div>

          <div class="form-group transform transition-all duration-300 hover:scale-105">
            <label for="region" class="block text-sm font-medium text-gray-700 mb-2">
              Région
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <input 
                id="region" 
                name="region" 
                type="text" 
                v-model="formData.region"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 gap-y-8 gap-x-6 sm:grid-cols-2">
            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="numero_licence" class="block text-sm font-medium text-gray-700 mb-2">
                Numéro de licence professionnelle
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <input 
                  id="numero_licence" 
                  name="numero_licence" 
                  type="text" 
                  required 
                  v-model="formData.numero_licence"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>

            <div class="form-group transform transition-all duration-300 hover:scale-105">
              <label for="date_licence" class="block text-sm font-medium text-gray-700 mb-2">
                Date d'obtention de la licence
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <input 
                  id="date_licence" 
                  name="date_licence" 
                  type="date" 
                  required 
                  v-model="formData.date_licence"
                  class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
                />
              </div>
            </div>
          </div>

          <div class="form-group transform transition-all duration-300 hover:scale-105">
            <label for="documents" class="block text-sm font-medium text-gray-700 mb-2">
              Documents justificatifs
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
                </svg>
              </div>
              <input 
                id="documents" 
                name="documents" 
                type="file" 
                multiple 
                accept=".pdf,.jpg,.jpeg,.png"
                @change="handleFileUpload"
                class="appearance-none block w-full pl-10 px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-all duration-200"
              />
              <p class="mt-1 text-sm text-gray-500">
                Formats acceptés : PDF, JPG, PNG. Taille maximale : 5MB par fichier
              </p>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-2">
            <div class="transform transition-all duration-300 hover:scale-105">
              <label for="password" class="block text-sm font-medium text-gray-700">
                Mot de passe
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <input 
                  id="password" 
                  name="password" 
                  :type="showPassword ? 'text' : 'password'" 
                  required 
                  v-model="formData.password"
                  class="appearance-none block w-full pl-3 pr-10 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-colors duration-200"
                />
                <button 
                  type="button" 
                  @click="togglePasswordVisibility('password')"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500 focus:outline-none"
                  :aria-label="showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                >
                  <svg v-if="!showPassword" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="transform transition-all duration-300 hover:scale-105">
              <label for="password_confirmation" class="block text-sm font-medium text-gray-700">
                Confirmer le mot de passe
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <input 
                  id="password_confirmation" 
                  name="password_confirmation" 
                  :type="showConfirmPassword ? 'text' : 'password'" 
                  required 
                  v-model="formData.password_confirmation"
                  class="appearance-none block w-full pl-3 pr-10 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 sm:text-sm transition-colors duration-200"
                />
                <button 
                  type="button" 
                  @click="togglePasswordVisibility('confirm')"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500 focus:outline-none"
                  :aria-label="showConfirmPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
                >
                  <svg v-if="!showConfirmPassword" class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                    <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                  </svg>
                  <svg v-else class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M3.707 2.293a1 1 0 00-1.414 1.414l14 14a1 1 0 001.414-1.414l-1.473-1.473A10.014 10.014 0 0019.542 10C18.268 5.943 14.478 3 10 3a9.958 9.958 0 00-4.512 1.074l-1.78-1.781zm4.261 4.26l1.514 1.515a2.003 2.003 0 012.45 2.45l1.514 1.514a4 4 0 00-5.478-5.478z" clip-rule="evenodd" />
                    <path d="M12.454 16.697L9.75 13.992a4 4 0 01-3.742-3.741L2.335 6.578A9.98 9.98 0 00.458 10c1.274 4.057 5.065 7 9.542 7 .847 0 1.669-.105 2.454-.303z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <div class="flex items-center mb-6">
            <input 
              id="terms" 
              name="terms" 
              type="checkbox" 
              required 
              v-model="formData.terms"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
            />
            <label for="terms" class="ml-2 block text-sm text-gray-900">
              J'accepte les <a href="#" class="text-primary-600 hover:text-primary-500">conditions d'utilisation</a> et la <a href="#" class="text-primary-600 hover:text-primary-500">politique de confidentialité</a>
            </label>
          </div>

          <div class="flex flex-col items-center space-y-4">
            <button 
              type="submit" 
              class="w-full sm:w-auto px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transform transition-all duration-300 hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="loading"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline-block" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ loading ? 'Inscription en cours...' : 'S\'inscrire' }}</span>
            </button>
          
            <div class="text-center mt-4">
            <p class="text-sm text-gray-600">
              Vous avez déjà un compte?
              <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500 transition-colors duration-200">
                Connectez-vous
              </router-link>
            </p>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'RegisterView',
  setup() {
    const store = useStore()
    const router = useRouter()
    const errorMessage = ref('')
    const showPassword = ref(false)
    const showConfirmPassword = ref(false)
    
    const formData = reactive({
      email: '',
      password: '',
      password_confirmation: '',
      first_name: '',
      last_name: '',
      role: '',
      specialist_type: '',
      phone: '',
      hopital: '',
      region: '',
      numero_licence: '',
      date_licence: '',
      documents: [],
      terms: false
    })
    
    const loading = computed(() => store.getters['auth/loading'])
    const error = computed(() => store.getters['auth/error'])
    const success = computed(() => store.getters['auth/success'])
    
    const handleRoleChange = () => {
      // Réinitialiser la spécialité si le rôle n'est pas spécialiste
      if (formData.role !== 'specialist') {
        formData.specialist_type = ''
      }
    }
    
    const handleFileUpload = (event) => {
      const files = event.target.files
      const maxSize = 5 * 1024 * 1024 // 5MB
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png']
      
      for (let file of files) {
        if (file.size > maxSize) {
          errorMessage.value = `Le fichier ${file.name} dépasse la taille maximale de 5MB`
          return
        }
        if (!allowedTypes.includes(file.type)) {
          errorMessage.value = `Le fichier ${file.name} n'est pas dans un format accepté`
          return
        }
      }
      
      formData.documents = Array.from(files)
      errorMessage.value = ''
    }
    
    const handleRegister = async () => {
      try {
        errorMessage.value = ''
        
        // Validation des données
        if (formData.password !== formData.password_confirmation) {
          errorMessage.value = 'Les mots de passe ne correspondent pas'
          return
        }

        // Création du FormData pour l'envoi des fichiers
        const formDataToSend = new FormData()
        
        // Ajout des champs de base
        formDataToSend.append('email', formData.email)
        formDataToSend.append('password', formData.password)
        formDataToSend.append('password_confirmation', formData.password_confirmation)
        formDataToSend.append('first_name', formData.first_name)
        formDataToSend.append('last_name', formData.last_name)
        formDataToSend.append('role', formData.role)
        formDataToSend.append('phone', formData.phone)
        formDataToSend.append('hopital', formData.hopital)
        formDataToSend.append('region', formData.region)
        formDataToSend.append('numero_licence', formData.numero_licence)
        formDataToSend.append('date_licence', formData.date_licence)
        formDataToSend.append('terms', formData.terms)

        // Ajout de la spécialité si le rôle est spécialiste
        if (formData.role === 'specialist' && formData.specialist_type) {
          formDataToSend.append('specialist_type', formData.specialist_type)
        }

        // Ajout des documents
        if (formData.documents && formData.documents.length > 0) {
            formData.documents.forEach(file => {
              formDataToSend.append('documents', file)
            })
          }

        // Envoi de la requête
        const response = await fetch('http://localhost:8000/api/auth/register/', {
          method: 'POST',
          body: formDataToSend,
          headers: {
            'Accept': 'application/json',
            'Origin': window.location.origin
          },
          credentials: 'include'
        })

        const data = await response.json()

        if (!response.ok) {
          // Gestion détaillée des erreurs
          if (data.detail) {
            throw new Error(data.detail)
          } else if (typeof data === 'object') {
            // Si les erreurs sont dans un format de validation Django
            const errorMessages = Object.entries(data)
              .map(([field, messages]) => `${field}: ${Array.isArray(messages) ? messages.join(', ') : messages}`)
              .join('\n')
            throw new Error(errorMessages)
          } else {
            throw new Error('Une erreur est survenue lors de l\'inscription')
          }
        }

        // Rediriger vers la page de succès
        router.push({
          name: 'RegistrationSuccess',
          params: { email: formData.email }
        })
      } catch (error) {
        console.error('Registration error:', error)
        errorMessage.value = error.message
      }
    }
    
    return {
      formData,
      loading,
      error,
      success,
      handleRegister,
      handleRoleChange,
      handleFileUpload,
      showPassword,
      showConfirmPassword,
      togglePasswordVisibility: (field) => {
        if (field === 'password') {
          showPassword.value = !showPassword.value
        } else if (field === 'confirm') {
          showConfirmPassword.value = !showConfirmPassword.value
        }
      }
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.transform {
  transition: transform 0.3s ease;
}

.transform:hover {
  transform: scale(1.02);
}

/* Styles pour le bouton */
button[type="submit"] {
  min-width: 200px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
  border-radius: 0.375rem;
  background-color: #4F46E5;
  color: white;
  transition: all 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #4338CA;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

button[type="submit"]:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

@media (max-width: 640px) {
  button[type="submit"] {
    width: 100%;
  }
}
</style>