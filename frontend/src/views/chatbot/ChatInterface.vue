<template>
  <div class="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
    <!-- En-tête -->
    <div class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white shadow-lg">
      <div class="container mx-auto px-4 py-3">
        <!-- Première ligne : Logo et titre -->
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <div class="bg-white bg-opacity-20 p-2 rounded-full mr-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold">MedLink Assistant</h1>
              <p class="text-xs opacity-90 font-light">
                <span v-if="userRole" class="font-medium">{{ userRole }}</span>
                <span v-else>Assistant médical intelligent</span>
              </p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <router-link 
              to="/public" 
              class="p-2 rounded-full hover:bg-blue-700 transition-colors duration-200" 
              title="Retour à l'accueil"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </router-link>
            <button @click="clearChat" class="p-2 rounded-full hover:bg-blue-700 transition-colors duration-200" title="Nouvelle conversation">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Sélecteur de type de session -->
        <div class="mt-3 flex space-x-1 overflow-x-auto pb-1">
          <button 
            v-for="type in sessionTypes" 
            :key="type.value"
            @click="changeSessionType(type.value)"
            class="px-3 py-1 text-sm rounded-full transition-colors duration-200 flex items-center"
            :class="{
              'bg-white text-blue-700': sessionType === type.value,
              'bg-blue-700 bg-opacity-20 text-white hover:bg-opacity-30': sessionType !== type.value
            }"
            :title="type.label"
          >
            <i :class="`fas fa-${type.icon} mr-1`"></i>
            <span class="whitespace-nowrap">{{ type.label }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Zone de chat -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 scroll-smooth">
      <!-- Message de bienvenue -->
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center px-4">
        <div class="max-w-md mx-auto">
          <div class="bg-white p-8 rounded-2xl shadow-lg mb-6 transform transition-all duration-300 hover:scale-105">
            <div class="text-blue-600 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold text-gray-800 mb-2">
              <template v-if="sessionType === 'MEDICAL'">
                Assistant Médical Professionnel
              </template>
              <template v-else-if="sessionType === 'TECHNICAL'">
                Support Technique
              </template>
              <template v-else-if="sessionType === 'ADMIN'">
                Administration
              </template>
              <template v-else>
                Bonjour ! 👋
              </template>
            </h2>
            
            <p class="text-gray-600 mb-6">
              <template v-if="sessionType === 'MEDICAL'">
                Je peux vous aider avec des questions médicales avancées, des procédures et des protocoles.
              </template>
              <template v-else-if="sessionType === 'TECHNICAL'">
                Besoin d'aide avec la plateforme ? Je suis là pour vous aider avec les problèmes techniques.
              </template>
              <template v-else-if="sessionType === 'ADMIN'">
                Gestion de la plateforme et administration du système.
              </template>
              <template v-else>
                Je suis votre assistant médical personnel. Posez-moi vos questions ou choisissez une suggestion ci-dessous.
              </template>
            </p>
            
            <div class="grid grid-cols-1 gap-3 mt-6">
              <button 
                v-for="(suggestion, index) in getCurrentSuggestions()" 
                :key="index"
                @click="usesuggestion(suggestion)"
                class="bg-white border border-blue-100 rounded-xl p-3 text-sm text-left hover:bg-blue-50 transition-colors duration-200 shadow-sm hover:shadow-md"
              >
                <div class="flex items-center">
                  <span class="bg-blue-100 text-blue-600 p-1.5 rounded-lg mr-3">
                    <i :class="`fas fa-${getSessionTypeIcon(sessionType)}`"></i>
                  </span>
                  <span class="text-gray-700">{{ suggestion }}</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Messages de conversation -->
      <div v-else class="max-w-4xl mx-auto space-y-4">
        <transition-group name="fade" tag="div" class="space-y-4">
          <div 
            v-for="(message, index) in messages" 
            :key="index"
            class="flex" 
            :class="message.type === 'USER' ? 'justify-end' : 'justify-start'"
          >
            <div 
              class="max-w-xs xs:max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl rounded-2xl px-4 py-3 shadow-sm transition-all duration-300 transform hover:scale-[1.02]"
              :class="message.type === 'USER' 
                ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-br-none' 
                : 'bg-white text-gray-800 rounded-bl-none border border-gray-100'"
            >
              <div class="prose prose-sm max-w-none">
                <p class="whitespace-pre-wrap">{{ message.content }}</p>
              </div>
              
              <!-- Évaluation du message du bot -->
              <div v-if="message.type === 'BOT'" class="mt-2 pt-2 border-t border-opacity-10 flex justify-end items-center">
                <div class="flex space-x-1">
                  <button 
                    v-for="rating in 5" 
                    :key="rating" 
                    @click="rateMessage(message, rating)"
                    class="text-sm focus:outline-none transition-all duration-200 transform hover:scale-125"
                    :class="message.rating && message.rating >= rating 
                      ? 'text-yellow-400 hover:text-yellow-500' 
                      : 'text-gray-300 hover:text-gray-400'"
                    :title="'Donner ' + rating + ' étoile(s)'"
                  >
                    ★
                  </button>
                </div>
              </div>
            </div>
          </div>
        </transition-group>

        <!-- Indicateur de frappe -->
        <div v-if="loading" class="flex justify-start">
          <div class="bg-white rounded-2xl rounded-bl-none border border-gray-100 px-4 py-3 shadow-sm">
            <div class="flex space-x-2">
              <div class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
              <div class="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
              <div class="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Zone de saisie -->
    <div class="border-t border-gray-200 bg-white/80 backdrop-blur-sm p-4">
      <!-- Suggestions rapides -->
      <div v-if="!messages.length" class="mb-3 overflow-x-auto pb-2">
        <div class="flex space-x-2">
          <button
            v-for="(suggestion, index) in suggestions"
            :key="index"
            @click="usesuggestion(suggestion)"
            class="flex-shrink-0 text-xs md:text-sm bg-white border border-blue-100 text-blue-600 rounded-full px-3 py-1.5 hover:bg-blue-50 transition-colors duration-200 shadow-sm"
          >
            {{ suggestion }}
          </button>
        </div>
      </div>

      <!-- Formulaire de saisie -->
      <form @submit.prevent="sendMessage" class="flex items-end gap-2">
        <div class="flex-1 relative">
          <textarea
            v-model="newMessage"
            placeholder="Écrivez votre message..."
            rows="1"
            class="w-full border border-gray-300 rounded-xl pl-4 pr-12 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            :disabled="loading"
            @keydown.enter.exact.prevent="sendMessage"
            @input="adjustTextareaHeight"
          ></textarea>
          <button
            type="button"
            @click="clearMessage"
            v-if="newMessage"
            class="absolute right-10 bottom-3 text-gray-400 hover:text-gray-600 focus:outline-none"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <button
          type="submit"
          :disabled="!newMessage.trim() || loading"
          class="h-12 w-12 flex-shrink-0 flex items-center justify-center bg-gradient-to-r from-blue-600 to-blue-500 text-white rounded-xl hover:from-blue-700 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105"
          :class="{ 'opacity-50 cursor-not-allowed': !newMessage.trim() }"
        >
          <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
          <div v-else class="flex space-x-1">
            <div class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-1.5 h-1.5 bg-white rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'ChatInterface',
  data() {
    return {
      sessionId: null,
      messages: [],
      newMessage: '',
      loading: false,
      isInitialized: false,  // Pour suivre l'initialisation
      sessionType: 'GENERAL',  // Type de session par défaut
      userRole: null,          // Rôle de l'utilisateur
      context: {},             // Contexte de la session
      suggestions: {
        // Suggestions pour le grand public
        GENERAL: [
          'Quels sont les symptômes du COVID-19?',
          'Comment prendre rendez-vous pour une radiographie?',
          'Quels sont les effets secondaires de l\'IRM?',
          'Comment me préparer pour un scanner?',
          'Combien de temps dure un examen d\'échographie?'
        ],
        // Suggestions pour les professionnels de santé
        MEDICAL: [
          'Procédure pour une ponction lombaire',
          'Posologie recommandée pour la ciprofloxacine',
          'Protocole de réanimation néonatale',
          'Critères diagnostiques du diabète',
          'Antibioprophylaxie en chirurgie propre'
        ],
        // Suggestions techniques
        TECHNICAL: [
          'Comment importer des images DICOM?',
          'Problème de connexion à la plateforme',
          'Mettre à jour mes informations personnelles',
          'Comment partager un dossier patient?',
          'Rapport de bug ou problème technique'
        ],
        // Suggestions administratives
        ADMIN: [
          'Statistiques d\'utilisation de la plateforme',
          'Gestion des utilisateurs',
          'Configuration des paramètres système',
          'Rapports d\'audit',
          'Sauvegarde des données'
        ]
      },
      // Options de type de session
      sessionTypes: [
        { value: 'GENERAL', label: 'Général', icon: 'users' },
        { value: 'MEDICAL', label: 'Médical', icon: 'stethoscope' },
        { value: 'TECHNICAL', label: 'Technique', icon: 'cog' },
        { value: 'ADMIN', label: 'Administratif', icon: 'shield-alt' }
      ]
    }
  },
  methods: {
    // Méthode pour changer le type de session
    changeSessionType(type) {
      this.sessionType = type
      // Réinitialiser la conversation avec le nouveau type
      this.clearChat()
    },
    
    // Méthode pour obtenir les suggestions en fonction du type de session
    getCurrentSuggestions() {
      return this.suggestions[this.sessionType] || this.suggestions.GENERAL
    },
    
    // Méthode pour obtenir l'icône du type de session
    getSessionTypeIcon(type) {
      const session = this.sessionTypes.find(s => s.value === type)
      return session ? session.icon : 'question'
    },
    
    async sendMessage() {
      if (!this.newMessage.trim()) return
      
      const messageToSend = this.newMessage
      
      // Créer le message utilisateur pour l'affichage
      const userMessage = {
        type: 'USER',
        content: messageToSend,
        timestamp: new Date().toISOString(),
        sessionType: this.sessionType
      }
      
      this.messages.push(userMessage)
      this.newMessage = ''
      this.loading = true
      
      // Réinitialiser la hauteur du textarea
      this.$nextTick(() => {
        this.adjustTextareaHeight()
      })
      
      try {
        const response = await api.post('/chatbot/request/', {
          message: messageToSend,
          session_id: this.sessionId,
          user_id: this.$store.state.auth.user?.id,
          session_type: this.sessionType  // Envoyer le type de session
        })
        
        // Mettre à jour le contexte et le rôle si fournis dans la réponse
        if (response.data.context) {
          this.context = response.data.context
        }
        if (response.data.user_role) {
          this.userRole = response.data.user_role
        }
        if (response.data.session_type) {
          this.sessionType = response.data.session_type
        }
        
        // Mettre à jour l'ID de session
        this.sessionId = response.data.session_id
        
        // Ajouter la réponse du bot
        const botMessage = {
          type: 'BOT',
          content: response.data.response,
          id: response.data.message_id,
          timestamp: new Date().toISOString()
        }
        
        this.messages.push(botMessage)
      } catch (error) {
        console.error('Erreur lors de l\'envoi du message:', error)
        
        // Ajouter un message d'erreur
        this.messages.push({
          type: 'BOT',
          content: 'Désolé, une erreur s\'est produite. Veuillez réessayer plus tard.',
          timestamp: new Date().toISOString()
        })
      } finally {
        this.loading = false
        
        this.$nextTick(() => {
          this.scrollToBottom()
        })
      }
    },
    
    usesuggestion(suggestion) {
      this.newMessage = suggestion
      this.sendMessage()
    },
    
    clearMessage() {
      this.newMessage = ''
      this.adjustTextareaHeight()
    },
    
    async clearChat() {
      // Fonction pour réinitialiser la conversation
      const resetConversation = async () => {
        try {
          // Créer une nouvelle session côté serveur
          const response = await api.post('/chatbot/session/', {})
          
          // Mettre à jour l'état local
          this.messages = []
          this.sessionId = response.data.session_id
          
          // Effacer le stockage local
          localStorage.removeItem('chatSession')
          
          // Sauvegarder la nouvelle session
          this.saveSessionToStorage()
          
          // Forcer la mise à jour du DOM
          this.$nextTick(() => {
            // Faire défiler vers le haut
            if (this.$refs.chatContainer) {
              this.$refs.chatContainer.scrollTop = 0
            }
            
            // Afficher un message de confirmation
            if (this.$toast) {
              this.$toast.success('Nouvelle conversation démarrée', { timeout: 2000 })
            } else if (window.alert) {
              alert('Nouvelle conversation démarrée')
            }
          })
          
          return true
        } catch (error) {
          console.error('Erreur lors de la création d\'une nouvelle session:', error)
          return false
        }
      }
      
      // Vérifier s'il y a des messages à effacer
      const hasMessages = this.messages && this.messages.length > 0
      
      // Si pas de messages, créer directement une nouvelle session
      if (!hasMessages) {
        await resetConversation()
        return
      }
      
      // Utiliser la boîte de dialogue native pour la confirmation
      const confirmed = window.confirm('Voulez-vous vraiment démarrer une nouvelle conversation ? L\'historique actuel sera effacé.')
      
      if (confirmed) {
        try {
          const success = await resetConversation()
          if (!success) {
            throw new Error('Échec de la création d\'une nouvelle session')
          }
        } catch (error) {
          console.error('Erreur lors de la réinitialisation de la conversation:', error)
          alert('Une erreur est survenue lors de la création d\'une nouvelle conversation.')
        }
      }
    },
    
    adjustTextareaHeight() {
      const textarea = this.$el.querySelector('textarea')
      if (textarea) {
        textarea.style.height = 'auto'
        textarea.style.height = `${Math.min(textarea.scrollHeight, 150)}px`
      }
    },
    
    scrollToBottom() {
      if (this.$refs.chatContainer) {
        this.$refs.chatContainer.scrollTo({
          top: this.$refs.chatContainer.scrollHeight,
          behavior: 'smooth'
        })
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return new Intl.DateTimeFormat('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
      }).format(date)
    },
    
    async rateMessage(message, rating) {
      if (!message.id) return
      
      // Sauvegarder l'ancienne valeur pour la réinitialiser en cas d'erreur
      const oldRating = message.rating
      
      // Mettre à jour l'interface utilisateur immédiatement
      message.rating = rating
      
      try {
        const response = await api.post('/chatbot/feedback/', {
          message: message.id,  // Le backend attend 'message' et non 'message_id'
          rating: rating,
          comment: ''  // Ajouter un commentaire vide pour être sûr
        })
        console.log('Feedback enregistré:', response.data)
      } catch (error) {
        console.error('Erreur lors de l\'envoi du feedback:', error)
        // Revenir à l'ancienne valeur en cas d'erreur
        message.rating = oldRating
      }
    },
    
    async loadSessionFromStorage() {
      try {
        const savedSession = localStorage.getItem('chatSession')
        if (savedSession) {
          const session = JSON.parse(savedSession)
          
          // Vérifier si la session existe côté serveur
          if (session.id) {
            try {
              const response = await api.get(`/chatbot/sessions/${session.id}/`)
              if (response.data && response.data.id) {
                this.sessionId = response.data.id
                this.messages = response.data.messages || []
                return
              }
            } catch (error) {
              console.warn('Session introuvable côté serveur, création d\'une nouvelle session', error)
              // Continuer pour créer une nouvelle session
            }
          }
        }
        
        // Si on arrive ici, il faut créer une nouvelle session
        this.sessionId = null
        this.messages = []
        
      } catch (e) {
        console.error('Erreur lors du chargement de la session:', e)
        localStorage.removeItem('chatSession')
        this.sessionId = null
        this.messages = []
      }
    },
    
    async saveSessionToStorage() {
      if (!this.isInitialized) return
      
      try {
        const session = {
          id: this.sessionId,
          messages: this.messages
        }
        
        // Sauvegarder localement
        localStorage.setItem('chatSession', JSON.stringify(session))
        
        // Si pas de session ID, on ne peut pas sauvegarder côté serveur
        if (!this.sessionId) return
        
        // Sauvegarder côté serveur si possible
        try {
          await api.put(`/chatbot/sessions/${this.sessionId}/`, {
            messages: this.messages,
            last_activity: new Date().toISOString()
          })
        } catch (error) {
          console.error('Erreur lors de la sauvegarde côté serveur:', error)
          if (error.response) {
            console.error('Détails de l\'erreur:', error.response.data)
          }
          // On continue même en cas d'erreur côté serveur
        }
      } catch (e) {
        console.error('Erreur lors de la sauvegarde de la session:', e)
      }
    }
  },
  
  watch: {
    messages: {
      handler() {
        if (this.isInitialized) {
          this.saveSessionToStorage()
        }
      },
      deep: true
    },
    
    sessionId() {
      if (this.isInitialized) {
        this.saveSessionToStorage()
      }
    },
    
    newMessage() {
      this.$nextTick(() => {
        this.adjustTextareaHeight()
      })
    }
  },
  
  async mounted() {
    // Charger la session existante ou en créer une nouvelle
    await this.loadSessionFromStorage()
    
    // Si aucune session n'existe, en créer une nouvelle
    if (!this.sessionId) {
      await this.clearChat()
    }
    
    this.$nextTick(() => {
      this.scrollToBottom()
      this.isInitialized = true
    })
    
    // Ajouter un écouteur d'événement pour le redimensionnement de la fenêtre
    window.addEventListener('resize', this.adjustTextareaHeight)
  },
  
  beforeUnmount() {
    // Nettoyer l'écouteur d'événement
    window.removeEventListener('resize', this.adjustTextareaHeight)
  }
}
</script>

<style scoped>
/* Animations */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Styles personnalisés */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Styles pour les messages */
.prose {
  max-width: 100%;
  line-height: 1.6;
}

.prose p {
  margin-bottom: 0.5em;
}

.prose p:last-child {
  margin-bottom: 0;
}

/* Barre de défilement personnalisée */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}

/* Animation de rebond pour les indicateurs de chargement */
.animate-bounce {
  animation: bounce 0.8s infinite ease-in-out;
  display: inline-block;
}

/* Transition pour les boutons */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Ajustements pour mobile */
@media (max-width: 640px) {
  .prose {
    font-size: 0.9375rem;
  }
  
  .prose p {
    line-height: 1.5;
  }
}

/* Effet de verre pour la zone de saisie */
.bg-white\/80 {
  background-color: rgba(255, 255, 255, 0.8);
}

.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}

/* Animation d'entrée pour les messages */
.message-enter-active {
  animation: fadeIn 0.3s ease-out;
}

/* Style pour les liens dans les messages */
.prose a {
  color: #3b82f6;
  text-decoration: underline;
  transition: color 0.2s;
}

.prose a:hover {
  color: #2563eb;
}

/* Style pour les listes dans les messages */
.prose ul {
  list-style-type: disc;
  padding-left: 1.5em;
  margin: 0.5em 0;
}

.prose ol {
  list-style-type: decimal;
  padding-left: 1.5em;
  margin: 0.5em 0;
}

/* Style pour le code dans les messages */
.prose code {
  background-color: rgba(0, 0, 0, 0.05);
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

/* Style pour les citations */
.prose blockquote {
  border-left: 3px solid #e5e7eb;
  padding-left: 1em;
  margin: 1em 0;
  color: #6b7280;
  font-style: italic;
}
</style>