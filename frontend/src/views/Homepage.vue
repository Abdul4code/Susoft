<script setup>
    import router from '@/router';
    import axios from 'axios'
    import {ref, watch, onMounted} from 'vue'
    import Toast from '../components/toasts.vue'
    import Navbar from '../components/navbar.vue'
    import EmptyGoal from '../components/emptyGoal.vue'
    import GoalForm from '../components/GoalForm.vue'

    const model = ref({
        status : {
            goal_open : false,
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
        <EmptyGoal @toggle_goal_form = 'toggleCreateGoal'></EmptyGoal>
        <GoalForm 
            :open="model.status.goal_open" 
            :fresh="model.status.fresh_page"
            @toggle_goal_form = 'toggleCreateGoal'>
        </GoalForm>
    </section>
</template>
    
<style scoped>
@import url("../assets/css/homepage.css");

</style>