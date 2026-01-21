<template>
  <el-card class="security-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>密码修改</span>
        <el-tag type="info" size="small">重要操作</el-tag>
      </div>
    </template>

    <el-alert
      title="安全提示"
      type="warning"
      :closable="false"
      show-icon
      class="security-alert"
    >
      <p>为了您的账户安全，请定期修改密码</p>
      <p>新密码需包含大小写字母、数字，长度至少8位</p>
    </el-alert>

    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="120px"
      class="password-form"
    >
      <el-form-item label="原密码" prop="oldPassword">
        <el-input 
          v-model="formData.oldPassword"
          type="password"
          placeholder="请输入原密码"
          show-password
          clearable
        >
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="新密码" prop="newPassword">
        <el-input 
          v-model="formData.newPassword"
          type="password"
          placeholder="请输入新密码"
          show-password
          clearable
        >
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
        </el-input>
        <!-- 密码强度指示器 -->
        <div v-if="formData.newPassword" class="password-strength">
          <span class="strength-label">密码强度：</span>
          <div class="strength-bar">
            <div 
              class="strength-level"
              :class="passwordStrengthClass"
              :style="{ width: passwordStrengthWidth }"
            ></div>
          </div>
          <span 
            class="strength-text"
            :style="{ color: passwordStrengthColor }"
          >
            {{ passwordStrengthText }}
          </span>
        </div>
      </el-form-item>

      <el-form-item label="确认新密码" prop="confirmPassword">
        <el-input 
          v-model="formData.confirmPassword"
          type="password"
          placeholder="请再次输入新密码"
          show-password
          clearable
        >
          <template #prefix>
            <el-icon><Lock /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item>
        <el-button 
          type="primary"
          :loading="saveLoading"
          @click="handleSubmit"
        >
          提交修改
        </el-button>
        <el-button @click="handleReset">
          重置
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'

// ==================== Props ====================
const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

// ==================== Emits ====================
const emit = defineEmits(['change-password'])

// ==================== 响应式数据 ====================
const formRef = ref(null)
const saveLoading = ref(false)

const formData = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

// ==================== 表单验证规则 ====================

/**
 * 验证原密码不为空
 */
const validateOldPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入原密码'))
  } else {
    callback()
  }
}

/**
 * 验证新密码强度
 * 要求：至少8位，包含大小写字母和数字
 */
const validateNewPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入新密码'))
  } else if (value.length < 8) {
    callback(new Error('密码长度至少8位'))
  } else if (!/[a-z]/.test(value)) {
    callback(new Error('密码必须包含小写字母'))
  } else if (!/[A-Z]/.test(value)) {
    callback(new Error('密码必须包含大写字母'))
  } else if (!/\d/.test(value)) {
    callback(new Error('密码必须包含数字'))
  } else if (value === formData.oldPassword) {
    callback(new Error('新密码不能与原密码相同'))
  } else {
    // 如果确认密码已填写，触发确认密码验证
    if (formData.confirmPassword) {
      formRef.value.validateField('confirmPassword')
    }
    callback()
  }
}

/**
 * 验证确认密码
 */
const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请再次输入新密码'))
  } else if (value !== formData.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const formRules = {
  oldPassword: [
    { required: true, validator: validateOldPassword, trigger: 'blur' }
  ],
  newPassword: [
    { required: true, validator: validateNewPassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

// ==================== 密码强度计算 ====================

/**
 * 计算密码强度
 * @returns {number} 0-4 表示弱-强
 */
const calculatePasswordStrength = (password) => {
  if (!password) return 0
  
  let strength = 0
  
  // 长度检查
  if (password.length >= 8) strength++
  if (password.length >= 12) strength++
  
  // 复杂度检查
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++
  if (/\d/.test(password)) strength++
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++
  
  return Math.min(strength, 4)
}

/**
 * 密码强度等级
 */
const passwordStrength = computed(() => {
  return calculatePasswordStrength(formData.newPassword)
})

/**
 * 密码强度文本
 */
const passwordStrengthText = computed(() => {
  const texts = ['很弱', '弱', '一般', '强', '很强']
  return texts[passwordStrength.value] || ''
})

/**
 * 密码强度颜色
 */
const passwordStrengthColor = computed(() => {
  const colors = ['#f56c6c', '#e6a23c', '#e6a23c', '#67c23a', '#67c23a']
  return colors[passwordStrength.value] || '#909399'
})

/**
 * 密码强度宽度
 */
const passwordStrengthWidth = computed(() => {
  return `${(passwordStrength.value / 4) * 100}%`
})

/**
 * 密码强度样式类
 */
const passwordStrengthClass = computed(() => {
  const classes = ['weak', 'weak', 'medium', 'strong', 'strong']
  return classes[passwordStrength.value] || ''
})

// ==================== 方法 ====================

/**
 * 提交密码修改
 */
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    // 表单验证
    await formRef.value.validate()
    
    // 检查密码强度是否足够
    if (passwordStrength.value < 2) {
      ElMessage.warning('密码强度太弱，请设置更复杂的密码')
      return
    }
    
    saveLoading.value = true
    
    // 准备提交数据
    const submitData = {
      oldPassword: formData.oldPassword,
      newPassword: formData.newPassword,
      confirmPassword: formData.confirmPassword
    }
    
    // 触发父组件事件
    emit('change-password', submitData)
    
    // 重置表单并关闭loading
    handleReset()
    saveLoading.value = false
  } catch (error) {
    console.error('Form validation failed:', error)
    ElMessage.warning('请检查表单填写是否正确')
    saveLoading.value = false
  }
}

/**
 * 重置表单
 */
const handleReset = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
  formData.oldPassword = ''
  formData.newPassword = ''
  formData.confirmPassword = ''
}
</script>

<style scoped>
.security-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.security-alert {
  margin-bottom: 30px;
}

.security-alert p {
  margin: 5px 0;
  font-size: 14px;
}

.password-form {
  max-width: 600px;
  margin: 0 auto;
}

.password-strength {
  display: flex;
  align-items: center;
  margin-top: 8px;
  font-size: 12px;
}

.strength-label {
  color: #606266;
  margin-right: 8px;
}

.strength-bar {
  flex: 1;
  height: 6px;
  background-color: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-right: 8px;
}

.strength-level {
  height: 100%;
  transition: all 0.3s ease;
}

.strength-level.weak {
  background-color: #f56c6c;
}

.strength-level.medium {
  background-color: #e6a23c;
}

.strength-level.strong {
  background-color: #67c23a;
}

.strength-text {
  font-weight: 500;
}
</style>
