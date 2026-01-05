<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ThemeToggle from './ThemeToggle.vue'
import { logout } from '@/api/index.js'
import { showMessage } from '@/utils/message.js'

const router = useRouter()
const currentUser = ref(null)

function checkLoginStatus() {
  const user = localStorage.getItem('user')
  if (user) {
    try {
      currentUser.value = JSON.parse(user)
    } catch (e) {
      currentUser.value = null
    }
  }
}

async function handleLogout() {
  try {
    await logout()
    localStorage.removeItem('user')
    currentUser.value = null
    showMessage('已登出', 'success')
    router.push('/')
  } catch (e) {
    console.error('Logout failed:', e)
    // 即使后端失败，也清除本地状态
    localStorage.removeItem('user')
    currentUser.value = null
    showMessage('已登出', 'success')
    router.push('/')
  }
}

onMounted(() => {
  checkLoginStatus()
})
</script>

<template>
  <header class="blog-header">
    <h1 @click="$router.push('/')">我的博客</h1>
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/categories">分类</router-link>
      <router-link to="/tags">标签</router-link>
      <router-link to="/archives">归档</router-link>
      <router-link to="/about">关于</router-link>
      <span v-if="currentUser" class="user-info">
        {{ currentUser.username }}
        <button @click="handleLogout" class="logout-btn">登出</button>
      </span>
      <router-link v-else to="/login">登录</router-link>
      <ThemeToggle />
      <a href="https://github.com/wilkinsddvd/fronted_pro" target="_blank">GitHub</a>
    </nav>
  </header>
</template>

<style scoped>
.blog-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  padding: 1rem 0;
}
nav { 
  display: flex;
  align-items: center;
  gap: 1rem;
}
nav a { 
  margin: 0;
  color: var(--color-text);
  text-decoration: none;
}
nav a:hover {
  color: #007bff;
}
.user-info {
  color: var(--color-text);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.logout-btn {
  padding: 0.3rem 0.8rem;
  background: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}
.logout-btn:hover {
  background: #c82333;
}
</style>