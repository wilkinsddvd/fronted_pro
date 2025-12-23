<script setup>
import BlogHeader from './components/BlogHeader.vue'
import BlogFooter from './components/BlogFooter.vue'
</script>

<template>
  <BlogHeader />
  <main>
    <router-view />
  </main>
  <BlogFooter />
</template>