import axios from 'axios';

// Créer une instance axios avec une configuration de base
const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000s',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Intercepteur pour ajouter le token JWT aux requêtes
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Gestion des réponses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Gestion des erreurs courantes
    if (error.response) {
      // Erreurs 401 non autorisé
      if (error.response.status === 401) {
        // Rediriger vers la page de connexion ou rafraîchir le token
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }
      
      // Vous pouvez ajouter d'autres gestions d'erreur ici
      // comme les erreurs 403, 404, 500, etc.
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;
