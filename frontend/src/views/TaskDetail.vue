<script setup>
import { ref, computed } from 'vue';
import Navbar from '../components/navbar.vue';
import router from '@/router';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();

const taskid = route.params.id;

// Define Status Options
const STATUS_OPTIONS = ['all', 'To do', 'In progress', 'In review', 'Completed'];

const taskDetail = ref("");

// Define Task Status
const taskStatus = ref({
    mainStatus: 'All',
    metrics: [
    ]
});

// Computed property to filter tasks based on main status
const filteredMetrics = computed(() => {
    if (taskStatus.value.mainStatus === 'All') {
        return taskStatus.value.metrics;
    }
    return taskStatus.value.metrics.filter(task => task.status === taskStatus.value.mainStatus);
});

// Function to dynamically assign class for styling based on status
const statusClass = (status) => {
    return {
        'to_do': status === 'To do',
        'in_progress': status === 'In progress',
        'in_review': status === 'In review',
        'completed': status === 'Completed'
    };
};

function status_to_value(status) {
    switch (status) {
        case 'To do':
            return 'to_do';
        case 'In progress':
            return 'in_progress';
        case 'In review':
            return 'in_review';
        case 'Completed':
            return 'completed';
        default:
            return status;
    }
}

// Use the base backend URL from environment variables
const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

function getTask(taskId) {
    axios.get(`${backendBaseUrl}/susaf/tasks/${taskId}`)
        .then(function (response) {
            taskDetail.value = response.data;
        })
        .catch(function (error) {
            alert(error);
        });
}

async function getMetrics(taskId) {
    try {
        const response = await axios.get(`${backendBaseUrl}/metrics/by-task/${taskId}/`);
        console.log('Metrics fetched:', response.data);
        // Update taskStatus metrics with the fetched data
        taskStatus.value.metrics = response.data.map(metric => ({
            name: metric.text,
            status: metric.status,
            id: metric.id,
        }));
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}


async function updateMetricStatus(metric) {
    console.log(metric);
    try {
        const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;
        await axios.patch(`${backendBaseUrl}/metrics/${metric.id}/`, {
            status: metric.status,
        });
        console.log(`Metric ${metric.id} updated to status ${metric.status}`);
    } catch (error) {
        console.error("Error updating metric status:", error);
        alert("Failed to update the metric's status. Please try again.");
    }
}

getTask(taskid);
getMetrics(taskid)
</script>



<template>
    <div>
        <Navbar />
        <div class="page-container">
            <h2 class="page-title">Project Task Tracker</h2>
            <p class="task-title"> {{ taskDetail.title }}</p>
            
            <div class="content-grid">
                <!-- Left Column -->
                <div class="left-column">
                    <div class="status-section">
                        <h3>Task Metrics</h3>

                        <div class="tasks">
                            <div v-for="(task, index) in filteredMetrics" :key="index" class="task-item">
                                <span>{{ task.name }}</span>
                                <select 
                                    v-model="task.status" 
                                    class="status-dropdown" 
                                    :class="task.status" 
                                    @change="updateMetricStatus(task)"
                                >
                                    <option 
                                        v-for="status in STATUS_OPTIONS.slice(1)"
                                        :key="status" 
                                        :value="status_to_value(status)"
                                    >
                                        {{ status }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Right Column -->
                <div class="right-column">
                    <div class="description">
                        <h3>Description</h3>
                        <p> {{ taskDetail.description }} </p>
                    </div>

                    <div class="sustainability-impact">
                        <h3> Sustainability Impact </h3>
                        <p>{{ taskDetail.impact.join(", ")}}</p>
                    </div>

                    <div class="Imapct Type">
                        <h3>Impact Type</h3>
                        <p>{{ taskDetail.type}}</p>
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
    max-width: 80%;
    margin: auto;
}
.page-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 20px;
    margin-top: 25px;
    font-family: 'Poppins', sans-serif;
}

.task-title{
    text-align: center;
    font-size: 20px;
    margin-bottom: 20px;
    margin-top: 25px;
    font-family: 'Poppins', sans-serif;
    margin-bottom: 50px;
}
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 120px;
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
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: background-color 0.3s ease;
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
.status-dropdown.to_do {
    background-color: #6c757d;
    color: white;
}
.status-dropdown.in_progress {
    background-color: #ffc107;
    color: black;
}
.status-dropdown.in_review {
    background-color: #17a2b8;
    color: white;
}
.status-dropdown.completed {
    background-color: #28a745;
    color: white;
}

h3{
    margin-top: 40px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr;
    }
}
</style>