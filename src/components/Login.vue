<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/api/index.js'
import { showMessage } from '@/utils/message.js'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function handleLogin() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空'
    return
  }
  
  loading.value = true
  try {
    const res = await login({
      username: username.value,
      password: password.value
    })
    // 保存用户信息到本地存储
    localStorage.setItem('user', JSON.stringify(res.data))
    showMessage('登录成功！', 'success')
    setTimeout(() => {
      router.push('/dashboard')
    }, 500)
  } catch (e) {
    error.value = e.message || '登录失败，请检查用户名和密码'
    showMessage(error.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="form-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="用户名" required autofocus />
      <input v-model="password" placeholder="密码" type="password" required />
      <button type="submit" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
      <p class="error" v-if="error">{{ error }}</p>
      <p>还没有账号？<router-link to="/register">注册</router-link></p>
    </form>
  </div>
</template>

<style scoped>
@import './form-common.css';
</style>