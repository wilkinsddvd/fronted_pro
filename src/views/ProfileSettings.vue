<template>
  <div class="profile-settings">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>{{ $t('profile.title') }}</h2>
      <p class="subtitle">{{ $t('profile.subtitle') }}</p>
    </div>

    <!-- 标签页布局 -->
    <el-tabs v-model="activeTab" class="settings-tabs" type="border-card">
      <!-- 基本信息标签页 -->
      <el-tab-pane :label="$t('profile.tabs.basic')" name="basic">
        <BasicInfoForm 
          :user-info="userInfo" 
          :loading="loading"
          @update="handleUpdateBasicInfo"
        />
      </el-tab-pane>

      <!-- 安全设置标签页 -->
      <el-tab-pane :label="$t('profile.tabs.security')" name="security">
        <SecuritySettings 
          :loading="loading"
          @change-password="handleChangePassword"
        />
      </el-tab-pane>

      <!-- 个性化设置标签页 -->
      <el-tab-pane :label="$t('profile.tabs.personalization')" name="personalization">
        <PersonalizationSettings 
          :preferences="userInfo.preferences"
          :loading="loading"
          @update="handleUpdatePreferences"
        />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUserInfo, updateUserInfo, changePassword, updateUserPreferences } from '@/api/user'
import BasicInfoForm from './profile-settings/BasicInfoForm.vue'
import SecuritySettings from './profile-settings/SecuritySettings.vue'
import PersonalizationSettings from './profile-settings/PersonalizationSettings.vue'

const router = useRouter()

// ==================== 响应式数据 ====================
const activeTab = ref('basic') // 当前激活的标签页
const loading = ref(false) // 全局加载状态
const userInfo = ref({
  id: null,
  username: '',
  nickname: '',
  email: '',
  phone: '',
  avatar: '',
  bio: '',
  createdAt: '',
  preferences: {
    theme: 'light',
    language: 'zh-CN',
    emailNotification: true,
    systemNotification: true
  }
})

// ==================== 生命周期钩子 ====================
/**
 * 组件挂载时加载用户信息
 */
onMounted(async () => {
  await loadUserInfo()
})

// ==================== 方法 ====================
/**
 * 加载用户信息
 */
const loadUserInfo = async () => {
  loading.value = true
  try {
    const res = await getUserInfo()
    if (res.code === 200) {
      userInfo.value = res.data
    } else {
      ElMessage.error(res.msg || '加载用户信息失败')
    }
  } catch (error) {
    ElMessage.error('加载用户信息失败，请检查网络')
    console.error('Load user info error:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 处理基本信息更新
 * @param {Object} data - 更新的基本信息数据
 */
const handleUpdateBasicInfo = async (data) => {
  // 重要操作前弹窗确认
  try {
    await ElMessageBox.confirm(
      '确定要更新基本信息吗？',
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }
    )

    loading.value = true
    
    const res = await updateUserInfo(data)
    if (res.code === 200) {
      if (res.data) {
        Object.assign(userInfo.value, res.data)
      }
      ElMessage.success('基本信息更新成功')
    } else {
      ElMessage.error(res.msg || '更新失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('更新失败，请重试')
      console.error('Update basic info error:', error)
    }
  } finally {
    loading.value = false
  }
}

/**
 * 处理密码修改
 * @param {Object} data - 密码修改数据
 */
const handleChangePassword = async (data) => {
  // 重要操作前弹窗确认
  try {
    await ElMessageBox.confirm(
      '修改密码后需要重新登录，确定要继续吗？',
      '修改密码确认',
      {
        confirmButtonText: '确定修改',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true
    
    await changePassword(data)
    
    ElMessage.success('密码修改成功，请重新登录')
    localStorage.removeItem('user')
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('密码修改失败，请检查原密码是否正确')
      console.error('Change password error:', error)
    }
  } finally {
    loading.value = false
  }
}

/**
 * 处理个性化设置更新
 * @param {Object} data - 个性化设置数据
 */
const handleUpdatePreferences = async (data) => {
  loading.value = true
  try {
    const res = await updateUserPreferences(data)
    if (res.code === 200) {
      userInfo.value.preferences = { ...userInfo.value.preferences, ...data }
      ElMessage.success('个性化设置已保存')
    } else {
      ElMessage.error(res.msg || '保存失败')
    }
  } catch (error) {
    ElMessage.error('保存失败，请重试')
    console.error('Update preferences error:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-settings {
  padding: 20px;
  animation: fadeIn 0.3s ease-in;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.page-header .subtitle {
  margin: 5px 0 0;
  font-size: 14px;
  color: #909399;
}

.settings-tabs {
  background: #fff;
  border-radius: 4px;
}

.settings-tabs :deep(.el-tabs__content) {
  padding: 20px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
