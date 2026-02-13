import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '../components/dashboard/DashboardLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Tickets from '../views/Tickets.vue'
import TicketDetail from '../views/TicketDetail.vue'
import QuickReply from '../views/QuickReply.vue'
import CategoryManagement from '../views/CategoryManagement.vue'
import Statistics from '../views/Statistics.vue'
import ProfileSettings from '../views/ProfileSettings.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

/**
 * 路由配置
 * 定义应用的所有页面路由
 */
const routes = [
  {
    path: '/',
    component: DashboardLayout,
    redirect: '/dashboard',
    children: [
      { path: '/dashboard', name: 'Dashboard', component: Dashboard },
      { path: '/tickets', name: 'Tickets', component: Tickets },
      { path: '/tickets/:id', name: 'TicketDetail', component: TicketDetail },
      { path: '/quick-reply', name: 'QuickReply', component: QuickReply },
      { path: '/categories', name: 'Categories', component: CategoryManagement },
      { path: '/statistics', name: 'Statistics', component: Statistics },
      // 个人设置页面路由
      { path: '/profile-settings', name: 'ProfileSettings', component: ProfileSettings }
    ]
  },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 检查用户是否已登录
  const userStr = localStorage.getItem('user')
  const isAuthenticated = !!userStr

  // 公共路由列表
  const publicRoutes = ['Login', 'Register']
  const isPublicRoute = publicRoutes.includes(to.name)

  // 如果用户未登录且访问的不是公共路由，则重定向到登录页
  if (!isAuthenticated && !isPublicRoute) {
    next({ name: 'Login' })
  } 
  // 如果用户已登录且访问登录或注册页，则重定向到仪表板
  else if (isAuthenticated && isPublicRoute) {
    next({ name: 'Dashboard' })
  } 
  // 其他情况允许访问
  else {
    next()
  }
})

export default router