<template>
  <el-card class="personalization-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>个性化设置</span>
      </div>
    </template>

    <el-form
      ref="formRef"
      :model="formData"
      label-width="120px"
      class="personalization-form"
    >
      <!-- 主题设置 -->
      <el-divider content-position="left">
        <el-icon><Picture /></el-icon>
        界面主题
      </el-divider>

      <el-form-item label="主题模式">
        <el-radio-group v-model="formData.theme">
          <el-radio label="light">
            <el-icon><Sunny /></el-icon>
            浅色模式
          </el-radio>
          <el-radio label="dark">
            <el-icon><Moon /></el-icon>
            深色模式
          </el-radio>
          <el-radio label="auto">
            <el-icon><Monitor /></el-icon>
            跟随系统
          </el-radio>
        </el-radio-group>
        <div class="form-tip">选择您喜欢的界面主题</div>
      </el-form-item>

      <!-- 语言设置 -->
      <el-divider content-position="left">
        <el-icon><Reading /></el-icon>
        语言偏好
      </el-divider>

      <el-form-item label="显示语言">
        <el-select 
          v-model="formData.language" 
          placeholder="请选择语言"
          style="width: 200px"
        >
          <el-option label="简体中文" value="zh-CN">
            <span style="float: left">简体中文</span>
            <span style="float: right; color: #8492a6; font-size: 13px">zh-CN</span>
          </el-option>
          <el-option label="English" value="en-US">
            <span style="float: left">English</span>
            <span style="float: right; color: #8492a6; font-size: 13px">en-US</span>
          </el-option>
        </el-select>
        <div class="form-tip">选择界面显示语言</div>
      </el-form-item>

      <!-- 通知设置 -->
      <el-divider content-position="left">
        <el-icon><Bell /></el-icon>
        通知设置
      </el-divider>

      <el-form-item label="邮件通知">
        <el-switch 
          v-model="formData.emailNotification"
          active-text="开启"
          inactive-text="关闭"
        />
        <div class="form-tip">接收重要事件的邮件通知</div>
      </el-form-item>

      <el-form-item label="短信通知">
        <el-switch 
          v-model="formData.smsNotification"
          active-text="开启"
          inactive-text="关闭"
        />
        <div class="form-tip">接收重要事件的短信通知</div>
      </el-form-item>

      <el-form-item label="系统通知">
        <el-switch 
          v-model="formData.systemNotification"
          active-text="开启"
          inactive-text="关闭"
        />
        <div class="form-tip">在系统内显示通知消息</div>
      </el-form-item>

      <!-- 操作按钮区域 - 底部右对齐 -->
      <el-form-item class="form-actions">
        <div class="actions-wrapper">
          <el-button @click="handleReset">
            重置
          </el-button>
          <el-button 
            type="primary"
            :loading="saveLoading"
            :disabled="!hasChanges"
            @click="handleSave"
          >
            保存设置
          </el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Picture, Sunny, Moon, Monitor, Reading, Bell } from '@element-plus/icons-vue'

// ==================== Props ====================
const props = defineProps({
  preferences: {
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
const formRef = ref(null)
const saveLoading = ref(false)

// 表单数据
const formData = reactive({
  theme: 'light',
  language: 'zh-CN',
  emailNotification: true,
  smsNotification: false,
  systemNotification: true
})

// 原始数据快照，用于检测变更
const originalData = ref({})

// ==================== 计算属性 ====================

/**
 * 检查表单数据是否有变更
 * 用于控制保存按钮的禁用状态
 */
const hasChanges = computed(() => {
  if (!originalData.value || Object.keys(originalData.value).length === 0) {
    return false
  }
  
  return (
    formData.theme !== originalData.value.theme ||
    formData.language !== originalData.value.language ||
    formData.emailNotification !== originalData.value.emailNotification ||
    formData.smsNotification !== originalData.value.smsNotification ||
    formData.systemNotification !== originalData.value.systemNotification
  )
})

// ==================== 监听 preferences 变化 ====================
watch(() => props.preferences, (newVal) => {
  if (newVal) {
    const data = {
      theme: newVal.theme || 'light',
      language: newVal.language || 'zh-CN',
      emailNotification: newVal.emailNotification !== undefined ? newVal.emailNotification : true,
      smsNotification: newVal.smsNotification !== undefined ? newVal.smsNotification : false,
      systemNotification: newVal.systemNotification !== undefined ? newVal.systemNotification : true
    }
    Object.assign(formData, data)
    // 保存原始数据快照
    originalData.value = { ...data }
  }
}, { immediate: true, deep: true })

// ==================== 方法 ====================

/**
 * 保存个性化设置
 */
const handleSave = async () => {
  saveLoading.value = true
  
  try {
    // 准备提交数据
    const submitData = {
      theme: formData.theme,
      language: formData.language,
      emailNotification: formData.emailNotification,
      smsNotification: formData.smsNotification,
      systemNotification: formData.systemNotification
    }
    
    // 触发父组件更新事件
    emit('update', submitData)
    
    // 更新原始数据快照
    originalData.value = { ...submitData }
    
    // 父组件会控制全局loading，这里立即关闭本地loading
    saveLoading.value = false
  } catch (error) {
    console.error('Save preferences error:', error)
    ElMessage.error('保存失败，请重试')
    saveLoading.value = false
  }
}

/**
 * 重置为初始值
 */
const handleReset = () => {
  if (props.preferences) {
    Object.assign(formData, {
      theme: props.preferences.theme || 'light',
      language: props.preferences.language || 'zh-CN',
      emailNotification: props.preferences.emailNotification !== undefined ? props.preferences.emailNotification : true,
      smsNotification: props.preferences.smsNotification !== undefined ? props.preferences.smsNotification : false,
      systemNotification: props.preferences.systemNotification !== undefined ? props.preferences.systemNotification : true
    })
  }
  ElMessage.info('已重置为当前保存的设置')
}
</script>

<style scoped>
.personalization-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.personalization-form {
  max-width: 600px;
  margin: 0 auto;
}

.personalization-form :deep(.el-divider) {
  margin: 30px 0 20px;
}

.personalization-form :deep(.el-divider__text) {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.personalization-form :deep(.el-radio) {
  margin-right: 30px;
}

.form-tip {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.personalization-form :deep(.el-form-item__content) {
  flex-direction: column;
  align-items: flex-start;
}

/* 操作按钮区域样式 */
.form-actions {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.form-actions :deep(.el-form-item__content) {
  flex-direction: row;
  align-items: center;
  justify-content: flex-end;
  width: 100%;
}

.actions-wrapper {
  display: flex;
  gap: 12px;
}
</style>
