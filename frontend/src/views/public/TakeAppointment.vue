<template>
  <div class="public-page">
    <h1 class="text-2xl font-bold mb-4">Prendre rendez-vous</h1>
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
        <label class="block mb-1 font-semibold">Date souhaitée</label>
        <input v-model="form.date" type="date" class="w-full border rounded px-3 py-2" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Motif</label>
        <textarea v-model="form.reason" class="w-full border rounded px-3 py-2" placeholder="Ex : consultation, don, examen..." required></textarea>
      </div>
      <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">Envoyer la demande</button>
      <div v-if="success" class="mt-4 p-3 bg-green-100 text-green-800 rounded">Votre demande a bien été envoyée! Nous vous contacterons rapidement.</div>
      <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-800 rounded">Erreur lors de l'envoi. Merci de vérifier vos informations ou réessayer plus tard.</div>
    </form>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';

defineOptions({
  name: 'PublicTakeAppointmentView'
});

const { proxy } = getCurrentInstance();
const form = ref({
  name: '',
  phone: '',
  date: '',
  reason: ''
});
const success = ref(false);
const error = ref(false);

async function submitForm() {
  success.value = false;
  error.value = false;
  try {
    // À remplacer par l'appel API réel
    const response = await fetch('http://localhost:8000/api/public/appointments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Erreur lors de la prise de rendez-vous');
    }
    
    proxy.$toast.success('Rendez-vous enregistré avec succès !', {
      position: 'top-right',
      timeout: 5000
    });
    
    form.value = { name: '', phone: '', date: '', reason: '' };
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
