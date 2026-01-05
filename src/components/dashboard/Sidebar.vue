<template>
  <div class="sidebar">
    <div class="logo-container">
      <h2>工单管理系统</h2>
    </div>
    <el-menu
      :default-active="activeMenu"
      class="sidebar-menu"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
      :router="true"
    >
      <el-menu-item index="/dashboard">
        <el-icon><DataLine /></el-icon>
        <span>数据概览</span>
      </el-menu-item>
      <el-menu-item index="/tickets">
        <el-icon><Tickets /></el-icon>
        <span>工单管理</span>
      </el-menu-item>
      <el-menu-item index="/quick-reply">
        <el-icon><ChatLineSquare /></el-icon>
        <span>快速回复</span>
      </el-menu-item>
      <el-menu-item index="/categories">
        <el-icon><FolderOpened /></el-icon>
        <span>分类管理</span>
      </el-menu-item>
      <el-menu-item index="/statistics">
        <el-icon><TrendCharts /></el-icon>
        <span>数据统计</span>
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <span>系统配置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { DataLine, Tickets, ChatLineSquare, FolderOpened, TrendCharts, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: #304156;
  position: fixed;
  left: 0;
  top: 0;
  overflow-y: auto;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b3947;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.logo-container h2 {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
}
</style>
