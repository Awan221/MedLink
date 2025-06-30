<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-8">Hôpitaux à proximité</h1>
    
    <!-- Barre de recherche et filtres -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <input
            id="search-input"
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher un hôpital ou une adresse..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            @keyup.enter="searchLocation"
          />
        </div>
        <div class="w-full md:w-64">
          <select
            v-model="selectedSpecialty"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option v-for="specialty in specialties" :key="specialty" :value="specialty">
              {{ specialty }}
            </option>
          </select>
        </div>
        <button
          @click="getUserLocation"
          :disabled="isLocating"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center justify-center"
        >
          <svg v-if="!isLocating" class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span v-if="!isLocating">Me localiser</span>
          <span v-else>Localisation...</span>
        </button>
      </div>
    </div>

    <!-- Carte -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden mb-8">
      <div id="map" class="w-full h-[500px] z-0"></div>
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="isLocating" class="text-center py-8">
      <div class="inline-flex items-center px-4 py-2 text-blue-600">
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Localisation en cours...
      </div>
    </div>

    <!-- Liste des hôpitaux -->
    <div v-if="filteredHospitals.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="hospital in filteredHospitals" :key="hospital.id" class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-200">
        <div class="flex justify-between items-start mb-2">
          <h2 class="text-xl font-semibold text-gray-800">{{ hospital.name }}</h2>
          <span v-if="userLocation" class="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
            {{ calculateDistance(userLocation.lat, userLocation.lng, hospital.lat, hospital.lng) }} km
          </span>
        </div>
        
        <p class="text-gray-600 mb-4 flex items-start">
          <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>{{ hospital.address }}</span>
        </p>
        
        <div class="space-y-3 text-gray-700">
          <div class="flex items-start">
            <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span><span class="font-medium">Téléphone:</span> {{ hospital.phone }}</span>
          </div>
          
          <div class="flex items-start">
            <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            <span><span class="font-medium">Services:</span> {{ hospital.services }}</span>
          </div>
          
          <div class="flex items-start">
            <svg class="h-5 w-5 text-gray-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span><span class="font-medium">Horaires:</span> {{ hospital.hours }}</span>
          </div>
        </div>
        
        <div class="mt-4 flex flex-wrap gap-2">
          <a
            :href="hospital.directions"
            target="_blank"
            class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            Itinéraire
          </a>
          <a
            :href="'tel:' + hospital.phone"
            class="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            Appeler
          </a>
          <button
            @click="centerOnHospital(hospital)"
            class="inline-flex items-center px-3 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200"
            title="Centrer sur la carte"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
            </svg>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Aucun résultat -->
    <div v-else class="text-center py-12 bg-white rounded-lg shadow-sm">
      <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h3 class="mt-2 text-lg font-medium text-gray-900">Aucun hôpital trouvé</h3>
      <p class="mt-1 text-gray-500">Essayez de modifier vos critères de recherche.</p>
      <div class="mt-6">
        <button
          @click="resetFilters"
          class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Réinitialiser les filtres
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Correction pour les icônes manquantes dans Webpack
import icon from 'leaflet/dist/images/marker-icon.png';
import iconRetina from 'leaflet/dist/images/marker-icon-2x.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Configuration des icônes de marqueur
let DefaultIcon = L.icon({
  iconUrl: icon,
  iconRetinaUrl: iconRetina,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

// Utilisation de Nominatim pour le géocodage
const NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search';
const NOMINATIM_PARAMS = 'format=json&addressdetails=1&limit=1';

export default {
  name: 'NearbyHospitals',
  data() {
    return {
      map: null,
      markers: [],
      userLocation: null,
      isLocating: false,
      searchQuery: '',
      selectedSpecialty: '',
      specialties: [
        'Toutes spécialités',
        'Urgences',
        'Médecine générale',
        'Pédiatrie',
        'Chirurgie',
        'Cardiologie',
        'Gynécologie',
        'Maternité',
        'Médecine interne'
      ],
      hospitals: [
        {
          id: 1,
          name: 'Hôpital Principal de Dakar',
          address: 'Avenue Nelson Mandela, Dakar',
          phone: '+221 33 839 50 50',
          services: 'Urgences, Médecine générale, Chirurgie',
          hours: '24h/24',
          lat: 14.7167,
          lng: -17.4677,
          directions: 'https://www.google.com/maps/dir//Hôpital+Principal+de+Dakar'
        },
        {
          id: 2,
          name: 'Centre Hospitalier National d\'Enfants Albert Royer',
          address: 'Avenue Cheikh Anta Diop, Dakar',
          phone: '+221 33 825 98 98',
          services: 'Pédiatrie, Urgences pédiatriques',
          hours: '24h/24',
          lat: 14.7189,
          lng: -17.4733,
          directions: 'https://www.google.com/maps/dir//Centre+Hospitalier+National+d\'Enfants+Albert+Royer'
        },
        {
          id: 3,
          name: 'Hôpital Aristide Le Dantec',
          address: 'Avenue Pasteur, Dakar',
          phone: '+221 33 839 50 50',
          services: 'Médecine interne, Chirurgie, Cardiologie',
          hours: '24h/24',
          lat: 14.7167,
          lng: -17.4677,
          directions: 'https://www.google.com/maps/dir//Hôpital+Aristide+Le+Dantec'
        },
        {
          id: 4,
          name: 'Clinique de la Madeleine',
          address: 'Rue 10 Prolongée, Dakar',
          phone: '+221 33 889 89 89',
          services: 'Médecine générale, Gynécologie, Pédiatrie',
          hours: 'Lun-Sam: 8h-20h',
          lat: 14.7167,
          lng: -17.4677,
          directions: 'https://www.google.com/maps/dir//Clinique+de+la+Madeleine'
        },
        {
          id: 5,
          name: 'Clinique du Cap',
          address: 'Avenue Cheikh Anta Diop, Dakar',
          phone: '+221 33 825 98 98',
          services: 'Médecine générale, Chirurgie, Maternité',
          hours: '24h/24',
          lat: 14.7189,
          lng: -17.4733,
          directions: 'https://www.google.com/maps/dir//Clinique+du+Cap'
        }
      ]
    }
  },
  async mounted() {
    // Attendre que le DOM soit complètement chargé
    await this.$nextTick();
    
    // Initialiser la carte
    await this.initMap();
    
    // Mettre à jour les marqueurs avec les hôpitaux
    if (this.map) {
      this.updateMapMarkers(this.filteredHospitals);
    }
    
    // Essayer d'obtenir la position de l'utilisateur
    if (navigator.geolocation) {
      this.getUserLocation();
    }
  },
  
  beforeUnmount() {
    // Nettoyer la carte lors de la destruction du composant
    if (this.map) {
      try {
        // Marquer la carte comme en cours de suppression
        this.map._removed = true;
        
        // Désactiver les événements
        this.map.off();
        
        // Arrêter toutes les animations en cours
        if (this.map._panAnim) {
          this.map._panAnim.stop();
        }
        
        // Supprimer tous les calques
        this.map.eachLayer(layer => {
          try {
            this.map.removeLayer(layer);
          } catch (e) {
            console.warn('Erreur lors de la suppression d\'un calque:', e);
          }
        });
        
        // Vider le conteneur de la carte
        const container = this.map.getContainer();
        if (container) {
          container._leaflet_id = null;
          container.innerHTML = '';
        }
        
        // Supprimer la carte
        this.map.remove();
        
      } catch (e) {
        console.warn('Erreur lors du nettoyage de la carte:', e);
      } finally {
        this.map = null;
      }
    }
  },
  computed: {
    filteredHospitals() {
      let result = [...this.hospitals];
      
      // Filtrer par recherche
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(hospital => 
          hospital.name.toLowerCase().includes(query) ||
          hospital.address.toLowerCase().includes(query) ||
          hospital.services.toLowerCase().includes(query)
        );
      }
      
      // Filtrer par spécialité
      if (this.selectedSpecialty && this.selectedSpecialty !== 'Toutes spécialités') {
        result = result.filter(hospital => 
          hospital.services.includes(this.selectedSpecialty)
        );
      }
      
      return result;
    }
  },
  watch: {
    filteredHospitals: {
      immediate: true,
      handler(newHospitals) {
        this.updateMapMarkers(newHospitals);
      }
    }
  },
  methods: {
    // Obtenir la position de l'utilisateur
    getUserLocation() {
      if (navigator.geolocation) {
        this.isLocating = true;
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
            this.centerMapOnLocation(this.userLocation);
            this.addUserLocationMarker(this.userLocation);
            this.isLocating = false;
          },
          (error) => {
            console.error('Erreur de géolocalisation:', error);
            alert('Impossible de récupérer votre position. Veuillez vérifier les autorisations de géolocalisation.');
            this.isLocating = false;
          },
          {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
          }
        );
      } else {
        alert('La géolocalisation n\'est pas supportée par votre navigateur.');
      }
    },
    
    // Rechercher un emplacement avec Nominatim
    async searchLocation() {
      if (!this.searchQuery.trim()) return;
      
      try {
        this.isLocating = true;
        const response = await fetch(`${NOMINATIM_URL}?q=${encodeURIComponent(this.searchQuery)}&${NOMINATIM_PARAMS}`);
        const data = await response.json();
        
        if (data && data.length > 0) {
          const location = data[0];
          const newLocation = {
            lat: parseFloat(location.lat),
            lng: parseFloat(location.lon)
          };
          
          this.userLocation = newLocation;
          this.centerMapOnLocation(newLocation);
          this.addUserLocationMarker(newLocation);
        } else {
          alert('Aucun résultat trouvé pour cette recherche.');
        }
      } catch (error) {
        console.error('Erreur lors de la recherche:', error);
        alert('Une erreur est survenue lors de la recherche.');
      } finally {
        this.isLocating = false;
      }
    },
    
    // Centrer la carte sur une position de manière sécurisée
    centerMapOnLocation(position) {
      if (!this.map || !position || typeof position.lat !== 'number' || typeof position.lng !== 'number') {
        console.error('La carte ou la position n\'est pas valide');
        return;
      }
      
      // Vérifier que les coordonnées sont valides
      if (Math.abs(position.lat) > 90 || Math.abs(position.lng) > 180 || 
          isNaN(position.lat) || isNaN(position.lng)) {
        console.error('Coordonnées de position invalides:', position);
        return;
      }
      
      // S'assurer que la carte est toujours valide
      if (!this.map._loaded) {
        console.warn('La carte n\'est pas encore chargée, report du centrage...');
        setTimeout(() => this.centerMapOnLocation(position), 100);
        return;
      }
      
      try {
        // Sauvegarder l'état d'animation
        const wasAnimated = this.map._zoomAnimated;
        
        // Désactiver les animations
        this.map._zoomAnimated = false;
        
        // Mettre à jour la vue sans animation
        this.map.setView(
          L.latLng(position.lat, position.lng), 
          15, 
          { 
            animate: false,
            duration: 0,
            reset: true
          }
        );
        
        // Forcer une mise à jour immédiate
        this.map._resetView(
          L.latLng(position.lat, position.lng),
          15,
          false,
          false
        );
        
        // Réactiver les animations après un délai
        if (wasAnimated) {
          setTimeout(() => {
            if (this.map && !this.map._removed) {
              this.map._zoomAnimated = true;
            }
          }, 100);
        }
      } catch (error) {
        console.error('Erreur lors du centrage de la carte:', error);
        // Réessayer une fois en cas d'échec
        setTimeout(() => {
          if (this.map && !this.map._removed) {
            this.centerMapOnLocation(position);
          }
        }, 100);
      }
    },
    
    // Ajouter un marqueur pour la position de l'utilisateur
    addUserLocationMarker(position) {
      if (!this.map) {
        console.error('La carte n\'est pas encore initialisée');
        return;
      }
      
      // Supprimer l'ancien marqueur s'il existe
      if (this.userMarker) {
        this.userMarker.remove();
      }
      
      try {
        this.userMarker = L.marker([position.lat, position.lng])
          .addTo(this.map)
          .bindPopup('Votre position');
      } catch (error) {
        console.error('Erreur lors de l\'ajout du marqueur utilisateur:', error);
      }
    },
    
    // Mettre à jour les marqueurs sur la carte
    updateMapMarkers(hospitals) {
      // Vérifier que la carte est initialisée
      if (!this.map) {
        console.error('La carte n\'est pas encore initialisée');
        // Réessayer après un court délai
        setTimeout(() => this.updateMapMarkers(hospitals), 100);
        return;
      }

      // Vérifier que le composant est toujours monté
      if (!this.$el) {
        console.log('Composant démonté, arrêt de la mise à jour des marqueurs');
        return;
      }

      // Supprimer les anciens marqueurs
      this.clearMarkers();

      // Vérifier s'il y a des hôpitaux à afficher
      if (!hospitals || hospitals.length === 0) {
        console.log('Aucun hôpital à afficher');
        return;
      }

      // Ajouter un marqueur pour chaque hôpital
      const validMarkers = [];
      
      hospitals.forEach((hospital) => {
        try {
          // Vérifier que les coordonnées sont valides
          if (typeof hospital.lat !== 'number' || typeof hospital.lng !== 'number' || 
              isNaN(hospital.lat) || isNaN(hospital.lng)) {
            console.warn('Coordonnées invalides pour l\'hôpital:', hospital.name);
            return;
          }

          // Créer le contenu du popup
          const popupContent = `
            <div class="text-center p-2">
              <h3 class="font-bold text-base mb-1">${hospital.name || 'Hôpital'}</h3>
              ${hospital.address ? `<p class="text-xs text-gray-600 mb-2">${hospital.address}</p>` : ''}
              <div class="mt-1">
                <a 
                  href="https://www.openstreetmap.org/directions?from=${this.userLocation?.lat || ''},${this.userLocation?.lng || ''}&to=${hospital.lat},${hospital.lng}&route=car" 
                  target="_blank" 
                  rel="noopener noreferrer"
                  class="inline-block bg-blue-500 hover:bg-blue-600 text-white text-xs px-2 py-1 rounded transition-colors"
                >
                  Itinéraire
                </a>
              </div>
            </div>
          `;

          // Créer et ajouter le marqueur
          const marker = L.marker([hospital.lat, hospital.lng], {
            title: hospital.name || 'Hôpital',
            alt: hospital.name || 'Hôpital',
            riseOnHover: true
          });

          // Ajouter le popup
          marker.bindPopup(popupContent, {
            maxWidth: 250,
            minWidth: 200,
            className: 'custom-popup'
          });

          // Ajouter le marqueur à la carte
          marker.addTo(this.map);
          validMarkers.push(marker);
          
        } catch (error) {
          console.error('Erreur lors de l\'ajout du marqueur pour', hospital.name, ':', error);
        }
      });

      // Mettre à jour la liste des marqueurs avec uniquement ceux qui ont été créés avec succès
      this.markers = validMarkers;

      // Ajuster la vue pour afficher tous les marqueurs
      if (validMarkers.length > 0) {
        try {
          const group = L.featureGroup(validMarkers);
          const bounds = group.getBounds().pad(0.1);
          
          // Vérifier que les limites sont valides avant de les appliquer
          if (bounds.isValid()) {
            this.map.fitBounds(bounds);
          } else {
            console.warn('Les limites de la carte ne sont pas valides');
          }
        } catch (error) {
          console.error('Erreur lors du réglage des limites de la carte:', error);
        }
      } else {
        console.log('Aucun marqueur valide à afficher');
      }
    },
    
    // Calculer la distance entre deux coordonnées géographiques (formule de Haversine)
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // Rayon de la Terre en km
      const dLat = this.deg2rad(lat2 - lat1);
      const dLon = this.deg2rad(lon2 - lon1);
      const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      const distance = R * c; // Distance en km
      return distance.toFixed(1);
    },
    
    // Convertir des degrés en radians
    deg2rad(deg) {
      return deg * (Math.PI / 180);
    },
    
    // Centrer la carte sur un hôpital spécifique
    centerOnHospital(hospital) {
      if (!this.map) return;
      
      const position = [hospital.lat, hospital.lng];
      this.map.setView(position, 16);
      
      // Mettre en surbrillance le marqueur de l'hôpital
      const marker = this.markers.find(m => 
        m.getLatLng().lat === hospital.lat && 
        m.getLatLng().lng === hospital.lng
      );
      
      if (marker) {
        // Ouvrir le popup du marqueur
        marker.openPopup();
        
        // Animation du marqueur
        marker.setZIndexOffset(1000);
        setTimeout(() => {
          marker.setZIndexOffset(0);
        }, 1500);
      }
    },
    
    // Réinitialiser tous les filtres
    resetFilters() {
      this.searchQuery = '';
      this.selectedSpecialty = 'Toutes spécialités';
    }, 
    
    // Supprimer tous les marqueurs
    clearMarkers() {
      this.markers.forEach(marker => {
        if (marker && marker.remove) {
          marker.remove();
        }
      });
      this.markers = [];
    },
    
    // Initialiser la carte
    async initMap() {
      try {
        // S'assurer que le composant est toujours monté
        if (!this.$el || !document.getElementById('map')) {
          console.error('L\'élément de la carte n\'est pas disponible');
          return false;
        }

        // Coordonnées par défaut (Dakar)
        const defaultLocation = { lat: 14.7167, lng: -17.4677 };
        
        // Attendre que l'élément de la carte soit disponible dans le DOM
        await this.$nextTick();
        
        // Détruire la carte existante si elle existe
        if (this.map) {
          try {
            this.map.off();
            this.map.remove();
          } catch (e) {
            console.warn('Erreur lors du nettoyage de la carte existante:', e);
          }
          this.map = null;
        }
        
        // Créer la carte avec des options optimisées
        this.map = L.map('map', {
          center: [defaultLocation.lat, defaultLocation.lng],
          zoom: 12,
          zoomControl: true,
          preferCanvas: true, // Meilleures performances pour de nombreux marqueurs
          zoomSnap: 0.1, // Contrôle plus fin du zoom
          zoomDelta: 0.5, // Vitesse de zoom réduite
          trackResize: false, // Désactive le suivi du redimensionnement automatique
          fadeAnimation: false, // Désactive l'animation de fondu
          markerZoomAnimation: false, // Désactive l'animation des marqueurs au zoom
          transform3DLimit: 0, // Désactive les transformations 3D
          zoomAnimation: false // Désactive complètement l'animation de zoom
        });
        
        // Désactiver les animations problématiques
        if (this.map._zoomAnimated) {
          this.map._zoomAnimated = false;
          // Désactiver également les animations de couches
          L.DomUtil.TRANSITION = false;
        }

        // Ajouter la couche OpenStreetMap
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          maxZoom: 19,
          detectRetina: true
        }).addTo(this.map);

        // Ajouter les contrôles de la carte
        L.control.scale({ imperial: false }).addTo(this.map);

        // Réactiver les animations après un court délai
        setTimeout(() => {
          if (this.map) {
            this.map._zoomAnimated = true;
          }
        }, 500);

        // Initialiser la barre de recherche
        this.initSearchBox();

        // Mettre à jour les marqueurs avec les hôpitaux
        this.updateMapMarkers(this.filteredHospitals);
        
        return true;
      } catch (error) {
        console.error('Erreur lors de l\'initialisation de la carte:', error);
        return false;
      }
    },
    
    // Initialiser la barre de recherche
    initSearchBox() {
      const input = document.getElementById('search-input');
      
      // Ajouter un écouteur d'événement pour la touche Entrée
      input.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
          this.searchLocation();
        }
      });
    }
  }
}
</script>

<style scoped>
#map {
  height: 500px;
  width: 100%;
  border-radius: 0.5rem;
}

/* Style pour les popups personnalisés */
:deep(.custom-popup) {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

:deep(.custom-popup .leaflet-popup-content-wrapper) {
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 0;
  overflow: hidden;
}

:deep(.custom-popup .leaflet-popup-content) {
  margin: 0;
  line-height: 1.5;
}

:deep(.custom-popup .leaflet-popup-tip) {
  background: white;
}

:deep(.custom-popup h3) {
  color: #1a202c;
  margin: 0;
  padding: 0.5rem 0.75rem;
  background-color: #f7fafc;
  border-bottom: 1px solid #e2e8f0;
}

:deep(.custom-popup p) {
  margin: 0.5rem 0.75rem;
}

:deep(.custom-popup .mt-1) {
  margin-top: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: #f8fafc;
  border-top: 1px solid #edf2f7;
}

:deep(.custom-popup a) {
  text-decoration: none;
  transition: background-color 0.2s ease-in-out;
}

:deep(.custom-popup a:hover) {
  text-decoration: none;
}
</style>