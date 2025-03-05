<script setup>
import DatePicker from '../components/datePicker.vue'
import TimePicker from '../components/TimePicker.vue'
import {ref, onMounted} from 'vue'

const props = defineProps({
        open: Boolean,
        fresh: Boolean
})

</script>

<template>
    <section class="new-goal-cont" :class="{'open_goal_form' : props.open && !fresh, 'close_goal_form' : !props.open && !fresh}">
        <form action="">
            <h1 class='form-header'> Create New Goal </h1>
            <div class="Element">
                <p class="element_header"> Goal Title </p>
                <label for="" class="element_label"> What should your goal to be called (Max 100 chars) </label>
                <input type="text" class="elemen_input"/>
            </div>

            <div class="Element">
                <p class="element_header"> Goal Description </p>
                <label for="" class="element_label"> What does this goal mean? Describe it </label>
                <textarea rows=3 class="elemen_input"></textarea>
            </div>

            <div class="Element">
                <p class="element_header"> Goal Commencement Date </p>
                <label for="" class="element_label"> What date will you start pursuing this goal? </label>
                <div class="inline-input first-inline">
                    <DatePicker />
                </div><div class="inline-input">
                    <TimePicker />
                </div>
            </div>

            <div class="Element">
                <p class="element_header"> Goal Deadline </p>
                <label for="" class="element_label"> What is the feasible date you intend to achieve this goal? </label>
                <div class="inline-input first-inline">
                    <DatePicker />
                </div><div class="inline-input">
                    <TimePicker />
                </div>
            </div>

            <div class="button-cont">
                <button @click.prevent="$emit('toggle_goal_form')"> Cancel </button>
                <button> Create Goal </button>
            </div>
        </form>
    </section>
</template>

<style scoped>
    .new-goal-cont{
        position: absolute;
        bottom: 20px;
        right: 20px;
        border: 1px solid black;
        min-width: 350px;
        width: 32%;
        padding: 30px;
        border-radius: 10px;
        background-color: white;
        overflow: hidden;
        visibility: hidden;
    }

    .form-header{
        color: rgba(83, 165, 72, 1);
        font-size: 25px;
        font-family: Rubik;
        font-weight: 700;
        margin-bottom: 30px;
    }

    .Element{
        width: 100%;
        margin: 30px 0px;
    }

    .element_header{
        font-size: 14pt;
        font-family: Poppins;
        font-weight: 600;
        color: rgba(53, 53, 53, 1);
    }

    .element_label{
        font-size: 14px;
        font-weight: 400;
        font-family: Poppins;
        color: rgba(0, 0, 0, 0.5);
        margin-bottom: 10px;
        display: block;
    }

    .elemen_input{
        width: 97%;
        border-radius: 10px;
        border: 2px solid rgba(102, 102, 102, 0.6);
        font-size: 12pt;
        padding: 1.5%;
        color: rgba(102, 102, 102, 0.8);
    }

    .inline-input{
        display: inline-block;
        padding: 10px;
        border: 2px solid rgba(102, 102, 102, 0.6);
        border-radius: 10px;
        width: 44.4%;
        min-width: 220px;
    }

    .first-inline{
        margin-right: 3%;
    }

    .button-cont{
        display: flex;
        justify-content: space-between;
        margin-top: 50px;
    }

    .button-cont button{
        width: 150px;
        padding: 15px 20px;
        border-radius: 5px;
        border: none;
        font-size: 16px;
        font-family: Rubik;
        cursor: pointer
    }

    .button-cont button:nth-child(1){
        color: rgba(199, 199, 199, 1);
        background-color: rgba(245, 245, 245, 1);
    }

    .button-cont button:nth-child(1):hover{
        color: rgba(0, 0, 0, 0.7);
        background-color: rgba(100, 100, 100, 0.2);
    }

    .button-cont button:nth-child(2){
        color: white;
        background-color: rgba(76, 147, 76, 1);
    }

    .button-cont button:nth-child(2):hover{
        color: white;
        background-color: rgba(76, 200, 76, 1);
    }

    @media (max-width: 760px){
        .new-goal-cont{
            position: absolute;
            bottom: 5px;
            right: 5px;
            left: 15px;
            padding: 10px;
            min-width: auto;
            width: auto;
        }

        .form-header{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .Element{
            width: 100%;
            margin: 15px 0px;
        }

        .element_header{
            font-size: 12pt;
        }

        .element_label{
            font-size: 9pt;
            font-weight: 400;
            margin-bottom: 5px;
        }

        .elemen_input{
            width: 97%;
            border-radius: 5px;
            font-size: 10pt;
            padding: 1%;
        }

        .inline-input{
            display: inline-block;
            padding: 0px;
            border-radius: 5px;
            width: 47%;
            min-width: auto;
            overflow: hidden;
        }
        .button-cont{
            margin-top: 25px;
        }

        .button-cont button{
            width: 110px;
            padding: 10px;
            border-radius: 5px;
            font-size: 11pt;
        }
    }

    @keyframes openGoal {
        0%{
            overflow: hidden;
            max-height: 0%;
            visibility:visible;
        }

        50%{
            overflow:hidden;
            max-height: 50%;
            visibility:visible;
        }

        100%{
            overflow:auto;
            max-height: auto;
            visibility:visible;
        }
    }

    @keyframes closeGoal {
        0%{
            overflow: hidden;
            visibility:visible;
            max-height: 100%;
        }

        50%{
            max-height: 40%;
            overflow: hidden;
            visibility:visible;
            opacity: 1
        }

        100%{
            overflow:hidden;
            max-height: 0px;
            visibility:hidden;
            opacity: 0
        }
    }

    .open_goal_form{
        animation: openGoal 0.7s ease forwards;
    }
    
    .close_goal_form{
        animation: closeGoal 1s ease forwards;
    }
</style>