import Login from "./components/Login.vue";
import VmHome from "./components/Home.vue";
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        name: 'Login',
        component: Login,
        path: '/login'
    },
    {
        name: 'VmHome',
        component: VmHome,
        path: '/'
    },
]
const router = createRouter({
    history:createWebHistory(),
    routes
})

export default router