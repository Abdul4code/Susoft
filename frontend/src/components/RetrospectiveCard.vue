<script setup>
const props = defineProps({
    title: String,
    tasks: Object,
    card_id: Number, // Unique identifier for the card
    status_id: Number, // Current status ID
});

const emits = defineEmits(["drag_start", "update:title"]);

function handleDragStart(event) {
    event.dataTransfer.setData("card_id", props.card_id);
    event.dataTransfer.setData("from_status", props.status_id);
    emits("drag_start", props.card_id);
}

function updateTitle(event) {
    emits("update:title", event.target.value);
}
</script>

<template>
    <div 
        class="app_cont" 
        draggable="true"
        @dragstart="handleDragStart"
    >
        <textarea 
            class="title" 
            type="text" 
            :value="props.title" 
            @input="updateTitle"
            rows="5"
        ></textarea>
    </div>
</template>

<style scoped>
    .app_cont{
        width: 90%;
        margin-bottom: 15px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
        padding: 5%;
        cursor: grab;
    }

    .title{
        font-family: 'Poppins';
        font-size: 11pt;
        font-weight: 400;
        width: 100%;
        height: 50px;
        margin-bottom: 25px;
        border: none;
        background: none;
    }

    .app_summary{
        font-size: 9.5pt;
        color: rgba(102, 102, 102, 1);
        font-family: 'Poppins';
        margin: -2px 10px;
    }

    .status-cont{
        display: flex;
        margin: 10px 0px;
    }

    .app-status{
        flex: 1 1 10%;
        height:6px;
        margin: 15px 0px;
    }

    .progress{
        background-color: rgba(50, 46, 252, 0.6);
    }

    .canceled{
        background-color: rgba(220, 54, 52, 1);
    }

    .completed{
        background-color: rgba(0, 120, 0, 0.6);
    }

    .current{
        text-align: center;
        font-size: 10pt;
    }
</style>

