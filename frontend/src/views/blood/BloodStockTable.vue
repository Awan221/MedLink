<template>
  <div class="blood-stock-table">
    <h2>Disponibilité des Produits Sanguins</h2>
    <div class="pagination-info" v-if="totalItems > 0">
      Affichage de {{ startItem }}-{{ endItem }} sur {{ totalItems }} entrées
    </div>
    <div class="pagination-info" v-if="totalItems > 0">
      Affichage de {{ startItem }}-{{ endItem }} sur {{ totalItems }} entrées
    </div>
    <div class="filters">
      <label>Groupe sanguin :
        <select v-model="selectedGroup">
          <option value="">Tous</option>
          <option v-for="group in bloodGroups" :key="group" :value="group">{{ group }}</option>
        </select>
      </label>
      <label>Localité :
        <input v-model="searchLocation" placeholder="Rechercher une ville ou un centre" />
      </label>
      <button @click="fetchStocks">Actualiser</button>
    </div>
    <table>
      <thead>
        <tr>
          <th>Centre</th>
          <th>Ville</th>
          <th>Groupe sanguin</th>
          <th>Quantité (ml)</th>
          <th>Dernière mise à jour</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="stock in filteredStocks" :key="stock.id">
          <td>{{ stock.center_name }}</td>
          <td>{{ stock.center_city || 'Non spécifiée' }}</td>
          <td>{{ stock.blood_type }}</td>
          <td :class="{'low': stock.quantity_ml < stock.minimum_required_ml}">
            {{ stock.quantity_ml }} ml
            <span v-if="stock.quantity_ml < stock.minimum_required_ml" class="status-warning"> (Faible)</span>
          </td>
          <td>{{ formatDate(stock.last_updated) }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="error" class="error">{{ error }}</p>
    
    <div class="pagination-controls" v-if="totalPages > 1">
      <button 
        @click="changePage(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="pagination-button"
      >
        Précédent
      </button>
      
      <span class="page-number">
        Page {{ currentPage }} sur {{ totalPages }}
      </span>
      
      <button 
        @click="changePage(currentPage + 1)" 
        :disabled="currentPage === totalPages"
        class="pagination-button"
      >
        Suivant
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'BloodStockTable',
  data() {
    return {
      stocks: [],
      bloodGroups: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'],
      selectedGroup: '',
      searchLocation: '',
      error: '',
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: 10
    };
  },
  computed: {
    filteredStocks() {
      let filtered = this.stocks;
      if (this.selectedGroup) {
        filtered = filtered.filter(s => s.blood_type === this.selectedGroup);
      }
      if (this.searchLocation) {
        const search = this.searchLocation.toLowerCase();
        filtered = filtered.filter(s =>
          (s.center_name && s.center_name.toLowerCase().includes(search)) ||
          (s.center_city && s.center_city.toLowerCase().includes(search))
        );
      }
      return filtered.sort((a, b) => a.blood_type.localeCompare(b.blood_type));
    },
    startItem() {
      return ((this.currentPage - 1) * this.itemsPerPage) + 1;
    },
    endItem() {
      return Math.min(this.currentPage * this.itemsPerPage, this.totalItems);
    },
  },
  created() {
    this.fetchStocks(1);
  },
  methods: {
    changePage(page) {
      if (page >= 1 && page <= this.totalPages) {
        this.fetchStocks(page);
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    },
    async fetchStocks(page = 1) {
      this.error = '';
      this.currentPage = page;
      try {
        const res = await axios.get(`/blood-bank/inventory/?page=${page}`);
        this.stocks = res.data.results || [];
        this.totalItems = res.data.count || this.stocks.length;
        this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
        
        this.stocks = this.stocks.map(s => ({
          ...s,
          center_name: s.center_name || s.center?.name || 'Centre inconnu',
          center_city: s.center_city || s.center?.city || 'Ville inconnue',
        }));
      } catch (e) {
        console.error('Error fetching blood inventory:', e);
        this.error = "Impossible de charger les stocks.";
      }
    },
    formatDate(dt) {
      if (!dt) return '';
      const date = new Date(dt);
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
.blood-stock-table {
  max-width: 900px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  padding: 2rem;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}
th, td {
  border: 1px solid #eee;
  padding: 0.75rem;
  text-align: left;
}
th {
  background: #f7f7f7;
}
.low {
  color: #d32f2f;
  font-weight: bold;
}
.status-warning {
  color: #ff9800;
  font-size: 0.9em;
}
.filters {
  display: flex;
  gap: 2rem;
  align-items: center;
  margin-bottom: 1rem;
}
label {
  font-weight: bold;
}
input, select {
  margin-left: 0.5rem;
  padding: 0.3rem 0.7rem;
  border-radius: 4px;
  border: 1px solid #eee;
}
.error {
  color: #d32f2f;
  margin: 1rem 0;
  text-align: center;
}

.pagination-info {
  text-align: right;
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.9em;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.pagination-button {
  padding: 0.5rem 1rem;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #e0e0e0;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-number {
  font-weight: 500;
  min-width: 100px;
  text-align: center;
}
</style>
