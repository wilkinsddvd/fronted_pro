<template>
  <div>
    <BlogHeader/>
    <SearchBar @search="handleSearch"/>
    <CalendarPanel @select="handleDate"/>

    <!-- 主内容 -->
    <router-view :search="searchKeyword" :date="selectedDate"/>

    <BlogFooter/>
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