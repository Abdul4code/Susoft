<script setup>
    import { RouterLink } from 'vue-router'
    import router from '../router/index';
    import onboard from '../components/onboard.vue'
    import { ref } from 'vue'
    import axios from 'axios'
    import { handler, get_error_400_messages } from '../utilities/error_handlers'
    import Toast from '../components/toasts.vue'

    const formData = ref({
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password : ''
    })

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

    const errors = ref({
        all : '',
        messages : ''
    })

    const baseUrl = 'http://127.0.0.1:8000'
  
    function submit_register(){
        console.log(formData)
        axios.defaults.headers.common['Authorization'] = ''
        axios.defaults.baseURL = baseUrl

        axios({
            method : 'post',
            url : '/accounts/register/',
            data: formData.value

        }).then(function(response){
            axios.defaults.headers.common['Authorization'] = `Bearer ${response['data']['Access Token']}`
            localStorage.setItem('access', response['data']['Access Token']);
            
            notifications.value.show = true
            notifications.value.message = "Your account has been created successfully"
            notifications.value.type = "success"
            notifications.value.callback = ()=>{
                router.push({name : 'login'})
            }
           
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
                    <p> Register </p>
                    <p> Already have an Account? <RouterLink to="login" class="sign-up-link"> Sign in </RouterLink></p>
                </div>
                <form class="auth-form" @submit.prevent="submit_register">
                    <div class="form-element">
                        <label for=""> Username </label>
                        <input type="text" v-model="formData.username" :class="{'error-input': errors.all['username']}"/>
                        <div v-if="errors.all['username']" class="error-text">
                            <div v-for="error in errors.all['username']"> {{ error }} </div>  
                        </div>
                    </div>

                    <div class="form-element multi-elem">
                        <div class="form-sub-element">
                            <label for=""> Firstname </label>
                            <input type="text" v-model="formData.first_name" :class="{'error-input': errors.all['first_name']}"/>
                            <div v-if="errors.all['first_name']" class="error-text">
                                <div v-for="error in errors.all['first_name']"> {{ error }} </div>  
                            </div>
                        </div>
                        <div class="form-sub-element">
                            <label for=""> Lastname </label>
                            <input type="text" v-model="formData.last_name" :class="{'error-input': errors.all['last_name']}"/>
                            <div v-if="errors.all['last_name']" class="error-text">
                                <div v-for="error in errors.all['last_name']"> {{ error }} </div> 
                            </div>
                        </div>
                    </div>
                    <div class="form-element">
                        <label for=""> Email </label>
                        <input type="email" v-model="formData.email" :class="{'error-input': errors.all['email']}"/>
                        <div v-if="errors.all['email']" class="error-text">
                            <div v-for="error in errors.all['email']"> {{ error }} </div> 
                        </div>
                    </div>

                    <div class="form-element">
                        <label for=""> Password </label>
                        <input type="password" v-model="formData.password" :class="{'error-input': errors.all['password']}"/>
                        <div v-if="errors.all['password']" class="error-text">
                            <div v-for="error in errors.all['password']"> {{ error }} </div> 
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
                        <button class="button"> Sign Up </button>
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
</style>