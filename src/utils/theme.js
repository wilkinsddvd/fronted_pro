const THEME_KEY = 'blog_theme'

export function setTheme(theme) {
  if (theme === 'dark') {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem(THEME_KEY, theme)
}

export function getTheme() {
  // 优先取本地存储
  let theme = localStorage.getItem(THEME_KEY)
  if (!theme) {
    // 自动探测系统主题
    theme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
      ? 'dark'
      : 'light'
  }
  return theme
}