<template>
  <el-card class="personalization-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>{{ $t('personalization.cardTitle') }}</span>
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
        {{ $t('personalization.themeSection') }}
      </el-divider>

      <el-form-item :label="$t('personalization.themeMode')">
        <el-radio-group v-model="formData.theme">
          <el-radio value="light">
            <el-icon><Sunny /></el-icon>
            {{ $t('personalization.themeLight') }}
          </el-radio>
          <el-radio value="dark">
            <el-icon><Moon /></el-icon>
            {{ $t('personalization.themeDark') }}
          </el-radio>
          <el-radio value="auto">
            <el-icon><Monitor /></el-icon>
            {{ $t('personalization.themeAuto') }}
          </el-radio>
        </el-radio-group>
        <div class="form-tip">{{ $t('personalization.themeTip') }}</div>
      </el-form-item>

      <!-- 语言设置 -->
      <el-divider content-position="left">
        <el-icon><Reading /></el-icon>
        {{ $t('personalization.languageSection') }}
      </el-divider>

      <el-form-item :label="$t('personalization.displayLanguage')">
        <el-select 
          v-model="formData.language" 
          :placeholder="$t('personalization.languagePlaceholder')"
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
        <div class="form-tip">{{ $t('personalization.languageTip') }}</div>
      </el-form-item>

      <!-- 通知设置 -->
      <el-divider content-position="left">
        <el-icon><Bell /></el-icon>
        {{ $t('personalization.notificationSection') }}
      </el-divider>

      <el-form-item :label="$t('personalization.emailNotification')">
        <el-switch 
          v-model="formData.emailNotification"
          :active-text="$t('personalization.on')"
          :inactive-text="$t('personalization.off')"
        />
        <div class="form-tip">
          {{ $t('personalization.emailTip') }}
          <el-tag type="info" size="small" style="margin-left: 8px">{{ $t('personalization.emailPending') }}</el-tag>
        </div>
      </el-form-item>

      <el-form-item :label="$t('personalization.systemNotification')">
        <el-switch 
          v-model="formData.systemNotification"
          :active-text="$t('personalization.on')"
          :inactive-text="$t('personalization.off')"
        />
        <div class="form-tip">{{ $t('personalization.systemTip') }}</div>
      </el-form-item>

      <!-- 操作按钮区域 - 底部右对齐 -->
      <el-form-item class="form-actions">
        <div class="actions-wrapper">
          <el-button @click="handleReset">
            {{ $t('personalization.reset') }}
          </el-button>
          <el-button 
            type="primary"
            :loading="saveLoading"
            :disabled="!hasChanges"
            @click="handleSave"
          >
            {{ $t('personalization.save') }}
          </el-button>
        </div>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { Picture, Sunny, Moon, Monitor, Reading, Bell } from '@element-plus/icons-vue'
import { useThemeStore } from '@/stores/themeStore'

const themeStore = useThemeStore()

const { t, locale } = useI18n()

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

// 表单数据（已移除 smsNotification）
const formData = reactive({
  theme: 'light',
  language: 'zh-CN',
  emailNotification: true,
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
    formData.systemNotification !== originalData.value.systemNotification
  )
})

// ==================== 监听 preferences 变化 ====================
watch(() => props.preferences, (newVal) => {
  if (newVal) {
    const data = {
      theme: newVal.theme || localStorage.getItem('app_theme') || 'light',
      language: newVal.language || localStorage.getItem('app_language') || 'zh-CN',
      emailNotification: newVal.emailNotification !== undefined ? newVal.emailNotification : true,
      systemNotification: newVal.systemNotification !== undefined ? newVal.systemNotification : true
    }
    Object.assign(formData, data)
    // 保存原始数据快照
    originalData.value = { ...data }
  }
}, { immediate: true, deep: true })

// 实时预览主题（选择即生效）
watch(() => formData.theme, (newTheme) => {
  themeStore.applyTheme(newTheme)
})

// ==================== 方法 ====================

/**
 * 保存个性化设置
 */
const handleSave = async () => {
  saveLoading.value = true
  
  try {
    const submitData = {
      theme: formData.theme,
      language: formData.language,
      emailNotification: formData.emailNotification,
      systemNotification: formData.systemNotification
    }

    // 立即应用主题
    localStorage.setItem('app_theme', submitData.theme)
    themeStore.applyTheme(submitData.theme)

    // 立即切换语言
    localStorage.setItem('app_language', submitData.language)
    locale.value = submitData.language

    // 触发父组件更新事件（保存到后端）
    emit('update', submitData)
    
    // 更新原始数据快照
    originalData.value = { ...submitData }
    saveLoading.value = false

    ElMessage.success(t('personalization.saveSuccess'))
  } catch (error) {
    console.error('Save preferences error:', error)
    ElMessage.error(t('personalization.saveError'))
    saveLoading.value = false
  }
}

/**
 * 重置为初始值
 */
const handleReset = () => {
  if (props.preferences) {
    Object.assign(formData, {
      theme: props.preferences.theme || localStorage.getItem('app_theme') || 'light',
      language: props.preferences.language || localStorage.getItem('app_language') || 'zh-CN',
      emailNotification: props.preferences.emailNotification !== undefined ? props.preferences.emailNotification : true,
      systemNotification: props.preferences.systemNotification !== undefined ? props.preferences.systemNotification : true
    })
  }
  ElMessage.info(t('personalization.resetSuccess'))
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
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
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
