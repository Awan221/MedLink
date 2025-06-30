<template>
  <div class="public-page">
    <h1 class="text-2xl font-bold mb-4">Contactez-nous</h1>
    <form class="max-w-lg mx-auto bg-white p-6 rounded shadow" @submit.prevent="submitForm">
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Nom complet</label>
        <input v-model="form.name" type="text" class="w-full border rounded px-3 py-2" placeholder="Votre nom et prénom" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Email</label>
        <input v-model="form.email" type="email" class="w-full border rounded px-3 py-2" placeholder="votre@email.com" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Téléphone</label>
        <input v-model="form.phone" type="tel" class="w-full border rounded px-3 py-2" placeholder="06 00 00 00 00" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Sujet</label>
        <input v-model="form.subject" type="text" class="w-full border rounded px-3 py-2" placeholder="Sujet de votre message" required>
      </div>
      <div class="mb-4">
        <label class="block mb-1 font-semibold">Message</label>
        <textarea v-model="form.message" class="w-full border rounded px-3 py-2" rows="5" placeholder="Votre message..." required></textarea>
      </div>
      <button type="submit" class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">Envoyer le message</button>
      <div v-if="success" class="mt-4 p-3 bg-green-100 text-green-800 rounded">Votre message a bien été envoyé! Nous vous répondrons dans les plus brefs délais.</div>
      <div v-if="error" class="mt-4 p-3 bg-red-100 text-red-800 rounded">Erreur lors de l'envoi. Merci de vérifier vos informations ou réessayer plus tard.</div>
    </form>
    
    <div class="mt-8 max-w-lg mx-auto">
      <h2 class="text-xl font-bold mb-4">FAQ</h2>
      <div class="space-y-4">
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Comment prendre rendez-vous ?</h3>
          <p>Vous pouvez prendre rendez-vous en ligne via notre formulaire de prise de rendez-vous, ou en nous appelant directement.</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Quels sont les critères pour donner son sang ?</h3>
          <p>Pour donner votre sang, vous devez être âgé de 18 à 70 ans, peser plus de 50 kg et être en bonne santé. Un questionnaire médical sera rempli lors de votre don.</p>
        </div>
        <div class="bg-white p-4 rounded shadow">
          <h3 class="font-semibold mb-2">Comment accéder à mes résultats d'analyses ?</h3>
          <p>Vous pouvez accéder à vos résultats d'analyses via votre espace patient après vous être connecté avec vos identifiants.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';

defineOptions({
  name: 'PublicContactView'
});

const { proxy } = getCurrentInstance();
const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
});
const success = ref(false);
const error = ref(false);

async function submitForm() {
  success.value = false;
  error.value = false;
  try {
    const response = await fetch('http://localhost:8000/api/public/contact/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(form.value)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Erreur lors de l\'envoi du message');
    }
    
    proxy.$toast.success('Message envoyé avec succès !', {
      position: 'top-right',
      timeout: 5000
    });
    
    form.value = { name: '', email: '', phone: '', subject: '', message: '' };
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
