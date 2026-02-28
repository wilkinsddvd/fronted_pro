<template>
  <div class="header-bar">
    <div class="header-left">
      <h3>{{ title }}</h3>
    </div>
    <div class="header-right">
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-icon><User /></el-icon>
          <span class="username">{{ userStore.username }}</span>
          <el-tag v-if="userStore.isAdmin" type="danger" size="small" style="margin: 0 4px;">管理员</el-tag>
          <el-icon class="el-icon--right"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { User, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { logout } from '@/api/index.js'
import { userStore } from '@/store/user.js'

const router = useRouter()
const route = useRoute()

/**
 * 根据当前路由计算页面标题
 */
const title = computed(() => {
  const titles = {
    '/dashboard': '数据概览',
    '/tickets': '工单管理',
    '/quick-reply': '快速回复',
    '/statistics': '数据统计',
    '/profile-settings': '个人设置'
  }
  return titles[route.path] || '工单管理系统'
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
    userStore.clear()
    ElMessage.success('退出成功')
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
  background-color: #fff;
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
  transition: left 0.3s;
}

.header-left h3 {
  margin: 0;
  font-size: 18px;
  color: #303133;
  font-weight: 500;
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
  color: #606266;
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
</style>
