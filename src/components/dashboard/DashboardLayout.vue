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
  display: flex;
  height: 100vh;
  background-color: #f0f2f5;
  overflow: hidden;
}

.main-container {
  margin-left: 200px;
  display: flex;
  flex-direction: column;
  flex: 1;
  height: 100vh;
  overflow: hidden;
  transition: margin-left 0.3s;
}

.content-wrapper {
  padding: 84px 24px 24px 24px;
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
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
