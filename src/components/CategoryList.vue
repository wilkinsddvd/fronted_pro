<script setup>
import { ref } from 'vue'
const categories = ref([
  { name: '日常', count: 2 },
  { name: '技术', count: 5 }
])
</script>
<template>
  <section>
    <h2>全部分类</h2>
    <ul>
      <li v-for="c in categories" :key="c.name">
        {{c.name}} ({{c.count}})
      </li>
    </ul>
  </section>
</template>