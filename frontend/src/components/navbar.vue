<script setup>
    import {ref} from 'vue'
    import axios from 'axios'

    const model = ref({
        styles : {
            "navbar_open" : false,
            "fresh_load": true,
            "project_nav_open": false,
            "sprint_nav_open": false,
            "contributors_nav_open": false
        }
    })

    const projects = ref("")

    const base_url = import.meta.env.BASE_URL
    
    function open_nav(){
        model.value.styles.navbar_open = true
        model.value.styles.fresh_load = false
    }

    function close_nav(){
        model.value.styles.navbar_open = false
    }

    function toggle_subnav(nav){
        if(nav == "Applications"){
            model.value.styles.sprint_nav_open = !model.value.styles.sprint_nav_open
            model.value.styles.project_nav_open = false
            model.value.styles.contributors_nav_open = false

        }else if(nav == "Goals"){
            model.value.styles.project_nav_open = !model.value.styles.project_nav_open
            model.value.styles.contributors_nav_open = false
            model.value.styles.sprint_nav_open = false

        }else if(nav == "Contacts"){
            model.value.styles.contributors_nav_open = !model.value.styles.contributors_nav_open
            model.value.styles.project_nav_open = false
            model.value.styles.sprint_nav_open = false
        }
    }

    function get_project(){
        axios.get(`http://localhost:8000/susaf/projects/`)
            .then(function (response) {
                projects.value = response.data
            })
            .catch(function (error) {
                console.log(error)
                alert(error)
            });
    }

    get_project()



</script>

<template>
    <nav class="nav-container" :class="{'unfoldbar' : model.styles.navbar_open, 'foldbar': !model.styles.navbar_open && !model.styles.fresh_load}">
        <a :href="base_url" class="brand-link">
            <div class="brand">
                <img src="../assets/images/icon.png" alt="" class="icon" />
                <p class="brand-text">Susoft</p>
            </div>
        </a>

        <div v-if="model.styles.navbar_open" class="fold" @click.prevent="close_nav"> <img src="../assets/images/fold.svg" alt=""></div>
        <div v-else @click.prevent="open_nav" class="fold"> <img src="../assets/images/harmburger.svg" alt=""></div>
        

        <nav class="nav">
            <ul class="left-nav"> 
                <li> <a class="list" :href="base_url + 'learninghub'"> <span class="nav-text">Learning Hub</span></a></li>
                <li :class="{'nav-active': model.styles.project_nav_open}" @click.prevent="toggle_subnav('Goals')">
                    <div class="nav-header"><span class="nav-text">Projects</span> 
                        <span class="down-icon"> <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.project_nav_open}"/></span>
                    </div>
                    <div class="goals-dropdown" :class="{'foldsubbar': !model.styles.project_nav_open, 'unfoldsubbar': model.styles.project_nav_open}">
                        <p v-for="(project, index) in projects" :key="index">
                            <a :href="`${base_url}backlogs/${project.id}`" class="nav-link">{{ project.name }}</a>
                        </p>
                        <p><a href="#" class="nav-link"> Add Project </a> </p>
                    </div>
                </li>
                <li :class="{'nav-active': model.styles.sprint_nav_open}" @click.prevent="toggle_subnav('Applications')"> 
                    <div class="nav-header">
                        <span class="nav-text" > Sprints </span> <span class="down-icon"> 
                            <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.sprint_nav_open}"/></span>
                        </div>
                    <div class="applications-dropdown" :class="{'foldsubbar': !model.styles.sprint_nav_open, 'unfoldsubbar': model.styles.sprint_nav_open}">
                        <p> Sprint 1 </p>
                        <p> Sprint 2 </p>
                        <p> Sprint 3 </p>
                        <p> Sprint 4 </p>
                        <p><a href="#" class="nav-link"> Add Sprint </a> </p>
                    </div>
                </li>
                <li :class="{'nav-active': model.styles.contributors_nav_open}" @click.prevent="toggle_subnav('Contacts')"> 
                    <div class="nav-header">
                        <span class="nav-text"> Contributors </span><span class="down-icon"> 
                        <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.contributors_nav_open}"/></span>
                    </div>
                    <div class="contacts-dropdown" :class="{'foldsubbar': !model.styles.contributors_nav_open, 'unfoldsubbar': model.styles.contributors_nav_open}">
                        <p> Abdul4code </p>
                        <p> ersirleem </p>
                        <p> mrcrdr </p>
                        <p> melissapuerto </p>
                        <p><a href="#" class="nav-link"> Add contributor </a> </p>
                    </div>
                </li>
            </ul>
            <ul class="right-nav">
                <div class="left-right-nav">
                    <li class="search-field"> <input type="text" placeholder="Search by any keyword"/> </li>
                    <li class="create_new"> <button> <router-link to="/new_project">Add New</router-link> </button></li>
                </div>
                <div class="right-right-nav">
                    <li class="notification"> <img src="../assets/images/bell.svg"> <span class="note-count">43</span> </li>
                    <div>
                        <li class="user"> <img src="../assets/images/user.svg"> <span class="down-icon"> <img src="../assets/images/down.svg" /></span> </li>
                        <div class="user-dropitem">
                            <li class="username"> Mpape </li>
                            <li class="logout"> Log out </li>
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

</style>