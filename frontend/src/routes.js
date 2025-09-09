import Login from "./components/Login.vue";
import VmHome from "./components/Home.vue";
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {
        name: 'Login',
        component: Login,
        path: '/login',
        meta: { auth: false}
    },
    {
        name: 'VmHome',
        component: VmHome,
        path: '/',
        meta: { auth: true}
    }
]
const router = createRouter({
    history:createWebHistory(),
    routes: routes,
})

// router.beforeEach((to, from, next) =>{
//     // console.log(to)
//     if (!to.meta.auth && !sessionStorage.getItem('user-info')){
//         next('/login')
//     } else if (to.meta.auth && sessionStorage.getItem('user-info')){
//         next('/')
//     } else {

//     }
// })

export default router