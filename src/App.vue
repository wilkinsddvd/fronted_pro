<template>
  <div class="main-app">
    <!-- 顶部导航栏 -->
    <BlogHeader />

    <!-- 搜索栏，居中美化 -->
    <div class="search-container">
      <SearchBar @search="handleSearch" />
    </div>

    <!-- 右上角折叠日历 -->
    <CalendarPanel @select="handleDate" />

    <!-- 主内容区域 -->
    <div class="content-container">
      <router-view :search="searchKeyword" :date="selectedDate" />
    </div>

    <!-- 页脚 -->
    <BlogFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BlogHeader from './components/BlogHeader.vue'
import BlogFooter from './components/BlogFooter.vue'
import SearchBar from '@/components/SearchBar.vue'
import CalendarPanel from '@/components/CalendarPanel.vue'

const searchKeyword = ref('')
const selectedDate = ref('')

function handleSearch(val) {
  searchKeyword.value = val
}
function handleDate(date) {
  selectedDate.value = date
}
</script>

<style>
body {
  background: #181920;
  color: #fff;
  font-family: "PingFang SC", "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif;
  margin: 0;
}

.main-app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.search-container {
  margin: 0 auto;
  margin-top: 36px;
  margin-bottom: 12px;
  max-width: 700px;
  width: 90%;
}

.content-container {
  margin: 0 auto;
  flex: 1;
  max-width: 800px;
  width: 95%;
  padding-bottom: 24px;
  background: transparent;
}
</style>