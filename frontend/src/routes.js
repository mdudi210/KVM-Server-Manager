import { createRouter, createWebHistory } from 'vue-router';

import Login from './components/Login.vue';
import NewVm from './components/NewVm.vue';
import NotFound from './components/NotFound.vue';
import VmHome from './components/Home.vue';
import { isAuthenticated } from '../auth/auth';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'VmHome',
    component: VmHome,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/vms',
    name: 'VmAdmin',
    component: NewVm,
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { requiresAuth: false },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authed = isAuthenticated();

  if (to.meta.requiresAuth && !authed) {
    next({ name: 'Login' });
    return;
  }

  if (to.name === 'Login' && authed) {
    next({ name: 'VmHome' });
    return;
  }

  next();
});

export default router;
