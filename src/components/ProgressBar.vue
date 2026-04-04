<template>
  <Teleport to="body">
    <div class="progress-bar-wrap">
      <div
        class="progress-bar"
        :style="{ width: progress + '%', opacity: visible ? 1 : 0 }"
      />
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { useLoadingStore } from '@/stores/loadingStore'

const loadingStore = useLoadingStore()
const progress = ref(0)
const visible = ref(false)
let timer = null

const start = () => {
  visible.value = true
  progress.value = 0
  clearInterval(timer)
  // Simulate auto-progress
  timer = setInterval(() => {
    if (progress.value < 85) {
      const increment = (85 - progress.value) * 0.08
      progress.value = Math.min(85, progress.value + increment)
    }
  }, 100)
}

const finish = () => {
  clearInterval(timer)
  timer = null
  progress.value = 100
  setTimeout(() => {
    visible.value = false
    progress.value = 0
  }, 400)
}

onUnmounted(() => {
  clearInterval(timer)
  timer = null
})

// Watch route loading state from store
watch(() => loadingStore.routeLoading, (loading) => {
  if (loading) {
    start()
  } else {
    finish()
  }
})

defineExpose({ start, finish })
</script>

<style scoped>
.progress-bar-wrap {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 10000;
  pointer-events: none;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #409eff, #67c23a);
  transition: width 0.2s ease, opacity 0.4s ease;
  box-shadow: 0 0 8px rgba(64, 158, 255, 0.6);
}
</style>
