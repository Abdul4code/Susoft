<script setup>
import { ref, computed, onMounted } from 'vue';
import Navbar from '../components/navbar.vue';
import router from '@/router';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'vue-chartjs';

// Register Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend);

const route = useRoute();
const taskid = route.params.id;

// Define Status Options
const STATUS_OPTIONS = ['all', 'To do', 'In progress', 'In review', 'Completed'];

const taskDetail = ref("");
const taskStatus = ref({
    mainStatus: 'All',
    metrics: []
});

// Computed property to filter tasks based on main status
const filteredMetrics = computed(() => {
    if (taskStatus.value.mainStatus === 'All') {
        return taskStatus.value.metrics;
    }
    return taskStatus.value.metrics.filter(task => task.status === taskStatus.value.mainStatus);
});

// Pie chart data
const chartData = ref({
    labels: ['To do', 'In progress', 'In review', 'Completed'],
    datasets: [
        {
            label: 'Metrics Status',
            data: [0, 0, 0, 0],
            backgroundColor: ['#b0bec5', '#fdd835', '#26c6da', '#66bb6a'],
            borderWidth: 1
        }
    ]
});

// Function to map status to value
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
            return '';
    }
}

// Function to update chart data
function updateChartData() {
    const statusCounts = { 'to_do': 0, 'in_progress': 0, 'in_review': 0, 'completed': 0 };
    taskStatus.value.metrics.forEach(metric => {
        statusCounts[metric.status] = (statusCounts[metric.status] || 0) + 1;
    });

    chartData.value.datasets[0].data = [
        statusCounts['to_do'],
        statusCounts['in_progress'],
        statusCounts['in_review'],
        statusCounts['completed']
    ];
}

// Fetch task details
function getTask(taskId) {
    axios.get(`${import.meta.env.VITE_BACKEND_BASE_URL}/susaf/tasks/${taskId}`)
        .then(response => {
            taskDetail.value = response.data;
        })
        .catch(error => {
            alert(error);
        });
}

// Fetch metrics and update chart data
async function getMetrics(taskId) {
    try {
        const response = await axios.get(`${import.meta.env.VITE_BACKEND_BASE_URL}/metrics/by-task/${taskId}/`);
        taskStatus.value.metrics = response.data.map(metric => ({
            name: metric.text,
            status: metric.status,
            id: metric.id
        }));
        updateChartData();
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}

// Update metric status
async function updateMetricStatus(metric) {
    try {
        await axios.patch(`${import.meta.env.VITE_BACKEND_BASE_URL}/metrics/${metric.id}/`, {
            status: metric.status
        });
        updateChartData();
    } catch (error) {
        console.error("Error updating metric status:", error);
        alert("Failed to update the metric's status. Please try again.");
    }
}

getTask(taskid);
getMetrics(taskid);
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

                    <!-- Pie Chart Section -->
                    <div class="chart-section">
                        <h3> </h3>
                        <Pie :data="chartData" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.page-container {
    padding: 40px 20px;
    font-family: 'Inter', sans-serif;
    width: 95%;
    margin: auto;
    color: #333;
}

.page-title {
    text-align: center;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 10px;
    color: #2c3e50;
}

.task-title {
    text-align: center;
    font-size: 22px;
    font-weight: 500;
    color: #555;
    margin-bottom: 40px;
}

.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 60px;
}

.left-column, .right-column {
    background: #fff;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease-in-out;
}

.left-column:hover,
.right-column:hover {
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.12);
}

.status-section h3,
.description h3,
.sustainability-impact h3,
.Imapct\ Type h3 {
    margin-bottom: 16px;
    font-weight: 600;
    font-size: 20px;
    color: #34495e;
    border-bottom: 2px solid #ecf0f1;
    padding-bottom: 8px;
}

.status-dropdown {
    padding: 10px 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    font-size: 14px;
    appearance: none;
    transition: background-color 0.3s ease, color 0.3s ease;
    min-width: 140px;
}

.tasks {
    margin-top: 10px;
}

.task-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #fdfdfd;
    padding: 14px 16px;
    margin-bottom: 12px;
    border-radius: 10px;
    border: 1px solid #eaeaea;
    font-size: 14px;
    font-weight: 500;
    transition: box-shadow 0.3s ease;
}

.task-item:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.status-dropdown.to_do {
    background-color: #b0bec5;
    color: #fff;
}
.status-dropdown.in_progress {
    background-color: #fdd835;
    color: #333;
}
.status-dropdown.in_review {
    background-color: #26c6da;
    color: #fff;
}
.status-dropdown.completed {
    background-color: #66bb6a;
    color: #fff;
}

.right-column p,
.left-column p {
    font-size: 14px;
    line-height: 1.6;
    color: #666;
}

h3 {
    margin-top: 30px;
}

.chart-section {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
    height: 400px; /* Ensure the height is consistent */
    text-align: center;
    flex-direction: column;
    margin-top: 100px;
    gap: 40px;
}

/* Responsive Design */
@media (max-width: 768px) {
    .content-grid {
        grid-template-columns: 1fr;
    }
    .page-title {
        font-size: 28px;
    }
    .task-title {
        font-size: 18px;
    }
}

/* Add styles for the chart section */
.chart-section {
    margin-top: 30px;
    text-align: center;
}
</style>