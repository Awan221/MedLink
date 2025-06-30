<template>
  <div class="public-portal">
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">Bienvenue sur MedLink</h1>
        <p class="hero-subtitle">Votre plateforme de santé connectée</p>
        <div class="hero-cta">
          <router-link to="/login" class="cta-button primary">Se connecter</router-link>
          <router-link to="/register" class="cta-button secondary">S'inscrire</router-link>
        </div>
      </div>
    </div>

    <!-- Emergency Numbers Section -->
    <div class="emergency-section">
      <h2 class="section-title">Numéros d'Urgence</h2>
      <div class="emergency-grid">
        <div class="emergency-card samu">
          <div class="emergency-icon">🚑</div>
          <h3>SAMU</h3>
          <p class="emergency-number">15</p>
          <p class="emergency-description">Urgences médicales</p>
        </div>
        <div class="emergency-card pompiers">
          <div class="emergency-icon">🚒</div>
          <h3>Pompiers</h3>
          <p class="emergency-number">18</p>
          <p class="emergency-description">Urgences et secours</p>
        </div>
        <div class="emergency-card police">
          <div class="emergency-icon">👮</div>
          <h3>Police</h3>
          <p class="emergency-number">17</p>
          <p class="emergency-description">Urgences et sécurité</p>
        </div>
        <div class="emergency-card sos-medecins">
          <div class="emergency-icon">👨‍⚕️</div>
          <h3>SOS Médecins</h3>
          <p class="emergency-number">33 824 24 24</p>
          <p class="emergency-description">Médecin à domicile</p>
        </div>
      </div>
    </div>

    <!-- Services Section -->
    <div class="services-section">
      <h2 class="section-title">Nos Services</h2>
      <div class="services-grid">
        <router-link to="/public/maladies" class="service-card">
          <div class="service-icon">📚</div>
          <h3>Documentation des Maladies</h3>
          <p>Informations détaillées sur les maladies et leurs traitements</p>
        </router-link>
        <router-link to="/public/hopitaux" class="service-card">
          <div class="service-icon">🏥</div>
          <h3>Hôpitaux à Proximité</h3>
          <p>Trouvez les établissements de santé les plus proches</p>
        </router-link>
        <router-link to="/public/statistiques" class="service-card">
          <div class="service-icon">📊</div>
          <h3>Statistiques</h3>
          <p>Données et analyses sur la santé publique</p>
        </router-link>
        <router-link to="/donner-sang" class="service-card">
          <div class="service-icon" style="color: #e53e3e;">❤️</div>
          <h3>Don de Sang</h3>
          <p>Trouvez le centre de don le plus proche</p>
        </router-link>
      </div>
    </div>

    <!-- Chatbot Section -->
    <div class="chatbot-section">
      <div class="chatbot-container">
        <div class="chatbot-header">
          <h2>Assistant Virtuel</h2>
          <p>Besoin d'aide ? Notre assistant virtuel est là pour vous</p>
        </div>
        <button @click="openChatbot" class="chatbot-button">
          <span class="chatbot-icon">💬</span>
          Démarrer la conversation
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PublicPortal',
  methods: {
    openChatbot() {
      // Rediriger vers la page du chatbot
      this.$router.push('/chat')
    }
  }
}
</script>

<style scoped>
.public-portal {
  min-height: 100vh;
  background: #f8fafc;
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #4299e1 0%, #667eea 100%);
  color: white;
  padding: 6rem 2rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.hero-cta {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: transform 0.2s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
}

.cta-button.primary {
  background: white;
  color: #4299e1;
}

.cta-button.secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

/* Emergency Section */
.emergency-section {
  padding: 4rem 2rem;
  background: white;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 3rem;
}

.emergency-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.emergency-card {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.emergency-card:hover {
  transform: translateY(-5px);
}

.emergency-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.emergency-card h3 {
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.emergency-number {
  font-size: 2rem;
  font-weight: 700;
  color: #e53e3e;
  margin: 0.5rem 0;
}

.emergency-description {
  color: #718096;
  font-size: 0.9rem;
}

/* Services Section */
.services-section {
  padding: 4rem 2rem;
  background: #f8fafc;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.service-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
}

.service-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.service-card h3 {
  font-size: 1.5rem;
  color: #2d3748;
  margin-bottom: 1rem;
}

.service-card p {
  color: #718096;
  line-height: 1.6;
}

/* Chatbot Section */
.chatbot-section {
  padding: 4rem 2rem;
  background: white;
}

.chatbot-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.chatbot-header {
  margin-bottom: 2rem;
}

.chatbot-header h2 {
  font-size: 2rem;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.chatbot-header p {
  color: #718096;
}

.chatbot-button {
  background: #4299e1;
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.3s ease;
}

.chatbot-button:hover {
  background: #3182ce;
  transform: translateY(-2px);
}

.chatbot-icon {
  font-size: 1.5rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .hero-cta {
    flex-direction: column;
  }

  .section-title {
    font-size: 2rem;
  }

  .emergency-grid,
  .services-grid {
    grid-template-columns: 1fr;
  }
}
</style> 