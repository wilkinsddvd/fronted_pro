/**
 * 用户状态管理（响应式 Store）
 * 作为用户信息和角色的单一数据源 (single source of truth)
 *
 * 用法：
 *   import { userStore } from '@/store/user.js'
 *   userStore.user       // 用户信息对象（含 role 字段）
 *   userStore.isAdmin    // 是否为管理员
 *   userStore.username   // 用户名
 *   await userStore.fetchSelf()  // 从 /api/self 刷新用户信息
 *   userStore.clear()    // 清除登录状态
 */
import { reactive } from 'vue'
import { getSelf } from '@/api/index.js'

export const userStore = reactive({
  /** 当前登录用户信息（来自 /api/self），null 表示未登录 */
  user: null,

  /** fetchSelf 请求加载中标记 */
  loading: false,

  /** 从 localStorage 初始化用户信息（应用启动时调用） */
  init() {
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        this.user = JSON.parse(userStr)
      } catch (e) {
        console.error('Failed to parse user data from localStorage')
      }
    }
  },

  /**
   * 从后端 /api/self 拉取完整用户信息（含 role）并同步到 localStorage
   * @returns {Promise<boolean>} 成功返回 true，失败返回 false
   */
  async fetchSelf() {
    this.loading = true
    try {
      const res = await getSelf()
      if (res && res.data) {
        this.user = res.data
        localStorage.setItem('user', JSON.stringify(res.data))
        return true
      }
      return false
    } catch (e) {
      console.error('fetchSelf failed:', e)
      return false
    } finally {
      this.loading = false
    }
  },

  /** 清除登录状态（登出时调用） */
  clear() {
    this.user = null
    localStorage.removeItem('user')
  },

  /** 当前用户是否为管理员（role === 'admin'） */
  get isAdmin() {
    return this.user?.role === 'admin'
  },

  /** 显示用户名（优先 nickname，次之 username） */
  get username() {
    return this.user?.nickname || this.user?.username || 'User'
  },

  /** 当前用户角色 */
  get role() {
    return this.user?.role || 'user'
  }
})

// 应用初始化时从 localStorage 恢复用户信息
userStore.init()
