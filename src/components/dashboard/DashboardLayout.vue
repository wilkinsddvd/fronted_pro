<template>
  <div class="dashboard-layout">
    <Sidebar />
    <div class="main-container">
      <HeaderBar />
      <div class="content-wrapper">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './Sidebar.vue'
import HeaderBar from './HeaderBar.vue'
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background-color: #f0f2f5;
}

.main-container {
  margin-left: 200px;
  min-height: 100vh;
  transition: margin-left 0.3s;
}

.content-wrapper {
  padding: 84px 24px 24px 24px;
  min-height: calc(100vh - 60px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-container {
    margin-left: 0;
  }
  
  .content-wrapper {
    padding: 84px 12px 12px 12px;
  }
}
</style>
