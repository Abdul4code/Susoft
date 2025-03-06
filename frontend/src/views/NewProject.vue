<script setup>
    import router from '@/router';
    import axios from 'axios'
    import {ref, watch, onMounted} from 'vue'
    import Toast from '../components/toasts.vue'
    import Navbar from '../components/navbar.vue'
    import Susaf from '../components/Susaf.vue'
    import Chat from '../components/Chat.vue'

    const model = ref({
        status : {
            goal_open : true,
            fresh_page : false
        }
    })

    onMounted(() => {
        model.value.status.fresh_page = true

        // check for user login - if not logged in redirect to login page
    })

    function toggleCreateGoal(){
        model.value.status.goal_open = !model.value.status.goal_open
        model.value.status.fresh_page = false
    }


</script>

<template>
    <section class="container">
        <Navbar></Navbar>
        <Susaf></Susaf>
        <Chat 
            :open="model.status.goal_open" 
            :fresh="model.status.fresh_page"
            @toggle_goal_form = 'toggleCreateGoal'>
        </Chat>
        <button class="back-button"> Generate Backlogs </button>
    </section>
</template>
    
<style scoped>
@import url("../assets/css/homepage.css");

</style>