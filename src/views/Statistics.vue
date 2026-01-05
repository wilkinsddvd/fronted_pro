<template>
  <div class="statistics">
    <el-card shadow="hover">
      <template #header>
        <span>数据统计</span>
      </template>
      
      <div class="statistics-content">
        <el-empty description="数据统计功能开发中" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.statistics {
  animation: fadeIn 0.3s ease-in;
}

.statistics-content {
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
