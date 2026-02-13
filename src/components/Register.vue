<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '@/api/index.js'
import { showMessage } from '@/utils/message.js'

const username = ref('')
const password = ref('')
const repassword = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function handleRegister() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = '用户名和密码不能为空'
    return
  }
  if (password.value !== repassword.value) {
    error.value = '两次密码输入不一致'
    return
  }
  
  loading.value = true
  try {
    const res = await register({
      username: username.value,
      password: password.value
    })
    // 保存用户信息到本地存储
    localStorage.setItem('user', JSON.stringify(res.data))
    showMessage('注册成功！', 'success')
    setTimeout(() => {
      router.push('/dashboard')
    }, 500)
  } catch (e) {
    error.value = e.message || '注册失败'
    showMessage(error.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="form-container">
    <h2>注册</h2>
    <form @submit.prevent="handleRegister">
      <input v-model="username" placeholder="用户名" required autofocus />
      <input v-model="password" placeholder="密码" type="password" required />
      <input v-model="repassword" placeholder="重复密码" type="password" required />
      <button type="submit" :disabled="loading">
        {{ loading ? '注册中...' : '注册' }}
      </button>
      <p class="error" v-if="error">{{ error }}</p>
      <p>已有账号？<router-link to="/login">登录</router-link></p>
    </form>
  </div>
</template>

<style scoped>
@import './form-common.css';
</style>