<template>
  <router-view />
</template>

<script setup>
import { onMounted, onUnmounted, provide } from 'vue'

// 媒体查询监听器（用于跟随系统模式）
let mediaQueryListener = null

/**
 * 应用主题到 html 元素
 * @param {string} theme - 'light' | 'dark' | 'auto'
 */
const applyTheme = (theme) => {
  const html = document.documentElement

  if (mediaQueryListener) {
    window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', mediaQueryListener)
    mediaQueryListener = null
  }

  if (theme === 'dark') {
    html.classList.add('dark')
  } else if (theme === 'auto') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    if (prefersDark) {
      html.classList.add('dark')
    } else {
      html.classList.remove('dark')
    }
    // 监听系统主题变化
    mediaQueryListener = (e) => {
      if (e.matches) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', mediaQueryListener)
  } else {
    // light
    html.classList.remove('dark')
  }
}

onMounted(() => {
  // 应用启动时，从 localStorage 读取保存的主题并立即应用
  const savedTheme = localStorage.getItem('app_theme') || 'light'
  applyTheme(savedTheme)
})

onUnmounted(() => {
  if (mediaQueryListener) {
    window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', mediaQueryListener)
  }
})

// 使用 provide 让子组件可以调用
provide('applyTheme', applyTheme)
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>