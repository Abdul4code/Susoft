<script setup>
    import ApplicationCard from './ApplicationCard.vue'

    const props = defineProps({
        status_id : Number,
        status_key: Number,
        status_item : Object,
        items_count : Number,
    })

    const emits = defineEmits(['move_status', 'set_dragged_item'])

    function dragStatus(event, id){
        const dragImage = new Image();
        dragImage.src = "/src/assets/images/moving.svg";
        event.dataTransfer.setDragImage(dragImage, 10, 10);
        event.dataTransfer.setData('status_id', id)
        event.dataTransfer.effectAllowed = 'move'
        event.dataTransfer.dropEffect = "move"
       emits('set_dragged_item', id)
    }

    function dragging(event) {
        const rect = event.target.getBoundingClientRect();
        const width = rect.width;
        const height = rect.height;

        event.target.style.position = 'absolute';
        event.target.style.top = event.clientY + 'px';
        event.target.style.left = event.clientX + 'px';
        event.target.style.width = width + 'px';
        event.target.style.height = 200 + 'px';
        event.target.style.overflow = "hidden";

    }


    function dragStatusEnter(event) {
        if (event.dataTransfer.types.includes("status_id")) {
            event.preventDefault();
            event.target.classList.add('dropable');
        }
    }

    function dragStatusLeave(event){
        event.target.classList.remove('dropable')
    }

    function dragStatusOver(event){
        if(event.dataTransfer.types.includes('status_id')){
            event.preventDefault()
        }
    }

    function dropStatus(event) {
        emits('move_status', event)
        event.target.classList.remove('dropable')
    }

</script>

<template>
    <div 
        :id = "props.status_id"
        :key = "props.status_key" 
        class="status"
        draggable="true"
        @dragstart="dragStatus($event, props.status_id)"
        @drag="dragging($event)"
        @dragenter="dragStatusEnter($event)"
        @dragleave="dragStatusLeave($event)"
        @dragover="dragStatusOver($event)"
        @drop="dropStatus($event)"
    > 
        <div class="goal_header"> 
            <p> {{ status_item.title }} </p>
            <p class="header-icons">
                <img src="../assets/images/Edit.svg" alt="">
                <img src="../assets/images/Trash.svg" alt="">
            </p>
        </div>
        <div class="status_bar_cont"><div v-for="i in items_count" :class="{status_level: i <= props.status_id}" class="status_bar"></div></div>
        <div class="status_body">
            <ApplicationCard />
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
}

.goal_header{
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.goal_header p{
    flex: 1 0 50%;
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
    margin-top: 1.4%;
    border-radius: 10px;
    padding: 5%;
}
</style>