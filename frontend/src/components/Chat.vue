<script setup>
import { ref } from 'vue';

const chat_tray = ref({
    open: true,
    fresh: false,
});

const cur_prompt = ref('');
const history = ref([]);

function toggleChatTray() {
    chat_tray.value.open = !chat_tray.value.open;
}

function addPrompt() {
    history.value.push({
        prompt: cur_prompt.value,
        response: '',
    });

    cur_prompt.value = '';
}

function addResponse() {
    let response = 'This is the response for the current days';

    let last_chat = history.value.pop();
    last_chat.response = response;

    history.value.push(last_chat);
}

function chat() {
    addPrompt();
    addResponse();
}
</script>

<template>
    <section class="chat-cont" :class="{ 'chat-closed': !chat_tray.open }">
        <!-- Chat Header -->
        <div class="chat-header" @click="toggleChatTray">
            <p class="header-text">Chat</p>

            <img v-if="chat_tray.open" src="../assets/images/chat-compress.svg" class="tray-icon" />
            <img v-else src="../assets/images/chat-expand.svg" class="tray-icon" />

            
        </div>

        <!-- Chat Messages (Visible Only When Open) -->
        <div v-if="chat_tray.open" class="chat">
            <div class="result">
                <div v-for="(chat, index) in history" :key="index" class="chat-message">
                    <p class="chat-prompt"> {{ chat.prompt }} </p>
                    <p class="chat-response"> {{ chat.response }} </p>
                </div>
            </div>
        </div>

        <!-- Chat Input (Visible Only When Open) -->
        <div v-if="chat_tray.open" class="prompt">
            <textarea v-model="cur_prompt" placeholder="Type your prompt..." class="chat-input"></textarea>
            <div @click="chat" class="send-btn">
                <img src="../assets/images/send.svg" alt="Send" class="send-icon" />
            </div>
        </div>
    </section>
</template>

<style scoped>
/* General Chat Container */
.chat-cont {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 700px;
    max-height: 80vh;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 15px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    transition: all 0.4s ease-in-out;
    overflow: hidden;
    z-index: 100000;
}

/* Chat Closed (Minimized) */
.chat-closed {
    height: 50px;
    width: 200px;
    overflow: hidden;
    transition: all 0.3s ease-in-out;
}

/* Chat Header */
.chat-header {
    background: rgba(76, 147, 76, 0.9);
    color: white;
    font-size: 18px;
    font-family: Rubik, sans-serif;
    font-weight: 600;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 15px 15px 0 0;
    cursor: pointer;
}

.tray-icon {
    width: 25px;
    height: 25px;
    cursor: pointer;
}

/* Chat Messages */
.chat {
    flex: 1;
    overflow-y: auto;
    padding: 15px;
    max-height: 300px;
    scrollbar-width: thin;
}

.result {
    display: flex;
    flex-direction: column;
}

.chat-message {
    max-width: 90%;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 14px;
    font-family: Poppins, sans-serif;
    word-wrap: break-word;
    animation: fadeIn 0.3s ease-in-out;
}

.chat-prompt {
    background: #e3fcef;
    color: #2b7a0b;
    align-self: flex-end;
    text-align: right;
    border-radius: 10px 10px 0 10px;
    padding: 10px;
}

.chat-response {
    background: #f1f1f1;
    color: #333;
    align-self: flex-start;
    text-align: left;
    border-radius: 10px 10px 10px 0;
    padding: 10px;
}

/* Chat Input Area */
.prompt {
    display: flex;
    align-items: center;
    padding: 10px;
    background: white;
    border-radius: 0 0 15px 15px;
}

.chat-input {
    flex: 1;
    padding: 10px;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-family: Poppins, sans-serif;
    outline: none;
    resize: none;
    background: rgba(240, 240, 240, 0.8);
}

.send-btn {
    margin-left: 10px;
    cursor: pointer;
    background: #4c934c;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: 0.3s;
}

.send-btn:hover {
    background: #67b067;
}

.send-icon {
    width: 20px;
    height: 20px;
}

/* Animations */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Mobile Responsive */
@media (max-width: 600px) {
    .chat-cont {
        width: 90%;
        right: 5%;
        bottom: 10px;
    }

    .chat-message {
        font-size: 12px;
        padding: 8px;
    }
}
</style>
