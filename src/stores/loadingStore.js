import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useLoadingStore = defineStore('loading', () => {
  // Map of loading keys to track multiple concurrent loading states
  const loadingMap = ref(new Map())

  // Global loading message
  const loadingText = ref('加载中...')

  // Route transition loading state
  const routeLoading = ref(false)

  // Whether any API/global loading is active
  const isLoading = computed(() => loadingMap.value.size > 0)

  /**
   * Start a loading state with a unique key
   * @param {string} key - Unique identifier for this loading state
   * @param {string} text - Optional loading message
   */
  const startLoading = (key = 'default', text = '加载中...') => {
    loadingText.value = text
    loadingMap.value = new Map(loadingMap.value.set(key, true))
  }

  /**
   * End a loading state by key
   * @param {string} key - Unique identifier for this loading state
   */
  const stopLoading = (key = 'default') => {
    const newMap = new Map(loadingMap.value)
    newMap.delete(key)
    loadingMap.value = newMap
  }

  /**
   * Clear all loading states
   */
  const clearAll = () => {
    loadingMap.value = new Map()
  }

  return { isLoading, loadingText, routeLoading, startLoading, stopLoading, clearAll }
})
