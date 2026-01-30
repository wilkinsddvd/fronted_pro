<template>
  <el-card class="privacy-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <span>隐私设置</span>
        <el-tag type="warning" size="small">敏感操作</el-tag>
      </div>
    </template>

    <el-alert
      title="隐私保护提示"
      type="info"
      :closable="false"
      show-icon
      class="privacy-alert"
    >
      合理设置您的隐私选项，保护个人信息安全
    </el-alert>

    <el-form
      ref="formRef"
      :model="formData"
      label-width="140px"
      class="privacy-form"
    >
      <!-- 账户可见性 -->
      <el-divider content-position="left">
        <el-icon><View /></el-icon>
        账户可见性
      </el-divider>

      <el-form-item label="个人资料公开">
        <el-switch 
          v-model="formData.profilePublic"
          active-text="公开"
          inactive-text="私密"
        />
        <div class="form-tip">设置为私密后，其他用户将无法查看您的个人资料</div>
      </el-form-item>

      <el-form-item label="允许被搜索">
        <el-switch 
          v-model="formData.allowSearch"
          active-text="允许"
          inactive-text="禁止"
        />
        <div class="form-tip">关闭后，其他用户无法通过搜索功能找到您</div>
      </el-form-item>

      <!-- 联系方式可见性 -->
      <el-divider content-position="left">
        <el-icon><Hide /></el-icon>
        联系方式可见性
      </el-divider>

      <el-form-item label="显示邮箱地址">
        <el-switch 
          v-model="formData.showEmail"
          active-text="显示"
          inactive-text="隐藏"
        />
        <div class="form-tip">
          <span v-if="formData.showEmail" style="color: #e6a23c">
            <el-icon><Warning /></el-icon>
            您的邮箱将对其他用户可见
          </span>
          <span v-else style="color: #67c23a">
            <el-icon><CircleCheck /></el-icon>
            您的邮箱已隐藏，仅自己可见
          </span>
        </div>
      </el-form-item>

      <el-form-item label="显示手机号码">
        <el-switch 
          v-model="formData.showPhone"
          active-text="显示"
          inactive-text="隐藏"
        />
        <div class="form-tip">
          <span v-if="formData.showPhone" style="color: #e6a23c">
            <el-icon><Warning /></el-icon>
            您的手机号将对其他用户可见
          </span>
          <span v-else style="color: #67c23a">
            <el-icon><CircleCheck /></el-icon>
            您的手机号已隐藏，仅自己可见
          </span>
        </div>
      </el-form-item>

      <!-- 数据与隐私 -->
      <el-divider content-position="left">
        <el-icon><Lock /></el-icon>
        数据与隐私
      </el-divider>

      <el-form-item>
        <div class="privacy-info">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="数据收集">
              我们仅收集必要的用户信息用于提供服务
            </el-descriptions-item>
            <el-descriptions-item label="数据使用">
              您的数据不会被用于任何未经授权的商业用途
            </el-descriptions-item>
            <el-descriptions-item label="数据安全">
              我们采用行业标准的安全措施保护您的数据
            </el-descriptions-item>
          </el-descriptions>
        </div>
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
import { View, Hide, Lock, Warning, CircleCheck } from '@element-plus/icons-vue'

// ==================== Props ====================
const props = defineProps({
  privacy: {
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
  profilePublic: true,
  showEmail: false,
  showPhone: false,
  allowSearch: true
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
    formData.profilePublic !== originalData.value.profilePublic ||
    formData.showEmail !== originalData.value.showEmail ||
    formData.showPhone !== originalData.value.showPhone ||
    formData.allowSearch !== originalData.value.allowSearch
  )
})

// ==================== 监听 privacy 变化 ====================
watch(() => props.privacy, (newVal) => {
  if (newVal) {
    const data = {
      profilePublic: newVal.profilePublic !== undefined ? newVal.profilePublic : true,
      showEmail: newVal.showEmail !== undefined ? newVal.showEmail : false,
      showPhone: newVal.showPhone !== undefined ? newVal.showPhone : false,
      allowSearch: newVal.allowSearch !== undefined ? newVal.allowSearch : true
    }
    Object.assign(formData, data)
    // 保存原始数据快照
    originalData.value = { ...data }
  }
}, { immediate: true, deep: true })

// ==================== 方法 ====================

/**
 * 保存隐私设置
 */
const handleSave = async () => {
  saveLoading.value = true
  
  try {
    // 准备提交数据
    const submitData = {
      profilePublic: formData.profilePublic,
      showEmail: formData.showEmail,
      showPhone: formData.showPhone,
      allowSearch: formData.allowSearch
    }
    
    // 触发父组件更新事件
    emit('update', submitData)
    
    // 更新原始数据快照
    originalData.value = { ...submitData }
    
    // 父组件会控制全局loading，这里立即关闭本地loading
    saveLoading.value = false
  } catch (error) {
    console.error('Save privacy error:', error)
    ElMessage.error('保存失败，请重试')
    saveLoading.value = false
  }
}

/**
 * 重置为初始值
 */
const handleReset = () => {
  if (props.privacy) {
    Object.assign(formData, {
      profilePublic: props.privacy.profilePublic !== undefined ? props.privacy.profilePublic : true,
      showEmail: props.privacy.showEmail !== undefined ? props.privacy.showEmail : false,
      showPhone: props.privacy.showPhone !== undefined ? props.privacy.showPhone : false,
      allowSearch: props.privacy.allowSearch !== undefined ? props.privacy.allowSearch : true
    })
  }
  ElMessage.info('已重置为当前保存的设置')
}
</script>

<style scoped>
.privacy-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.privacy-alert {
  margin-bottom: 30px;
}

.privacy-form {
  max-width: 600px;
  margin: 0 auto;
}

.privacy-form :deep(.el-divider) {
  margin: 30px 0 20px;
}

.privacy-form :deep(.el-divider__text) {
  font-size: 15px;
  font-weight: 500;
  color: #303133;
}

.form-tip {
  margin-top: 5px;
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
}

.form-tip .el-icon {
  vertical-align: middle;
  margin-right: 3px;
}

.privacy-info {
  width: 100%;
}

.privacy-info :deep(.el-descriptions__cell) {
  font-size: 13px;
}

.privacy-form :deep(.el-form-item__content) {
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
