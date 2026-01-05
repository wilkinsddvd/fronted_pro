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
            <el-dropdown-item command="profile">个人中心</el-dropdown-item>
            <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { User, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

const username = ref('Admin')

const title = computed(() => {
  const titles = {
    '/dashboard': '数据概览',
    '/tickets': '工单管理',
    '/quick-reply': '快速回复',
    '/categories': '分类管理',
    '/statistics': '数据统计',
    '/settings': '系统配置'
  }
  return titles[route.path] || '工单管理系统'
})

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('user')
    ElMessage.success('退出成功')
    router.push('/login')
  } else if (command === 'profile') {
    ElMessage.info('个人中心功能开发中')
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
</style>
