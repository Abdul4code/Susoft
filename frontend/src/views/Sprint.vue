<script setup>
    import router from '@/router';
    import axios from 'axios'
    import {ref, watch, onMounted} from 'vue'
    import Toast from '../components/toasts.vue'
    import Navbar from '../components/navbar.vue'
    import KabanBoard from '../components/KabanBoard.vue'


</script>

<template>
    <section class="container">
        <Navbar />
        <KabanBoard />
    </section>
</template>
    
<style scoped>


</style>