<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const repassword = ref('')
const error = ref('')
const router = useRouter()

function handleRegister() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空'
    return
  }
  if (password.value !== repassword.value) {
    error.value = '两次密码输入不一致'
    return
  }
  // 假注册逻辑
  localStorage.setItem('user', username.value)
  router.push('/')
}
</script>

<template>
  <div class="form-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" placeholder="用户名" required autofocus />
      <input v-model="password" placeholder="密码" type="password" required />
      <input v-model="repassword" placeholder="重复密码" type="password" required />
      <button type="submit">注册</button>
      <p class="error" v-if="error">{{ error }}</p>
      <p>已有账号？<router-link to="/login">登录</router-link></p>
    </form>
  </div>
</template>

<style scoped>
@import './form-common.css';
</style>