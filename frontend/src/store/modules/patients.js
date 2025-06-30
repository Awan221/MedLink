import axios from 'axios';

const state = {
  patients: [],
  patient: null,
  loading: false,
  error: null,
};

const getters = {
  allPatients: (state) => state.patients,
  patient: (state) => state.patient,
  patientsLoading: (state) => state.loading,
  patientsError: (state) => state.error,
};

const actions = {
  async fetchPatients({ commit }, search = '') {
    commit('setLoading', true);
    commit('setError', null);
    
    if (!process.env.VUE_APP_API_URL) {
      commit('setError', 'URL API non configurée');
      commit('setPatients', []);
      return [];
    }
    
    let url = `${process.env.VUE_APP_API_URL}patients/`;
    if (search) {
      url += `?search=${encodeURIComponent(search)}`;
    }
    
    try {
      const response = await axios.get(url, {
        headers: { 
          'Authorization': `Bearer ${localStorage.getItem('access')}`,
          'Content-Type': 'application/json'
        },
        validateStatus: status => status >= 200 && status < 500
      });
      
      if (response.status === 404) {
        commit('setPatients', []);
        return [];
      }
      
      // Gérer le format de réponse de Django REST Framework
      const patientsData = response.data.results || response.data;
      if (!Array.isArray(patientsData)) {
        commit('setError', 'Format de réponse invalide');
        commit('setPatients', []);
        return [];
      }
      
      commit('setPatients', patientsData);
      return patientsData;
    } catch (error) {
      console.error('Erreur lors de la recherche des patients:', error);
      
      // Gérer spécifiquement les erreurs 500
      if (error.response?.status === 500) {
        commit('setError', 'Une erreur est survenue côté serveur');
      } else {
        commit('setError', error.response?.data?.detail || error.message || 'Erreur lors de la recherche');
      }
      
      commit('setPatients', []);
      return [];
    } finally {
      commit('setLoading', false);
    }
  },
  async fetchPatient({ commit }, id) {
    commit('setLoading', true);
    commit('setError', null);
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}patients/${id}/`, {
        headers: { 
          'Authorization': `Bearer ${localStorage.getItem('access')}`,
          'Content-Type': 'application/json'
        },
        validateStatus: status => status >= 200 && status < 500
      });
      
      if (response.status === 404) {
        throw new Error('Patient non trouvé');
      } else if (response.status === 403) {
        throw new Error('Vous n\'avez pas les droits pour accéder à ce patient');
      } else if (response.status !== 200) {
        throw new Error('Erreur lors du chargement du patient');
      }
      
      commit('setPatient', response.data);
      return response.data;
    } catch (error) {
      console.error('Erreur fetchPatient:', error);
      commit('setError', error.response?.data?.detail || error.message || 'Erreur inconnue');
      commit('setPatient', null);
      throw error; // Propager l'erreur pour la gérer dans le composant
    } finally {
      commit('setLoading', false);
    }
  },
  async createPatient({ commit }, data) {
    commit('setLoading', true);
    try {
      // Génération d'un identifiant médical unique côté frontend (UUID ou timestamp)
      if (!data.medical_id) {
        data.medical_id = 'MED-' + Date.now() + '-' + Math.floor(Math.random() * 10000);
      }
      const response = await axios.post(`${process.env.VUE_APP_API_URL}patients/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('addPatient', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async updatePatient({ commit }, { id, data }) {
    commit('setLoading', true);
    try {
      const response = await axios.patch(`${process.env.VUE_APP_API_URL}patients/${id}/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('updatePatientInList', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async deletePatient({ commit }, id) {
    commit('setLoading', true);
    try {
      await axios.delete(`${process.env.VUE_APP_API_URL}patients/${id}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('removePatient', id);
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  clearPatientError({ commit }) {
    commit('setError', null);
  },
};

const mutations = {
  setPatients(state, patients) {
    // Toujours garantir un tableau
    state.patients = Array.isArray(patients)
      ? patients
      : (patients && Array.isArray(patients.results) ? patients.results : []);
  },
  setPatient(state, patient) {
    state.patient = patient;
  },
  addPatient(state, patient) {
    state.patients.unshift(patient);
  },
  updatePatientInList(state, updatedPatient) {
    const idx = state.patients.findIndex(p => p.id === updatedPatient.id);
    if (idx !== -1) {
      state.patients.splice(idx, 1, updatedPatient);
    }
    if (state.patient && state.patient.id === updatedPatient.id) {
      state.patient = updatedPatient;
    }
  },
  removePatient(state, id) {
    state.patients = state.patients.filter(p => p.id !== id);
    if (state.patient && state.patient.id === id) {
      state.patient = null;
    }
  },
  setLoading(state, loading) {
    state.loading = loading;
  },
  setError(state, error) {
    state.error = error;
  },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
