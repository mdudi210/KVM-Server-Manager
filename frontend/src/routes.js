import Login from "./components/Login.vue";
import VmHome from "./components/Home.vue";
import NotFound from "./components/NotFound.vue";
import {createRouter, createWebHistory} from 'vue-router'
import { isAuthenticated } from "../auth/auth";


const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login,
        meta: { requiresAuth: false } 
    },
    {
        path: '/',
        name: 'VmHome',
        component: VmHome,
        meta: { requiresAuth: true } 
    },
    {
      path: "/:singleSegment",
      name: "SingleSegment",
      component: VmHome,
      meta: { requiresAuth: true },
    },
    {
      path: "/:first/:rest(.*)",
      name: "NotFound",
      component: NotFound,
      meta: { requiresAuth: false },
    }
]
const router = createRouter({
    history:createWebHistory(),
    routes: routes,
})


// router.beforeEach((to, from, next) => {

//   if (to.meta.requiresAuth && !isAuthenticated()) {
//     next({ name: 'Login' })
//   } else if (!to.meta.requiresAuth && isAuthenticated() && to.name === 'Login') {
//     next({ name: 'VmHome' })
//   } else {
//     next()
//   }
// })

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !isAuthenticated()) {
    next({ name: "Login" });
  } else if (to.name === "SingleSegment" && isAuthenticated()) {
    next({ name: "Login" });
  } else if ((to.name === "Login" && isAuthenticated())) {
    next({ name: "VmHome" });
  } else {
    next();
  }
});

export default router