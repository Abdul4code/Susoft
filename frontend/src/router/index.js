import { createRouter, createWebHistory } from 'vue-router'
import register from '../views/Register.vue'
import login from '../views/Login.vue'
import homepage from '../views/Homepage.vue'
import reset from '../views/reset.vue'
import goal from '../views/Goal.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/', name: 'homepage',component: homepage
    },
    {
      path: '/goal/:id', name: 'goal', component: goal
    },

    // Authentication Pages
    {
      path: '/register', name: 'register', component: register
    },
    {
      path: '/login', name: 'login', component: login
    },
    {
      path: '/reset', name: 'reset', component: reset
    },
    {
      path: '/reset/:uuid/:token', name: 'reset_password', component: reset
    }
  ]
})

export default router
