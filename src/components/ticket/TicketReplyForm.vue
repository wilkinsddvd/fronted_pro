<template>
  <div class="ticket-reply-form">
    <el-input
      v-model="content"
      type="textarea"
      :rows="4"
      placeholder="请输入回复内容..."
      maxlength="2000"
      show-word-limit
    />
    <div class="form-toolbar">
      <div class="toolbar-left">
        <el-select
          v-if="quickReplies && quickReplies.length > 0"
          v-model="selectedQuickReplyId"
          placeholder="插入快速回复模板"
          clearable
          style="width: 200px;"
          @change="handleQuickReplySelect"
        >
          <el-option
            v-for="item in quickReplies"
            :key="item.id"
            :label="item.title"
            :value="item.id"
          />
        </el-select>
      </div>
      <div class="toolbar-right">
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          发表回复
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  ticketId: {
    type: Number,
    required: true
  },
  quickReplies: {
    type: Array,
    default: () => []
  },
  submitting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['submit'])

const content = ref('')
const selectedQuickReplyId = ref(null)

const handleQuickReplySelect = (id) => {
  if (!id) return
  const selected = props.quickReplies.find(item => item.id === id)
  if (selected && selected.content) {
    content.value = content.value ? content.value + '\n' + selected.content : selected.content
  }
}

const handleSubmit = () => {
  if (!content.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }
  emit('submit', { content: content.value, quick_reply_id: selectedQuickReplyId.value })
}

const resetForm = () => {
  content.value = ''
  selectedQuickReplyId.value = null
}

defineExpose({ resetForm })
</script>

<style scoped>
.form-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.toolbar-left {
  display: flex;
  align-items: center;
}

.toolbar-right {
  display: flex;
  align-items: center;
}
</style>
