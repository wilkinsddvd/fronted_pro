<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑工单' : '新建工单'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="标题" prop="title">
        <el-input
          v-model="formData.title"
          placeholder="请输入工单标题"
          maxlength="100"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="formData.description"
          type="textarea"
          :rows="4"
          placeholder="请输入工单描述"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="分类" prop="category">
        <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
          <el-option label="技术支持" value="technical" />
          <el-option label="售后服务" value="after_sales" />
          <el-option label="产品咨询" value="product" />
          <el-option label="其他" value="other" />
        </el-select>
      </el-form-item>

      <el-form-item label="优先级" prop="priority">
        <el-select v-model="formData.priority" placeholder="请选择优先级" style="width: 100%">
          <el-option label="低" value="low" />
          <el-option label="中" value="medium" />
          <el-option label="高" value="high" />
        </el-select>
      </el-form-item>

      <el-form-item label="状态" prop="status" v-if="isEdit">
        <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
          <el-option label="新建" value="open" />
          <el-option label="处理中" value="in_progress" />
          <el-option label="已解决" value="resolved" />
          <el-option label="已关闭" value="closed" />
        </el-select>
      </el-form-item>

      <el-form-item label="处理人" prop="assignee" v-if="isEdit">
        <el-input
          v-model="formData.assignee"
          placeholder="请输入处理人"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  ticket: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'submit'])

const formRef = ref(null)
const dialogVisible = ref(false)
const submitting = ref(false)
const isEdit = ref(false)

const formData = ref({
  title: '',
  description: '',
  category: '',
  priority: 'medium',
  status: 'open',
  assignee: ''
})

const ALLOWED_STATUSES = ['open', 'in_progress', 'resolved', 'closed']

const rules = {
  title: [
    { required: true, message: '请输入工单标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入工单描述', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  priority: [
    { required: true, message: '请选择优先级', trigger: 'change' },
    {
      validator: (rule, value, callback) => {
        if (!['low', 'medium', 'high'].includes(value)) {
          callback(new Error('优先级值无效'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ],
  status: [
    {
      validator: (rule, value, callback) => {
        if (value && !ALLOWED_STATUSES.includes(value)) {
          callback(new Error('状态值无效'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

watch(() => props.visible, (val) => {
  dialogVisible.value = val
  if (val) {
    isEdit.value = !!props.ticket
    if (props.ticket) {
      formData.value = {
        title: props.ticket.title || '',
        description: props.ticket.description || '',
        category: props.ticket.category || '',
        priority: props.ticket.priority || 'medium',
        status: props.ticket.status || 'open',
        assignee: props.ticket.assignee || ''
      }
    } else {
      resetForm()
    }
  }
})

watch(dialogVisible, (val) => {
  emit('update:visible', val)
})

const handleClose = () => {
  dialogVisible.value = false
  resetForm()
}

const resetForm = () => {
  formData.value = {
    title: '',
    description: '',
    category: '',
    priority: 'medium',
    status: 'open',
    assignee: ''
  }
  formRef.value?.clearValidate()
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await emit('submit', {
      id: props.ticket?.id,
      ...formData.value
    })
    handleClose()
  } finally {
    submitting.value = false
  }
}
</script>
