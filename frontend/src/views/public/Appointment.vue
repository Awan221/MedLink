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
        <label class="block mb-1 font-semibold">Email (optionnel)</label>
        <input v-model="form.email" type="email" class="w-full border rounded px-3 py-2" placeholder="votre@email.com">
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Date souhaitée</label>
        <input v-model="form.date" type="date" class="w-full border rounded px-3 py-2" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Motif de consultation</label>
        <textarea v-model="form.reason" class="w-full border rounded px-3 py-2" rows="3" placeholder="Décrivez brièvement le motif de votre consultation..." required></textarea>
      </div>
      <button type="submit" class="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700">Demander un rendez-vous</button>
      <div v-if="success" class="mt-4 p-3 bg-green-100 text-green-800 rounded">Votre demande de rendez-vous a bien été enregistrée! Nous vous contacterons pour confirmer.</div>
      <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-800 rounded">Erreur lors de la demande. Merci de vérifier vos informations ou réessayer plus tard.</div>
    </form>
    
    <div class="mt-8 max-w-lg mx-auto">
      <h2 class="text-xl font-bold mb-4">Informations importantes</h2>
      <div class="space-y-4">
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Horaires de consultation</h3>
          <p>Du lundi au vendredi : 8h - 19h<br>
          Samedi : 8h - 12h</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Documents à apporter</h3>
          <ul class="list-disc list-inside">
            <li>Carte vitale</li>
            <li>Carte d'identité</li>
            <li>Ordonnances récentes</li>
            <li>Résultats d'analyses</li>
          </ul>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Annulation</h3>
          <p>Pour annuler ou reporter votre rendez-vous, merci de nous contacter au moins 24h à l'avance.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';

defineOptions({
  name: 'PublicAppointmentView'
});

const { proxy } = getCurrentInstance();
const form = ref({
  name: '',
  phone: '',
  email: '',
  date: '',
  reason: ''
});
const success = ref(false);
const error = ref(false);

async function submitForm() {
  success.value = false;
  error.value = false;
  try {
    const response = await fetch('http://localhost:8000/api/public/appointments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Erreur lors de la demande de rendez-vous');
    }
    
    proxy.$toast.success('Demande de rendez-vous enregistrée avec succès !', {
      position: 'top-right',
      timeout: 5000
    });
    
    form.value = { name: '', phone: '', email: '', date: '', reason: '' };
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