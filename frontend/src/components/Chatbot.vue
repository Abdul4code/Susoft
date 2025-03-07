<template>
  <div class="chat-corner" :class="{ 'is-dark': darkMode }">
    <!-- Floating Icon -->
    <div class="floating-icon" @click="toggleChat">
      <span v-if="isMinimized">💬</span>
      <span v-else>✕</span>
    </div>

    <!-- Chat Container -->
    <div class="chat-container" v-if="!isMinimized">
      <div class="messages" ref="messageContainer">
        <div v-for="(message, index) in messages" :key="index" class="message" :class="message.role">
          <div v-if="message.role === 'user'" class="user-message">
            <p>{{ message.content }}</p>
          </div>
          <div v-else class="assistant-message">
            <p v-if="message.loading" class="loading">
              <span>.</span><span>.</span><span>.</span>
            </p>
            <p v-else>{{ message.content }}</p>
          </div>
        </div>
      </div>
      <div class="input-area">
        <input 
          v-model="newMessage" 
          @keyup.enter="sendMessage"
          placeholder="Type your message..."
          :disabled="isTyping"
        />
        <button @click="sendMessage" :disabled="isTyping">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sessionID: null,
      messages: [],
      newMessage: '',
      isTyping: false,
      darkMode: true,
      error: null,
      isMinimized: false
    };
  },
  async mounted() {
    try {
      const response = await fetch('http://129.213.86.120:5000/conversation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      this.sessionID = data.session_id;
      
      this.addMessage({
        role: 'assistant',
        content: data.welcome_message,
        loading: false
      });
    } catch (error) {
      this.error = 'Failed to start conversation';
      console.error('Error creating session:', error);
    }
  },
  methods: {
    async sendMessage() {
      if (!this.newMessage.trim()) return;

      const userMessage = {
        role: 'user',
        content: this.newMessage,
        loading: false
      };
      this.addMessage(userMessage);
      const userContent = this.newMessage;
      this.newMessage = '';
      
      this.isTyping = true;

      // Add loading indicator for assistant
      const assistantMessage = {
        role: 'assistant',
        content: '',
        loading: true
      };
      this.addMessage(assistantMessage);

      try {
        const response = await fetch(
          `http://129.213.86.120:5000/conversation/${this.sessionID}`, 
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userContent })
          }
        );

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        //eslint-disable-next-line
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split(/\r\n|\n|\r/);
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const content = line.substring(6);
              const lastMsg = this.messages[this.messages.length - 1];
              lastMsg.content += content;
            }
          }
          
          // Auto-scroll
          this.$nextTick(() => {
            this.$refs.messageContainer.scrollTop = 
              this.$refs.messageContainer.scrollHeight;
          });
        }

        // Process remaining buffer
        if (buffer.startsWith('data: ')) {
          const content = buffer.substring(6).trim();
          const lastMsg = this.messages[this.messages.length - 1];
          lastMsg.content += content;
        }

      } catch (error) {
        this.error = 'Failed to send message';
        console.error('Message send error:', error);
        const lastMsg = this.messages[this.messages.length - 1];
        lastMsg.content = 'Error processing response';
      } finally {
        this.isTyping = false;
        const lastMsg = this.messages[this.messages.length - 1];
        lastMsg.loading = false;
        
        // Final scroll to ensure bottom
        this.$nextTick(() => {
          this.$refs.messageContainer.scrollTop = 
            this.$refs.messageContainer.scrollHeight;
        });
      }
    },
    addMessage(message) {
      this.messages.push(message);
      this.$nextTick(() => {
        this.$refs.messageContainer.scrollTop = 
          this.$refs.messageContainer.scrollHeight;
      });
    },
    toggleChat() {
      this.isMinimized = !this.isMinimized;
    }
  }
};
</script>

<style>
.chat-corner {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 350px;
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}

.is-dark {
  background: #2d483b;
  color: white;
}

.chat-container {
  padding: 20px;
  max-height: 600px;
  display: flex;
  flex-direction: column;
}

.messages {
  max-height: 500px;
  overflow-y: auto;
  margin-bottom: 10px;
  flex: 1;
}

.message {
  margin-bottom: 15px;
  display: flex;
}

.user-message {
  margin-left: auto;
  background: #007bff;
  color: white;
  border-radius: 15px;
  padding: 10px 15px;
  max-width: 70%;
}

.assistant-message {
  margin-right: auto;
  background: #e9ecef;
  color: #333;
  border-radius: 15px;
  padding: 10px 15px;
  max-width: 70%;
}

.input-area {
  display: flex;
  gap: 10px;
  align-items: stretch;
  width: 100%;
  margin-top: 10px;
}
.input-area input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 5px;
  height: 40px;
  width: 100%; /* Add this */
  box-sizing: border-box; /* Add this */
}

.input-area button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  white-space: nowrap;
  height: 40px;
  font-size: 14px;
  min-width: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box; /* Add this */
  flex-shrink: 0; /* Add this */
}
button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  letter-spacing: 2px;
}

.loading span {
  animation: pulse 1.4s infinite ease-in-out;
  opacity: 0.3;
}

.loading span:nth-child(1) { animation-delay: 0s }
.loading span:nth-child(2) { animation-delay: 0.2s }
.loading span:nth-child(3) { animation-delay: 0.4s }

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
    transform: translateY(0);
  }
  50% {
    opacity: 1;
    transform: translateY(-2px);
  }
}

/* Dark mode styles */
.is-dark .user-message {
  background: #17a2b8;
}

.is-dark .assistant-message {
  background: #6c757d;
  color: white;
}

.is-dark input {
  background: #343a40;
  color: white;
  border-color: #495057;
}

.is-dark button {
  background: #17a2b8;
}

/* Floating Icon Styles */
.floating-icon {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 50px;
  height: 50px;
  background: #007bff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  z-index: 1001;
}

.floating-icon:hover {
  background: #0056b3;
}

.is-dark .floating-icon {
  background: #17a2b8;
}

.is-dark .floating-icon:hover {
  background: #138496;
}

/* When chat is open, adjust floating icon position */
.chat-container:not(.minimized) + .floating-icon {
  bottom: auto;
  top: 10px;
  right: 10px;
}
</style>