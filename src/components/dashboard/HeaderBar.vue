<template>
  <div class="header-bar">
    <div class="header-left">
      <h3>{{ title }}</h3>
    </div>
    <div class="header-right">
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-icon><User /></el-icon>
          <span class="username">{{ username }}</span>
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">{{ $t('header.profileCenter') }}</el-dropdown-item>
            <el-dropdown-item command="logout" divided>{{ $t('header.logout') }}</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { User, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { logout } from '@/api/index.js'

const router = useRouter()
const route = useRoute()
const { t } = useI18n()

const username = ref('Admin')

// 从localStorage读取用户名
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const userData = JSON.parse(userStr)
      if (userData.username) {
        username.value = userData.username
      }
    } catch (e) {
      console.error('Failed to parse user data from localStorage')
    }
  }
})

/**
 * 根据当前路由计算页面标题
 */
const title = computed(() => {
  const titles = {
    '/dashboard': t('header.dashboard'),
    '/tickets': t('header.tickets'),
    '/quick-reply': t('header.quickReply'),
    '/statistics': t('header.statistics'),
    '/profile-settings': t('header.profileSettings')
  }
  return titles[route.path] || t('header.defaultTitle')
})

/**
 * 处理下拉菜单命令
 * @param {string} command - 菜单命令
 */
const handleCommand = async (command) => {
  if (command === 'logout') {
    // 退出登录
    try {
      await logout()
    } catch (e) {
      console.error('Logout API error:', e)
    }
    localStorage.removeItem('user')
    ElMessage.success(t('header.logoutSuccess'))
    router.push('/login')
  } else if (command === 'profile') {
    // 跳转到个人设置页面
    router.push('/profile-settings')
  }
}
</script>

<style scoped>
.header-bar {
  height: 60px;
  background-color: var(--header-bg, #ffffff);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  position: fixed;
  top: 0;
  left: 200px;
  right: 0;
  z-index: 100;
  transition: left 0.3s, background-color 0.3s;
}

.header-left h3 {
  margin: 0;
  font-size: 18px;
  color: var(--app-text-color, #303133);
  font-weight: 500;
  transition: color 0.3s;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  margin: 0 8px;
  font-size: 14px;
  color: var(--app-text-secondary, #606266);
  transition: color 0.3s;
}

/* Responsive Design */
@media (max-width: 768px) {
  .header-bar {
    left: 0;
    padding: 0 12px;
  }
  
  .header-left h3 {
    font-size: 16px;
  }
  
  .username {
    display: none;
  }
}

/* Dark mode */
:global(html.dark) .header-bar {
  background-color: #1e1e2e;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
}

:global(html.dark) .header-left h3 {
  color: #cfd3dc;
}

:global(html.dark) .username {
  color: #a8b2c1;
}

:global(html.dark) .user-info:hover {
  background-color: #2a2d3a;
}
</style>
