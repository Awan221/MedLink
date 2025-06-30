<template>
  <div class="blood-stock-form">
    <h2>Saisie des Stocks de Sang</h2>
    <form @submit.prevent="submitStock">
      <div class="form-group">
        <label for="center">Centre de Banque de Sang</label>
        <select v-model="form.center" required>
          <option value="" disabled>Sélectionnez un centre</option>
          <option v-for="center in centers" :key="center.id" :value="center.id">
            {{ center.name }} ({{ center.region }})
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="blood_group">Groupe Sanguin</label>
        <select v-model="form.blood_group" required>
          <option v-for="group in bloodGroups" :key="group" :value="group">{{ group }}</option>
        </select>
      </div>
      <div class="form-group">
        <label for="units">Unités Disponibles</label>
        <input type="number" v-model.number="form.units_available" min="0" required />
      </div>
      <button type="submit">Enregistrer</button>
      <p v-if="success" class="success">Stock enregistré avec succès !</p>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BloodStockForm',
  data() {
    return {
      form: {
        center: '',
        blood_group: '',
        units_available: 0,
      },
      centers: [],
      bloodGroups: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
      success: false,
      error: '',
    };
  },
  created() {
    this.fetchCenters();
  },
  methods: {
    async fetchCenters() {
      try {
        const res = await axios.get('/blood-bank/centers/');
        // Gérer la réponse paginée (results contient le tableau des centres)
        const centersData = res.data.results || [];
        this.centers = centersData.filter(center => center && center.id);
        
        if (this.centers.length === 0) {
          this.error = "Aucun centre de don de sang trouvé";
        }
      } catch (e) {
        console.error('Erreur lors du chargement des centres:', e);
        this.error = `Impossible de charger les centres: ${e.response?.data?.detail || e.message}`;
      }
    },
    async submitStock() {
      this.error = '';
      this.success = false;
      try {
        await axios.post('/api/blood-bank/inventory/', {
          center: this.form.center,
          blood_type: this.form.blood_group,
          quantity_ml: this.form.units_available * 450, // Convertir en ml (1 unité = ~450ml)
        });
        this.success = true;
        this.form.units_available = 0;
      } catch (e) {
        this.error = e.response?.data?.detail || "Erreur lors de l'enregistrement.";
      }
    },
  },
};
</script>

<style scoped>
.blood-stock-form {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input, select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #eee;
  border-radius: 4px;
}
button {
  background: #d32f2f;
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}
.success {
  color: #388e3c;
  margin-top: 1rem;
}
.error {
  color: #d32f2f;
  margin-top: 1rem;
}
</style>
