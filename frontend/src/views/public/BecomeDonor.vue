<template>
  <div class="public-page">
    <h1 class="text-2xl font-bold mb-4">Devenir donneur de sang</h1>
    <form class="max-w-lg mx-auto bg-white p-6 rounded shadow" @submit.prevent="submitForm">
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Nom complet</label>
        <input v-model="form.name" type="text" class="w-full border rounded px-3 py-2" placeholder="Votre nom et prénom" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Téléphone</label>
        <input v-model="form.phone" type="tel" class="w-full border rounded px-3 py-2" placeholder="06 00 00 00 00" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Email (optionnel)</label>
        <input v-model="form.email" type="email" class="w-full border rounded px-3 py-2" placeholder="votre@email.com">
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Groupe sanguin</label>
        <select v-model="form.blood_group" class="w-full border rounded px-3 py-2" required>
          <option value="">Sélectionnez votre groupe sanguin</option>
          <option value="A+">A+</option>
          <option value="A-">A-</option>
          <option value="B+">B+</option>
          <option value="B-">B-</option>
          <option value="AB+">AB+</option>
          <option value="AB-">AB-</option>
          <option value="O+">O+</option>
          <option value="O-">O-</option>
        </select>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Région</label>
        <input v-model="form.region" type="text" class="w-full border rounded px-3 py-2" placeholder="Votre région" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Date préférée (optionnel)</label>
        <input v-model="form.preferred_date" type="date" class="w-full border rounded px-3 py-2">
      </div>
      <button type="submit" class="bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700">S'inscrire comme donneur</button>
      <div v-if="success" class="mt-4 p-3 bg-green-100 text-green-800 rounded">Votre inscription a bien été enregistrée! Nous vous contacterons pour confirmer la date.</div>
      <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-800 rounded">Erreur lors de l'inscription. Merci de vérifier vos informations ou réessayer plus tard.</div>
    </form>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';

defineOptions({
  name: 'PublicBecomeDonorView'
});

const { proxy } = getCurrentInstance();
const form = ref({
  name: '',
  phone: '',
  email: '',
  blood_group: '',
  region: '',
  preferred_date: ''
});
const success = ref(false);
const error = ref(false);

async function submitForm() {
  success.value = false;
  error.value = false;
  try {
    const response = await fetch('http://localhost:8000/api/public/donors/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Erreur lors de l\'inscription');
    }
    
    proxy.$toast.success('Inscription enregistrée avec succès !', {
      position: 'top-right',
      timeout: 5000
    });
    
    form.value = { name: '', phone: '', email: '', blood_group: '', region: '', preferred_date: '' };
    success.value = true;
  } catch (err) {
    console.error('Erreur:', err);
    proxy.$toast.error(err.message || 'Une erreur est survenue', {
      position: 'top-right',
      timeout: 5000
    });
    error.value = true;
  }
}
</script>

<style scoped>
.public-page {
  max-width: 800px;
  margin: 2em auto;
  padding: 2em;
}
</style>
