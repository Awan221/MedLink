import api from './base';

const BASE_URL = '/imaging';

export default {
  /**
   * Récupère la liste des études DICOM d'un patient
   * @param {number} patientId - ID du patient
   * @param {Object} params - Paramètres de pagination/filtrage
   * @returns {Promise<Array>} Liste des études DICOM
   */
  getPatientStudies(patientId, params = {}) {
    return api.get(`${BASE_URL}/studies/`, { 
      params: { ...params, patient: patientId } 
    });
  },

  /**
   * Récupère les détails d'une étude DICOM
   * @param {string} studyId - ID de l'étude DICOM
   * @returns {Promise<Object>} Détails de l'étude
   */
  getStudyDetails(studyId) {
    return api.get(`${BASE_URL}/studies/${studyId}/`);
  },

  /**
   * Récupère les séries DICOM d'une étude
   * @param {string} studyId - ID de l'étude DICOM
   * @returns {Promise<Array>} Liste des séries
   */
  getStudySeries(studyId) {
    return api.get(`${BASE_URL}/studies/${studyId}/series/`);
  },

  /**
   * Télécharge une instance DICOM
   * @param {string} seriesId - ID de la série DICOM
   * @param {string} instanceId - ID de l'instance DICOM
   * @returns {Promise<Blob>} Fichier DICOM
   */
  downloadInstance(seriesId, instanceId) {
    return api.get(`${BASE_URL}/series/${seriesId}/instances/${instanceId}/`, {
      responseType: 'blob'
    });
  },

  /**
   * Télécharge une étude DICOM complète au format ZIP
   * @param {string} studyId - ID de l'étude DICOM
   * @param {Object} config - Configuration de la requête
   * @returns {Promise<Blob>} Fichier ZIP contenant l'étude
   */
  downloadStudy(studyId, config = {}) {
    return api.get(`${BASE_URL}/studies/${studyId}/download/`, {
      responseType: 'blob',
      ...config
    });
  },

  /**
   * Crée une nouvelle étude DICOM, avec ou sans fichier attaché
   * @param {Object} studyData - Données de l'étude
   * @param {File} [file=null] - Fichier DICOM à uploader (optionnel)
   * @param {Object} [config={}] - Configuration de l'upload (headers, progression, etc.)
   * @returns {Promise<Object>} Étude créée
   */
  createStudy(studyData, file = null, config = {}) {
    // Si studyData est déjà un FormData, l'utiliser directement
    const formData = studyData instanceof FormData ? studyData : new FormData();
    
    // Si studyData est un objet, ajouter ses propriétés au FormData
    if (!(studyData instanceof FormData) && studyData && typeof studyData === 'object') {
      Object.entries(studyData).forEach(([key, value]) => {
        if (value !== null && value !== undefined) {
          // Si la valeur est un objet ou un tableau, la convertir en JSON
          const valueToAppend = (typeof value === 'object' || Array.isArray(value)) 
            ? JSON.stringify(value) 
            : value;
          formData.append(key, valueToAppend);
        }
      });
    }
    
    // Ajouter le fichier s'il est fourni séparément
    if (file) {
      formData.append('dicom_file', file);
    }
    
    // Afficher le contenu du FormData pour le débogage
    console.log('Envoi des données au serveur:');
    for (let pair of formData.entries()) {
      console.log(pair[0] + ': ', pair[1]);
    }
    
    return api.post(
      `${BASE_URL}/studies/`,
      formData,
      {
        ...config,
        headers: {
          'Content-Type': 'multipart/form-data',
          ...config.headers
        }
      }
    );
  },

  /**
   * Télécharge un fichier DICOM vers une étude existante
   * @param {string} studyId - ID de l'étude cible
   * @param {File} file - Fichier DICOM à uploader
   * @param {Object} config - Configuration de l'upload (headers, progression, etc.)
   * @returns {Promise<Object>} Réponse du serveur
   * @deprecated Utiliser createStudy avec un fichier à la place
   */
  uploadDicomFile(studyId, file, config = {}) {
    console.warn('uploadDicomFile est dépréciée, utilisez createStudy avec un fichier à la place');
    return this.createStudy({}, file, config);
  },

  /**
   * Met à jour les métadonnées d'une étude
   * @param {string} studyId - ID de l'étude
   * @param {Object} updates - Champs à mettre à jour
   * @returns {Promise<Object>} Étude mise à jour
   */
  updateStudy(studyId, updates) {
    return api.patch(`${BASE_URL}/studies/${studyId}/`, updates);
  },

  /**
   * Supprime une étude DICOM
   * @param {string} studyId - ID de l'étude à supprimer
   * @returns {Promise<void>}
   */
  deleteStudy(studyId) {
    return api.delete(`${BASE_URL}/studies/${studyId}/`);
  },

  /**
   * Récupère l'URL du visualiseur DICOM pour une étude
   * @param {string} studyId - ID de l'étude
   * @returns {string} URL du visualiseur
   */
  getViewerUrl(studyId) {
    return `${BASE_URL}/viewer/${studyId}/`;
  },

  /**
   * Récupère le rapport radiologique d'une étude
   * @param {string} studyId - ID de l'étude
   * @returns {Promise<Object>} Données du rapport
   */
  getReport(studyId) {
    return api.get(`${BASE_URL}/studies/${studyId}/report/`);
  },

  /**
   * Crée ou met à jour un rapport radiologique
   * @param {string} studyId - ID de l'étude
   * @param {Object} reportData - Données du rapport
   * @returns {Promise<Object>} Rapport créé/mis à jour
   */
  saveReport(studyId, reportData) {
    return api.post(`${BASE_URL}/studies/${studyId}/report/`, reportData);
  }
};
