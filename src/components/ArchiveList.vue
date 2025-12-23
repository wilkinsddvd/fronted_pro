<script setup>
import { ref } from 'vue'
const archives = ref([
  { year: 2025, posts: [{title:'你好，世界', slug:'hello-world', date:'2025-12-23'}] }
])
</script>
<template>
  <section>
    <h2>归档</h2>
    <div v-for="a in archives" :key="a.year">
      <h3>{{a.year}}</h3>
      <ul>
        <li v-for="p in a.posts" :key="p.slug">
          <router-link :to="'/post/' + p.slug">{{p.title}}</router-link> <small>{{p.date}}</small>
        </li>
      </ul>
    </div>
  </section>
</template>