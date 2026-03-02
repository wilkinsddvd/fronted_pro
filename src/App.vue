<template>
  <router-view />
</template>

<script setup>
import { onMounted, onUnmounted, provide } from 'vue'

// 媒体查询监听器引用（用于 auto 模式跟随系统）
let mediaQueryListener = null
let mediaQuery = null

/**
 * 应用主题到 html 元素
 * @param {string} theme - 'light' | 'dark' | 'auto'
 */
const applyTheme = (theme) => {
  const html = document.documentElement
  const mq = window.matchMedia('(prefers-color-scheme: dark)')
  mediaQuery = mq

  // 清除旧的系统主题监听器
  if (mediaQueryListener) {
    mq.removeEventListener('change', mediaQueryListener)
    mediaQueryListener = null
  }

  if (theme === 'dark') {
    html.classList.add('dark')
  } else if (theme === 'auto') {
    // 立即根据系统偏好设置
    if (mq.matches) {
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
    mq.addEventListener('change', mediaQueryListener)
  } else {
    // light（默认）
    html.classList.remove('dark')
  }
}

// 通过 provide 将 applyTheme 注入给子组件
provide('applyTheme', applyTheme)

onMounted(() => {
  // 应用启动时从 localStorage 读取已保存的主题并立即应用
  const savedTheme = localStorage.getItem('app_theme') || 'light'
  applyTheme(savedTheme)
})

onUnmounted(() => {
  if (mediaQueryListener && mediaQuery) {
    mediaQuery.removeEventListener('change', mediaQueryListener)
    mediaQueryListener = null
    mediaQuery = null
  }
})
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