import axios from 'axios';

const state = {
  appointments: [],
  loading: false,
  error: null,
};

const getters = {
  allAppointments: (state) => state.appointments,
  appointmentsLoading: (state) => state.loading,
  appointmentsError: (state) => state.error,
};

const actions = {
  async fetchAppointments({ commit }) {
    commit('setLoading', true);
    try {
      const response = await axios.get('/api/patients/appointments/');
      commit('setAppointments', response.data);
    } catch (error) {
      commit('setError', error);
    } finally {
      commit('setLoading', false);
    }
  },
};

const mutations = {
  setAppointments(state, appointments) {
    state.appointments = appointments;
    state.error = null;
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
