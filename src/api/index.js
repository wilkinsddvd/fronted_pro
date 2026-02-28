import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建axios实例
const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可在此添加token等认证信息
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const userData = JSON.parse(userStr)
        // 如果有token字段，使用token，否则可以传递用户ID等
        if (userData.token) {
          config.headers['Authorization'] = `Bearer ${userData.token}`
        } else if (userData.id) {
          config.headers['X-User-ID'] = userData.id
        }
      } catch (e) {
        console.error('Failed to parse user data from localStorage')
      }
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data
    // 统一处理后端返回格式 {code, data, msg}
    if (res.code !== 200 && res.code !== 201) {
      console.error('API Error:', res.msg || 'Unknown error')
      return Promise.reject(new Error(res.msg || 'Error'))
    }
    return res
  },
  error => {
    const status = error.response?.status
    // 401/403：清除登录态并跳转到登录页
    if (status === 401 || status === 403) {
      localStorage.removeItem('user')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    } else if (status >= 500) {
      // 5xx：友好提示服务器错误
      ElMessage.error('服务器错误，请稍后重试')
    }
    console.error('Network Error:', error.message)
    return Promise.reject(error)
  }
)

// ==================== 菜单相关API ====================

/**
 * 获取菜单列表
 */
export const getMenus = () => {
  return request({
    url: '/menus',
    method: 'get'
  })
}

// ==================== 站点信息相关API ====================

/**
 * 获取站点信息（含 captcha_enabled 等配置项）
 */
export const getSiteInfo = () => {
  return request({
    url: '/siteinfo',
    method: 'get'
  })
}

// ==================== 用户认证相关API ====================

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 */
export const login = (data) => {
  return request({
    url: '/login',
    method: 'post',
    data
  })
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.password - 密码
 */
export const register = (data) => {
  return request({
    url: '/register',
    method: 'post',
    data
  })
}

/**
 * 用户登出
 */
export const logout = () => {
  return request({
    url: '/logout',
    method: 'post'
  })
}

/**
 * 获取当前用户信息
 */
export const getSelf = () => {
  return request({
    url: '/self',
    method: 'get'
  })
}

// ==================== 仪表盘相关API ====================

/**
 * 获取仪表盘统计数据
 */
export const getDashboardStats = () => {
  return request({
    url: '/dashboard/stats',
    method: 'get'
  })
}

/**
 * 获取工单趋势数据
 * @param {Object} params - 查询参数
 * @param {string} params.range - 时间范围: week/month
 */
export const getTicketTrend = (params = {}) => {
  return request({
    url: '/dashboard/trend',
    method: 'get',
    params
  })
}

/**
 * 获取工单分类统计
 */
export const getCategoryStats = () => {
  return request({
    url: '/dashboard/category-stats',
    method: 'get'
  })
}

// ==================== 统计相关API ====================

/**
 * 获取详细统计数据
 * @param {Object} params - 查询参数
 * @param {string} params.startDate - 开始日期
 * @param {string} params.endDate - 结束日期
 */
export const getStatisticsData = (params = {}) => {
  return request({
    url: '/statistics/overview',
    method: 'get',
    params
  })
}

/**
 * 获取工单状态分布
 */
export const getTicketStatusDistribution = () => {
  return request({
    url: '/statistics/status-distribution',
    method: 'get'
  })
}

/**
 * 获取工单优先级分布
 */
export const getTicketPriorityDistribution = () => {
  return request({
    url: '/statistics/priority-distribution',
    method: 'get'
  })
}

/**
 * 获取用户处理统计
 */
export const getUserHandlingStats = () => {
  return request({
    url: '/statistics/user-handling',
    method: 'get'
  })
}

/**
 * 获取响应时间统计
 */
export const getResponseTimeStats = (params = {}) => {
  return request({
    url: '/statistics/response-time',
    method: 'get',
    params
  })
}

// ==================== 工单管理相关API ====================

/**
 * 获取工单列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码
 * @param {number} params.size - 每页数量
 * @param {string} params.status - 状态筛选
 * @param {string} params.search - 搜索关键词
 */
export const getTickets = (params = {}) => {
  return request({
    url: '/tickets',
    method: 'get',
    params
  })
}

/**
 * 获取工单详情
 * @param {number} id - 工单ID
 */
export const getTicket = (id) => {
  return request({
    url: `/tickets/${id}`,
    method: 'get'
  })
}

/**
 * 创建工单
 * @param {Object} data - 工单数据
 */
export const createTicket = (data) => {
  return request({
    url: '/tickets',
    method: 'post',
    data
  })
}

/**
 * 更新工单
 * @param {number} id - 工单ID
 * @param {Object} data - 更新数据
 */
export const updateTicket = (id, data) => {
  return request({
    url: `/tickets/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除工单
 * @param {number} id - 工单ID
 */
export const deleteTicket = (id) => {
  return request({
    url: `/tickets/${id}`,
    method: 'delete'
  })
}

/**
 * 获取工单状态变更历史（时间线）
 * @param {number} id - 工单ID
 */
export const getTicketHistory = (id) => {
  return request({
    url: `/tickets/${id}/history`,
    method: 'get'
  })
}

// ==================== 快速回复相关API ====================

/**
 * 获取快速回复列表
 */
export const getQuickReplies = () => {
  return request({
    url: '/quick-replies',
    method: 'get'
  })
}

/**
 * 创建快速回复
 * @param {Object} data - 快速回复数据
 */
export const createQuickReply = (data) => {
  return request({
    url: '/quick-replies',
    method: 'post',
    data
  })
}

/**
 * 更新快速回复
 * @param {number} id - 快速回复ID
 * @param {Object} data - 更新数据
 */
export const updateQuickReply = (id, data) => {
  return request({
    url: `/quick-replies/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除快速回复
 * @param {number} id - 快速回复ID
 */
export const deleteQuickReply = (id) => {
  return request({
    url: `/quick-replies/${id}`,
    method: 'delete'
  })
}

export default request
