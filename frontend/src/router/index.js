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
    },
    {
      path: '/book/:lot_id',
      name: 'book',
      component: () => import('../views/Bookspot.vue')
    },
    {
      path: '/release/:reservation_id',
      name: 'release',
      component: () => import('../views/Releasespot.vue')
    },
    {
      path: '/parkingrecords',
      name: 'parkingrecords',
      component: () => import('../views/Parkingrecords.vue')
    },
    {
      path: '/adminchart',
      name: 'adminchart',
      component: () => import('../views/AdminChart.vue')
    },
    {
      path: '/userchart',
      name: 'userchart',
      component: () => import('../views/UserChart.vue')
    },
    {
      path: '/adminsearch/:search/:search_type',
      name: 'adminsearch',
      component: () => import('../views/AdminSearch.vue')
    }

  ],
})

export default router
