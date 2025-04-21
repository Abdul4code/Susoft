<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import SprintStatus from "../components/RetroStatus.vue";
import { useStateStore } from "../stores/state.js";

const app_container = ref(null);
const sprints = ref([]); // List of sprints in the current project
const selectedSprint = ref(null); // Currently selected sprint

const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

const model = ref({
    data: {
        status: [
            { id: 1, order: 1, title: "What worked best and helped sustainability design decision?" },
            { id: 2, order: 2, title: "What were the obstacles and challenges?" },
            { id: 3, order: 3, title: "What can we do differently to improve the overall sprint process?" },
            { id: 4, order: 4, title: "What should we incorporate in the next sprint?" },
        ],
        cards: [],
    },
});

// Fetch all sprints for the current project
async function fetchSprints() {
    try {
        const projectStore = useStateStore();
        const projectId = projectStore.state.projectId; // Retrieve project ID from Pinia store
        const response = await axios.get(`${backendBaseUrl}/sprints/?project_id=${projectId}`);
        console.log("Sprints:", response.data);
        sprints.value = response.data;
        if (sprints.value.length > 0) {
            selectedSprint.value = sprints.value[0].id; // Default to the first sprint
            fetchSprintData();
        }
    } catch (error) {
        console.error("Error fetching sprints:", error);
    }
}

// Fetch data for the selected sprint
async function fetchSprintData() {
    try {
        const response = await axios.get(`${backendBaseUrl}/susaf/retro-notes/by-sprint/${selectedSprint.value}/`);
        model.value.data.cards = response.data.map(note => ({
            id: note.id,
            title: note.note,
            status_id: note.board_position || 1, // Default to status 1 if no board position
        }));
        console.log("Sprint Data:", model.value.data.cards);
    } catch (error) {
        console.error("Error fetching sprint data:", error);
    }
}

function moveCard({ card_id, from_status, to_status }) {
    const card = model.value.data.cards.find((c) => c.id == card_id);
    if (card) {
        card.status_id = to_status;

        axios
            .patch(`${backendBaseUrl}/susaf/retro-notes/${card_id}/`, {
                board_position: to_status,
            })
            .then(() => {
                console.log(`Card ${card_id} updated to position ${to_status}`);
            })
            .catch((error) => {
                console.error("Error updating card position:", error);
                alert("Failed to update the card's position. Please try again.");
            });
    }
}

async function addNewCard() {
    try {
        
        const response = await axios.post(`${backendBaseUrl}/susaf/retro-notes/`, {
            note: `New Note`,
            board_position: 1, // Default status
            sprint: selectedSprint.value,
        });
        const newCardId = response.data.id; // Get the ID from the response
        model.value.data.cards.push({
            id: newCardId,
            title: response.data.note,
            status_id: response.data.board_position,
        });
    } catch (error) {
        console.error("Error adding new card:", error);
    }
}

function updateNote(card) {
    axios
        .patch(`${backendBaseUrl}/susaf/retro-notes/${card.id}/`, {
            note: card.title,
        })
        .catch((error) => {
            console.error("Error updating note:", error);
            alert("Failed to update the note. Please try again.");
        });
}


onMounted(() => {
    fetchSprints();
    model.value.data.status.sort((a, b) => a.order - b.order);
});
</script>

<template>
    <section>
        <section class="goal-header">
            <div class="header-left"> 
                <div class="goal-title"> Retrospective </div>
                <select v-model="selectedSprint" @change="fetchSprintData" class="sprint-dropdown">
                    <option v-for="sprint in sprints" :key="sprint.id" :value="sprint.id">
                        {{ sprint.title }}
                    </option>
                </select>
            </div>
        </section>

        <section class="app-container" id="app-container" ref="app_container">      
            <SprintStatus 
                v-for="item in model.data.status"
                :key="item.id"
                :status_id="item.id"
                :status_key="item.id"
                :status_item="item"
                :items_count="model.data.status.length"
                :cards="model.data.cards.filter(card => card.status_id === item.id)"
                @move_card="moveCard"
                @update_note="updateNote"
            />

        </section>

        <!-- Add New Card Button -->
        <button class="add-card-btn" @click="addNewCard">
            <span class="add-card-icon">+</span>
            <span class="tooltip">Add a new card</span>
        </button>
    </section>
</template>

<style scoped>
    @import url("../assets/css/kanban.css");

    .sprint-dropdown {
        font-size: 16px;
        padding: 5px 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;
        color: #333;
        cursor: pointer;
    }

    .sprint-dropdown:focus {
        outline: none;
        border-color: #007AFF;
    }

    .app-container {
        display: flex;
        gap: 40px;
        overflow-x: auto;
        padding: 20px;
        height: 83vh;
    }

    .goal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 20px;
    }

    .add-card-btn {
        position: fixed;
        bottom: 50%;
        right: 60px;
        background: linear-gradient(135deg, #4A90E2, #007AFF);
        color: white;
        border: none;
        width: 70px;
        height: 70px;
        border-radius: 50%;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        font-size: 24px;
        font-weight: bold;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        transition: background-color 0.3s ease, transform 0.2s ease;
        z-index: 1000;
    }

    .add-card-btn:hover {
        background: linear-gradient(135deg, #007AFF, #0056B3);
        transform: scale(1.1);
    }

    .add-card-btn:active {
        transform: scale(0.95);
    }

    .add-card-btn .tooltip {
        position: absolute;
        bottom: -40px;
        left: 50%;
        transform: translateX(-50%);
        background: #333;
        color: #fff;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: opacity 0.3s ease, visibility 0.3s ease;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
    }

    .add-card-btn:hover .tooltip {
        opacity: 1;
        visibility: visible;
    }

    .add-card-icon {
        font-size: 28px;
        font-weight: bold;
        line-height: 1;
    }
</style>