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
          <el-option label="紧急" value="urgent" />
          <el-option label="高" value="high" />
          <el-option label="中" value="medium" />
          <el-option label="低" value="low" />
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

      <el-form-item label="截止日期" prop="due_date">
        <el-date-picker
          v-model="formData.due_date"
          type="date"
          placeholder="请选择截止日期"
          style="width: 100%"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <el-form-item label="处理人" prop="assignee_id">
        <el-select
          v-model="formData.assignee_id"
          placeholder="请选择处理人（可选）"
          clearable
          style="width: 100%"
        >
          <el-option
            v-for="user in userList"
            :key="user.id"
            :label="user.nickname ? `${user.nickname} (${user.username})` : user.username"
            :value="user.id"
          />
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
import { ref, watch, onMounted } from 'vue'
import { getStaffList } from '@/api/index.js'

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
const userList = ref([])

onMounted(async () => {
  try {
    const res = await getStaffList()
    if (res && res.data && res.data.staff) {
      userList.value = res.data.staff
    }
  } catch (e) {
    console.error('获取用户列表失败', e)
  }
})

const formData = ref({
  title: '',
  description: '',
  category: '',
  priority: 'medium',
  status: 'open',
  assignee_id: null,
  due_date: ''
})

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
    { required: true, message: '请选择优先级', trigger: 'change' }
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
        assignee_id: props.ticket.assignee_id || null,
        due_date: props.ticket.due_date || ''
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
    assignee_id: null,
    due_date: ''
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
