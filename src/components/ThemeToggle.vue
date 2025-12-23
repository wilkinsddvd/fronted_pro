<script setup>
import { ref, onMounted } from 'vue'
import { setTheme, getTheme } from '../utils/theme'

const theme = ref(getTheme())

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  setTheme(theme.value)
}

onMounted(() => {
  setTheme(theme.value)
})
</script>

<template>
  <button class="theme-toggle" @click="toggleTheme" :title="theme==='dark'? '切换为亮色':'切换为暗色'">
    <span v-if="theme === 'dark'">🌙</span>
    <span v-else>🌞</span>
  </button>
</template>

<style scoped>
.theme-toggle {
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 1.24em;
  margin-left: 8px;
}
</style>