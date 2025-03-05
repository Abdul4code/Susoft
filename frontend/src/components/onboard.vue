<script>
    import { Swiper, SwiperSlide } from 'swiper/vue';
    import 'swiper/swiper-bundle.css';
    import { register } from 'swiper/element/bundle';
    register();


</script>
<template>
    <section class="onboard-section">
        <swiper-container class="swipper-container" :slides-per-view="1" :grid-columns="1" 
        :autoplay="{delay: 5000}" :speed="1000" :space-between="250" :loop="true">
            <swiper-slide class="swipper-slides">
                <div class="onboard-img"><img src="../assets/images/slide_image1.png" alt=""></div>
                <div class="onboard-text"> 
                    <h1>Empower your Ambitions: Stay On Track and Take Control.</h1>
                    <p> Achieving goals sometimes require several attempts. Lets help you stay organize while you reach for your goals. </p>
                </div>
            </swiper-slide>
            <swiper-slide class="swipper-slides">
                <div class="onboard-img"><img src="../assets/images/slide_image2.png" alt=""></div>
                <div class="onboard-text"> 
                    <h1>Step 1: Create a Goal </h1>
                    <p> You want to get into Grad School? Or you want to get a job? Or you want to conduct a 
                        groundbreaking PhD research? Or you want to win a grant for your business? Register that goal with us. 
                    </p>
                </div>
            </swiper-slide>
            <swiper-slide class="swipper-slides">
                <div class="onboard-img"><img src="../assets/images/slide_image3.png" alt=""></div>
                <div class="onboard-text"> 
                    <h1>Step 2: Define Template for your goal</h1>
                    <p> Add important benchmarks for your goals. i.e Started, In process, in Review, finishing touches, submited etc.  </p>
                </div>
            </swiper-slide>
            <swiper-slide class="swipper-slides">
                <div class="onboard-img"><img src="../assets/images/slide_image4.png" alt=""></div>
                <div class="onboard-text"> 
                    <h1>Step 3: Define small Tasks</h1>
                    <p> Define tasks under each of this benchmark. This tasks are flexible and should mimic your recipe for success. </p>
                </div>
            </swiper-slide>
            <swiper-slide class="swipper-slides">
                <div class="onboard-img"><img src="../assets/images/slide_image5.png" alt=""></div>
                <div class="onboard-text"> 
                    <h1>Step 4: Manage all Applications</h1>
                    <p> You can create several applications for this goals. Every new application in this 
                        goal will follow same template. You can keep track of tasks for every application. 
                    </p>
                </div>
            </swiper-slide>            
        </swiper-container>
    </section>
</template>
<style scoped>
    .onboard-section{
    background-color: rgba(188, 248, 181, 1);
    display: flex;
    justify-content: center;
    align-items: center;
    }

    .onboard-section .swipper-container{
        width: 30vw;
        text-align: center;
    }

    .onboard-img{
    margin-bottom: 70px;
    }

    .onboard-text h1{
    font-size: 30px;
    font-weight: bold;
    color: rgba(102, 102, 102, 1)
    }

    .onboard-text p{
    font-size: 14px;
    font-weight: 500;
    color: rgba(102, 102, 102, 1);
    margin-top: 25px;
    }

    .scroll-control{
    display: flex;
    justify-content: space-around;
    width: 25%;
    margin: 0px auto;
    margin-top: 60px;
    }

    .scroll-control div{
    width: 15px;
    height: 15px;
    background-color: rgba(74, 147, 76, 1);
    border-radius: 10px;
    }

    .selected-onboard{
    width: 35px !important;
    }

    @media screen and (max-width: 760px) {
        .onboard-section{
            min-height: 100vh;
        }

        .onboard-section section{
            width: 80%;
            text-align: center;
        }
        
        .onboard-img{
            margin-bottom: 30px;
        }

        .onboard-img img{
            width: 100%;
            height: 100%;
        }
        
        .onboard-text h1{
            font-size: 22px;
            font-weight: bold;
            color: rgba(102, 102, 102, 1)
        }
        
        .scroll-control{
            display: flex;
            justify-content: space-around;
            width: 35%;
            margin: 0px auto;
            margin-top: 60px;
        }
        
        .scroll-control div{
            width: 12px;
            height: 12px;
            background-color: rgba(74, 147, 76, 1);
            border-radius: 10px;
        }
        
        .selected-onboard{
            width: 35px !important;
        }

        .onboard-section .swipper-container{
            width: 80vw;
            text-align: center;
        }
    }
</style>