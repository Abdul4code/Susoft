<script setup>
    import {ref} from 'vue'

    const model = ref({
        styles : {
            "navbar_open" : false,
            "fresh_load": true,
            "goal_nav_open": false,
            "application_nav_open": false,
            "contact_nav_open": false
        }
    })

    function open_nav(){
        model.value.styles.navbar_open = true
        model.value.styles.fresh_load = false
    }

    function close_nav(){
        model.value.styles.navbar_open = false
    }

    function toggle_subnav(nav){
        if(nav == "Applications"){
            model.value.styles.application_nav_open = !model.value.styles.application_nav_open
            model.value.styles.goal_nav_open = false
            model.value.styles.contact_nav_open = false

        }else if(nav == "Goals"){
            model.value.styles.goal_nav_open = !model.value.styles.goal_nav_open
            model.value.styles.contact_nav_open = false
            model.value.styles.application_nav_open = false

        }else if(nav == "Contacts"){
            model.value.styles.contact_nav_open = !model.value.styles.contact_nav_open
            model.value.styles.goal_nav_open = false
            model.value.styles.application_nav_open = false
        }
    }

</script>

<template>
    <nav class="nav-container" :class="{'unfoldbar' : model.styles.navbar_open, 'foldbar': !model.styles.navbar_open && !model.styles.fresh_load}">
        <a href="login" class="brand-link"><div class="brand">
                <img src="../assets/images/icon.png" alt="" class="icon" />
                <p class="brand-text"> Trakit </p>
        </div></a>

        <div v-if="model.styles.navbar_open" class="fold" @click.prevent="close_nav"> <img src="../assets/images/fold.svg" alt=""></div>
        <div v-else @click.prevent="open_nav" class="fold"> <img src="../assets/images/harmburger.svg" alt=""></div>
        

        <nav class="nav">
            <ul class="left-nav"> 
                <li> <span class="nav-text">Dashboard</span></li>
                <li :class="{'nav-active': model.styles.goal_nav_open}" @click.prevent="toggle_subnav('Goals')">
                    <div class="nav-header"><span class="nav-text">Goals</span> 
                        <span class="down-icon"> <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.goal_nav_open}"/></span>
                    </div>
                    <div class="goals-dropdown" :class="{'foldsubbar': !model.styles.goal_nav_open, 'unfoldsubbar': model.styles.goal_nav_open}">
                        <p> Graduate School Application </p>
                        <p> Getting Grant for New application </p>
                        <p> Getting investors for my new application </p>
                        <p> Sunday School </p>
                        <p><a href="#" class="nav-link"> More Goals </a> </p>
                    </div>
                </li>
                <li :class="{'nav-active': model.styles.application_nav_open}" @click.prevent="toggle_subnav('Applications')"> 
                    <div class="nav-header">
                        <span class="nav-text" >Applications</span> <span class="down-icon"> 
                            <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.application_nav_open}"/></span>
                        </div>
                    <div class="applications-dropdown" :class="{'foldsubbar': !model.styles.application_nav_open, 'unfoldsubbar': model.styles.application_nav_open}">
                        <p> University of Calgary </p>
                        <p> Google Internship </p>
                        <p> Email Responses </p>
                        <p> Sunday School Applications </p>
                        <p><a href="#" class="nav-link"> More Applications </a> </p>
                    </div>
                </li>
                <li :class="{'nav-active': model.styles.contact_nav_open}" @click.prevent="toggle_subnav('Contacts')"> 
                    <div class="nav-header">
                        <span class="nav-text">Contacts</span><span class="down-icon"> 
                        <img src="../assets/images/down.svg" :class="{'turn-dropdown-icon': model.styles.contact_nav_open}"/></span>
                    </div>
                    <div class="contacts-dropdown" :class="{'foldsubbar': !model.styles.contact_nav_open, 'unfoldsubbar': model.styles.contact_nav_open}">
                        <p> Sunday Olukoya </p>
                        <p> Aina Oluwole </p>
                        <p> Convenant Graduate School </p>
                        <p> Work station man </p>
                        <p><a href="#" class="nav-link"> More Contacts </a> </p>
                    </div>
                </li>
            </ul>
            <ul class="right-nav">
                <div class="left-right-nav">
                    <li class="search-field"> <input type="text" placeholder="Search by any keyword"/> </li>
                    <li class="create_new"> <button> + &nbsp;  Add New </button></li>
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