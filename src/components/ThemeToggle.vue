<script setup>
import { ref, onMounted } from 'vue'

// 获取/设置主题：优先取localStorage，其次系统偏好
const THEME_KEY = 'blog_theme'
const theme = ref(getTheme())

function setTheme(val) {
  if(val === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem(THEME_KEY, val)
}
function getTheme() {
  let t = localStorage.getItem(THEME_KEY)
  if (!t) {
    t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  return t
}
function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  setTheme(theme.value)
}
// 初始设定
onMounted(() => {
  setTheme(theme.value)
})
</script>

<template>
  <button class="theme-toggle" :title="theme === 'dark' ? '切换为亮色' : '切换为暗色'" @click="toggleTheme">
    <span v-if="theme === 'dark'">🌙</span>
    <span v-else>🌞</span>
  </button>
</template>

<style scoped>
.theme-toggle {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.5em;
  margin-left: 8px;
  transition: filter 0.2s;
}
.theme-toggle:hover {
  filter: brightness(1.3);
}
</style>