import axios from 'axios';

const state = {
  users: [],
  loading: false,
  error: null,
};

const getters = {
  allUsers: (state) => state.users,
  usersLoading: (state) => state.loading,
  usersError: (state) => state.error,
};

const actions = {
  // Cette action doit être réservée à l'admin pour la gestion des utilisateurs (liste complète),
  // ne pas l'utiliser pour récupérer le user connecté (utiliser /api/auth/me/ côté auth.js)
  async fetchUsers({ commit }) {
    commit('setLoading', true);
    try {
      const apiUrl = process.env.VUE_APP_API_URL;
      const response = await axios.get(`${apiUrl}auth/users/`);
      commit('setUsers', response.data);
    } catch (error) {
      commit('setError', error);
    } finally {
      commit('setLoading', false);
    }
  },
  async updateUser({ commit }, { id, data }) {
    commit('setLoading', true);
    try {
      const apiUrl = process.env.VUE_APP_API_URL;
      const response = await axios.patch(`${apiUrl}auth/users/${id}/`, data);
      commit('updateUserInList', response.data);
    } catch (error) {
      commit('setError', error);
    } finally {
      commit('setLoading', false);
    }
  },
  async updateUserRole({ commit }, { id, data }) {
    commit('setLoading', true);
    try {
      const apiUrl = process.env.VUE_APP_API_URL;
      const response = await axios.patch(`${apiUrl}auth/users/${id}/roles/`, data);
      commit('updateUserInList', response.data);
    } catch (error) {
      commit('setError', error);
    } finally {
      commit('setLoading', false);
    }
  },
};

const mutations = {
  setUsers(state, users) {
    state.users = Array.isArray(users) ? users : (users && Array.isArray(users.results) ? users.results : []);
  },
  updateUserInList(state, updatedUser) {
    const idx = state.users.findIndex(u => u.id === updatedUser.id);
    if (idx !== -1) {
      state.users.splice(idx, 1, updatedUser);
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
