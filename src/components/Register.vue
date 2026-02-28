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
  <div class="page-bg">
    <transition name="fade-up">
      <div class="form-card">
        <div class="avatar-wrap">
          <el-avatar :size="64" class="form-avatar">
            <el-icon :size="36"><User /></el-icon>
          </el-avatar>
        </div>
        <h2 class="form-title">创建账号</h2>
        <p class="form-subtitle">注册并开始使用</p>
        <el-form @submit.prevent="handleRegister" class="el-form-wrap">
          <el-form-item>
            <el-input
              v-model="username"
              placeholder="用户名"
              size="large"
              clearable
              autofocus
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="password"
              placeholder="密码"
              type="password"
              size="large"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-form-item>
            <el-input
              v-model="repassword"
              placeholder="重复密码"
              type="password"
              size="large"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          <el-alert
            v-if="error"
            :title="error"
            type="error"
            show-icon
            :closable="false"
            class="form-alert"
          />
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              class="submit-btn"
              :loading="loading"
              native-type="submit"
            >
              {{ loading ? '注册中...' : '注册' }}
            </el-button>
          </el-form-item>
        </el-form>
        <p class="form-footer">
          已有账号？
          <router-link to="/login" class="form-link">立即登录</router-link>
        </p>
      </div>
    </transition>
  </div>
</template>

<style scoped>
@import './form-common.css';
</style>