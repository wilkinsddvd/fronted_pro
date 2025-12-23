<script setup>
import { ref, onMounted } from 'vue'

// 主题切换storage key
const THEME_KEY = 'blog_theme'
const theme = ref(getTheme())

function setTheme(val) {
  // 先移除原有的主题class，保证互斥
  document.documentElement.classList.remove('dark', 'light')
  if (val === 'dark') {
    document.documentElement.classList.add('dark')
  } else if (val === 'light') {
    document.documentElement.classList.add('light')
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

onMounted(() => {
  setTheme(theme.value)
})
</script>

<template>
  <button class="theme-toggle" :title="theme === 'dark' ? '切换为浅色' : '切换为深色'" @click="toggleTheme">
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