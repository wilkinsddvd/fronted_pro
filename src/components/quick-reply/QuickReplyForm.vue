<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑快速回复' : '新建快速回复'"
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
          placeholder="请输入快速回复标题"
          maxlength="50"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="内容" prop="content">
        <el-input
          v-model="formData.content"
          type="textarea"
          :rows="6"
          placeholder="请输入快速回复内容"
          maxlength="1000"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="分类" prop="category">
        <el-select v-model="formData.category" placeholder="请选择分类" style="width: 100%">
          <el-option label="常见问题" value="faq" />
          <el-option label="技术支持" value="technical" />
          <el-option label="售后服务" value="after_sales" />
          <el-option label="其他" value="other" />
        </el-select>
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
  reply: {
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
  content: '',
  category: ''
})

const rules = {
  title: [
    { required: true, message: '请输入快速回复标题', trigger: 'blur' },
    { min: 2, max: 50, message: '标题长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入快速回复内容', trigger: 'blur' },
    { min: 2, max: 1000, message: '内容长度在 2 到 1000 个字符', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ]
}

watch(() => props.visible, (val) => {
  dialogVisible.value = val
  if (val) {
    isEdit.value = !!props.reply
    if (props.reply) {
      formData.value = {
        title: props.reply.title || '',
        content: props.reply.content || '',
        category: props.reply.category || ''
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
    content: '',
    category: ''
  }
  formRef.value?.clearValidate()
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await emit('submit', {
      id: props.reply?.id,
      ...formData.value
    })
    handleClose()
  } finally {
    submitting.value = false
  }
}
</script>
