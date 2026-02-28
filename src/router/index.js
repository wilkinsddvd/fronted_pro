import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import DashboardLayout from '../components/dashboard/DashboardLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Tickets from '../views/Tickets.vue'
import TicketDetail from '../views/TicketDetail.vue'
import QuickReply from '../views/QuickReply.vue'
import Statistics from '../views/Statistics.vue'
import ProfileSettings from '../views/ProfileSettings.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import { userStore } from '../store/user.js'

/**
 * 路由配置
 * 定义应用的所有页面路由
 * meta.requiresAdmin = true 表示该路由仅管理员可访问
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
      { path: '/statistics', name: 'Statistics', component: Statistics, meta: { requiresAdmin: true } },
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
router.beforeEach(async (to, from, next) => {
  // 检查用户是否已登录
  const userStr = localStorage.getItem('user')
  const isAuthenticated = !!userStr

  // 公共路由列表
  const publicRoutes = ['Login', 'Register']
  const isPublicRoute = publicRoutes.includes(to.name)

  // 如果用户未登录且访问的不是公共路由，则重定向到登录页
  if (!isAuthenticated && !isPublicRoute) {
    next({ name: 'Login' })
    return
  }

  // 如果用户已登录且访问登录或注册页，则重定向到仪表板
  if (isAuthenticated && isPublicRoute) {
    next({ name: 'Dashboard' })
    return
  }

  // RBAC：检查管理员权限
  if (to.meta.requiresAdmin && isAuthenticated) {
    // 若 store 尚未加载用户信息，则先刷新
    if (!userStore.user) {
      await userStore.fetchSelf()
    }
    if (!userStore.isAdmin) {
      // 非管理员访问管理员路由，重定向并提示
      ElMessage.warning('权限不足，无法访问该页面')
      next({ name: 'Dashboard' })
      return
    }
  }

  // 其他情况允许访问
  next()
})

export default router