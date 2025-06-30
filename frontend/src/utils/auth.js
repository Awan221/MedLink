import axios from 'axios'
import jwtDecode from 'jwt-decode'

export const setAuthToken = token => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    delete axios.defaults.headers.common['Authorization']
  }
}

export const removeAuthToken = () => {
  delete axios.defaults.headers.common['Authorization']
}

export const getTokenExpiration = token => {
  try {
    const decoded = jwtDecode(token)
    return decoded.exp
  } catch (error) {
    return null
  }
}

export const isTokenValid = () => {
  const token = localStorage.getItem('token')

  if (!token) {
    return false
  }

  try {
    const decoded = jwtDecode(token)
    const currentTime = Date.now() / 1000
    return decoded.exp > currentTime
  } catch (error) {
    return false
  }
}

export const getUserFromToken = token => {
  try {
    return jwtDecode(token)
  } catch (error) {
    return null
  }
}

/**
 * Récupère l'en-tête d'authentification avec le token JWT
 * @returns {Object} En-tête d'authentification
 */
export const getAuthHeader = () => {
  const token = localStorage.getItem('access');
  if (token) {
    return { 'Authorization': `Bearer ${token}` };
  }
  return {};
};

export const getUserRole = () => {
  const token = localStorage.getItem('access');
  if (!token) return null;
  try {
    const payload = jwtDecode(token);
    // Adapter à la structure du backend
    return payload.role || (payload.groups ? payload.groups[0] : null);
  } catch {
    return null;
  }
}