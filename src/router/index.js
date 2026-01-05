import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '../components/dashboard/DashboardLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Tickets from '../views/Tickets.vue'
import QuickReply from '../views/QuickReply.vue'
import CategoryManagement from '../views/CategoryManagement.vue'
import Statistics from '../views/Statistics.vue'
import Settings from '../views/Settings.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/dashboard',
    children: [
      { path: '/dashboard', name: 'Dashboard', component: Dashboard },
      { path: '/tickets', name: 'Tickets', component: Tickets },
      { path: '/quick-reply', name: 'QuickReply', component: QuickReply },
      { path: '/categories', name: 'Categories', component: CategoryManagement },
      { path: '/statistics', name: 'Statistics', component: Statistics },
      { path: '/settings', name: 'Settings', component: Settings }
    ]
  },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})