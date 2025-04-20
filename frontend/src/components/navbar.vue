<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useStateStore } from "../stores/state.js";
import { useRouter } from 'vue-router';

const router = useRouter();

const model = ref({
    styles: {
        "navbar_open": false,
        "fresh_load": true,
        "project_nav_open": false,
        "sprint_nav_open": false,
        "contributors_nav_open": false
    }
});

const projects = ref("");
const sprints = ref([]);

const base_url = import.meta.env.BASE_URL;
const backendBaseUrl = import.meta.env.VITE_BACKEND_BASE_URL;

const projectState = useStateStore();

function open_nav() {
    model.value.styles.navbar_open = true;
    model.value.styles.fresh_load = false;
}

function close_nav() {
    model.value.styles.navbar_open = false;
}

function toggle_subnav(nav) {
    if (nav == "Applications") {
        model.value.styles.sprint_nav_open = !model.value.styles.sprint_nav_open;
        model.value.styles.project_nav_open = false;
        model.value.styles.contributors_nav_open = false;
        handleSprintdropdownClick()
    } else if (nav == "Goals") {    
        model.value.styles.project_nav_open = !model.value.styles.project_nav_open;
        model.value.styles.contributors_nav_open = false;
        model.value.styles.sprint_nav_open = false;
    } else if (nav == "Contacts") {
        model.value.styles.contributors_nav_open = !model.value.styles.contributors_nav_open;
        model.value.styles.project_nav_open = false;
        model.value.styles.sprint_nav_open = false;
    }
}

async function get_project() {
  try {
    const response = await axios.get(`${backendBaseUrl}/susaf/projects/`);
    projects.value = response.data;
  } catch (error) {
    console.error(error);
    alert(error);
  }
}

onMounted(() => {
    projects.value = "";
    sprints.value = [];

    get_project();

    console.log("Project ID from state:", projectState.state.project_id);

    if (projectState.state.project_id) {
        get_sprints(projectState.state.project_id);
    }

});

function handleProjectClick(projectId) {
    projectState.saveProjectId(projectId); // Set the project ID in the state store
    get_sprints(projectId)


    router.push({ name: 'backlog', params: { id: projectId} });
    console.log(`Project clicked: ${projectState.state.project_id}`);
}


function handleSprintdropdownClick() {
    let new_id = projectState.state.project_id;
    get_sprints(new_id)
    
}

async function get_sprints(project_id) {
    sprints.value = [];

    try {
        const response = await axios.get(`${backendBaseUrl}/susaf/sprints/`);
        for (const sprint of response.data) {
            if (sprint.project == project_id) {
                sprints.value.push(sprint);
                console.log(sprints.value)
            }
            
        }

    } catch (error) {
        console.error(error);
    }
}

</script>

<template>
    <nav class="nav-container" :class="{'unfoldbar': model.styles.navbar_open, 'foldbar': !model.styles.navbar_open && !model.styles.fresh_load}">
        <router-link :to="base_url" class="brand-link">
            <div class="brand">
                <img src="../assets/images/icon.png" alt="" class="icon" />
                <p class="brand-text">Susoft</p>
            </div>
        </router-link>

        <div v-if="model.styles.navbar_open" class="fold" @click.prevent="close_nav">
            <img src="../assets/images/fold.svg" alt="">
        </div>
        <div v-else @click.prevent="open_nav" class="fold">
            <img src="../assets/images/harmburger.svg" alt="">
        </div>

        <nav class="nav">
            <ul class="left-nav">
                <li><router-link to="/learninghub" class="list"><span class="nav-text">Learning Hub</span></router-link></li>
                <li :class="{'nav-active': model.styles.project_nav_open}" @click.prevent="toggle_subnav('Goals')">
                    <div class="nav-header">
                        <span class="nav-text">Projects</span>
                        <span class="down-icon">
                            <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.project_nav_open}" />
                        </span>
                    </div>
                    <div class="goals-dropdown" :class="{'foldsubbar': !model.styles.project_nav_open, 'unfoldsubbar': model.styles.project_nav_open}">
                        <p v-for="(project, index) in projects" :key="index" @click="handleProjectClick(project.id)">
                            <router-link :to="`/backlogs/${project.id}`" class="nav-link">{{ project.name }}</router-link>
                        </p>
                        <p><router-link to="/new_project" class="nav-link">Add Project</router-link></p>
                    </div>
                </li>
                <li :class="{'nav-active': model.styles.sprint_nav_open}" @click.prevent="toggle_subnav('Applications')">
                    <div class="nav-header">
                        <span class="nav-text">Kanban Boards</span>
                        <span class="down-icon">
                            <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.sprint_nav_open}" />
                        </span>
                    </div>
                    <div class="applications-dropdown" 
                        :class="{'foldsubbar': !model.styles.sprint_nav_open, 'unfoldsubbar': model.styles.sprint_nav_open}"
                        >
                        
                        <template v-if="sprints.length > 0">
                            <p v-for="(sprint, index) in sprints" :key="index">
                                <router-link :to="`/sprint/${sprint.id}`" class="nav-link">{{ sprint.title }}</router-link>
                            </p>
                        </template>
                        <template v-else>
                            <p class="no-sprints nav-link">No project is selected</p>
                        </template>
                        
                    </div>
                </li>
                
                <li><router-link to="/retrospective/1" class="list"><span class="nav-text">Retrospective</span></router-link></li>
            </ul>
            <ul class="right-nav">
                <div class="left-right-nav">
                    <li class="search-field"><input type="text" placeholder="Search by any keyword" /></li>
                    <li class="create_new">
                        <button><router-link to="/new_project">Add New</router-link></button>
                    </li>
                </div>
                <div class="right-right-nav">
                    
                    <div>
                        <li class="user">
                            <img src="../assets/images/user.svg" />
                            <span class="down-icon">
                                <img src="../assets/images/down.svg" />
                            </span>
                        </li>
                        <div class="user-dropitem">
                            <li class="username">Mpape</li>
                            <li class="logout">Log out</li>
                            <li class="email">nightingale9ja@gmail.com</li>
                        </div>
                    </div>
                </div>
            </ul>
        </nav>
    </nav>
</template>

<style scoped>
@import url("../assets/css/nav.css");

.no-sprints {
    color: red;
}
</style>
