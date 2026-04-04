import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDarkMode = ref(false)

  let mediaQueryListener = null
  let mediaQuery = null

  /**
   * Apply theme to the html element
   * @param {string} theme - 'light' | 'dark' | 'auto'
   */
  const applyTheme = (theme) => {
    const html = document.documentElement
    const mq = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery = mq

    // Remove old system theme listener
    if (mediaQueryListener) {
      mq.removeEventListener('change', mediaQueryListener)
      mediaQueryListener = null
    }

    if (theme === 'dark') {
      html.classList.add('dark')
      isDarkMode.value = true
    } else if (theme === 'auto') {
      const prefersDark = mq.matches
      if (prefersDark) {
        html.classList.add('dark')
      } else {
        html.classList.remove('dark')
      }
      isDarkMode.value = prefersDark

      // Listen for system theme changes
      mediaQueryListener = (e) => {
        if (e.matches) {
          document.documentElement.classList.add('dark')
          isDarkMode.value = true
        } else {
          document.documentElement.classList.remove('dark')
          isDarkMode.value = false
        }
      }
      mq.addEventListener('change', mediaQueryListener)
    } else {
      // light (default)
      html.classList.remove('dark')
      isDarkMode.value = false
    }

    localStorage.setItem('app_theme', theme)
  }

  /**
   * Toggle between light and dark modes
   */
  const toggleTheme = () => {
    const newTheme = isDarkMode.value ? 'light' : 'dark'
    applyTheme(newTheme)
  }

  /**
   * Initialize theme from localStorage on app start
   */
  const initTheme = () => {
    const savedTheme = localStorage.getItem('app_theme') || 'light'
    applyTheme(savedTheme)
  }

  /**
   * Clean up media query listener
   */
  const cleanup = () => {
    if (mediaQueryListener && mediaQuery) {
      mediaQuery.removeEventListener('change', mediaQueryListener)
      mediaQueryListener = null
      mediaQuery = null
    }
  }

  return { isDarkMode, applyTheme, toggleTheme, initTheme, cleanup }
})
