<script setup>
import { ref, computed } from 'vue';
import Navbar from '../components/navbar.vue';
import router from '@/router';
import { useRoute } from 'vue-router';
import axios from 'axios'

const route = useRoute();

const taskid = route.params.id;

// Define Status Options
const STATUS_OPTIONS = ['All', 'To do', 'In progress', 'In review', 'Completed'];

const taskDetail = ref("");

// Define Task Status
const taskStatus = ref({
    mainStatus: 'All',
    metrics: [
        { name: 'Has at least one sustainability practice/criteria', status: 'To do' },
        { name: 'Ensure sustainability considerations are included in the task description', status: 'To do' },
        { name: 'Identify sustainability objectives related to the task', status: 'To do' },
        { name: "Assign sustainability-related labels ('energy efficient', 'low carbon')", status: 'To do' },
        { name: 'Implement green coding practices (optimized queries, efficient algorithms)', status: 'In progress' },
        { name: 'Ensure that cloud services are deployed in low-carbon data centers', status: 'In progress' },
        { name: 'Validate that the feature sustainability benchmarks/criteria were achieved', status: 'In review' },
        { name: 'Ensure the UI follows accessibility', status: 'In review' },
        { name: 'Document sustainability impact in sprint reports', status: 'Completed' },
        { name: 'Generate sustainability KPIs', status: 'Completed' }
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
        'to-do': status === 'To do',
        'in-progress': status === 'In progress',
        'in-review': status === 'In review',
        'completed': status === 'Completed'
    };
};

function getTask(taskId){
    axios.get(`http://129.213.86.120:8000/susaf/tasks/${taskId}`)
        .then(function (response) {
            taskDetail.value = response.data
        })
        .catch(function (error) {
            alert(error)
        });
}

getTask(taskid)
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
                        <label for="main-status">Filter by Status:</label>
                        <select v-model="taskStatus.mainStatus" id="main-status" class="status-dropdown">
                            <option v-for="status in STATUS_OPTIONS" :key="status" :value="status">{{ status }}</option>
                        </select>

                        <div class="tasks">
                            <div v-for="(task, index) in filteredMetrics" :key="index" class="task-item">
                                <span>{{ task.name }}</span>
                                <select v-model="task.status" class="status-dropdown" :class="statusClass(task.status)">
                                    <option v-for="status in STATUS_OPTIONS.slice(1)" :key="status" :value="status">{{ status }}</option>
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
.status-dropdown.to-do {
    background-color: #6c757d;
    color: white;
}
.status-dropdown.in-progress {
    background-color: #ffc107;
    color: black;
}
.status-dropdown.in-review {
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