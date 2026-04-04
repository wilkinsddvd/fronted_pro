import { createRouter, createWebHistory } from 'vue-router'
import DashboardLayout from '../components/dashboard/DashboardLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Tickets from '../views/Tickets.vue'
import TicketDetail from '../views/TicketDetail.vue'
import QuickReply from '../views/QuickReply.vue'
import Statistics from '../views/Statistics.vue'
import ProfileSettings from '../views/ProfileSettings.vue'
import StaffManagement from '../views/StaffManagement.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import { useLoadingStore } from '../stores/loadingStore'

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
      { path: '/statistics', name: 'Statistics', component: Statistics },
      // 个人设置页面路由
      { path: '/profile-settings', name: 'ProfileSettings', component: ProfileSettings },
      { path: '/staff-management', name: 'StaffManagement', component: StaffManagement }
    ]
  },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/**
 * 校验 localStorage 中存储的 Token 是否合法且未过期
 */
function isTokenValid() {
  const userStr = localStorage.getItem('user')
  if (!userStr) return false
  let user
  try {
    user = JSON.parse(userStr)
  } catch {
    return false
  }
  if (!user || !user.token) return false
  try {
    const parts = user.token.split('.')
    if (parts.length !== 3) return false
    const payload = JSON.parse(atob(parts[1]))
    if (payload.exp * 1000 <= Date.now()) {
      localStorage.removeItem('user')
      return false
    }
  } catch {
    return false
  }
  return true
}

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // Show route loading progress bar
  const loadingStore = useLoadingStore()
  loadingStore.routeLoading = true

  // 检查用户是否已登录且 Token 有效
  const isAuthenticated = isTokenValid()

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

router.afterEach(() => {
  // Hide route loading progress bar
  const loadingStore = useLoadingStore()
  loadingStore.routeLoading = false
})

export default router