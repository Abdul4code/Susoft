
<script setup>
import { computed, watch } from 'vue';

    const props = defineProps({
        message : String, // The message to be displayed by the toast
        type : String, // Toast kind (success, error, info, warning)
        position: String, // Where to display the toast (left, right)
        show: Boolean, // should the toast be shown
        wide: Number, // how wide in percentage
        callback: Function, // function to call when the duration elapse
        duration: Number   // duration the toast will be visible for in ms
    })

    const emits = defineEmits(['close_toast'])
    
    const header = computed(()=>{
        if(props.type == "success"){
            return "Success"
        }else if(props.type == "error"){
            return "Error"
        }else if(props.type == "info"){
            return "Notification"
        }else if(props.type == "warning"){
            return "Warning"
        }
    })

    const toast_icon = computed(()=>{
        return `../src/assets/images/${props.type}.svg`
    })

    const width = computed(()=>{
        return `${props.wide}%`
    })

    const header_color = computed(()=>{
        if(props.type == "success"){
            return "RGBA(64,160,108,1)"
        }else if(props.type == "error"){
            return "RGBA(220,54,52,1)"
        }else if(props.type == "info"){
            return "RGBA(50,46,252,1)"
        }else if(props.type == "warning"){
            return "RGBA(160,145,64,1)"
        } 
    })

    const background_color = computed(()=>{
        if(props.type == "success"){
            return "RGBA(186,244,181,0.46)"
        }else if(props.type == "error"){
            return "RGBA(238,137,137,0.78)"
        }else if(props.type == "info"){
            return "RGBA(41,128,185,0.43)"
        }else if(props.type == "warning"){
            return "RGBA(239,232,169,0.46)"
        } 
    })

    const get_position = computed(()=>{
        if(props.position == 'top-left'){
            return {left : "10px", top : "10px"}
        }else if(props.position == 'top-right'){
            return {right : "10px", top : "10px"}
        }else if(props.position == 'bottom-left'){
            return {left : "10px", bottom : "10px"}
        }else if(props.position == 'bottom-right'){
            return {right : "10px", bottom : "10px"} 
        }
    })

    function close(){
        emits('close_toast')
    }

    watch(() => props.show, (new_state, old_state)=>{
        if(new_state == true){
            setTimeout(function(){
                emits('close_toast')
            }, props.duration)
        }
    })

</script>

<template>
    <div v-if="show" class="toast" :class="type, position" :style="{ width:width, backgroundColor:background_color} ">
        <div class="icon"> 
            <img :src="toast_icon" />
        </div>
        <div class="content">
            <div class="header" :style="{color:header_color}">{{ header }}</div>
            <div class="message">{{ message }}</div>
        </div>
        <button class="delete" @click="close"><img src='../assets/images/close.svg' /></button>
    </div>
</template>

<style>
    .toast{
        display: flex;
        justify-content: space-around;
        align-items: center;
        height: 70px;
        min-width: 250px;
        flex-wrap: no-wrap;
        border-radius: 10px;
        position: absolute;
        top: 10px;
        animation: slideInRight 0.5s ease-out, bounce 0.5s ease-out 0.5s;
    }

    .icon{
        display: inline-block;
        width: 15%;
        height: 70%;
    }

    .icon img{
        width: 100%;
        height: 100%;
    }

    .content{
        display: flex;
        flex-direction: column;
        justify-content: center;
        width: 65%;
        position: relative;
        height: 70%;
    }

    .content .header{
        font-size: 20px;
        font-weight: 600;
        font-family: Rubik;
    }

    .content .message{
        font-family: Poppins;
        font-size: 12px;
        color: rgba(102, 102, 102, 1)
    }

    .delete{
        width: 10%;
        height: 70%;
        background-color: rgba(0,0,0,0);
        border: none;
        cursor: pointer;
    }

    .delete img{
        width: 15px;
        height: 15px;
    }

    .left{
        left: 10px;
    }

    .right{
        right: 10px;
    }


    @keyframes slideInRight {
        0% {
            transform: translateY(-50%);
            opacity: 0;
        }
        30% {
            transform: translateY(80%);
            opacity: 1;
        }
        90% {
            transform: translateY(-20%);
        }
        100% {
            transform: translateY(0);
        }
        }

        @keyframes bounce {
        0%, 100% {
            transform: translateX(0);
        }
        50% {
            transform: translateX(-20px);
        }
    }

    @media screen and (max-width: 760px){
        .toast{
            height: 60px;
            min-width: 80%;
        }
    }


</style>
  

  