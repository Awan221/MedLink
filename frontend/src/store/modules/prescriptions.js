import axios from 'axios';

const state = {
  prescriptions: [],
  loading: false,
  error: null,
};

const getters = {
  allPrescriptions: (state) => state.prescriptions,
  prescriptionsLoading: (state) => state.loading,
  prescriptionsError: (state) => state.error,
};

const actions = {
  async fetchPrescriptions({ commit }, patientId) {
    commit('setLoading', true);
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}patients/${patientId}/prescriptions/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('setPrescriptions', response.data);
    } catch (error) {
      commit('setError', error);
      commit('setPrescriptions', []);
    } finally {
      commit('setLoading', false);
    }
  },
  async createPrescription({ commit }, { patientId, data }) {
    commit('setLoading', true);
    try {
      const response = await axios.post(`${process.env.VUE_APP_API_URL}patients/${patientId}/prescriptions/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('addPrescription', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async updatePrescription({ commit }, { patientId, prescriptionId, data }) {
    commit('setLoading', true);
    try {
      const response = await axios.patch(`${process.env.VUE_APP_API_URL}patients/${patientId}/prescriptions/${prescriptionId}/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('updatePrescriptionInList', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async deletePrescription({ commit }, { patientId, prescriptionId }) {
    commit('setLoading', true);
    try {
      await axios.delete(`${process.env.VUE_APP_API_URL}patients/${patientId}/prescriptions/${prescriptionId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('removePrescription', prescriptionId);
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  clearPrescriptionsError({ commit }) {
    commit('setError', null);
  },
};

const mutations = {
  setPrescriptions(state, prescriptions) {
    state.prescriptions = prescriptions;
  },
  addPrescription(state, prescription) {
    state.prescriptions.unshift(prescription);
  },
  updatePrescriptionInList(state, updatedPrescription) {
    const idx = state.prescriptions.findIndex(p => p.id === updatedPrescription.id);
    if (idx !== -1) {
      state.prescriptions.splice(idx, 1, updatedPrescription);
    }
  },
  removePrescription(state, id) {
    state.prescriptions = state.prescriptions.filter(p => p.id !== id);
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
