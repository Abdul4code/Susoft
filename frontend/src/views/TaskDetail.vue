<script setup>
import { ref } from 'vue';
import Navbar from '../components/navbar.vue';

const taskStatus = ref({
    mainStatus: 'In progress',
    metrics: [
        { name: 'Message Graduate School Coordinator', status: 'Done' },
        { name: 'Write Statement of Purpose', status: 'Progress' },
        { name: 'Gather program requirements', status: 'Done' },
        { name: 'Write Statement of Purpose', status: 'Canceled' }
    ],
    statusOptions: ['In progress', 'Done', 'Progress', 'Canceled']
});
</script>

<template>
    <div>
        <Navbar />
        <div class="page-container">
            <h2 class="page-title">Implement Login feature for all registered users and content creators</h2>
            
            <div class="content-grid">
                <div class="left-column">
                    <div class="status-section">
                        <h3>Sustainability metrics</h3>
                        <select v-model="taskStatus.mainStatus" class="status-dropdown">
                            <option v-for="status in taskStatus.statusOptions" :key="status" :value="status">{{ status }}</option>
                        </select>
                        <div class="tasks">
                            <div v-for="(task, index) in taskStatus.metrics" :key="index" class="task-item">
                                <span>{{ task.name }}</span>
                                <select v-model="task.status" class="status-dropdown">
                                    <option v-for="status in taskStatus.statusOptions" :key="status" :value="status">{{ status }}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="right-column">
                    <div class="description">
                        <h3>Description</h3>
                        <p>Create a login button to use the user and environment data and also fetch the various capable data used.</p>
                    </div>

                    <div class="sustainability-impact">
                        <h3>Sustainability Impact</h3>
                        <p>Economic and Social</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.page-container {
    padding: 20px;
    font-family: 'Poppins', sans-serif;
    max-width: 1200px;
    margin: auto;
}
.page-title {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}
.left-column, .right-column {
    background: #ffffff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.status-section h3,
.description h3,
.sustainability-impact h3 {
    margin-bottom: 10px;
    font-weight: 600;
}
.status-dropdown {
    background-color: #6ca8f0;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
}
.tasks {
    margin-top: 10px;
}
.task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f5f5f5;
    padding: 12px;
    margin: 8px 0;
    border-radius: 5px;
    font-size: 14px;
    font-weight: 500;
}
</style>
