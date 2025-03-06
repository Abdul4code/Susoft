<script setup>
import { ref, onMounted } from "vue";
import SprintStatus from "../components/RetroStatus.vue";

const app_container = ref(null);

const model = ref({
    data: {
        status: [
            { id: 1, order: 1, title: "What worked best and helped sustainability design decision?" },
            { id: 2, order: 2, title: "What were the obstacles and challenges?" },
            { id: 4, order: 4, title: "What can we do differently to improve the overall sprint process?" },
            { id: 5, order: 5, title: "What should we incorporate in the next sprint?" },
        ],
        cards: [
            { id: 101, title: "Task A", status_id: 1 },
            { id: 102, title: "Task B", status_id: 2 },
            { id: 103, title: "Task C", status_id: 2 },
            { id: 104, title: "Task D", status_id: 4 },
        ],
    },
});

function moveCard({ card_id, from_status, to_status }) {
    const card = model.value.data.cards.find((c) => c.id == card_id);
    if (card) {
        card.status_id = to_status;
    }
}

onMounted(() => {
    model.value.data.status.sort((a, b) => a.order - b.order);
});
</script>

<template>
    <section>
        <section class="goal-header">
            <div class="header-left">
                <div class="goal-title"> Retro </div>
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
            />
        </section>
    </section>
</template>

<style scoped>
    @import url("../assets/css/kanban.css");

    .app-container {
        display: flex;
        gap: 25px;
        overflow-x: auto;
        padding: 20px;
    }
</style>