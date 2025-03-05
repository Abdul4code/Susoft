<script setup>
    import { RouterLink } from 'vue-router'
    import router from '../router/index';
    import onboard from '../components/onboard.vue'
    import { ref } from 'vue'
    import axios from 'axios'
    import { handler } from '../utilities/error_handlers'
    import Toast from '../components/toasts.vue'

    const formData = ref({
        username: '',
        password: ''
    })

    const errors = ref('')

    const notifications = ref({
        message : "",
        type : "",
        position: "right",
        show: false,
        wide: 45, 
        callback: ()=>{},
        duration: 2000
    })

    function close_toast(){
        notifications.value.show = false
        notifications.value.callback()
    }

    const baseUrl = 'http://127.0.0.1:8000'
  
    function submit_login(){
        axios.defaults.headers.common['Authorization'] = ''
        axios.defaults.baseURL = baseUrl

        axios({
            method : 'post',
            url : '/accounts/login/',
            data: formData.value
        }).then(function(response){
            axios.defaults.headers.common['Authorization'] = `Bearer ${response['data']['Access Token']}`
            localStorage.setItem('access', response['data']['Access Token']);

            notifications.value.message = "You are logged in successfully"
            notifications.value.type = "success"
            notifications.value.show = true
            notifications.value.callback = ()=>{
                router.push({name : "homepage"})
            }

        }).catch(function(error){
            if(error.response.status == 400){

                errors.value = handler(error)
                
                if (errors.value.non_field_errors) {
                    
                    notifications.value.message = errors.value.non_field_errors[0]
                    notifications.value.type = "error"
                    notifications.value.show = true

                }
            }

        })
    }


</script>

<template>
<section class="container">
    <section class="form-section"> 
        <div class="form">
            <header>
                <img src="../assets/images/icon.png" alt="">
                <p class="font-title "> Trakit </p>
            </header>
            <section>
                <div class="form-header">
                    <p> Sign In </p>
                    <p> You dont have an Account? <RouterLink to="register" class="sign-up-link"> Sign up </RouterLink></p>
                </div>
                <form class="auth-form" @submit.prevent="submit_login">
                    
                    <div class="form-element">
                        <label for=""> Username </label>
                        <input type="text" v-model="formData.username" :class="{'error-input': errors['username']}"/>
                        <div v-if="errors['username']" class="error-text">
                            <div v-for="error in errors['username']"> {{ error }} </div>  
                        </div>
                    </div>

                    <div class="form-element">
                        <label for=""> Password </label>
                        <input type="password" v-model="formData.password" :class="{'error-input': errors['password']}"/>
                        <div v-if="errors['password']" class="error-text">
                            <div v-for="error in errors['password']"> {{ error }} </div>  
                        </div>
                    </div>
                    

                    <p class="f-password"><a href="/reset"> Forget password </a></p>
                    
                    <div class="form-element">
                        <button class="button"> Sign in </button>
                    </div>
                </form>
                <p class="or"> Or </p>

                <div class="google-signin">
                    <img src="../assets/images/google.png" alt="">
                    <p> Sign in with Google </p>
                </div>

            </section>
        </div>
        <Toast 
            :message="notifications.message" 
            :type="notifications.type"
            :show = "notifications.show"
            :position = "notifications.position"
            :wide="notifications.wide"
            :duration = "notifications.duration"
            @close_toast = "close_toast"
        />
    </section>
    <onboard></onboard>
</section>
</template>
<style scoped>
    @import url("../assets/css/auth.css");

    .form header{
        margin-bottom: 70px;
    }

    .form-element{
        margin-bottom: 40px;
    }

    .form-element label{
        margin-bottom: 10px;
    }

    .form-element input{
        height: 35px;
        padding: 1.5%;
    }

    .form-header{
        margin-bottom: 40px;
    }

    .button{
        margin-top:20px;
    }

    .f-password{
        margin-top: -20px;
        margin-bottom: 30px;
        text-align: right;
        font-size: 14px;
        font-weight: 400;
        color: rgba(74, 147, 76, 1);
        cursor: pointer;
    }

    @media screen and (max-width: 760px){
        .form-section{
            min-height: 100vh;
        }

        .form header{
            margin-bottom: 30px;
        }

        .form-element{
            margin-bottom: 20px;
        }

        .form-element input{
            height: 25px;
        }

        .form-header{
            margin-bottom: 30px;
        }

        .button{
            margin-top:20px;
        }

        .f-password{
            margin-top: -10px;
            margin-bottom: 20px;
            font-size: 12px;
        }
    }
</style>