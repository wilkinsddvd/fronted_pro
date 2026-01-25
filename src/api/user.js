import request from './index'

// ==================== 用户信息相关API ====================

/**
 * 获取当前用户详细信息
 * 用于个人设置页面展示用户信息
 * @returns {Promise} - 返回用户信息对象
 */
export const getUserInfo = () => {
  return request({
    url: '/user/info',
    method: 'get'
  })
}

/**
 * 更新用户基本信息
 * 用于修改昵称、邮箱、手机号等基本信息
 * @param {Object} data - 用户信息数据
 * @param {string} data.nickname - 昵称
 * @param {string} data.email - 邮箱
 * @param {string} data.phone - 手机号
 * @param {string} data.bio - 个人简介
 * @returns {Promise} - 返回更新结果
 */
export const updateUserInfo = (data) => {
  return request({
    url: '/user/info',
    method: 'put',
    data
  })
}

/**
 * 修改用户密码
 * 需要验证原密码，新密码需符合强度要求
 * @param {Object} data - 密码修改数据
 * @param {string} data.oldPassword - 原密码
 * @param {string} data.newPassword - 新密码
 * @param {string} data.confirmPassword - 确认新密码
 * @returns {Promise} - 返回修改结果
 */
export const changePassword = (data) => {
  return request({
    url: '/user/password',
    method: 'put',
    data
  })
}

/**
 * 上传用户头像
 * 支持图片文件上传，返回头像URL
 * @param {FormData} formData - 包含文件的FormData对象
 * @returns {Promise} - 返回头像URL
 */
export const uploadAvatar = (formData) => {
  return request({
    url: '/user/avatar',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 更新用户个性化设置
 * 包括主题、语言、通知偏好等
 * @param {Object} data - 个性化设置数据
 * @param {string} data.theme - 主题设置 (light/dark/auto)
 * @param {string} data.language - 语言设置 (zh-CN/en-US)
 * @param {boolean} data.emailNotification - 邮件通知开关
 * @param {boolean} data.smsNotification - 短信通知开关
 * @param {boolean} data.systemNotification - 系统通知开关
 * @returns {Promise} - 返回更新结果
 */
export const updateUserPreferences = (data) => {
  return request({
    url: '/user/preferences',
    method: 'put',
    data
  })
}

/**
 * 更新用户隐私设置
 * @param {Object} data - 隐私设置数据
 * @param {boolean} data.profilePublic - 个人资料是否公开
 * @param {boolean} data.showEmail - 是否显示邮箱
 * @param {boolean} data.showPhone - 是否显示手机号
 * @param {boolean} data.allowSearch - 是否允许被搜索
 * @returns {Promise} - 返回更新结果
 */
export const updatePrivacySettings = (data) => {
  return request({
    url: '/user/privacy',
    method: 'put',
    data
  })
}

// ==================== Mock数据处理 ====================
// 在实际后端API未就绪时，可以使用本地存储模拟数据

/**
 * 获取模拟用户信息（开发环境使用）
 * @returns {Object} - 模拟的用户信息
 */
export const getMockUserInfo = () => {
  const mockData = {
    id: 1,
    username: 'admin',
    nickname: '管理员',
    email: 'admin@example.com',
    phone: '13800138000',
    avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
    bio: '这是一段个人简介',
    createdAt: '2024-01-01',
    preferences: {
      theme: 'light',
      language: 'zh-CN',
      emailNotification: true,
      smsNotification: false,
      systemNotification: true
    },
    privacy: {
      profilePublic: true,
      showEmail: false,
      showPhone: false,
      allowSearch: true
    }
  }
  
  // 从localStorage获取已保存的数据，如果有的话
  const savedData = localStorage.getItem('userProfile')
  if (savedData) {
    try {
      return JSON.parse(savedData)
    } catch (e) {
      console.error('Failed to parse saved user profile')
    }
  }
  
  return mockData
}

/**
 * 保存模拟用户信息到本地存储（开发环境使用）
 * @param {Object} data - 要保存的用户信息
 */
export const saveMockUserInfo = (data) => {
  const currentData = getMockUserInfo()
  const updatedData = { ...currentData, ...data }
  localStorage.setItem('userProfile', JSON.stringify(updatedData))
  return Promise.resolve({ code: 200, data: updatedData, msg: '保存成功' })
}
