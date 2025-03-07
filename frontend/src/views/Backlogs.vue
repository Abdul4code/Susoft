<script setup>
    import router from '@/router';
    import axios from 'axios'
    import {ref, watch, onMounted} from 'vue'
    import Toast from '../components/toasts.vue'
    import Navbar from '../components/navbar.vue'
import Backlogs from '../components/Backlogs.vue';


</script>

<template>
    <section class="container">
        <Navbar />
        <Backlogs />
    </section>
</template>
    
<style scoped>


</style>