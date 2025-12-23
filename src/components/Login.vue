<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

function handleLogin() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空'
    return
  }
  // 假登录逻辑
  if (username.value === 'test' && password.value === '123456') {
    localStorage.setItem('user', username.value)
    router.push('/')
  } else {
    error.value = '用户名或密码错误'
  }
}
</script>

<template>
  <div class="form-container">
    <h2>登录</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="用户名" required autofocus />
      <input v-model="password" placeholder="密码" type="password" required />
      <button type="submit">登录</button>
      <p class="error" v-if="error">{{ error }}</p>
      <p>还没有账号？<router-link to="/register">注册</router-link></p>
    </form>
  </div>
</template>

<style scoped>
@import './form-common.css';
</style>