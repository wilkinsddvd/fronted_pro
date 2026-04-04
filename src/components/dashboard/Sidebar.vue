<template>
  <div class="sidebar">
    <!-- Logo 区域 -->
    <div class="logo-container">
      <h2>{{ $t('sidebar.systemName') }}</h2>
    </div>
    
    <!-- 侧边栏菜单 -->
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      :background-color="sidebarBg"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      :router="true"
    >
      <!-- 数据概览 -->
      <el-menu-item index="/dashboard">
        <el-icon><DataLine /></el-icon>
        <span>{{ $t('sidebar.dashboard') }}</span>
      </el-menu-item>
      
      <!-- 工单管理 -->
      <el-menu-item index="/tickets">
        <el-icon><Tickets /></el-icon>
        <span>{{ $t('sidebar.tickets') }}</span>
      </el-menu-item>
      
      <!-- 快速回复 -->
      <el-menu-item index="/quick-reply">
        <el-icon><ChatLineSquare /></el-icon>
        <span>{{ $t('sidebar.quickReply') }}</span>
      </el-menu-item>
      
      <!-- 数据统计 -->
      <el-menu-item index="/statistics">
        <el-icon><TrendCharts /></el-icon>
        <span>{{ $t('sidebar.statistics') }}</span>
      </el-menu-item>
      
      <!-- 后勤人员管理 -->
      <el-menu-item index="/staff-management">
        <el-icon><Avatar /></el-icon>
        <span>{{ $t('sidebar.staffManagement') }}</span>
      </el-menu-item>

      <!-- 个人设置 -->
      <el-menu-item index="/profile-settings">
        <el-icon><User /></el-icon>
        <span>{{ $t('sidebar.profileSettings') }}</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataLine, Tickets, ChatLineSquare, TrendCharts, User, Avatar } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/themeStore'

const route = useRoute()
const themeStore = useThemeStore()

/**
 * 根据当前路由计算激活的菜单项
 */
const activeMenu = computed(() => route.path)

/**
 * 根据主题动态设置侧边栏背景色
 */
const sidebarBg = computed(() => themeStore.isDarkMode ? '#1a1d23' : '#304156')
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: var(--sidebar-bg, #304156);
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: transform 0.3s, background-color 0.3s;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--sidebar-logo-bg, #2b3947);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  transition: background-color 0.3s;
}

.logo-container h2 {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  text-align: center;
  padding: 0 10px;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}

/* Responsive Design */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-200px);
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
}

/* Dark mode */
:global(html.dark) .sidebar-menu :deep(.el-menu-item:hover) {
  background-color: #252830 !important;
}

:global(html.dark) .sidebar-menu :deep(.el-menu-item.is-active) {
  color: #409EFF !important;
  background-color: #252830 !important;
}
</style>
