<template>
  <ProgressBar />
  <LoadingOverlay :visible="appLoading" text="应用加载中..." />
  <router-view />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useThemeStore } from '@/stores/themeStore'
import LoadingOverlay from '@/components/LoadingOverlay.vue'
import ProgressBar from '@/components/ProgressBar.vue'

const themeStore = useThemeStore()
const appLoading = ref(true)

onMounted(async () => {
  themeStore.initTheme()
  // Show splash screen briefly on app startup, then hide
  await new Promise(resolve => setTimeout(resolve, 600))
  appLoading.value = false
})

onUnmounted(() => {
  themeStore.cleanup()
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
