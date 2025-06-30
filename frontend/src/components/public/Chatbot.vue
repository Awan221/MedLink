<template>
  <div class="chatbot-container">
    <div class="chatbot-button" @click="toggleChat" v-if="!isOpen">
      <i class="fas fa-comments"></i>
    </div>
    <div class="chatbot-window" v-if="isOpen">
      <div class="chatbot-header">
        <h3>Assistant Médical</h3>
        <button class="close-button" @click="toggleChat">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="chatbot-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.type]">
          {{ message.text }}
        </div>
      </div>
      <div class="chatbot-input">
        <input 
          type="text" 
          v-model="userInput" 
          @keyup.enter="sendMessage"
          placeholder="Posez votre question..."
        >
        <button @click="sendMessage">
          <i class="fas fa-paper-plane"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'

export default {
  name: 'Chatbot',
  setup() {
    const isOpen = ref(false)
    const messages = ref([])
    const userInput = ref('')
    const messagesContainer = ref(null)

    const toggleChat = () => {
      isOpen.value = !isOpen.value
      if (isOpen.value) {
        // Initialiser la conversation avec Botpress
        initializeBotpress()
      }
    }

    const initializeBotpress = async () => {
      // Configuration de Botpress
      const botpressConfig = {
        host: process.env.VUE_APP_BOTPRESS_HOST || 'http://localhost:3000',
        botId: process.env.VUE_APP_BOTPRESS_BOT_ID || 'medlink-bot'
      }

      // Ajouter un message de bienvenue
      messages.value.push({
        type: 'bot',
        text: 'Bonjour ! Je suis votre assistant médical. Comment puis-je vous aider aujourd\'hui ?'
      })
    }

    const sendMessage = async () => {
      if (!userInput.value.trim()) return

      // Ajouter le message de l'utilisateur
      messages.value.push({
        type: 'user',
        text: userInput.value
      })

      const userMessage = userInput.value
      userInput.value = ''

      // Envoyer le message à Botpress
      try {
        const response = await fetch(`${process.env.VUE_APP_BOTPRESS_HOST}/api/v1/bots/${process.env.VUE_APP_BOTPRESS_BOT_ID}/converse`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            type: 'text',
            text: userMessage
          })
        })

        const data = await response.json()
        
        // Ajouter la réponse du bot
        messages.value.push({
          type: 'bot',
          text: data.responses[0].text
        })

        // Faire défiler vers le bas
        await nextTick()
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      } catch (error) {
        console.error('Erreur lors de la communication avec le bot:', error)
        messages.value.push({
          type: 'bot',
          text: 'Désolé, je rencontre des difficultés techniques. Veuillez réessayer plus tard.'
        })
      }
    }

    return {
      isOpen,
      messages,
      userInput,
      messagesContainer,
      toggleChat,
      sendMessage
    }
  }
}
</script>

<style scoped>
.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chatbot-button {
  width: 60px;
  height: 60px;
  background-color: #4CAF50;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.2);
  color: white;
  font-size: 24px;
}

.chatbot-window {
  position: fixed;
  bottom: 90px;
  right: 20px;
  width: 350px;
  height: 500px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  display: flex;
  flex-direction: column;
}

.chatbot-header {
  padding: 15px;
  background-color: #4CAF50;
  color: white;
  border-radius: 10px 10px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chatbot-header h3 {
  margin: 0;
}

.close-button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 20px;
}

.chatbot-messages {
  flex-grow: 1;
  padding: 15px;
  overflow-y: auto;
}

.message {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 10px;
  max-width: 80%;
}

.message.user {
  background-color: #e3f2fd;
  margin-left: auto;
}

.message.bot {
  background-color: #f5f5f5;
  margin-right: auto;
}

.chatbot-input {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.chatbot-input input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}

.chatbot-input button {
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chatbot-input button:hover {
  background-color: #45a049;
}
</style> 