import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/user-dashboard',
      name: 'user-dashboard',
      component: () => import('../views/User_Dashboard.vue'),
    },
    {
      path: '/admin-dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/Admin_Dashboard.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path:'/lots',
      name:'lots-list',
      component: () => import('../views/AddlotView.vue')
    },
    {
      path:'/lots/:lot_id',
      name:'lots',
      component: () => import('../views/EditlotView.vue')
    },
    {
      path:'/spots/:spot_id',
      name:'spots',
      component: () => import('../views/Viewspot.vue')
    },
    {
      path:'/spotdetails/:spot_id',
      name:'spotsdetails',
      component: () => import('../views/Viewspotdetails.vue')
    },
    {
      path: '/users',
      name: 'users',
      component: () => import('../views/users.vue')
    }

  ],
})

export default router
