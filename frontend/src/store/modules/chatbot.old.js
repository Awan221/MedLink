import chatService from '@/services/chatService';

const state = {
  // Session et état du chat
  sessionId: null,
  messages: [],
  isLoading: false,
  isChatOpen: false,
  error: null,
  messageCount: 0,
  botStatus: 'idle', // 'idle', 'typing', 'waiting', 'error'
  
  // Paramètres utilisateur
  userRole: 'anonymous',
  settings: {
    theme: 'light',
    fontSize: 'medium',
    notifications: true
  },
  
  // Suggestions
  suggestions: [],
  isSuggestionsLoading: false
};
  isChatOpen: false,
  
  // Messages
  messages: [],
  isLoading: false,
  error: null,
  
  // Configuration
  settings: {
    enableNotifications: true,
    darkMode: false,
    fontSize: 'medium', // small, medium, large
    language: 'fr',
  },
  
  // État de l'assistant
  botStatus: 'idle', // idle, typing, waiting_for_input
  
  // Historique des conversations
  conversationHistory: [],
  currentConversationId: null,
  
  // Métriques
  messageCount: 0,
  lastInteraction: null,
  
  // État de la reconnaissance vocale
  isListening: false,
  isSpeechAvailable: 'speechSynthesis' in window,
  
  // État des suggestions
  suggestions: [],
  isSuggestionsLoading: false,
};

const getters = {
  // Getters de base
  getMessages: (state) => state.messages,
  getIsLoading: (state) => state.isLoading,
  getError: (state) => state.error,
  getIsChatOpen: (state) => state.isChatOpen,
  getBotStatus: (state) => state.botStatus,
  getSessionId: (state) => state.sessionId,
  getSettings: (state) => state.settings,
  getSuggestions: (state) => state.suggestions,
  isSuggestionsLoading: (state) => state.isSuggestionsLoading,
  
  // Getters calculés
  unreadMessageCount: (state) => 
    state.messages.filter(msg => !msg.read && msg.sender === 'bot').length,
    
  lastMessage: (state) => 
    state.messages.length > 0 ? state.messages[state.messages.length - 1] : null,
    
  conversationHistory: (state) => state.conversationHistory,
  currentConversation: (state) => 
    state.conversationHistory.find(conv => conv.id === state.currentConversationId) || null,
};

const actions = {
  // Initialisation
  async initializeChatbot({ commit, dispatch }) {
    try {
      // Vérifier si une session existe déjà
      const savedSession = localStorage.getItem('chatbot_session');
      
      if (savedSession) {
        const session = JSON.parse(savedSession);
        commit('SET_SESSION', session.id);
        commit('SET_MESSAGES', session.messages || []);
      } else {
        // Créer une nouvelle session
        const sessionId = 'chat_' + Math.random().toString(36).substr(2, 9);
        commit('SET_SESSION', sessionId);
        
        // Enregistrer la session
        dispatch('saveSession');
        
        // Envoyer un message de bienvenue
        dispatch('sendWelcomeMessage');
      }
      
      // Charger l'historique des conversations
      await dispatch('loadConversationHistory');
      
      return { success: true };
    } catch (error) {
      console.error('Erreur lors de l\'initialisation du chatbot:', error);
      commit('SET_ERROR', 'Impossible d\'initialiser le chatbot');
      return { success: false, error: error.message };
    }
  },

  // Action pour initialiser le chatbot
  async initializeChatbot({ commit, dispatch }) {
    try {
      // Vérifier si une session existe déjà
      const savedSession = localStorage.getItem('chatbot_session');
      const savedRole = localStorage.getItem('chatbot_userRole');
      
      // Restaurer le rôle utilisateur s'il existe
      if (savedRole) {
        commit('SET_USER_ROLE', savedRole);
      }
      
      if (savedSession) {
        const session = JSON.parse(savedSession);
        commit('SET_SESSION', session.id);
        commit('SET_MESSAGES', session.messages || []);
      } else {
        // Créer une nouvelle session
        const sessionId = 'chat_' + Math.random().toString(36).substr(2, 9);
        commit('SET_SESSION', sessionId);
        await dispatch('saveSession');
      }
      
      return { success: true };
    } catch (error) {
      console.error('Erreur lors de l\'initialisation du chatbot:', error);
      commit('SET_ERROR', 'Impossible d\'initialiser le chatbot');
      return { success: false, error: error.message };
    }
  },
  
  // Action pour envoyer un message
  async sendChatMessage({ commit, state, dispatch }, { content, type = 'text', metadata = {} }) {
    if (!content || state.isLoading) return;
    
    // Créer le message utilisateur
    const userMessage = {
      id: 'msg_' + Date.now(),
      content,
      type: 'USER',
      role: state.userRole || 'anonymous',
      timestamp: new Date().toISOString(),
      metadata: {
        ...metadata,
        user_agent: process.client ? navigator.userAgent : '',
        ip_address: '' // Serait rempli côté serveur
      }
    };
    
    // Ajouter le message à l'interface
    commit('ADD_MESSAGE', userMessage);
    commit('SET_LOADING', true);
    commit('SET_BOT_STATUS', 'typing');
    
    try {
      // Envoyer le message au backend
      const response = await chatService.sendMessage(state.sessionId, {
        content,
        type,
        metadata: {
          ...metadata,
          user_role: state.userRole,
          session_id: state.sessionId
        }
      });
      
      // Ajouter la réponse du bot
      const botMessage = {
        id: 'msg_' + Date.now() + 1,
        content: response.content,
        type: 'BOT',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        metadata: response.metadata || {},
        rating: null
      };
      
      commit('ADD_MESSAGE', botMessage);
      commit('SET_LAST_INTERACTION', new Date().toISOString());
      
      // Sauvegarder la session après l'envoi du message
      await dispatch('saveSession');
      
      return response;
      
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      
      // Ajouter un message d'erreur
      const errorMessage = {
        id: 'err_' + Date.now(),
        content: error.response?.data?.message || 'Désolé, une erreur est survenue. Veuillez réessayer plus tard.',
        type: 'BOT',
        role: 'assistant',
        timestamp: new Date().toISOString(),
        isError: true
      };
      
      commit('ADD_MESSAGE', errorMessage);
      commit('SET_ERROR', error.response?.data?.message || 'Erreur lors de l\'envoi du message');
      
      throw error;
      
    } finally {
      commit('SET_LOADING', false);
      commit('SET_BOT_STATUS', 'idle');
    }
  },
  
  // Action pour noter un message
  async rateMessage({ commit, state }, { messageId, rating, metadata = {} }) {
    try {
      await chatService.sendFeedback(messageId, {
        rating,
        metadata: {
          ...metadata,
          user_role: state.userRole,
          session_id: state.sessionId
        }
      });
      
      // Mettre à jour la note dans l'état local
      commit('UPDATE_MESSAGE_RATING', { messageId, rating });
      
      return { success: true };
      
    } catch (error) {
      console.error('Erreur lors de l\'évaluation du message:', error);
      commit('SET_ERROR', 'Impossible d\'enregistrer votre évaluation');
      return { success: false, error: error.message };
    }
  },
  
  // Action pour charger l'historique des conversations
  async loadConversationHistory({ commit }) {
    try {
      if (!state.sessionId) return;
      
      const messages = await chatService.getSessionMessages(state.sessionId);
      
      // Transformer les messages au format attendu
      const formattedMessages = messages.map(msg => ({
        ...msg,
        type: msg.sender === 'user' ? 'USER' : 'BOT',
        role: msg.sender === 'user' ? state.userRole : 'assistant'
      }));
      
      commit('SET_MESSAGES', formattedMessages);
      return formattedMessages;
      
    } catch (error) {
      console.error('Erreur lors du chargement de l\'historique:', error);
      commit('SET_ERROR', 'Impossible de charger l\'historique des conversations');
      throw error;
    }
  },
  
  // Action pour sauvegarder la session
  async saveSession({ state }) {
    if (!process.client) return;
    
    try {
      const sessionData = {
        id: state.sessionId,
        messages: state.messages,
        lastUpdated: new Date().toISOString()
      };
      
      localStorage.setItem('chatbot_session', JSON.stringify(sessionData));
      return { success: true };
      
    } catch (error) {
      console.error('Erreur lors de la sauvegarde de la session:', error);
      return { success: false, error: error.message };
    }
  },
  
  // Action pour effacer les erreurs
  clearError({ commit }) {
    commit('CLEAR_ERROR');
  },
  
  // Action pour envoyer un message (version précédente, à supprimer après vérification)
  async sendMessage({ commit, state, dispatch }, { content, type = 'text', metadata = {} }) {
    if (!content || state.isLoading) return;

    // Créer une nouvelle session si elle n'existe pas
    if (!state.sessionId) {
      try {
        const sessionData = {
          user_id: localStorage.getItem('user_id') || 'anonymous',
          message: content
        };
        const session = await chatService.createSession(sessionData);
        commit('SET_SESSION', session.id);
      } catch (error) {
        console.error('Erreur lors de la création de la session:', error);
        commit('SET_ERROR', 'Impossible de démarrer la conversation');
        return { success: false, error: error.message };
      }
    }

    // Créer et ajouter le message de l'utilisateur
    const userMessage = {
      id: `msg-${Date.now()}`,
      content,
      type,
      metadata,
      sender: 'user',
      timestamp: new Date().toISOString(),
      read: true
    };
    
    commit('ADD_MESSAGE', userMessage);
    commit('SET_LOADING', true);
    commit('SET_BOT_STATUS', 'typing');
    commit('SET_LAST_INTERACTION', new Date().toISOString());

    try {
      // Envoyer le message au serveur
      const response = await chatService.sendMessage(state.sessionId, {
        message: content,
        sender: 'user',
        type,
        metadata
      });

      // Traiter la réponse du bot
      if (response && response.message) {
        const botMessage = {
          id: `msg-${Date.now()}`,
          content: response.message.content,
          type: response.message.type || 'text',
          metadata: response.message.metadata || {},
          sender: 'bot',
          timestamp: new Date().toISOString(),
          read: false
        };
        
        commit('ADD_MESSAGE', botMessage);
        
        // Mettre à jour les suggestions si présentes dans la réponse
        if (response.suggestions) {
          commit('SET_SUGGESTIONS', response.suggestions);
        }
      }
      
      // Sauvegarder la session
      await dispatch('saveSession');
      
      return { success: true };
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
      
      // Créer un message d'erreur pour l'utilisateur
      const errorMessage = {
        id: `error-${Date.now()}`,
        content: 'Désolé, une erreur est survenue. Veuillez réessayer plus tard.',
        type: 'error',
        sender: 'system',
        timestamp: new Date().toISOString(),
        read: true
      };
      
      commit('ADD_MESSAGE', errorMessage);
      commit('SET_ERROR', error.message || 'Erreur lors de la communication avec le serveur');
      
      return { success: false, error: error.message };
    } finally {
      commit('SET_LOADING', false);
      commit('SET_BOT_STATUS', 'idle');
  toggleChat({ commit, state }) {
    const newState = !state.isChatOpen;
    commit('SET_CHAT_OPEN', newState);
    
    // Marquer les messages comme lus lorsque le chat est ouvert
    if (newState) {
      commit('MARK_MESSAGES_AS_READ');
    }
    
    return newState;
  },
  
  // Gestion des paramètres
  updateSettings({ commit }, newSettings) {
    commit('UPDATE_SETTINGS', newSettings);
    // Ici, vous pourriez également sauvegarder les paramètres sur le serveur
    return { success: true };
  },
  
  // Gestion des suggestions
  async loadSuggestions({ commit,axios}, query) {
    if (!query || query.length < 2) {
      commit('SET_SUGGESTIONS', []);
      return [];
    }
    
    commit('SET_SUGGESTIONS_LOADING', true);
    
    try {
      const response = await axios.get(`/chat/suggestions/?q=${encodeURIComponent(query)}`);
      commit('SET_SUGGESTIONS', response.data.suggestions || []);
      return response.data.suggestions || [];
    } catch (error) {
      console.error('Erreur lors du chargement des suggestions:', error);
      commit('SET_SUGGESTIONS', []);
      return [];
    } finally {
      commit('SET_SUGGESTIONS_LOADING', false);
    }
  },
  
  // Message de bienvenue
  sendWelcomeMessage({ commit}) {
    const welcomeMessage = {
      id: `welcome_${Date.now()}`,
      content: 'Bonjour ! Je suis votre assistant médical. Comment puis-je vous aider aujourd\'hui ?',
      type: 'text',
      sender: 'bot',
      timestamp: new Date().toISOString(),
      metadata: {
        isWelcome: true,
        quickReplies: [
          { text: 'Prendre un rendez-vous', payload: 'RDV' },
          { text: 'Questions médicales', payload: 'QUESTIONS' },
          { text: 'Trouver un médecin', payload: 'FIND_DOCTOR' },
        ]
      },
      read: false
    };

const mutations = {
  // Mutations de base
  SET_LOADING(state, isLoading) {
    state.isLoading = isLoading;
  },
  
  SET_ERROR(state, error) {
    state.error = error;
  },
  
  // Gestion des sessions
  SET_SESSION(state, sessionId) {
    state.sessionId = sessionId;
  },
  
  // Gestion des messages
  SET_MESSAGES(state, messages) {
    state.messages = messages;
  },
  
  ADD_MESSAGE(state, message) {
    state.messages.push(message);
    state.messageCount++;
  },
  
  UPDATE_MESSAGE_RATING(state, { messageId, rating }) {
    const message = state.messages.find(m => m.id === messageId);
    if (message) {
      message.rating = rating;
    }
  },
  
  // Gestion de l'interface utilisateur
  SET_CHAT_OPEN(state, isOpen) {
    state.isChatOpen = isOpen;
  },
  
  SET_BOT_STATUS(state, status) {
    state.botStatus = status;
  },
  
  // Gestion des paramètres
  UPDATE_SETTINGS(state, settings) {
    state.settings = { ...state.settings, ...settings };
  },
  
  // Gestion des suggestions
  SET_SUGGESTIONS_LOADING(state, isLoading) {
    state.isSuggestionsLoading = isLoading;
  },
  
  SET_SUGGESTIONS(state, suggestions) {
    state.suggestions = suggestions;
  },
  
    // Gestion des erreurs
  CLEAR_ERROR(state) {
    state.error = null;
  },
  
  // Gestion du rôle utilisateur
  SET_USER_ROLE(state, role) {
    state.userRole = role;
    if (process.client) {
      localStorage.setItem('chatbot_userRole', role);
    }
  },
  
  // Réinitialisation de l'état
  RESET_STATE(state) {
    const { settings } = state;
    
    Object.assign(state, {
      messages: [],
      sessionId: null,
      isLoading: false,
      error: null,
      botStatus: 'idle',
      suggestions: [],
      isSuggestionsLoading: false,
      settings
    });
  }
  
  SET_MESSAGES(state, messages) {
    state.messages = messages;
  },
  
  ADD_MESSAGE(state, message) {
    state.messages.push(message);
    state.messageCount++;
  },
  
  SET_CHAT_OPEN(state, isOpen) {
    state.isChatOpen = isOpen;
  },
  
  SET_BOT_STATUS(state, status) {
    state.botStatus = status;
  },
  
  // Gestion des messages
  MARK_MESSAGES_AS_READ(state) {
    state.messages = state.messages.map(msg => ({
      ...msg,
      read: true
    }));
  },
  
  // Gestion des paramètres
  UPDATE_SETTINGS(state, newSettings) {
    state.settings = {
      ...state.settings,
      ...newSettings
    };
  },
  
  // Gestion de l'historique
  SET_CONVERSATION_HISTORY(state, history) {
    state.conversationHistory = history;
  },
  
  SET_CURRENT_CONVERSATION(state, conversationId) {
    state.currentConversationId = conversationId;
  },
  
  // Gestion des suggestions
  SET_SUGGESTIONS(state, suggestions) {
    state.suggestions = suggestions;
  },
  
  SET_SUGGESTIONS_LOADING(state, isLoading) {
    state.isSuggestionsLoading = isLoading;
  },
  
  // Métriques
  SET_LAST_INTERACTION(state, timestamp) {
    state.lastInteraction = timestamp;
  },
  
  // Réinitialisation
  RESET_STATE(state) {
    // Sauvegarder les paramètres avant la réinitialisation
    const settings = { ...state.settings };
    
    // Réinitialiser l'état
    Object.assign(state, {
      sessionId: null,
      isChatOpen: false,
      messages: [],
      isLoading: false,
      error: null,
      botStatus: 'idle',
      conversationHistory: [],
      currentConversationId: null,
      messageCount: 0,
      lastInteraction: null,
      isListening: false,
      isSpeechAvailable: 'speechSynthesis' in window,
      suggestions: [],
      isSuggestionsLoading: false
    });
    
    // Restaurer les paramètres
    state.settings = settings;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};