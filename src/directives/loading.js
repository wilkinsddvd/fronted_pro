/**
 * v-loading directive
 * Usage: <div v-loading="isLoading">...</div>
 *        <div v-loading.fullscreen="isLoading">...</div>
 */

function createLoadingEl(isDark) {
  const el = document.createElement('div')
  el.className = `v-loading-mask${isDark ? ' is-dark' : ''}`
  el.innerHTML = `
    <div class="v-loading-content">
      <svg class="v-loading-spinner" viewBox="0 0 50 50">
        <circle class="v-loading-path" cx="25" cy="25" r="20"
          fill="none" stroke-width="4" stroke-linecap="round" />
      </svg>
    </div>
  `
  return el
}

function isDarkMode() {
  return document.documentElement.classList.contains('dark')
}

export const vLoading = {
  mounted(el, binding) {
    const loadingEl = createLoadingEl(isDarkMode())
    el._loadingEl = loadingEl

    const isFullscreen = binding.modifiers?.fullscreen
    if (isFullscreen) {
      loadingEl.classList.add('is-fullscreen')
      document.body.appendChild(loadingEl)
    } else {
      // Ensure positioned parent
      const position = window.getComputedStyle(el).position
      if (position === 'static') {
        el.style.position = 'relative'
      }
      el.appendChild(loadingEl)
    }

    if (!binding.value) {
      loadingEl.style.display = 'none'
    }
  },

  updated(el, binding) {
    const loadingEl = el._loadingEl
    if (!loadingEl) return

    // Update dark mode class
    if (isDarkMode()) {
      loadingEl.classList.add('is-dark')
    } else {
      loadingEl.classList.remove('is-dark')
    }

    loadingEl.style.display = binding.value ? '' : 'none'
  },

  unmounted(el) {
    const loadingEl = el._loadingEl
    if (loadingEl && loadingEl.parentNode) {
      loadingEl.parentNode.removeChild(loadingEl)
    }
    delete el._loadingEl
  }
}

/**
 * Inject v-loading global styles into document head (called once from main.js)
 */
export function injectLoadingStyles() {
  if (document.getElementById('v-loading-styles')) return
  const style = document.createElement('style')
  style.id = 'v-loading-styles'
  style.textContent = `
    .v-loading-mask {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 2000;
      border-radius: inherit;
    }
    .v-loading-mask.is-fullscreen {
      position: fixed;
      z-index: 9999;
    }
    .v-loading-mask.is-dark {
      background: rgba(19, 20, 26, 0.8);
    }
    .v-loading-content {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .v-loading-spinner {
      width: 36px;
      height: 36px;
      animation: v-loading-rotate 1.4s linear infinite;
    }
    .v-loading-path {
      stroke: #409eff;
      stroke-dasharray: 90, 150;
      stroke-dashoffset: 0;
      animation: v-loading-dash 1.4s ease-in-out infinite;
    }
    @keyframes v-loading-rotate {
      100% { transform: rotate(360deg); }
    }
    @keyframes v-loading-dash {
      0% { stroke-dasharray: 1, 200; stroke-dashoffset: 0; }
      50% { stroke-dasharray: 90, 150; stroke-dashoffset: -40px; }
      100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124px; }
    }
  `
  document.head.appendChild(style)
}
