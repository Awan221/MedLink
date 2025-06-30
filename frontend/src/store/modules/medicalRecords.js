import axios from 'axios';

const state = {
  records: [],
  loading: false,
  error: null,
};

const getters = {
  allMedicalRecords: (state) => state.records,
  medicalRecordsLoading: (state) => state.loading,
  medicalRecordsError: (state) => state.error,
};

const actions = {
  async fetchMedicalRecords({ commit }, patientId) {
    commit('setLoading', true);
    try {
      const response = await axios.get(`${process.env.VUE_APP_API_URL}patients/${patientId}/medical-records/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('setRecords', response.data);
    } catch (error) {
      commit('setError', error);
      commit('setRecords', []);
    } finally {
      commit('setLoading', false);
    }
  },
  async createMedicalRecord({ commit }, { patientId, data }) {
    commit('setLoading', true);
    try {
      const response = await axios.post(`${process.env.VUE_APP_API_URL}patients/${patientId}/medical-records/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('addRecord', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async updateMedicalRecord({ commit }, { patientId, recordId, data }) {
    commit('setLoading', true);
    try {
      const response = await axios.patch(`${process.env.VUE_APP_API_URL}patients/${patientId}/medical-records/${recordId}/`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('updateRecordInList', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  async deleteMedicalRecord({ commit }, { patientId, recordId }) {
    commit('setLoading', true);
    try {
      await axios.delete(`${process.env.VUE_APP_API_URL}patients/${patientId}/medical-records/${recordId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('access')}` }
      });
      commit('removeRecord', recordId);
    } catch (error) {
      commit('setError', error);
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },
  clearMedicalRecordsError({ commit }) {
    commit('setError', null);
  },
};

const mutations = {
  setRecords(state, records) {
    state.records = records;
  },
  addRecord(state, record) {
    state.records.unshift(record);
  },
  updateRecordInList(state, updatedRecord) {
    const idx = state.records.findIndex(r => r.id === updatedRecord.id);
    if (idx !== -1) {
      state.records.splice(idx, 1, updatedRecord);
    }
  },
  removeRecord(state, id) {
    state.records = state.records.filter(r => r.id !== id);
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
