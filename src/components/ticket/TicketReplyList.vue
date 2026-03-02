<template>
  <div class="ticket-reply-list">
    <el-skeleton v-if="loading" :rows="3" animated />
    <el-empty v-else-if="!replies || replies.length === 0" description="暂无回复，快来发表第一条回复吧" />
    <el-timeline v-else>
      <el-timeline-item
        v-for="reply in replies"
        :key="reply.id"
        :timestamp="reply.created_at"
        placement="top"
      >
        <div class="reply-item">
          <div class="reply-header">
            <el-avatar :size="32" style="background-color: #409eff;">
              {{ reply.user ? reply.user.charAt(0).toUpperCase() : '?' }}
            </el-avatar>
            <strong class="reply-username">{{ reply.user }}</strong>
            <el-button
              v-if="reply.user === currentUsername"
              type="danger"
              size="small"
              link
              @click="$emit('delete', reply)"
            >
              删除
            </el-button>
          </div>
          <div class="reply-content">{{ reply.content }}</div>
        </div>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup>
defineProps({
  replies: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  currentUsername: {
    type: String,
    default: ''
  }
})

defineEmits(['delete'])
</script>

<style scoped>
.reply-item {
  padding: 4px 0;
}

.reply-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.reply-username {
  font-size: 14px;
  flex: 1;
}

.reply-content {
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  padding-left: 40px;
}
</style>
