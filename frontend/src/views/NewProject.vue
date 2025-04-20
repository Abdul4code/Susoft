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

        for (const metric of task.metrics) {
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
            text: metric.text,
            status: metric.status,
            task: task_id
        });
    } catch (error) {
        showNotification(error.response?.data?.message || "Error sending metric", "error");
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
        <button class="back-button" @click="openModal"> Generate Backlogs </button>

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
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 300px;
}

.modal h2 {
    margin-bottom: 15px;
    font-size: 18px;
}

.modal-input {
    width: 100%;
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.modal-actions {
    display: flex;
    justify-content: space-between;
}

.modal-btn {
    padding: 8px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.modal-btn.confirm {
    background: #4CAF50;
    color: white;
}

.modal-btn.cancel {
    background: #f44336;
    color: white;
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
</style>
