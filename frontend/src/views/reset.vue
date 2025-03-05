<script setup>
    import { RouterLink, useRoute } from 'vue-router'
    import router from '../router/index';
    import onboard from '../components/onboard.vue'
    import { ref, onMounted } from 'vue'
    import axios from 'axios'
    import { handler, get_error_400_messages } from '../utilities/error_handlers'
    import Toast from '../components/toasts.vue'

    const formData = ref({
        email: '',
        password: '',
        confirm_password : '',
        uuid : '',
        token: ''
    })

    const errors = ref({
        all : '',
        messages : ''
    })

    onMounted(() => {
        let route = useRoute()
        formData.value.uuid = route.params.uuid
        formData.value.token = route.params.token
    })

    const notifications = ref({
        message : "",
        type : "",
        position: "right",
        show: false,
        wide: 45, 
        callback: ()=>{},
        duration: 3000
    })

    function close_toast(){
        notifications.value.show = false
        notifications.value.callback()
    }

    const baseUrl = 'http://127.0.0.1:8000'
  
    function submit_email(){
        axios.defaults.baseURL = baseUrl
        axios({
            method : 'post',
            url : '/accounts/recover/link',
            data: {'email': formData.value.email}
        }).then(function(response){
            
            notifications.value.message = "We have sent you a link to recover your password"
            notifications.value.type = "success"
            notifications.value.show = true
            notifications.value.wide = 60

        }).catch(function(error){
            if(error.response.status == 400){

                errors.value.all = handler(error)
                errors.value.messages = get_error_400_messages(error.response.data)

                notifications.value.show = true
                notifications.value.message = errors.value.messages[0]
                notifications.value.type = "error"

            }

        })
    }

    function change_password(){
        axios.defaults.baseURL = baseUrl

        axios({
            method : 'post',
            url : '/accounts/recover/update',
            data: formData.value
        }).then(function(response){
            notifications.value.message = "Password Changed Successfully"
            notifications.value.type = "success"
            notifications.value.show = true
            notifications.value.callback = ()=>{
                router.push({name : 'login'})
            }
            
        }).catch(function(error){
            console.log(error)
            if(error.response.status == 400){

                errors.value.all = handler(error)
                errors.value.messages = get_error_400_messages(error.response.data)
                notifications.value.type = 'error'
                notifications.value.show = true
                notifications.value.message = errors.value.messages[0]
            }

            if (error.response.status == 500){
                errors.value.messages = get_error_400_messages(error.response.data)
                notifications.value.type = 'error'
                notifications.value.show = true
                notifications.value.message = errors.value.messages[0]
                notifications.value.callback = ()=>{
                    formData.value.uuid = ''
                    formData.value.token = ''
                    router.push({name : 'reset'})
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
            <section v-if="formData.uuid && formData.token">
                <div class="form-header">
                    <p> Password Reset </p>
                    <p> Please provide a new password for your account </p>
                </div>
                <form class="auth-form" @submit.prevent="change_password">
                    
                    <div class="form-element">
                        <label for=""> password </label>
                        <input type="password" v-model="formData.password" :class="{'error-input': errors.all['password']}"/>
                        <div v-if="errors.all['password']" class="error-text">
                            <div v-for="error in errors['password']"> {{ error }} </div>  
                        </div>
                    </div>

                    <div class="form-element">
                        <label for=""> Confirm Password </label>
                        <input type="password" v-model="formData.confirm_password" :class="{'error-input': errors.all['confirm_password']}"/>
                        <div v-if="errors.all['confirm_password']" class="error-text">
                            <div v-for="error in errors.all['confirm_password']"> {{ error }} </div>  
                        </div>
                    </div>

                    <div class="form-element">
                        <button class="button"> Submit </button>
                    </div>

                </form>
            </section>
            <section v-else>
                <div class="form-header">
                    <p> Password Reset </p>
                    <p> Please provide your registered email account </p>
                </div>
                <form class="auth-form" @submit.prevent="submit_email">
                    
                    <div class="form-element">
                        <label for=""> email </label>
                        <input type="text" v-model="formData.email" :class="{'error-input': errors.all['email']}"/>
                        <div v-if="errors.all['email']" class="error-text">
                            <div v-for="error in errors.all['email']"> {{ error }} </div>  
                        </div>
                    </div>

                    <div class="form-element">
                        <button class="button"> Send </button>
                    </div>

                </form>
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