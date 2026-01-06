import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // 配置开发环境下的代理
      // 将前端发起的 /api 请求代理到后端服务器 http://localhost:8000
      '/api': {
        target: 'http://localhost:8000', // 后端服务器地址
        changeOrigin: true, // 改变请求头中的 origin 字段，解决跨域问题
        rewrite: (path) => path.replace(/^\/api/, ''), // 重写路径，去掉 /api 前缀
        // 例如：前端请求 /api/users -> 代理后端 http://localhost:8000/users
      }
    }
  }
})
