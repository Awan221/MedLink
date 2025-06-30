<template>
  <div class="health-info-container">
    <div class="diseases-section">
      <h2>Informations sur les Maladies</h2>
      <div class="disease-cards">
        <div v-for="disease in diseases" :key="disease.id" class="disease-card">
          <h3>{{ disease.name }}</h3>
          <p>{{ disease.description }}</p>
          <a :href="disease.link" target="_blank" class="learn-more">En savoir plus</a>
        </div>
      </div>
    </div>

    <div class="hospitals-section">
      <h2>Hôpitaux à Proximité</h2>
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Entrez votre adresse..."
          @input="searchHospitals"
        >
      </div>
      <div class="hospitals-list">
        <div v-for="hospital in nearbyHospitals" :key="hospital.id" class="hospital-card">
          <h3>{{ hospital.name }}</h3>
          <p>{{ hospital.address }}</p>
          <p>Distance: {{ hospital.distance }} km</p>
          <div class="hospital-actions">
            <a :href="hospital.directions" target="_blank" class="directions-btn">
              <i class="fas fa-directions"></i> Itinéraire
            </a>
            <a :href="hospital.phone" class="phone-btn">
              <i class="fas fa-phone"></i> Appeler
            </a>
          </div>
        </div>
      </div>
    </div>

    <div class="blood-donation-section">
      <h2>Centres de Don de Sang</h2>
      <div class="blood-centers">
        <div v-for="center in bloodCenters" :key="center.id" class="blood-center-card">
          <h3>{{ center.name }}</h3>
          <p>{{ center.address }}</p>
          <div class="blood-levels">
            <div class="blood-level" :class="{ 'critical': center.isCritical }">
              <span>Niveau de stock: {{ center.stockLevel }}%</span>
              <div class="progress-bar">
                <div :style="{ width: center.stockLevel + '%' }" 
                     :class="{ 'critical': center.isCritical }"></div>
              </div>
            </div>
          </div>
          <button v-if="center.isCritical" @click="subscribeToAlert(center)" class="alert-btn">
            Recevoir une alerte
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'HealthInfo',
  setup() {
    const searchQuery = ref('')
    const nearbyHospitals = ref([])
    const bloodCenters = ref([])
    const diseases = ref([
      {
        id: 1,
        name: 'Diabète',
        description: 'Le diabète est une maladie chronique qui affecte la façon dont votre corps traite le glucose.',
        link: 'https://www.who.int/fr/news-room/fact-sheets/detail/diabetes'
      },
      {
        id: 2,
        name: 'Hypertension',
        description: 'L\'hypertension artérielle est une pression anormalement élevée du sang dans les artères.',
        link: 'https://www.who.int/fr/news-room/fact-sheets/detail/hypertension'
      },
      {
        id: 3,
        name: 'Asthme',
        description: 'L\'asthme est une maladie inflammatoire chronique des voies respiratoires.',
        link: 'https://www.who.int/fr/news-room/fact-sheets/detail/asthma'
      }
    ])

    const searchHospitals = async () => {
      if (!searchQuery.value) return

      try {
        // Utiliser l'API Google Maps pour la géolocalisation
        const geocoder = new google.maps.Geocoder()
        const result = await geocoder.geocode({ address: searchQuery.value })
        
        if (result.results[0]) {
          const location = result.results[0].geometry.location
          
          // Rechercher les hôpitaux à proximité
          const service = new google.maps.places.PlacesService(document.createElement('div'))
          const request = {
            location: location,
            radius: '5000',
            type: ['hospital']
          }

          service.nearbySearch(request, (results, status) => {
            if (status === google.maps.places.PlacesServiceStatus.OK) {
              nearbyHospitals.value = results.map(place => ({
                id: place.place_id,
                name: place.name,
                address: place.vicinity,
                distance: calculateDistance(location, place.geometry.location),
                directions: `https://www.google.com/maps/dir/?api=1&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}`,
                phone: place.formatted_phone_number
              }))
            }
          })
        }
      } catch (error) {
        console.error('Erreur lors de la recherche d\'hôpitaux:', error)
      }
    }

    const calculateDistance = (point1, point2) => {
      const R = 6371 // Rayon de la Terre en km
      const dLat = (point2.lat() - point1.lat()) * Math.PI / 180
      const dLon = (point2.lng() - point1.lng()) * Math.PI / 180
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(point1.lat() * Math.PI / 180) * Math.cos(point2.lat() * Math.PI / 180) * 
        Math.sin(dLon/2) * Math.sin(dLon/2)
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
      return (R * c).toFixed(1)
    }

    const subscribeToAlert = async (center) => {
      try {
        // Demander la permission pour les notifications
        const permission = await Notification.requestPermission()
        
        if (permission === 'granted') {
          // Enregistrer l'abonnement
          const response = await fetch('/api/blood-donation/subscribe', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              centerId: center.id,
              email: localStorage.getItem('userEmail')
            })
          })

          if (response.ok) {
            alert('Vous recevrez une notification lorsque le niveau de stock sera critique.')
          }
        }
      } catch (error) {
        console.error('Erreur lors de l\'abonnement aux alertes:', error)
      }
    }

    onMounted(() => {
      // Charger les centres de don de sang
      fetch('/api/blood-donation/centers')
        .then(response => response.json())
        .then(data => {
          bloodCenters.value = data
        })
        .catch(error => {
          console.error('Erreur lors du chargement des centres de don:', error)
        })
    })

    return {
      searchQuery,
      nearbyHospitals,
      bloodCenters,
      diseases,
      searchHospitals,
      subscribeToAlert
    }
  }
}
</script>

<style scoped>
.health-info-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.diseases-section,
.hospitals-section,
.blood-donation-section {
  margin-bottom: 40px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.disease-cards,
.hospitals-list,
.blood-centers {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.disease-card,
.hospital-card,
.blood-center-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.search-box {
  margin-bottom: 20px;
}

.search-box input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.hospital-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.directions-btn,
.phone-btn {
  padding: 8px 16px;
  border-radius: 4px;
  text-decoration: none;
  color: white;
  display: flex;
  align-items: center;
  gap: 5px;
}

.directions-btn {
  background-color: #4CAF50;
}

.phone-btn {
  background-color: #2196F3;
}

.blood-levels {
  margin: 15px 0;
}

.progress-bar {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar div {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.progress-bar div.critical {
  background-color: #f44336;
}

.alert-btn {
  width: 100%;
  padding: 10px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.alert-btn:hover {
  background-color: #d32f2f;
}

.learn-more {
  display: inline-block;
  margin-top: 10px;
  color: #2196F3;
  text-decoration: none;
}

.learn-more:hover {
  text-decoration: underline;
}
</style> 