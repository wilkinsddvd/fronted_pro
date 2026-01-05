<template>
  <div class="settings">
    <el-card shadow="hover">
      <template #header>
        <span>系统配置</span>
      </template>
      
      <div class="settings-content">
        <el-empty description="系统配置功能开发中" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.settings {
  animation: fadeIn 0.3s ease-in;
}

.settings-content {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
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
