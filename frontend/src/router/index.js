import { createRouter, createWebHistory } from 'vue-router'
import register from '../views/Register.vue'
import login from '../views/Login.vue'
import homepage from '../views/Homepage.vue'
import reset from '../views/reset.vue'
import goal from '../views/Goal.vue'
import new_project from '../views/NewProject.vue'
import Sprint from '../views/Sprint.vue'
import TaskDetail from '../views/TaskDetail.vue'
import Retrospective from '../views/Retrospective.vue'
import Backlogs from '../views/Backlogs.vue'
import learninghub from '../views/Learninghub.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [

    {
      path: '/', name: 'homepage',component: homepage
    },
    {
      path: '/learninghub', name: 'learninghub', component: learninghub
    },
    {
      path: '/new_project', name: 'new_project',component: new_project
    },
    {
      path: '/backlogs/:id', name: 'backlog', component: Backlogs
    },

    {
      path: '/sprint/:id', name: 'kanban', component: Sprint
    },

    {
      path: '/retrospective/:id', name: 'retrospective', component: Retrospective
    },
    {
      path: '/detail/:id', name: 'detail', component: TaskDetail
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
