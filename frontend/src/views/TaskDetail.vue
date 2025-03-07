<script setup>
import { ref, computed } from 'vue';
import Navbar from '../components/navbar.vue';
import { useRoute } from 'vue-router';
import axios from 'axios'

const route = useRoute();

const taskId = route.params.id;

const taskStatus = ref({
    title: "",
    description: "",
    type: "",
    imapct: "",
    mainStatus: 'In progress',
    metrics: [
    ],
    statusOptions: ['In progress', 'Done', 'Progress', 'Canceled']
});

// Dynamic status color classes
const statusColors = {
    'In progress': 'status-in-progress',
    'Done': 'status-done',
    'Progress': 'status-progress',
    'Canceled': 'status-canceled'
};

const mainStatusClass = computed(() => statusColors[taskStatus.value.mainStatus] || 'status-default');

function get_task(){
    axios.get(`http://localhost:8000/susaf/tasks/${taskId}`)
        .then(function (response) {
            taskStatus.value.title = response.data.title
            taskStatus.value.description = response.data.description
            taskStatus.value.type = response.data.type
            taskStatus.value.impact = response.data.impact

            console.log(taskStatus)

            
        })
        .catch(function (error) {
            console.log(error)
            alert(error)
        });
}

function get_metrics(){
    axios.get(`http://localhost:8000/susaf/metrics/${taskId}`)
        .then(function (response) {
            for (const metric of response.data) {
                if(metric.task == taskId){
                    let metric = {
                            "name":  metric.text,
                            "status": metric.status
                        }

                    taskStatus.value.metrics.push(metric)
                } 
            }

            console.log(taskStatus)
            
            
        })
        .catch(function (error) {
            console.log(error)
            alert(error)
        });
}

get_task()
</script>

<template>
    <div class="app-container">
        <Navbar />
        <div class="page-container">
            <!-- Page Title -->
            <h1 class="section-heading">Task Detail</h1>
            <h2 class="page-title">{{taskStatus.title}}</h2>

            <div class="content-grid">
                <!-- Left Column -->
                <div class="left-column">
                    <h3 class="section-title">Sustainability Metrics</h3>
                    <div class="status-container">
                        <span class="status-box" :class="mainStatusClass">{{ taskStatus.mainStatus }}</span>
                        <select v-model="taskStatus.mainStatus" class="status-dropdown">
                            <option v-for="status in taskStatus.statusOptions" :key="status" :value="status">
                                {{ status }}
                            </option>
                        </select>
                    </div>

                    <div class="tasks">
                        <div v-for="(task, index) in taskStatus.metrics" :key="index" class="task-item">
                            <span>{{ task.name }}</span>
                            <select v-model="task.status" class="task-dropdown">
                                <option v-for="status in taskStatus.statusOptions" :key="status" :value="status">
                                    {{ status }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Right Column -->
                <div class="right-column">
                    <div class="section">
                        <h3 class="section-title">Description</h3>
                        <p>{{taskStatus.description}}</p>
                    </div>

                    <div class="section">
                        <h3 class="section-title">Sustainability Impact</h3>
                        <p><strong>{{ taskStatus.impact.join(", ") }}</strong></p>

                    </div>

                    <div class="section">
                        <h3 class="section-title">Impact Type</h3>
                        <p><strong>{{taskStatus.type}}</strong></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
/* General Page Styling */
.app-container {
    background: linear-gradient(to right, #eef2f3, #ffffff);
    min-height: 100vh;
    padding: 20px;
    font-family: 'Poppins', sans-serif;
}

.page-container {
    max-width: 1200px;
    margin: auto;
    padding: 20px;
}

/* Page & Section Titles */
.section-heading {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    color: #333;
    margin-bottom: 10px;
    margin-top: 40px;
}

.page-title {
    text-align: center;
    font-size: 26px;
    font-weight: 700;
    color: #555;
    margin-bottom: 30px;
}

/* Content Layout */
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 100px;
    margin-top: 100px;
}

/* Increased Card Width */
.left-column, .right-column {
    background: #ffffff;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease-in-out;
    width: 100%;
}
.left-column:hover, .right-column:hover {
    transform: translateY(-5px);
}

/* Section Titles */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
    color: #4A4A4A;
}

/* Status Box & Dropdown */
.status-container {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.status-box {
    padding: 8px 15px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    text-transform: uppercase;
    text-align: center;
    min-width: 120px;
}

/* Dynamic Status Colors */
.status-in-progress {
    background: #f4c430;
    color: #fff;
}
.status-done {
    background: #28a745;
    color: #fff;
}
.status-progress {
    background: #17a2b8;
    color: #fff;
}
.status-canceled {
    background: #dc3545;
    color: #fff;
}
.status-default {
    background: #6c757d;
    color: #fff;
}

/* Status Dropdown */
.status-dropdown {
    padding: 10px;
    border-radius: 8px;
    background-color: #6ca8f0;
    color: white;
    font-weight: bold;
    cursor: pointer;
    border: 2px solid transparent;
    transition: background 0.3s ease, border 0.3s ease;
}
.status-dropdown:hover {
    background-color: #4a90e2;
    border-color: #357ab7;
}

/* Tasks Section */
.tasks {
    margin-top: 20px;
}
.task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #f9f9f9;
    padding: 12px;
    margin-bottom: 12px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.08);
}
.task-item:hover {
    background: #eceff1;
}

/* Task Dropdown */
.task-dropdown {
    padding: 6px 12px;
    border-radius: 6px;
    background-color: #4a90e2;
    color: white;
    font-weight: bold;
    border: none;
    cursor: pointer;
    transition: background 0.3s ease;
}
.task-dropdown:hover {
    background-color: #357ab7;
}

/* Right Column Sections */
.section {
    margin-bottom: 20px;
}
.section p {
    font-size: 16px;
    line-height: 1.6;
    color: #555;
}
</style>
