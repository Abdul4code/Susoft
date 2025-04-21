<script setup>
import { ref } from "vue";
import ApplicationCard from "./RetrospectiveCard.vue";

const props = defineProps({
    status_id: Number,
    status_key: Number,
    status_item: Object,
    items_count: Number,
    cards: Array, // List of cards belonging to this status
});

const emits = defineEmits(["move_card"]);

function allowDrop(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const card_id = event.dataTransfer.getData("card_id");
    const from_status = event.dataTransfer.getData("from_status");
    
    if (card_id && from_status !== props.status_id) {
        emits("move_card", { card_id, from_status, to_status: props.status_id });
    }
}
</script>

<template>
    <div 
        :id="props.status_id"
        :key="props.status_key"
        class="status"
        @dragover="allowDrop"
        @drop="handleDrop"
    > 
        <div class="goal_header"> 
            <p> {{ status_item.title }} </p>
            <p class="header-icons">
            </p>
        </div>
        <div class="status_bar_cont">
            <div v-for="i in items_count" :class="{ status_level: i <= props.status_id }" class="status_bar"></div>
        </div>
        <div class="status_body">
            <ApplicationCard 
                v-for="card in props.cards"
                :key="card.id"
                :card_id="card.id"
                :title="card.title"
                :status_id="props.status_id"
                @drag_start="(card_id) => console.log(`Dragging card ${card_id}`)"
                @update:title="(newTitle) => $emit('update_note', { ...card, title: newTitle })"
            />

        </div>
    </div>
</template>

<style>
.dropable{
    box-shadow: 0 0 15px 2px rgba(100, 100, 100, 0.5);
}

.status{
    width: 400px;
    min-width: 400px;
    border-radius: 5px;
    min-height: 200px;
}

.goal_header{
    display: flex;
    justify-content: space-between;
    align-items: center;
    
}

.goal_header p{
    flex: 1 0 75%;
    font-size: 16px !important;
}

.goal_header p:nth-child(1){
    font-size: 18px;
    font-family: 'Poppins';
    font-weight: 600;
    color: rgba(53, 53, 53, 1);
    margin: 8px 0px;
}

.goal_header p:nth-child(2){
    text-align: right;
}

.goal_header p:nth-child(2) img{
    margin-left: 25px;
}

.status_bar_cont{
    display: flex;
    justify-content: space-between;
    gap: 2px;
}

.status_bar{
    height: 7px;
    flex: 1 0 10%;
    background-color: rgba(217, 217, 217, 1);
    border-radius: 10px;
}

.status_level{
    background-color: rgba(83, 165, 72, 1)
}

.status_body{
    background-color: rgba(240, 240, 240, 1); 
    height: 92%;
    width: 90%;
    margin-top: 5%;
    border-radius: 10px;
    padding: 5%;
}
</style>