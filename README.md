# MedLink - Plateforme de Télémédecine Intégrée

## 📋 Aperçu

MedLink est une plateforme complète de télémédecine conçue pour faciliter la gestion des dossiers patients, la téléradiologie, la banque de sang et l'assistance médicale via un chatbot intelligent. La solution intègre des fonctionnalités avancées d'imagerie médicale avec Orthanc et propose une interface moderne et intuitive.

## ✨ Fonctionnalités Principales

- **Gestion des Utilisateurs et Authentification**
  - Inscription et authentification sécurisée
  - Gestion des rôles et permissions (Médecins, Spécialistes, Administrateurs)
  - Tableau de bord personnalisé par profil

- **Dossier Médical Électronique**
  - Création et gestion des dossiers patients
  - Historique médical complet
  - Gestion des consultations et prescriptions

- **Téléradiologie**
  - Visualisation DICOM avec OHIF Viewer
  - Partage sécurisé d'images médicales
  - Annotation et mesure des images

- **Banque de Sang**
  - Gestion des stocks de sang
  - Suivi des dons
  - Interface publique pour les donneurs

- **Chatbot Médical**
  - Assistance en temps réel
  - Réponses basées sur l'IA
  - Support multilingue

## 🚀 Technologies Utilisées

### Frontend
- Vue.js 3 (Composition API)
- Vue Router & Vuex
- Tailwind CSS
- OHIF Viewer (DICOM)
- Leaflet.js (Cartographie)

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL avec PostGIS
- Celery (tâches asynchrones)
- Redis (cache et file d'attente)

### Infrastructure
- Docker & Docker Compose
- Nginx (reverse proxy)
- Let's Encrypt (SSL)
- Monitoring avec Prometheus/Grafana

## 🛠 Installation

### Prérequis
- Docker 20.10+
- Docker Compose 2.0+
- Node.js 16+
- Python 3.9+

### Démarrage Rapide

```bash
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/medlink.git
cd medlink

# Démarrer les services
docker-compose up -d

# Installer les dépendances frontend
cd frontend
npm install
npm run serve
```

## 📚 Documentation

- [Documentation Technique](./docs/TECHNICAL_DOCUMENTATION.md)
- [Documentation Fonctionnelle](./docs/FUNCTIONAL_DOCUMENTATION.md)

## 📞 Contact

Pour toute question ou suggestion, veuillez ouvrir une issue ou nous contacter à contact@medlink.example.com
