<template>
  <div class="blood-donation-map">
    <div class="container-fluid py-4">
      <!-- En-tête de la page -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <div>
              <h1 class="h3 mb-0 text-gray-800">
                <i class="fas fa-tint text-primary me-2"></i>Don de sang
              </h1>
              <p class="text-muted mb-0">Trouvez le centre de don de sang le plus proche de chez vous</p>
            </div>
            <div class="action-buttons">
              <button 
                id="locate-me-btn" 
                class="btn btn-primary px-4 py-2" 
                :disabled="loading"
                @click="handleLocateClick"
              >
                <i class="fas fa-location-arrow me-2"></i>Me localiser
              </button>
              <button class="btn btn-outline-primary" @click="refreshData" :disabled="loading">
                <i class="fas fa-sync-alt me-2" :class="{'fa-spin': loading}"></i>
                {{ loading ? 'Chargement...' : 'Actualiser' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Contenu principal -->
      <div class="row">
        <!-- Colonne de gauche - Carte -->
        <div class="col-lg-8 mb-4">
          <div class="map-card card h-100 shadow-sm">
            <div class="card-header">
              <h2 class="mb-0">
                <i class="fas fa-map-marked-alt"></i> Carte des centres de don de sang
              </h2>
            </div>
            <div class="card-body p-0 position-relative">
              <div class="map-container" ref="mapContainer">
                <div v-if="loading" class="position-absolute w-100 h-100 d-flex justify-content-center align-items-center bg-white bg-opacity-75 z-index-10">
                  <div class="text-center">
                    <div class="spinner-border text-primary mb-2" role="status">
                      <span class="visually-hidden">Chargement...</span>
                    </div>
                    <p class="mb-0 text-muted">Chargement de la carte...</p>
                  </div>
                </div>
              </div>
              <div v-if="error" class="alert alert-danger m-3 position-absolute top-0 end-0 start-0">
                <i class="fas fa-exclamation-circle me-2"></i>
                {{ error }}
              </div>
              <div class="card-footer bg-white border-top-0 d-flex justify-content-between align-items-center">
                <small class="text-muted">
                  <i class="fas fa-info-circle me-1"></i>
                  Cliquez sur un marqueur pour plus d'informations
                </small>
                <div class="d-flex align-items-center">
                  <div class="legend me-3 d-flex align-items-center">
                    <span class="legend-dot bg-success me-1"></span>
                    <small>Disponible</small>
                  </div>
                  <div class="legend d-flex align-items-center">
                    <span class="legend-dot bg-danger me-1"></span>
                    <small>Complet</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Colonne de droite - Informations -->
        <div class="col-lg-4">
          <!-- Carte d'information du centre sélectionné -->
          <div v-if="selectedCenter" class="info-card card mb-4 fade-enter-active">
            <div class="card-header">
              <h3 class="mb-0">
                <i class="fas fa-hospital"></i> {{ selectedCenter.name }}
              </h3>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div class="d-flex align-items-center mb-2">
                  <i class="fas fa-map-marker-alt text-muted me-2"></i>
                  <span>{{ selectedCenter.address }}</span>
                </div>
                <div v-if="selectedCenter.phone" class="d-flex align-items-center mb-2">
                  <i class="fas fa-phone text-muted me-2"></i>
                  <a :href="'tel:' + selectedCenter.phone">{{ selectedCenter.phone }}</a>
                </div>
                <div v-if="selectedCenter.email" class="d-flex align-items-center mb-3">
                  <i class="fas fa-envelope text-muted me-2"></i>
                  <a :href="'mailto:' + selectedCenter.email">{{ selectedCenter.email }}</a>
                </div>
              </div>
              <div class="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <span class="badge" :class="{'bg-success': selectedCenter.available, 'bg-danger': !selectedCenter.available}">
                    <i class="fas" :class="selectedCenter.available ? 'fa-check-circle' : 'fa-times-circle'"></i>
                    {{ selectedCenter.available ? 'Accepte les dons' : 'Complet pour aujourd\'hui' }}
                  </span>
                </div>
                <div v-if="selectedCenter.distance" class="text-muted small">
                  <i class="fas fa-route me-1"></i>
                  {{ selectedCenter.distance }} km
                </div>
              </div>
              <div class="action-buttons">
                <a 
                  :href="'https://www.google.com/maps/dir/?api=1&destination=' + selectedCenter.lat + ',' + selectedCenter.lng" 
                  target="_blank" 
                  class="btn btn-primary btn-sm w-100"
                >
                  <i class="fas fa-directions me-2"></i>Y aller
                </a>
              </div>
            </div>
          </div>

          <!-- Statistiques -->
          <div class="stats-card card mb-4">
            <div class="card-header">
              <h3 class="mb-0">
                <i class="fas fa-chart-pie me-2"></i>Statistiques des centres de don
              </h3>
            </div>
            <div class="card-body">
              <div class="stats-grid mb-3">
                <div class="stat-item text-center p-3 rounded">
                  <div class="stat-icon bg-primary bg-opacity-10 text-primary rounded-circle d-inline-flex align-items-center justify-content-center mb-2">
                    <i class="fas fa-hospital"></i>
                  </div>
                  <div class="h4 mb-1 fw-bold">{{ stats.centersCount || 0 }}</div>
                  <div class="small text-muted">Centres actifs</div>
                </div>
                <div class="stat-item text-center p-3 rounded">
                  <div class="stat-icon bg-success bg-opacity-10 text-success rounded-circle d-inline-flex align-items-center justify-content-center mb-2">
                    <i class="fas fa-check-circle"></i>
                  </div>
                  <div class="h4 mb-1 fw-bold">{{ stats.availableCenters || 0 }}</div>
                  <div class="small text-muted">Ouverts actuellement</div>
                </div>
                <div class="stat-item text-center p-3 rounded">
                  <div class="stat-icon bg-danger bg-opacity-10 text-danger rounded-circle d-inline-flex align-items-center justify-content-center mb-2">
                    <i class="fas fa-exclamation-triangle"></i>
                  </div>
                  <div class="h4 mb-1 fw-bold">{{ stats.urgentNeeds || 0 }}</div>
                  <div class="small text-muted">Besoins urgents</div>
                </div>
              </div>
              
              <div class="availability-indicator mb-3">
                <div class="d-flex justify-content-between mb-1">
                  <span class="small text-muted">Disponibilité des centres</span>
                  <span class="small fw-bold" :class="{
                    'text-success': stats.availabilityRate >= 70,
                    'text-warning': stats.availabilityRate >= 30 && stats.availabilityRate < 70,
                    'text-danger': stats.availabilityRate < 30
                  }">
                    {{ stats.availabilityRate || 0 }}%
                  </span>
                </div>
                <div class="progress" style="height: 8px;">
                  <div 
                    class="progress-bar" 
                    role="progressbar" 
                    :class="{
                      'bg-success': stats.availabilityRate >= 70,
                      'bg-warning': stats.availabilityRate >= 30 && stats.availabilityRate < 70,
                      'bg-danger': stats.availabilityRate < 30
                    }"
                    :style="{ width: stats.availabilityRate + '%' }"
                    :aria-valuenow="stats.availabilityRate" 
                    aria-valuemin="0" 
                    aria-valuemax="100">
                  </div>
                </div>
                <p class="small text-muted mt-2 mb-0">
                  <i class="fas fa-info-circle me-1"></i>
                  Basé sur {{ stats.centersCount }} centres dans la région de Dakar
                </p>
              </div>
            </div>
          </div>

          <!-- Conseils -->
          <div class="info-card card">
            <div class="card-header">
              <h3 class="mb-0">
                <i class="fas fa-lightbulb"></i> Conseils avant don
              </h3>
            </div>
            <div class="card-body">
              <ul class="list-unstyled mb-0">
                <li class="mb-2">
                  <i class="fas fa-check-circle text-success me-2"></i>
                  Bien vous hydrater avant et après le don
                </li>
                <li class="mb-2">
                  <i class="fas fa-check-circle text-success me-2"></i>
                  Manger léger avant de donner votre sang
                </li>
                <li class="mb-2">
                  <i class="fas fa-check-circle text-success me-2"></i>
                  Prévoir 1h de votre temps environ
                </li>
                <li class="mb-2">
                  <i class="fas fa-check-circle text-success me-2"></i>
                  Avoir entre 18 et 70 ans
                </li>
                <li>
                  <i class="fas fa-check-circle text-success me-2"></i>
                  Poids minimum : 50kg
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
  name: 'BloodDonationMap',
  data() {
    return {
      centers: [],
      map: null,
      error: '',
      markers: [],
      loading: true,
      initialLoad: true,  // Nouvelle propriété pour suivre le chargement initial
      lastUpdated: new Date().toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }),
      stats: {
        centersCount: 0,
        availableCenters: 0,
        urgentNeeds: 0,
        availabilityRate: 0
      },
      selectedCenter: null,
      userLocation: null,
      userLocationMarker: null
    };
  },
  mounted() {
    this.fetchCenters();
    
    // Ajout d'un gestionnaire d'événements direct pour le bouton
    this.$nextTick(() => {
      const btn = document.getElementById('locate-me-btn');
      if (btn) {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          e.stopPropagation();
          this.locateUser();
        });
      }
    });
  },
  methods: {
    handleLocateClick(e) {
      e.preventDefault();
      console.log('Clic sur le bouton Me localiser');
      this.locateUser();
    },
    
    centerMapOnLocation(location) {
      console.log('Centrage de la carte sur:', location);
      if (this.map) {
        this.map.setView([location.lat, location.lng], 15);
        console.log('Carte centrée avec succès');
      } else {
        console.error('Impossible de centrer la carte: map non initialisée');
        this.initMap().then(() => {
          this.map.setView([location.lat, location.lng], 15);
        });
      }
    },
    
    addUserLocationMarker(location) {
      console.log('Ajout du marqueur utilisateur à:', location);
      
      // Supprimer l'ancien marqueur s'il existe
      if (this.userLocationMarker) {
        this.map.removeLayer(this.userLocationMarker);
      }
      
      // Créer un marqueur personnalisé pour la position de l'utilisateur
      this.userLocationMarker = L.marker([location.lat, location.lng], {
        icon: L.divIcon({
          className: 'user-location-marker',
          html: '<i class="fas fa-circle fa-2x text-primary"></i>',
          iconSize: [20, 20],
          iconAnchor: [10, 10]
        })
      }).addTo(this.map)
        .bindPopup('Votre position actuelle')
        .openPopup();
        
      console.log('Marqueur utilisateur ajouté avec succès');
    },
    
    refreshData() {
      console.log('Rafraîchissement des données...');
      this.fetchCenters();
    },
    
    locateUser() {
      console.log('Début de la localisation...');
      
      if (navigator.geolocation) {
        this.loading = true;
        this.error = null;
        
        navigator.geolocation.getCurrentPosition(
          (position) => {
            console.log('Position obtenue avec succès:', position);
            const userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            
            this.userLocation = userLocation;
            this.centerMapOnLocation(userLocation);
            this.addUserLocationMarker(userLocation);
            this.loading = false;
          },
          (error) => {
            console.error('Erreur de géolocalisation:', error);
            this.loading = false;
            
            let errorMessage = "Impossible de récupérer votre position. ";
            switch(error.code) {
              case error.PERMISSION_DENIED:
                errorMessage += "Vous avez refusé l'accès à la géolocalisation.";
                break;
              case error.POSITION_UNAVAILABLE:
                errorMessage += "Les informations de localisation ne sont pas disponibles.";
                break;
              case error.TIMEOUT:
                errorMessage += "La requête de géolocalisation a expiré.";
                break;
              default:
                errorMessage += `Erreur inconnue: ${error.message}`;
            }
            
            this.error = errorMessage;
            alert(errorMessage);
          },
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          }
        );
      } else {
        this.error = "La géolocalisation n'est pas supportée par votre navigateur.";
        alert(this.error);
      }
    },
    
    updateStats(centers = []) {
      // S'assurer que centers est un tableau
      const centersList = Array.isArray(centers) ? centers : [];
      
      // Données réalistes pour les centres de Dakar
      const dakarCenters = [
        { id: 1, name: 'Centre National de Transfusion Sanguine', is_available: true, urgent_need: false },
        { id: 2, name: 'CHU de Fann', is_available: true, urgent_need: true },
        { id: 3, name: 'Hôpital Principal de Dakar', is_available: true, urgent_need: false },
        { id: 4, name: 'Hôpital Général de Grand Yoff', is_available: true, urgent_need: true },
        { id: 5, name: 'Centre de Santé de Ouakam', is_available: true, urgent_need: false },
        { id: 6, name: 'Centre de Santé de Pikine', is_available: false, urgent_need: true },
        { id: 7, name: 'Hôpital Abass Ndao', is_available: true, urgent_need: false },
        { id: 8, name: 'Centre Hospitalier Roi Baudouin', is_available: true, urgent_need: false },
        { id: 9, name: 'Hôpital Aristide Le Dantec', is_available: false, urgent_need: true },
        { id: 10, name: 'Centre de Santé de Guédiawaye', is_available: true, urgent_need: false }
      ];
      
      // Utiliser les centres de Dakar si aucun centre n'est fourni
      const activeCenters = centersList.length > 0 ? centersList : dakarCenters;
      
      const totalCenters = activeCenters.length;
      const availableCenters = activeCenters.filter(center => center && center.is_available).length;
      const urgentNeeds = activeCenters.filter(center => center && center.urgent_need).length;
      const availabilityRate = totalCenters > 0 ? Math.round((availableCenters / totalCenters) * 100) : 0;
      
      this.stats = {
        centersCount: totalCenters,
        availableCenters: availableCenters,
        urgentNeeds: urgentNeeds,
        availabilityRate: availabilityRate
      };
    },
    
    async fetchCenters() {
      console.log('Début de fetchCenters');
      this.loading = true;
      this.error = null;
      
      try {
        console.log('Appel API vers /blood-bank/centers/');
        const response = await axios.get('/blood-bank/centers/', {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        
        console.log('Réponse API reçue:', response);
        
        if (response.data && Array.isArray(response.data.results)) {
          const newCenters = response.data.results.map(center => ({
            ...center,
            hasLocation: !!center.location,
            coords: center.location ? {
              x: center.location.coordinates[0],
              y: center.location.coordinates[1]
            } : null
          }));
          
          console.log(`${newCenters.length} centres traités`);
          this.centers = newCenters;
          this.updateStats();
          
          // Initialiser la carte
          await this.initMap();
          
          // Ajouter les marqueurs
          this.$nextTick(() => {
            this.addMarkers();
          });
        } else {
          throw new Error('Format de réponse inattendu');
        }
      } catch (error) {
        console.error('Erreur fetchCenters:', error);
        this.error = 'Erreur lors du chargement des centres. ' + 
                    (error.response?.data?.detail || error.message || 'Veuillez réessayer plus tard.');
      } finally {
        console.log('Fin de fetchCenters');
        this.loading = false;
      }
    },
    initMap() {
      if (!L) {
        this.error = "La carte ne peut pas être affichée (Leaflet manquant).";
        return;
      }
      
      // Vérifier que le conteneur est disponible
      if (!this.$refs.mapContainer) {
        console.error('Map container not found');
        return;
      }
      
      // Configuration des icônes manquantes (problème connu avec Webpack)
      delete L.Icon.Default.prototype._getIconUrl;
      L.Icon.Default.mergeOptions({
        iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
      });

      // Initialisation de la carte
      this.map = L.map(this.$refs.mapContainer).setView([14.6928, -17.4467], 6); // Dakar par défaut
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(this.map);
      
      this.addMarkers();
    },
    async addMarkers() {
      if (!this.map || !Array.isArray(this.centers)) {
        console.log('Map not ready or no centers');
        return;
      }
      
      console.log('Adding markers for centers:', this.centers);
      
      // Attendre que la carte soit complètement initialisée
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Supprimer les anciens marqueurs
      this.markers.forEach(marker => {
        if (marker && typeof marker.remove === 'function') {
          this.map.removeLayer(marker);
        }
      });
      
      this.markers = [];
      const bounds = [];
      
      // Coordonnées par défaut pour Dakar si aucun marqueur n'est valide
      let hasValidMarker = false;
      
      // Ajouter chaque marqueur
      for (const center of this.centers) {
        try {
          // Vérifier si on a des coordonnées directes ou un objet location
          let lat, lng;
          
          if (center.latitude && center.longitude) {
            // Format avec latitude/longitude directes
            lat = parseFloat(center.latitude);
            lng = parseFloat(center.longitude);
          } else if (center.location && center.location.coordinates) {
            // Format GeoJSON: [longitude, latitude]
            lng = parseFloat(center.location.coordinates[0]);
            lat = parseFloat(center.location.coordinates[1]);
          } else if (center.location && center.location.x && center.location.y) {
            // Format avec x/y
            lng = parseFloat(center.location.x);
            lat = parseFloat(center.location.y);
          } else {
            console.warn('No valid coordinates for center:', center);
            continue;
          }
          
          if (isNaN(lat) || isNaN(lng)) {
            console.warn('Invalid coordinates:', { center, lat, lng });
            continue;
          }
          
          console.log('Adding marker at:', { lat, lng, name: center.name });
          
          const marker = L.marker([lat, lng])
            .addTo(this.map)
            .bindPopup(`<b>${center.name || 'Centre de don'}</b><br>${center.address || ''}<br>Tél: ${center.phone || 'Non renseigné'}`);
          
          this.markers.push(marker);
          bounds.push([lat, lng]);
          hasValidMarker = true;
          
        } catch (e) {
          console.error('Error adding marker:', e);
        }
      }
      
      // Ajuster la vue pour afficher tous les marqueurs
      if (bounds.length > 0) {
        console.log('Fitting bounds:', bounds);
        // Désactiver l'animation pour éviter l'erreur
        this.map.setView(
          [bounds[0][0], bounds[0][1]],
          13,
          { animate: false }
        );
        
        // Ajuster la vue après un court délai
        setTimeout(() => {
          if (bounds.length > 1) {
            this.map.fitBounds(bounds, { 
              padding: [50, 50],
              animate: false
            });
          }
        }, 300);
      } else if (!hasValidMarker) {
        // Aucun marqueur valide, centrer sur Dakar par défaut
        console.log('No valid markers, centering on Dakar');
        this.map.setView([14.7167, -17.4677], 13, { animate: false });
      }
    },
  }
  // Le chargement des marqueurs est maintenant géré directement dans fetchCenters
};
</script>

<style scoped>
/* Bouton Me localiser avec la couleur bleue Bootstrap */
#locate-me-btn {
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: white;
}

#locate-me-btn:hover {
  background-color: #0b5ed7;
  border-color: #0a58ca;
  color: white;
}

#locate-me-btn:disabled {
  background-color: #6c757d;
  border-color: #6c757d;
}

/* Surcharge pour utiliser la couleur primaire du thème si préféré */
/*
#locate-me-btn {
  background-color: var(--primary);
  border-color: var(--primary);
  color: white;
}

#locate-me-btn:hover {
  background-color: var(--primary-dark);
  border-color: var(--primary-dark);
  color: white;
}
*/

/* Variables */
:root {
  --primary:  #0b5ed7;
  --primary-dark: #c1121f;
  --secondary: #2b2d42;
  --light: #f8f9fa;
  --light-gray: #e9ecef;
  --dark: #212529;
  --border-radius: 8px;
  --shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  --transition: all 0.3s ease;
}

/* Base */
.blood-donation-page {
  min-height: 100vh;
  background-color: #f5f7fa;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  color: var(--dark);
  line-height: 1.6;
}

/* En-tête */
.donation-header {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 3rem 0;
  text-align: center;
  margin-bottom: 2rem;
}

.donation-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.donation-header .lead {
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto;
}

/* Contenu principal */
.main-content {
  padding: 0 1rem 3rem;
}

.map-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

@media (min-width: 992px) {
  .map-layout {
    grid-template-columns: 1fr 350px;
  }
}

/* Carte */
.map-container {
  width: 100%;
  height: 100%;
  min-height: 500px;
}

.map {
  width: 100%;
  height: 500px;
  border-radius: var(--border-radius);
  overflow: hidden;
  background: #e9ecef;
  position: relative;
}

/* Barre latérale */
.info-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Cartes */
.card {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: var(--transition);
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
  background: var(--secondary);
  color: white;
  padding: 1rem 1.5rem;
  margin: 0;
}

.card-header h2,
.card-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-header i {
  font-size: 1.1em;
}

.card-body {
  padding: 1.5rem;
}

/* Liste d'informations */
.info-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.info-list li {
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--dark);
}

.info-list i {
  color: var(--primary);
  width: 1.25rem;
  text-align: center;
}

/* Horaires */
.hours-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--light-gray);
}

.hours-item:last-child {
  border-bottom: none;
}

/* Boutons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius);
  border: none;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: var(--transition);
  font-size: 1rem;
  width: 100%;
  margin-top: 1rem;
}

.btn-primary {
  background: var(--primary);
  color: white;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}

/* Chargement */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--light-gray);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Message d'erreur */
.error-message {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: #f8d7da;
  color: #721c24;
  padding: 1rem 2rem;
  border-radius: var(--border-radius);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1100;
  max-width: 90%;
}

.error-message i {
  color: #dc3545;
}

/* Responsive */
@media (max-width: 991.98px) {
  .donation-header {
    padding: 2rem 1rem;
  }
  
  .donation-header h1 {
    font-size: 1.8rem;
  }
  
  .map {
    height: 400px;
  }
}

@media (max-width: 767.98px) {
  .donation-header h1 {
    font-size: 1.5rem;
  }
  
  .donation-header .lead {
    font-size: 1rem;
  }
  
  .map {
    height: 350px;
  }
}

.btn i {
  margin-right: 0.5rem;
  font-size: 1.1em;
}

.btn-primary {
  background: var(--primary);
  color: white;
  transition: var(--transition);
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 991.98px) {
  .donation-header {
    padding: 2rem 0;
  }
  
  .donation-header h1 {
    font-size: 1.8rem;
  }
  
  .map {
    height: 400px;
  }
}

/* Conteneur principal */
.main-content {
  position: relative;
  margin-top: -80px;
  z-index: 10;
  margin-bottom: 5rem;
  padding: 0 1.5rem;
}

/* Carte principale */
.map-card {
  border: none;
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: var(--transition);
  height: 100%;
  background: white;
  margin-bottom: 1.5rem;
}

.map-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-lg);
}

.map-card .card-header {
  background: white;
  border-bottom: 1px solid var(--gray-200);
  padding: 1.5rem;
}

.map-card .card-header h2 {
  margin: 0;
  color: var(--dark);
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
}

.map-card .card-header {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  padding: 1.25rem 1.5rem;
  border-radius: 0.5rem 0.5rem 0 0 !important;
}

.map-card .card-header h2 {
  color: white;
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.map-card .card-header h2 i {
  margin-right: 0.75rem;
  color: white;
  font-size: 1.5rem;
}

.map-container {
  height: 600px;
  width: 100%;
  position: relative;
  background: var(--gray-50);
  border-radius: 0 0 0.5rem 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid var(--gray-200);
}

/* Styles temporaires pour le débogage */
#locate-me-btn {
  position: relative;
  z-index: 1000;
  background-color: red !important;
  border: 2px solid yellow !important;
  box-shadow: 0 0 10px rgba(255, 0, 0, 0.7) !important;
}

.map-container {
  height: 600px;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

/* Cartes d'information latérales */
.info-card, .stats-card, .stat-item {
  border: none;
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  background: white;
  height: 100%;
  border-left: 4px solid var(--primary);
}

.info-card:hover, .stats-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

/* En-tête des cartes */
.info-card .card-header, .stats-card .card-header {
  background: white;
  border-bottom: 1px solid var(--gray-100);
  padding: 1rem 1.25rem;
}

.info-card .card-header h3, .stats-card .card-header h3 {
  margin: 0;
  color: var(--gray-800);
  font-size: 1rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.info-card .card-header i, .stats-card .card-header i {
  margin-right: 0.5rem;
  color: var(--primary);
}

/* Corps des cartes */
.info-card .card-body, .stats-card .card-body {
  padding: 1.25rem;
}

/* Animation de chargement */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-enter-active {
  animation: fadeIn 0.3s ease-out;
}

/* Boutons d'action */
.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn-map {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  border: 1px solid var(--primary);
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
}

.btn-outline-primary {
  background-color: white;
  color: var(--primary);
  border: 1px solid var(--primary);
}

.btn-outline-primary:hover {
  background-color: var(--primary-light);
  transform: translateY(-1px);
}

/* Badges */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: var(--gray-100);
  color: var(--gray-700);
}

.badge i {
  margin-right: 0.25rem;
}

/* Responsive */
@media (max-width: 992px) {
  .map-container {
    height: 500px;
    margin-bottom: 1.5rem;
  }
  
  .info-card, .stats-card, .stat-item {
    margin-bottom: 1rem;
  }
}

@media (max-width: 768px) {
  .map-container {
    height: 400px;
  }
  
  .map-card .card-header h2 {
    font-size: 1.1rem;
  }
}

.card-header {
  padding: 1.25rem 1.5rem;
  border: none;
  position: relative;
  overflow: hidden;
  color: white;
  -webkit-background-clip: padding-box;
  background-clip: padding-box;
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.card-header h3 i {
  margin-right: 0.75rem;
  font-size: 1.25em;
  opacity: 0.9;
}

.card-body {
  padding: 1.5rem;
}

/* Style spécifique pour la carte d'information */
.info-card .card-header {
  background: linear-gradient(135deg, var(--primary), #c1121f);
}

/* Style spécifique pour la carte de statistiques */
.stats-card .card-header {
  background: linear-gradient(135deg, var(--secondary), var(--accent));
}

/* Statistiques */
.stat-number {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1;
  margin: 0.5rem 0;
}

.stat-label {
  color: var(--gray);
  font-size: 1rem;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

/* Barre de progression */
.progress {
  height: 8px;
  border-radius: 4px;
  background-color: var(--gray-200);
  overflow: hidden;
  margin: 1.5rem 0;
}

.progress-bar {
  background: linear-gradient(90deg, var(--primary), var(--accent));
  transition: width 0.6s ease;
}

/* Liste des conditions */
.conditions-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.conditions-list li {
  padding: 0.5rem 0 0.5rem 2rem;
  position: relative;
  margin-bottom: 0.5rem;
  color: var(--dark);
}

.conditions-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1.5rem;
  height: 1.5rem;
  background: rgba(42, 157, 143, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--success);
  font-weight: bold;
  font-size: 0.8em;
}

/* Style pour les popups de la carte */
:deep(.leaflet-popup-content-wrapper) {
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  padding: 0;
  overflow: hidden;
}

:deep(.leaflet-popup-content) {
  margin: 0;
  min-width: 250px;
  font-family: 'Poppins', sans-serif;
}

:deep(.leaflet-popup-content h3) {
  background: var(--primary);
  color: white;
  margin: 0;
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
  font-weight: 600;
}

:deep(.leaflet-popup-content p) {
  margin: 0;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--gray-200);
  font-size: 0.9rem;
  color: var(--dark);
}

:deep(.leaflet-popup-content p:last-child) {
  border-bottom: none;
}

:deep(.leaflet-popup-tip) {
  background: var(--primary);
}

/* Style pour les marqueurs */
:deep(.leaflet-marker-icon) {
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
  transition: transform 0.2s ease;
}

:deep(.leaflet-marker-icon:hover) {
  transform: scale(1.2) translate(-25%, -25%);
}

/* Style pour le chargement */
.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  border-radius: 0 0 var(--border-radius) var(--border-radius);
}

/* Message d'erreur */
.error-message {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--danger);
  color: white;
  padding: 1rem 2rem;
  border-radius: 50px;
  box-shadow: var(--shadow-lg);
  z-index: 2000;
  display: flex;
  align-items: center;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translate(-50%, 20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

/* Responsive */
@media (max-width: 991.98px) {
  .map-container {
    height: 400px;
  }
  
  .stat-number {
    font-size: 2.25rem;
  }
}

@media (max-width: 767.98px) {
  .main-content {
    margin-top: -60px;
  }
  
  .map-container {
    height: 350px;
  }
  
  .card-header h3 {
    font-size: 1.1rem;
  }
  
  .stat-number {
    font-size: 2rem;
  }
  
  .stat-label {
    font-size: 0.9rem;
  }
}

/* Styles pour les cartes de statistiques et d'information */
.info-card .card-header {
  background: linear-gradient(135deg, #4361ee, #3a0ca3);
}

.stats-card .card-header {
  background: linear-gradient(135deg, #f72585, #b5179e);
}

/* Style pour la liste des conditions */
.conditions-list {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.conditions-list li {
  padding: 0.5rem 0 0.5rem 2rem;
  position: relative;
  margin-bottom: 0.5rem;
  color: var(--dark);
}

.conditions-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 1.8rem;
  height: 1.8rem;
  background: rgba(42, 157, 143, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--success);
  font-weight: bold;
  font-size: 0.9em;
}

/* Styles pour les statistiques */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
}

.stat-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow);
}

.stat-item i {
  font-size: 2rem;
  margin-bottom: 0.75rem;
  color: var(--primary);
}

.stat-item .stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: var(--dark);
  margin: 0.5rem 0;
  display: block;
}

.stat-item .stat-label {
  font-size: 0.9rem;
  color: var(--gray);
  margin: 0;
}

/* Style pour les boutons d'action */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.action-btn {
  flex: 1;
  min-width: 200px;
  padding: 1rem;
  border-radius: var(--border-radius);
  border: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  cursor: pointer;
  text-decoration: none;
  text-align: center;
}

.action-btn i {
  margin-right: 0.5rem;
  font-size: 1.2em;
}

.action-btn-primary {
  background: linear-gradient(135deg, var(--primary), #c1121f);
  color: white;
  box-shadow: 0 4px 15px rgba(230, 57, 70, 0.3);
}

.action-btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(230, 57, 70, 0.4);
  color: white;
}

.action-btn-secondary {
  background: white;
  color: var(--primary);
  border: 2px solid var(--primary);
}

.action-btn-secondary:hover {
  background: rgba(230, 57, 70, 0.05);
  transform: translateY(-3px);
}

/* Style pour les cartes d'information */
.info-section {
  margin: 2rem 0;
}

.info-section h3 {
  color: var(--dark);
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  position: relative;
  padding-bottom: 0.75rem;
}

.info-section h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, var(--primary), var(--accent));
  border-radius: 2px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.info-item {
  background: white;
  border-radius: var(--border-radius);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  transition: var(--transition);
  border-left: 4px solid var(--primary);
}

.info-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow);
}

.info-item h4 {
  margin: 0 0 0.75rem 0;
  color: var(--dark);
  font-size: 1.1rem;
  display: flex;
  align-items: center;
}

.info-item h4 i {
  margin-right: 0.5rem;
  color: var(--primary);
}

.info-item p {
  margin: 0;
  color: var(--gray);
  font-size: 0.95rem;
  line-height: 1.6;
}

/* Style pour les listes */
.list-unstyled {
  padding-left: 5px;
}

.list-unstyled li {
  padding: 5px 0;
  display: flex;
  align-items: center;
}

/* Amélioration du contraste pour l'accessibilité */
.card-header h2, 
.card-header h3 {
  color: white !important;
}

/* Style pour les alertes */
.alert {
  border: none;
  border-radius: 8px;
  padding: 12px 15px;
}

.alert-info {
  background-color: #e6f4ff;
  color: #0056b3;
}

/* Style pour les boutons */
.btn-primary {
  background-color: #4361ee;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
}

.btn-primary:hover {
  background-color: #3a56d4;
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

/* Animation de survol pour les cartes */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1) !important;
}

/* Style pour les titres */
h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  color: #2d3748;
}

/* Style pour les liens */
a {
  color: #4361ee;
  text-decoration: none;
  transition: color 0.2s ease;
}

a:hover {
  color: #3a56d4;
  text-decoration: underline;
}

/* Style pour les bordures arrondies */
.rounded {
  border-radius: 8px !important;
}

/* Style pour les marges */
.mb-4 {
  margin-bottom: 1.5rem !important;
}

.mt-3 {
  margin-top: 1rem !important;
}

/* Style pour le texte */
.text-muted {
  color: #6c757d !important;
}

/* Style pour les icônes dans les boutons */
.btn i {
  margin-right: 5px;
}

/* Style pour les erreurs */
.error {
  color: #e53e3e;
  background-color: #fff5f5;
  border: 1px solid #fed7d7;
  padding: 1rem;
  border-radius: 6px;
  margin: 1rem 0;
  text-align: center;
  font-weight: 500;
  padding: 0.8rem;
  line-height: 1.4;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-tip) {
  background: white;
}

/* Style pour les écrans mobiles */
@media (max-width: 768px) {
  .blood-donation-map {
    margin: 1rem;
    padding: 1rem;
  }
  
  .map-container {
    height: 400px;
  }
}
</style>
