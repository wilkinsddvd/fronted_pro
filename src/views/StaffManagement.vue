<template>
  <div class="staff-management">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>后勤人员管理</span>
          <el-button type="primary" @click="handleCreate">新增后勤人员</el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索用户名或昵称"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button :icon="Search" @click="handleSearch" />
            </template>
          </el-input>
        </el-col>
      </el-row>

      <!-- 后勤人员表格 -->
      <el-table :data="staffList" v-loading="loading" stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="nickname" label="昵称" min-width="120">
          <template #default="{ row }">
            {{ row.nickname || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号" min-width="140">
          <template #default="{ row }">
            {{ row.phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="120" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑后勤人员' : '新增后勤人员'"
      width="500px"
      @close="resetForm"
    >
      <el-form ref="formRef" :model="formData" :rules="formRules" label-width="90px">
        <!-- 新增时显示用户名和密码 -->
        <template v-if="!isEdit">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="formData.username" placeholder="3-32位，字母数字下划线" maxlength="32" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="formData.password" type="password" placeholder="至少8位，含字母和数字" show-password />
          </el-form-item>
        </template>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="formData.nickname" placeholder="真实姓名（可选）" maxlength="64" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="手机号（可选）" maxlength="32" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getStaff, createStaff, updateStaff, deleteStaff } from '@/api/index.js'

const staffList = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')

const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const currentStaff = ref(null)
const formRef = ref(null)

const formData = ref({
  username: '',
  password: '',
  nickname: '',
  phone: ''
})

const formRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 32, message: '用户名长度在3-32字符之间', trigger: 'blur' },
    { pattern: /^[A-Za-z0-9_]+$/, message: '只允许字母、数字和下划线', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少8位', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (!/[A-Za-z]/.test(value) || !/\d/.test(value)) {
          callback(new Error('密码需同时包含字母和数字'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const fetchStaff = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value, size: pageSize.value }
    if (searchQuery.value) params.search = searchQuery.value
    const res = await getStaff(params)
    if (res && res.data) {
      staffList.value = res.data.staff || []
      total.value = res.data.total || 0
    }
  } catch (e) {
    ElMessage.error('获取后勤人员列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchStaff()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchStaff()
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  fetchStaff()
}

const handleCreate = () => {
  isEdit.value = false
  currentStaff.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row) => {
  isEdit.value = true
  currentStaff.value = row
  formData.value = {
    username: row.username,
    password: '',
    nickname: row.nickname || '',
    phone: row.phone || ''
  }
  dialogVisible.value = true
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确认取消 "${row.username}" 的后勤人员权限吗？该账号将保留但不再是后勤人员。`,
      '提示',
      { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' }
    )
    await deleteStaff(row.id)
    ElMessage.success('已取消后勤人员权限')
    fetchStaff()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error(`操作失败: ${e.message || ''}`)
  }
}

const handleSubmit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateStaff(currentStaff.value.id, {
        nickname: formData.value.nickname,
        phone: formData.value.phone
      })
      ElMessage.success('更新成功')
    } else {
      await createStaff(formData.value)
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    fetchStaff()
  } catch (e) {
    ElMessage.error(`${isEdit.value ? '更新' : '新增'}失败: ${e.message || ''}`)
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  formData.value = { username: '', password: '', nickname: '', phone: '' }
  formRef.value?.clearValidate()
}

onMounted(() => {
  fetchStaff()
})
</script>

<style scoped>
.staff-management {
  animation: fadeIn 0.3s ease-in;
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
