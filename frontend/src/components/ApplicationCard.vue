<script setup>
const props = defineProps({
    title: String,
    tasks: Object,
    card_id: Number, // Unique identifier for the card
    status_id: Number, // Current status ID
});

const emits = defineEmits(["drag_start"]);

function handleDragStart(event) {
    event.dataTransfer.setData("card_id", props.card_id);
    event.dataTransfer.setData("from_status", props.status_id);
    emits("drag_start", props.card_id);
}
</script>

<template>
    <div 
        class="app_cont" 
        draggable="true"
        @dragstart="handleDragStart"
    >
        <p class="title"> Implement Security  </p>
        <p>
            <span class="app_icon"><img src="../assets/images/tasks.svg" /></span>
            <span class="app_summary"> 15 Metrics </span>
        </p>
        <p>
            <span class="app_icon"><img src="../assets/images/done.svg" /></span>
            <span class="app_summary"> 9 Satisfied </span>
        </p>
        <div class="status-cont">
            <div class="app-status progress"></div>
            <div class="app-status completed"></div>
        </div>
        <p class="current"> Impact: Economic, Environmental</p>
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
        font-size: 14pt;
        font-weight: 400;
        width: 70%;
        margin-bottom: 25px;
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

