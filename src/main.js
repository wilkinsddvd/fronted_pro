import './assets/main.css'
import './styles/auth-background.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import i18n from './i18n/index.js'
import { vLoading, injectLoadingStyles } from './directives/loading.js'

const app = createApp(App)
const pinia = createPinia()

// Register all Element Plus icons
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Inject v-loading directive styles
injectLoadingStyles()

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.use(i18n)
app.directive('loading', vLoading)
app.mount('#app')