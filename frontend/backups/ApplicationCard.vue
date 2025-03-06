<script setup>
    let props = defineProps({
        title : String,
        tasks : Object,
    })
</script>

<template>
    <div class="app_cont">
        <p class="title"> University of Alabama PhD in Chemistry Application </p>
        <p> <span class="app_icon"><img src="../assets/images/clock.svg" /> </span> 
            <span class="app_summary"> 7 days ago </span>
            <span class="app_summary"> 3:14:30 left </span>
        </p>
        <p> <span class="app_icon"><img src="../assets/images/tasks.svg" /> </span> 
            <span class="app_summary"> 15 tasks </span>
        </p>
        <p> <span class="app_icon"><img src="../assets/images/done.svg" /> </span> 
            <span class="app_summary"> 9 Done </span>
        </p>
        <div class="status-cont">
            <div class="app-status progress"></div>
            <div class="app-status completed"></div>
            <div class="app-status canceled"></div>
        </div>
        <p class="current"> Current Task: Cold Mailing Proffessors</p>
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
        background-color: rgba(50, 46, 252, 1);
    }

    .canceled{
        background-color: rgba(220, 54, 52, 1);
    }

    .completed{
        background-color: green;
    }

    .current{
        text-align: center;
        font-size: 10pt;
    }
</style>

