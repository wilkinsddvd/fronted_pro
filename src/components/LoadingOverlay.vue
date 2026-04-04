<template>
  <Teleport to="body">
    <Transition name="loading-fade">
      <div v-if="visible" class="loading-overlay" :class="{ 'is-dark': isDark }">
        <div class="loading-content">
          <!-- Spinner SVG animation -->
          <svg class="loading-spinner" viewBox="0 0 50 50" xmlns="http://www.w3.org/2000/svg">
            <circle
              class="loading-path"
              cx="25"
              cy="25"
              r="20"
              fill="none"
              stroke-width="4"
              stroke-linecap="round"
            />
          </svg>
          <p class="loading-text">{{ text }}</p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/themeStore'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: '加载中...'
  }
})

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDarkMode)
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.loading-overlay.is-dark {
  background: rgba(19, 20, 26, 0.9);
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  animation: loading-rotate 1.4s linear infinite;
}

.loading-path {
  stroke: #409eff;
  stroke-dasharray: 90, 150;
  stroke-dashoffset: 0;
  animation: loading-dash 1.4s ease-in-out infinite;
}

.loading-text {
  color: #606266;
  font-size: 14px;
  margin: 0;
  letter-spacing: 0.5px;
}

.is-dark .loading-text {
  color: #a0a8b7;
}

/* Transition animations */
.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: opacity 0.3s ease;
}

.loading-fade-enter-from,
.loading-fade-leave-to {
  opacity: 0;
}

@keyframes loading-rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes loading-dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -40px;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124px;
  }
}
</style>
