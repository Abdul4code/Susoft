<script setup>
import router from '@/router';
import axios from 'axios'
import { ref, onMounted } from 'vue'
import Toast from '../components/toasts.vue'
import Navbar from '../components/navbar.vue'
import Susaf from '../components/Susaf.vue'

const model = ref({
    status: {
        goal_open: true,
        fresh_page: false
    }
})

const project_data = ref({
    name: '',
    token: '',
    description: '',
})

const notifications = ref({
    message: "",
    type: "",
    position: "right",
    show: false,
    wide: 45,
    callback: () => { },
    duration: 2000
})

const susaf_response = ref('')

// Modal state
const showModal = ref(false)
const projectToken = ref('') // Stores user input

function close_toast() {
    notifications.value.show = false
    notifications.value.callback()
}

onMounted(() => {
    model.value.status.fresh_page = true
})

function toggleCreateGoal() {
    model.value.status.goal_open = !model.value.status.goal_open
    model.value.status.fresh_page = false
}

// Show modal when button is clicked
function openModal() {
    showModal.value = true
}

// Hide modal
function closeModal() {
    showModal.value = false
}

// Get project with user input token
function submitProjectToken() {
    if (!projectToken.value) {
        notifications.value.show = true;
        notifications.value.message = "Project token is required";
        notifications.value.type = "error";
        return;
    }

    closeModal(); // Close modal
    generate_project(projectToken.value); // Call API with user input token
}

function generate_project(token) {
    axios.defaults.baseURL = 'https://api.susaf.se4gd.eu';

    axios.post(`/api/v1/recommendations/${token}`)
        .then(function (response) {
            susaf_response.value = response.data
            saveProject(response, token)
            
        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error fetching project";
            notifications.value.type = "error";
        });

    
}

function saveProject(result, token) {
    project_data.value.name = result.data.project_name
    project_data.value.token = token
    project_data.value.description = result.data.project_description

    axios.defaults.baseURL = 'http://129.213.86.120:8000';

    axios.post('http://129.213.86.120:8000/susaf/projects/', {
        name: project_data.value.name,
        token: project_data.value.token,
        description: project_data.value.description
    })
        .then(function (response) {
            console.log(response)
            generateDefaultBacklogsSprint(response.data.id)

            notifications.value.show = true;
            notifications.value.message = "Your project was successfully created";
            notifications.value.type = "success";
            
                    // Ensure response contains the expected project ID
            const projectId = response.data?.id; 

            if (projectId) {
                notifications.value.callback = () => {
                    // router.push({ name: 'backlog', params: { id: projectId } });
                };
            }
        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error saving project";
            notifications.value.type = "error";
        });
}

function generateDefaultBacklogsSprint(project_id){
    axios.defaults.baseURL = 'http://129.213.86.120:8000';

    axios.post('http://129.213.86.120:8000/susaf/sprints/', {
        title: "Backlogs",
        project: project_id
    })
        .then(function (response) {
            generateBacklogs(response.data.id, susaf_response.value)
        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error saving project";
            notifications.value.type = "error";
        });
}


function generateBacklogs(sprint_id, response_data){
    axios.post('http://129.213.86.120:5000/generate-backlog', response_data)
        .then(function (response) {
            let tasks = response.data.map(data => ({
                ...data, 
                sprint: sprint_id 
            }));

            console.log(tasks)

            for (const task of tasks) {
                send_task(task)
            }
        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error saving project";
            notifications.value.type = "error";
        });

    // var tasks = [
    //     {
    //         'title': 'Create an Hate speech Detection functionality',
    //         'description': 'This functionality should allow people who are natural believers of independence to overcome same',
    //         'type': 'positive',
    //         'sprint':sprint_id,
    //         'impact': ['economic', 'social'],
    //         'metrics': [
    //             {
    //                 'text': "Does the implemented code suggest user sustainability",
    //                 'status': 'done'
    //             }
    //         ]
    //     },
    //     {
    //         'title': 'Open the figure of the National Assemby',
    //         'description': 'This functionality should allow people who are natural believers of independence to overcome same',
    //         'type': 'negative',
    //         'sprint':sprint_id,
    //         'impact': ['economic', 'social', 'environmental'],
    //         'metrics': [
    //             {
    //                 'text': "Is it necessary to obtain this",
    //                 'status': 'done'
    //             },
    //             {
    //                 'text': "Is it necessary to obtain this",
    //                 'status': 'done'
    //             }
    //         ]
    //     },
    //     {
    //         'title': 'Open the figure of the National Assemby',
    //         'description': 'This functionality should allow people who are natural believers of independence to overcome same',
    //         'type': 'negative',
    //         'sprint':sprint_id,
    //         'impact': ['economic', 'social', 'environmental'],
    //         'metrics': [
    //             {
    //                 'text': "Is it necessary to obtain this",
    //                 'status': 'done'
    //             },
    //             {
    //                 'text': "Is it necessary to obtain this",
    //                 'status': 'done'
    //             }
    //         ]
    //     }
    // ]
}

function send_task(task){
    axios.defaults.baseURL = 'http://129.213.86.120:8000';

        axios.post('http://129.213.86.120:8000/susaf/tasks/', {
            title: task.title,
            description: task.description,
            type: task.type,
            sprint:task.sprint,
            impact: task.impact,
        })
        .then(function (response) {
            for (const metric of task.metrics) {
                send_metric(metric, response.data.id)
            }
        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error saving project";
            notifications.value.type = "error";
        });
}

function send_metric(metric, task_id){
    axios.defaults.baseURL = 'http://129.213.86.120:8000';

        axios.post('http://129.213.86.120:8000/susaf/metrics/', {
            text: metric.text,
            status: metric.status,
            task: task_id
        })
        .then(function (response) {

        })
        .catch(function (error) {
            console.log(error)
            notifications.value.show = true;
            notifications.value.message = error.response?.data?.message || "Error saving project";
            notifications.value.type = "error";
        });
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
</style>
