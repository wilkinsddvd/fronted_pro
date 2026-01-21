<template>
  <el-card class="info-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>基本信息</span>
        <el-button 
          type="primary" 
          :loading="saveLoading"
          @click="handleSave"
        >
          保存修改
        </el-button>
      </div>
    </template>

    <!-- 头像上传区域 -->
    <div class="avatar-section">
      <div class="avatar-upload">
        <el-avatar 
          :size="120" 
          :src="formData.avatar || defaultAvatar"
          class="avatar-preview"
        />
        <el-upload
          class="upload-btn"
          :auto-upload="false"
          :show-file-list="false"
          :on-change="handleAvatarChange"
          accept="image/*"
        >
          <el-button type="primary" size="small">
            <el-icon><Upload /></el-icon>
            更换头像
          </el-button>
        </el-upload>
        <p class="upload-tip">支持 JPG、PNG 格式，文件大小不超过 2MB</p>
      </div>
    </div>

    <!-- 基本信息表单 -->
    <el-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      class="info-form"
    >
      <el-form-item label="用户名">
        <el-input 
          v-model="formData.username" 
          disabled
          placeholder="用户名不可修改"
        />
      </el-form-item>

      <el-form-item label="昵称" prop="nickname">
        <el-input 
          v-model="formData.nickname" 
          placeholder="请输入昵称"
          clearable
        />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input 
          v-model="formData.email" 
          placeholder="请输入邮箱"
          clearable
        >
          <template #prefix>
            <el-icon><Message /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="手机号" prop="phone">
        <el-input 
          v-model="formData.phone" 
          placeholder="请输入手机号"
          clearable
        >
          <template #prefix>
            <el-icon><Phone /></el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="个人简介" prop="bio">
        <el-input 
          v-model="formData.bio"
          type="textarea"
          :rows="4"
          placeholder="请输入个人简介"
          maxlength="200"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="注册时间">
        <el-input 
          v-model="formData.createdAt" 
          disabled
        />
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Upload, Message, Phone } from '@element-plus/icons-vue'

// ==================== Props ====================
const props = defineProps({
  userInfo: {
    type: Object,
    required: true,
    default: () => ({})
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// ==================== Emits ====================
const emit = defineEmits(['update'])

// ==================== 响应式数据 ====================
const formRef = ref(null) // 表单引用
const saveLoading = ref(false) // 保存按钮加载状态
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

// 表单数据
const formData = reactive({
  username: '',
  nickname: '',
  email: '',
  phone: '',
  avatar: '',
  bio: '',
  createdAt: ''
})

// ==================== 表单验证规则 ====================
const formRules = {
  nickname: [
    { required: true, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { 
      type: 'email', 
      message: '请输入正确的邮箱地址', 
      trigger: ['blur', 'change'] 
    }
  ],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { 
      pattern: /^1[3-9]\d{9}$/, 
      message: '请输入正确的手机号码', 
      trigger: ['blur', 'change'] 
    }
  ],
  bio: [
    { max: 200, message: '个人简介不能超过200个字符', trigger: 'blur' }
  ]
}

// ==================== 监听 userInfo 变化 ====================
watch(() => props.userInfo, (newVal) => {
  if (newVal) {
    Object.assign(formData, {
      username: newVal.username || '',
      nickname: newVal.nickname || '',
      email: newVal.email || '',
      phone: newVal.phone || '',
      avatar: newVal.avatar || '',
      bio: newVal.bio || '',
      createdAt: newVal.createdAt || ''
    })
  }
}, { immediate: true, deep: true })

// ==================== 方法 ====================
/**
 * 处理头像文件变更
 * 实现本地预览功能
 * @param {Object} file - 上传的文件对象
 */
const handleAvatarChange = (file) => {
  const rawFile = file.raw
  
  // 验证文件类型
  const isImage = rawFile.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return
  }
  
  // 验证文件大小（2MB）
  const isLt2M = rawFile.size / 1024 / 1024 < 2
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return
  }
  
  // 本地预览：使用 FileReader 读取文件并转换为 base64
  const reader = new FileReader()
  reader.onload = (e) => {
    formData.avatar = e.target.result
    ElMessage.success('头像已更新，请点击保存按钮')
  }
  reader.readAsDataURL(rawFile)
}

/**
 * 保存基本信息
 * 先进行表单验证，通过后触发更新事件
 */
const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    // 表单验证
    await formRef.value.validate()
    
    saveLoading.value = true
    
    // 准备要提交的数据
    const submitData = {
      nickname: formData.nickname,
      email: formData.email,
      phone: formData.phone,
      avatar: formData.avatar,
      bio: formData.bio
    }
    
    // 触发更新事件，由父组件处理实际的API调用
    emit('update', submitData)
    
    // 延迟关闭加载状态（父组件会控制全局loading）
    setTimeout(() => {
      saveLoading.value = false
    }, 500)
  } catch (error) {
    console.error('Form validation failed:', error)
    ElMessage.warning('请检查表单填写是否正确')
    saveLoading.value = false
  }
}
</script>

<style scoped>
.info-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 1px solid #ebeef5;
}

.avatar-upload {
  text-align: center;
}

.avatar-preview {
  display: block;
  margin: 0 auto 15px;
  border: 2px solid #dcdfe6;
  transition: all 0.3s;
}

.avatar-preview:hover {
  border-color: #409eff;
}

.upload-btn {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}

.upload-tip {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

.info-form {
  max-width: 600px;
  margin: 0 auto;
}

.info-form :deep(.el-form-item__label) {
  font-weight: 500;
}
</style>
