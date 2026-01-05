import axios from 'axios'

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
    console.error('Network Error:', error.message)
    return Promise.reject(error)
  }
)

// ==================== 文章相关API ====================

/**
 * 获取文章列表
 * @param {Object} params - 查询参数
 * @param {number} params.page - 页码，默认1
 * @param {number} params.size - 每页数量，默认10
 * @param {string} params.search - 搜索关键词
 * @param {string} params.category - 分类筛选
 * @param {string} params.tag - 标签筛选
 * @param {string} params.date - 日期筛选
 */
export const getPosts = (params = {}) => {
  return request({
    url: '/posts',
    method: 'get',
    params
  })
}

/**
 * 获取文章详情
 * @param {number} id - 文章ID
 */
export const getPost = (id) => {
  return request({
    url: `/posts/${id}`,
    method: 'get'
  })
}

/**
 * 增加文章浏览量
 * @param {number} id - 文章ID
 */
export const addPostView = (id) => {
  return request({
    url: `/posts/${id}/view`,
    method: 'post'
  })
}

/**
 * 点赞文章
 * @param {number} id - 文章ID
 */
export const addPostLike = (id) => {
  return request({
    url: `/posts/${id}/like`,
    method: 'post'
  })
}

// ==================== 分类相关API ====================

/**
 * 获取分类列表
 */
export const getCategories = () => {
  return request({
    url: '/categories',
    method: 'get'
  })
}

// ==================== 标签相关API ====================

/**
 * 获取标签列表
 */
export const getTags = () => {
  return request({
    url: '/tags',
    method: 'get'
  })
}

// ==================== 归档相关API ====================

/**
 * 获取归档列表
 */
export const getArchive = () => {
  return request({
    url: '/archive',
    method: 'get'
  })
}

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
 * 获取站点信息
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

export default request
