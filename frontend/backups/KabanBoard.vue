<script setup>
    import {ref, watch, onMounted} from 'vue'
    import SprintStatus from './SprintStatus.vue'

    const app_container = ref(null)

    const model =  ref({
        styles : {
            
        },

        data : {
            status : [
                        { 
                            id : 1,
                            order: 1,
                            title :'Created'
                        },
                         {
                            id : 2,
                            order: 2,
                            title: 'In progress'
                         },
                         {
                            id : 3,
                            order: 3,
                            title :'Modified'
                         },
                         {
                            id : 6,
                            order: 6,
                            title: 'Completed'
                         },
                         {
                            id : 4,
                            order: 4,
                            title :'In review'
                         },
                         {
                            id : 5,
                            order: 5,
                            title :'Accepted'
                         } 
                    ]
                },
                drag : {
                    item : '',
                    displaced : ''
                }   
    })

function scrollLeft() {
    app_container.value.scrollLeft -= 400;
}

function scrollRight() {
    app_container.value.scrollLeft += 400;
}

onMounted(()=>{
    model.value.data.status.sort((a, b) => a.order - b.order);
})

watch(model.value.data.status, async(newStatus, oldStatus)=>{
    model.value.data.status.sort((a, b) => a.order - b.order);
})

function move_status(event) {
    
    let movedStatusId = event.dataTransfer.getData("status_id");


    let displacedStatusId = event.target.id;

    if (displacedStatusId === "") {
        displacedStatusId = event.target.closest('.status').id;
        console.log(displacedStatusId);
    }

    // Find indices of moved and displaced status items
    const indexMoved = model.value.data.status.findIndex(item => item.id == movedStatusId);
    const indexDisplaced = model.value.data.status.findIndex(item => item.id == displacedStatusId);

    // Retrieve order values of moved and displaced status items
    const movedStatusOrder = model.value.data.status[indexMoved].order;
    const displacedStatusOrder = model.value.data.status[indexDisplaced].order;

    // Update order of moved status item to match displaced status item
    model.value.data.status[indexMoved].order = displacedStatusOrder;

    // Adjust order of other status items based on proximity to moved and displaced items
    if (Math.abs(parseInt(movedStatusOrder) - parseInt(displacedStatusOrder)) == 1) {
        // If the moved and displaced items are adjacent, swap their orders
        model.value.data.status[indexDisplaced].order = movedStatusOrder;
    } else {
        // Otherwise, adjust orders of other items based on their positions relative to moved and displaced items
        model.value.data.status.forEach(item => {
            if (movedStatusOrder < displacedStatusOrder && item.id != movedStatusId && item.order <= displacedStatusOrder) {
                item.order -= 1;
            } else if (movedStatusOrder > displacedStatusOrder && item.id != movedStatusId && item.order >= displacedStatusOrder && item.order < movedStatusOrder) {
                item.order += 1;
            }
        });
    }

    event.target.classList.remove('dropable')
}

</script>

<template>
    <section>
        <section class="goal-header">
            <div class="header-left">
                <div class="goal-title"> Graduate School Dream </div>
                <button class="goal-detail-button"> View Detail </button>
            </div>
            <div class="header-right">
                <div class="timeElement">
                    <p class="value"> 3 </p>
                    <p class="desc"> Years </p>
                </div>
                <div class="colon">
                    :
                </div>

                <div class="timeElement">
                    <p class="value"> 15 </p>
                    <p class="desc"> Days </p>
                </div>
                <div class="colon">
                    :
                </div>

                <div class="timeElement">
                    <p class="value"> 24 </p>
                    <p class="desc"> Hours </p>
                </div>
                <div class="colon">
                    :
                </div>

                <div class="timeElement">
                    <p class="value"> 48 </p>
                    <p class="desc"> Seconds </p>
                </div>
            </div>
        </section>
        <section class="filter-pane">
            <div class="filter-element">
                <label for="" class="filter-label"> Filter By:  </label>
                <div class="dropdwon-item">
                    <p class="dropdown-header"> Progress </p><span class="dropdown-icon"> <img src="../assets/images/down.svg" alt=""></span>
                    <div class="dropdown-values">
                        <p> Started </p>
                        <p> Completed </p>
                        <p> Cancelled </p>
                    </div>
                </div>
                <div class="dropdown-item">
                    <p class="dropdown-header"> Date </p><span class="dropdown-icon"> <img src="../assets/images/down.svg" alt=""></span>
                    <div class="dropdown-values">
                        <p> Created Date </p>
                        <p> Target Date </p>
                    </div>
                </div>
            </div>
            <div class="filter-element">
                <label for="" class="filter-label"> Sort By:  </label>
                <div class="dropdwon-item">
                    <p class="dropdown-header"> Date </p><span class="dropdown-icon"> <img src="../assets/images/down.svg" alt=""></span>
                    <div class="dropdown-values">
                        <p> Created </p>
                        <p> Target </p>
                    </div>
                </div>
            </div>
        </section>

        <section class="app-container" id="app-container" ref="app_container">      
            <GoalStatus v-for="item in model.data.status"
                :status_id = "item.id"
                :status_key = "item.id"
                :status_item = "item"
                :items_count = "model.data.status.length"
                @move_status = "move_status($event)"
            >
            </GoalStatus>    
        </section>

        <section class="slider-controls">
            <div class="scroll-icon left" @click="scrollLeft"> </div>
            <div class="scroll-icon right" @click="scrollRight"> </div>
        </section>
    </section>
</template>

<style scoped>
    @import url("../assets/css/kanban.css");
</style>