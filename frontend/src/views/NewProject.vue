<script setup>
import router from '@/router';
import axios from 'axios';
import { ref, onMounted } from 'vue';
import Toast from '../components/toasts.vue';
import Navbar from '../components/navbar.vue';
import Susaf from '../components/Susaf.vue';
import { useStateStore } from "../stores/state.js";

const projectState = useStateStore();

const model = ref({
    status: {
        goal_open: true,
        fresh_page: false
    }
});

const metrics = ref([
        { name: 'Has at least one sustainability practice/criteria', status: 'to_do' },
        { name: 'Ensure sustainability considerations are included in the task description', status: 'to_do' },
        { name: 'Identify sustainability objectives related to the task', status: 'to_do' },
        { name: "Assign sustainability-related labels ('energy efficient', 'low carbon')", status: 'to_do' },
        { name: 'Implement green coding practices (optimized queries, efficient algorithms)', status: 'to_do' },
        { name: 'Ensure that cloud services are deployed in low-carbon data centers', status: 'to_do' },
        { name: 'Validate that the feature sustainability benchmarks/criteria were achieved', status: 'to_do' },
        { name: 'Ensure the UI follows accessibility', status: 'to_do' },
        { name: 'Document sustainability impact in sprint reports', status: 'to_do' },
        { name: 'Generate sustainability KPIs', status: 'to_do' }
]);

const project_data = ref({
    name: '',
    token: '',
    description: '',
});

const notifications = ref({
    message: "",
    type: "",
    position: "right",
    show: false,
    wide: 45,
    callback: () => { },
    get duration() {
        return this.type === "success" ? 2000 : 4000;
    }
});

const susaf_response = ref('');
const showModal = ref(false);
const showProgressModal = ref(false);
const projectToken = ref('');
const progress = ref(0);
const progressMessage = ref('');

function close_toast() {
    notifications.value.show = false;
    notifications.value.callback();
}

onMounted(() => {
    model.value.status.fresh_page = true;
});

function toggleCreateGoal() {
    model.value.status.goal_open = !model.value.status.goal_open;
    model.value.status.fresh_page = false;
}

function openModal() {
    showModal.value = true;
}

function closeModal() {
    showModal.value = false;
}

async function submitProjectToken() {
    if (!projectToken.value) {
        showNotification("Project token is required", "error");
        return;
    }

    closeModal();
    showProgressModal.value = true;
    progress.value = 0;
    progressMessage.value = "Fetching project data...";
    await generate_project(projectToken.value);
    showProgressModal.value = false;
}

async function generate_project(token) {
    try {
        axios.defaults.baseURL = 'https://api.susaf.se4gd.eu';
        const response = await axios.post(`/api/v1/recommendations/${token}`);
        susaf_response.value = response.data;

        if (response.data.error) {
            showNotification(response.data.error, "error");
        } else {
            progress.value = 25;
            progressMessage.value = "Saving project...";
            await saveProject(response.data, token);
        }
    } catch (error) {
        showNotification(error.response?.data?.message || "Error fetching project", "error");
    }
}

async function saveProject(data, token) {
    try {
        const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;
        axios.defaults.baseURL = backendBaseUrl;

        project_data.value = {
            name: data.project_name,
            token,
            description: data.project_description
        };

        const response = await axios.post(`${backendBaseUrl}/susaf/projects/`, {
            name: project_data.value.name,
            token: project_data.value.token,
            description: project_data.value.description
        });

        progress.value = 50;
        progressMessage.value = "Generating default backlogs...";
        await generateDefaultBacklogsSprint(response.data.id);
        showNotification("Your project was successfully created", "success");

        notifications.value.callback = () => {
            projectState.saveProjectId(response.data.id); // Set the project ID in the state store
            router.push({ name: 'backlog', params: { id: response.data.id } });
        };
    } catch (error) {
        showNotification(error.response?.data?.message || "You cannot use a token multiple times. Regenerate your token", "error");
    }
}

async function generateDefaultBacklogsSprint(project_id) {
    try {
        const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;
        axios.defaults.baseURL = backendBaseUrl;

        const response = await axios.post(`${backendBaseUrl}/susaf/sprints/`, {
            title: "Backlogs",
            project: project_id
        });

        progress.value = 75;
        progressMessage.value = "Generating backlogs...";
        await generateBacklogs(response.data.id, susaf_response.value);
    } catch (error) {
        showNotification(error.response?.data?.message || "Error saving project", "error");
    }
}

async function generateBacklogs(sprint_id, response_data) {
    const maxRetries = 5; // Maximum number of retries
    let attempt = 0;

    while (attempt < maxRetries) {
        try {
            const backendBaseUrl = import.meta.env.VITE_AI_BACKEND_BASE_URL;
            const data = { message: response_data };

            const response = await axios.post(`${backendBaseUrl}/generate-backlog`, data);

            const tasks = response.data.map(task => ({ ...task, sprint: sprint_id }));
            for (const task of tasks) {
                progressMessage.value = `Sending task: ${task.title}`;
                await send_task(task);
            }
            progress.value = 100;
            progressMessage.value = "Backlogs generated successfully!";
            return; // Exit the function if successful
        } catch (error) {
            attempt++;
            console.error(`Attempt ${attempt} failed:`, error);

            if (attempt >= maxRetries) {
                showNotification(
                    error.response?.data?.message || "Error generating backlogs after multiple attempts",
                    "error"
                );
            } else {
                progressMessage.value = `Retrying to generate backlogs... (Attempt ${attempt + 1})`;
            }
        }
    }
}

async function send_task(task) {
    try {
        const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;
        axios.defaults.baseURL = backendBaseUrl;

        task.impact = task.impact.map(impact => impact.toLowerCase());

        const response = await axios.post(`${backendBaseUrl}/susaf/tasks/`, {
            title: task.title,
            description: task.description,
            type: task.type,
            sprint: task.sprint,
            impact: task.impact,
        });

        for (const metric of metrics.value) {
            await send_metric(metric, response.data.id);
        }
    } catch (error) {
        showNotification(error.response?.data?.message || "Error sending task", "error");
    }
}

async function send_metric(metric, task_id) {
    try {
        const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;
        axios.defaults.baseURL = backendBaseUrl;

        await axios.post(`${backendBaseUrl}/susaf/metrics/`, {
            text: metric.name,
            status: metric.status,
            task: task_id
        });

    } catch (error) {
        alert(error.message);
        showNotification(error.response?.data?.message || "Error sending metric", "error");
        console.log(error);
    }
}

function showNotification(message, type) {
    notifications.value.message = message;
    notifications.value.type = type;
    notifications.value.show = true;
}
</script>

<template>
    <section class="container">
        <Navbar></Navbar>
        <Susaf></Susaf>

        <!-- Button to open modal -->
        <button class="generate-button" @click="openModal"> Generate Backlogs </button>

        <!-- Modal -->
        <div v-if="showModal" class="modal-overlay">
            <div class="modal">
                <h2>Enter Project Token</h2>
                <input v-model="projectToken" type="text" placeholder="Enter token..." class="modal-input"/>
                <div class="modal-actions">
                    <button class="modal-btn confirm" @click="submitProjectToken">Submit</button>
                    <button class="modal-btn cancel" @click="closeModal">Cancel</button>
                </div>
            </div>
        </div>

        <!-- Progress Modal -->
        <div v-if="showProgressModal" class="modal-overlay">
            <div class="modal">
                <h2>Progress</h2>
                <p>{{ progressMessage }}</p>
                <div class="progress-bar">
                    <div class="progress" :style="{ width: progress + '%' }"></div>
                </div>
            </div>
        </div>

        <Toast 
            :message="notifications.message" 
            :type="notifications.type"
            :show="notifications.show"
            :position="notifications.position"
            :wide="notifications.wide"
            :duration="notifications.duration"
            @close_toast="close_toast"
        />
    </section>
</template>

<style scoped>
@import url("../assets/css/homepage.css");

/* Modal Styles */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal {
    background: white;
    padding: 40px; /* Increased padding for more spacing */
    border-radius: 20px; /* Slightly more rounded corners */
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    text-align: center;
    width: 500px; /* Slightly wider modal */
    max-width: 90%; /* Responsive design */
    animation: fadeIn 0.3s ease-in-out;
}

.modal h2 {
    margin-bottom: 50px; /* Add more space below the heading */
    font-size: 18px; /* Keep font size consistent */
    font-weight: 500px;
    color: #333;
}

.modal-input {
    width: 95%;
    padding: 15px; /* Add more padding inside the input */
    margin-bottom: 50px; /* Add more space below the input */
    border: 1px solid #ccc;
    border-radius: 10px; /* Slightly more rounded input */
    font-size: 14px;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.modal-actions {
    display: flex;
    justify-content: space-between;
    gap: 15px; /* Add more spacing between buttons */
}

.modal-btn {
    padding: 15px 25px; /* Add more padding to buttons */
    border: none;
    border-radius: 10px; /* Slightly more rounded buttons */
    cursor: pointer;
    font-size: 14px;
    font-weight: 400;
    transition: all 0.3s ease;
}

.modal-btn.confirm {
    background: linear-gradient(135deg, #4CAF50, #2E7D32);
    color: white;
}

.modal-btn.confirm:hover {
    background: linear-gradient(135deg, #66BB6A, #388E3C);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.modal-btn.cancel {
    background: linear-gradient(135deg, #f44336, #d32f2f);
    color: white;
}

.modal-btn.cancel:hover {
    background: linear-gradient(135deg, #e57373, #c62828);
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Fade-in animation for modal */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

/* Progress Bar Styles */
.progress-bar {
    width: 100%;
    height: 10px;
    background: #e0e0e0;
    border-radius: 5px;
    overflow: hidden;
    margin-top: 10px;
}

.progress {
    height: 100%;
    background: #4CAF50;
    transition: width 0.3s ease;
}

/* Generate Button Styles */
.generate-button {
    position: absolute;
    bottom: 50px;
    left: 50px;
    background: linear-gradient(135deg, #4CAF50, #2E7D32);
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    border-radius: 25px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: all 0.3s ease;
}

.generate-button:hover {
    background: linear-gradient(135deg, #66BB6A, #388E3C);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    transform: translateY(-2px);
}

.generate-button:active {
    transform: translateY(0);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
