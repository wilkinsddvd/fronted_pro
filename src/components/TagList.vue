<script setup>
import { ref } from 'vue'
const tags = ref([
  '前端','后端','全栈', '爱情','生活','学习', 'Vue', 'fastapi','笔记'
])
</script>
<template>
  <section>
    <h2>标签云</h2>
    <ul>
      <li v-for="t in tags" :key="t">{{t}}</li>
    </ul>
  </section>
</template>