import imagingApi from '@/api/imaging';

const state = {
  studies: [],
  currentStudy: null,
  studySeries: [],
  loading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    page: 1,
    pageSize: 10,
    totalPages: 1
  }
};

const getters = {
  allStudies: state => state.studies,
  currentStudy: state => state.currentStudy,
  studySeries: state => state.studySeries,
  loading: state => state.loading,
  error: state => state.error,
  pagination: state => state.pagination
};

const actions = {
  /**
   * Récupère les études DICOM d'un patient
   */
  async fetchPatientStudies({ commit }, { patientId, page = 1, pageSize = 10 } = {}) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.getPatientStudies(patientId, { 
        page, 
        page_size: pageSize 
      });
      
      commit('setStudies', response.data.results);
      commit('setPagination', {
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        page: page,
        pageSize: pageSize,
        totalPages: Math.ceil(response.data.count / pageSize)
      });
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de la récupération des examens');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Récupère les détails d'une étude DICOM (alias de fetchStudyDetails pour compatibilité)
   */
  async fetchStudy({ dispatch }, studyId) {
    try {
      const response = await dispatch('fetchStudyDetails', studyId);
      return { data: response?.data || {} };
    } catch (error) {
      console.error('Error in fetchStudy:', error);
      throw error;
    }
  },

  /**
   * Récupère les détails d'une étude DICOM
   */
  async fetchStudyDetails({ commit }, studyId) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.getStudyDetails(studyId);
      const studyData = response?.data || {};
      commit('setCurrentStudy', studyData);
      return { 
        data: studyData,
        success: true 
      };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Erreur lors de la récupération des détails de l\'examen';
      commit('setError', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Récupère les séries d'une étude DICOM
   */
  async fetchStudySeries({ commit }, studyId) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.getStudySeries(studyId);
      commit('setStudySeries', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de la récupération des séries');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Crée une nouvelle étude DICOM
   */
  async createStudy({ commit }, studyData) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.createStudy(studyData);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de la création de l\'examen');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Met à jour une étude DICOM existante
   */
  async updateStudy({ commit }, { studyId, updates }) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.updateStudy(studyId, updates);
      commit('updateStudyInList', response.data);
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de la mise à jour de l\'examen');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Supprime une étude DICOM
   */
  async deleteStudy({ commit }, studyId) {
    commit('setLoading', true);
    try {
      await imagingApi.deleteStudy(studyId);
      commit('removeStudyFromList', studyId);
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de la suppression de l\'examen');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Télécharge un fichier DICOM vers une étude existante
   */
  async uploadDicomFile({ commit }, { studyId, file, onUploadProgress }) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.uploadDicomFile(studyId, file, {
        onUploadProgress,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors de l\'upload du fichier DICOM');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Réinitialise l'état d'erreur
   */
  clearError({ commit }) {
    commit('setError', null);
  },

  /**
   * Télécharge une étude DICOM complète
   */
  async downloadStudy({ commit }, { studyId, fileName }) {
    commit('setLoading', true);
    try {
      const response = await imagingApi.downloadStudy(studyId, { responseType: 'blob' });
      
      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName || `etude-${studyId}.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      return true;
    } catch (error) {
      commit('setError', error.response?.data?.message || 'Erreur lors du téléchargement de l\'examen');
      throw error;
    } finally {
      commit('setLoading', false);
    }
  },

  /**
   * Réinitialise l'état du module
   */
  resetState({ commit }) {
    commit('resetState');
  }
};

const mutations = {
  setLoading(state, isLoading) {
    state.loading = isLoading;
  },

  setError(state, error) {
    state.error = error;
  },

  setStudies(state, studies) {
    state.studies = studies;
  },

  setCurrentStudy(state, study) {
    state.currentStudy = study;
  },
  
  // Alias pour setCurrentStudy pour la compatibilité
  setStudy(state, study) {
    state.currentStudy = study;
  },

  setStudySeries(state, series) {
    state.studySeries = series;
  },

  setPagination(state, pagination) {
    state.pagination = { ...state.pagination, ...pagination };
  },

  addStudyToList(state, study) {
    state.studies.unshift(study);
  },

  updateStudyInList(state, updatedStudy) {
    const index = state.studies.findIndex(s => s.id === updatedStudy.id);
    if (index !== -1) {
      state.studies.splice(index, 1, updatedStudy);
    }
  },

  removeStudyFromList(state, studyId) {
    state.studies = state.studies.filter(study => study.id !== studyId);
  },

  resetState(state) {
    state.studies = [];
    state.currentStudy = null;
    state.studySeries = [];
    state.loading = false;
    state.error = null;
    state.pagination = {
      count: 0,
      next: null,
      previous: null,
      page: 1,
      pageSize: 10,
      totalPages: 1
    };
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};