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
  // 假登录逻辑：用户名为test，密码为123456即通过
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
.form-container {
  margin: 3rem auto;
  max-width: 340px;
  padding:2rem 2rem 1.5rem;
  border-radius: 10px;
  background: var(--color-background-soft);
  box-shadow: 0 2px 24px 0 #ccc5;
}
form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
input {
  font-size: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  padding: .7em 1em;
  background: var(--color-background-mute);
  color: var(--color-text);
}
button {
  padding: .7em;
  font-size: 1rem;
  background: hsla(160, 100%, 37%, 1);
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
button:hover {
  background: hsla(160, 100%, 45%, 1);
}
.error { color: #e55; font-size: .95em;}
</style>