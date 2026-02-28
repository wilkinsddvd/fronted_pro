<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { register, getSiteInfo } from '@/api/index.js'
import { userStore } from '@/store/user.js'
import { showMessage } from '@/utils/message.js'

const username = ref('')
const password = ref('')
const repassword = ref('')
const captcha = ref('')
const error = ref('')
const loading = ref(false)
const captchaEnabled = ref(false)
const router = useRouter()

// 检查后端是否启用了验证码
onMounted(async () => {
  try {
    const res = await getSiteInfo()
    if (res && res.data) {
      captchaEnabled.value = !!res.data.captcha_enabled
    }
  } catch (e) {
    // 后端未返回配置时默认不显示验证码，保持向下兼容
  }
})

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
  if (captchaEnabled.value && !captcha.value) {
    error.value = '请输入验证码'
    return
  }

  loading.value = true
  try {
    const payload = { username: username.value, password: password.value }
    if (captchaEnabled.value) {
      payload.captcha = captcha.value
    }
    const res = await register(payload)
    // 先保存注册响应（含token），再拉取完整用户信息（含role）
    localStorage.setItem('user', JSON.stringify(res.data))
    await userStore.fetchSelf()
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
      <!-- 验证码字段：仅在后端配置启用时显示 -->
      <input
        v-if="captchaEnabled"
        v-model="captcha"
        placeholder="验证码"
        autocomplete="off"
      />
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