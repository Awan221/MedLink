<template>
  <div class="ai-diagnostic-container">
    <div class="header-section">
      <h1 class="page-title">Assistant Diagnostic IA</h1>
      <p class="page-description">
        Analysez les symptômes et obtenez des suggestions de diagnostic assistées par l'IA
      </p>
    </div>

    <div class="main-content">
      <div class="input-section">
        <div class="form-group">
          <label for="symptoms" class="form-label">Symptômes</label>
          <textarea
            id="symptoms"
            v-model="symptoms"
            class="form-control symptoms-input"
            rows="4"
            placeholder="Décrivez les symptômes du patient..."
          ></textarea>
        </div>

        <div class="form-group">
          <label for="medicalHistory" class="form-label">Antécédents médicaux</label>
          <textarea
            id="medicalHistory"
            v-model="medicalHistory"
            class="form-control"
            rows="3"
            placeholder="Antécédents médicaux pertinents..."
          ></textarea>
        </div>

        <div class="form-group">
          <label for="medications" class="form-label">Médicaments actuels</label>
          <textarea
            id="medications"
            v-model="medications"
            class="form-control"
            rows="2"
            placeholder="Liste des médicaments en cours..."
          ></textarea>
        </div>

        <button 
          @click="analyzeSymptoms" 
          class="analyze-button"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          {{ isLoading ? 'Analyse en cours...' : 'Analyser les symptômes' }}
        </button>
      </div>

      <div class="results-section" v-if="diagnosis">
        <div class="results-card">
          <h2 class="results-title">Résultats de l'analyse</h2>
          
          <div class="diagnosis-section">
            <h3 class="section-title">Diagnostic suggéré</h3>
            <p class="diagnosis-text">{{ diagnosis.diagnosis }}</p>
          </div>

          <div class="confidence-section">
            <h3 class="section-title">Niveau de confiance</h3>
            <div class="confidence-bar">
              <div 
                class="confidence-fill"
                :style="{ width: `${diagnosis.confidence}%` }"
              ></div>
            </div>
            <span class="confidence-value">{{ diagnosis.confidence }}%</span>
          </div>

          <div class="recommendations-section">
            <h3 class="section-title">Recommandations</h3>
            <ul class="recommendations-list">
              <li v-for="(rec, index) in diagnosis.recommendations" 
                  :key="index"
                  class="recommendation-item">
                {{ rec }}
              </li>
            </ul>
          </div>

          <div class="actions-section">
            <button @click="saveDiagnosis" class="action-button save-button">
              Sauvegarder le diagnostic
            </button>
            <button @click="resetForm" class="action-button reset-button">
              Nouvelle analyse
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'AIDiagnostic',
  data() {
    return {
      patients: [],
      models: [],
      predictions: [],
      patientStudies: [],
      selectedPatientId: '',
      selectedModelId: '',
      selectedStudyId: '',
      additionalData: '',
      loading: false,
      showValidationModal: false,
      selectedPrediction: null,
      validationNotes: '',
      symptoms: '',
      medicalHistory: '',
      medications: '',
      diagnosis: null,
      isLoading: false
    }
  },
  computed: {
    canRunDiagnostic() {
      return this.selectedPatientId && this.selectedModelId
    }
  },
  methods: {
    async fetchPatients() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}patients/`)
        this.patients = response.data.results
      } catch (error) {
        console.error('Erreur lors de la récupération des patients:', error)
      }
    },
    async fetchModels() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}ai-diagnostic/models/`)
        this.models = response.data.results
      } catch (error) {
        console.error('Erreur lors de la récupération des modèles:', error)
      }
    },
    async fetchPredictions() {
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}ai-diagnostic/predictions/`)
        this.predictions = response.data.results
      } catch (error) {
        console.error('Erreur lors de la récupération des prédictions:', error)
      }
    },
    async fetchPatientStudies() {
      if (!this.selectedPatientId) {
        this.patientStudies = []
        return
      }
      
      try {
        const response = await axios.get(`${process.env.VUE_APP_API_URL}imaging/studies/?patient=${this.selectedPatientId}`)
        this.patientStudies = response.data.results
      } catch (error) {
        console.error('Erreur lors de la récupération des études:', error)
      }
    },
    async runDiagnostic() {
      if (!this.canRunDiagnostic) return
      
      this.loading = true
      
      try {
        const payload = {
          patient_id: this.selectedPatientId,
          model_id: this.selectedModelId,
          input_data: {
            additional_data: this.additionalData
          }
        }
        
        if (this.selectedStudyId) {
          payload.medical_record_id = this.selectedStudyId
          payload.input_data.study_id = this.selectedStudyId
        }
        
        const response = await axios.post(`${process.env.VUE_APP_API_URL}ai-diagnostic/predictions/predict/`, payload)
        
        // Ajouter la nouvelle prédiction à la liste
        this.predictions.unshift(response.data)
        
        // Réinitialiser le formulaire
        this.additionalData = ''
        
        // Afficher un message de succès
        alert('Analyse terminée avec succès!')
      } catch (error) {
        console.error('Erreur lors de l\'analyse:', error)
        alert('Une erreur s\'est produite lors de l\'analyse. Veuillez réessayer.')
      } finally {
        this.loading = false
      }
    },
    viewPrediction(prediction) {
      // Rediriger vers la page de détail de la prédiction
      this.$router.push(`/ai/predictions/${prediction.id}`)
    },
    validatePrediction(prediction) {
      this.selectedPrediction = prediction
      this.validationNotes = ''
      this.showValidationModal = true
    },
    closeValidationModal() {
      this.showValidationModal = false
      this.selectedPrediction = null
    },
    async submitValidation() {
      if (!this.selectedPrediction) return
      
      try {
        await axios.post(`/ai/predictions/${this.selectedPrediction.id}/validate/`, {
          validated: true,
          validation_notes: this.validationNotes
        })
        
        // Mettre à jour la prédiction dans la liste
        const index = this.predictions.findIndex(p => p.id === this.selectedPrediction.id)
        if (index !== -1) {
          this.predictions[index].validated = true
          this.predictions[index].validation_notes = this.validationNotes
        }
        
        this.closeValidationModal()
        alert('Prédiction validée avec succès!')
      } catch (error) {
        console.error('Erreur lors de la validation:', error)
        alert('Une erreur s\'est produite lors de la validation. Veuillez réessayer.')
      }
    },
    getModelName(modelId) {
      const model = this.models.find(m => m.id === modelId)
      return model ? model.name : modelId
    },
    getSeverityLabel(severity) {
      const labels = {
        'LOW': 'Faible',
        'MEDIUM': 'Moyenne',
        'HIGH': 'Élevée',
        'CRITICAL': 'Critique'
      }
      return labels[severity] || severity
    },
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    formatDateTime(dateTimeString) {
      if (!dateTimeString) return ''
      const date = new Date(dateTimeString)
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`
    },
    async analyzeSymptoms() {
      this.isLoading = true
      try {
        const response = await axios.post(`${process.env.VUE_APP_API_URL}ai-diagnostic/predictions/analyze/`, {
          symptoms: this.symptoms,
          medical_history: this.medicalHistory,
          medications: this.medications
        })
        this.diagnosis = response.data
      } catch (error) {
        console.error('Erreur lors de l\'analyse des symptômes:', error)
        alert('Une erreur s\'est produite lors de l\'analyse des symptômes. Veuillez réessayer.')
      } finally {
        this.isLoading = false
      }
    },
    saveDiagnosis() {
      // Implementation of saveDiagnosis method
    },
    resetForm() {
      this.symptoms = ''
      this.medicalHistory = ''
      this.medications = ''
      this.diagnosis = null
    }
  },
  watch: {
    selectedPatientId() {
      this.fetchPatientStudies()
    }
  },
  created() {
    this.fetchPatients()
    this.fetchModels()
    this.fetchPredictions()
  }
}
</script>

<style scoped>
.ai-diagnostic-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header-section {
  text-align: center;
  margin-bottom: 3rem;
}

.page-title {
  font-size: 2.5rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.page-description {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.input-section {
  background: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: #4299e1;
}

.symptoms-input {
  min-height: 120px;
}

.analyze-button {
  width: 100%;
  padding: 1rem;
  background: #4299e1;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.analyze-button:hover {
  background: #3182ce;
}

.analyze-button:disabled {
  background: #a0aec0;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid #ffffff;
  border-top: 3px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.results-section {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.results-card {
  padding: 2rem;
}

.results-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 2rem;
  text-align: center;
}

.section-title {
  font-size: 1.2rem;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.diagnosis-text {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #4a5568;
  margin-bottom: 1.5rem;
}

.confidence-section {
  margin: 2rem 0;
}

.confidence-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.confidence-fill {
  height: 100%;
  background: #48bb78;
  transition: width 0.3s ease;
}

.confidence-value {
  font-size: 0.9rem;
  color: #718096;
}

.recommendations-list {
  list-style: none;
  padding: 0;
}

.recommendation-item {
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: #f7fafc;
  border-radius: 6px;
  color: #4a5568;
}

.actions-section {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.save-button {
  background: #48bb78;
  color: white;
}

.save-button:hover {
  background: #38a169;
}

.reset-button {
  background: #e2e8f0;
  color: #4a5568;
}

.reset-button:hover {
  background: #cbd5e0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .ai-diagnostic-container {
    padding: 1rem;
  }
  
  .page-title {
    font-size: 2rem;
  }
}
</style>