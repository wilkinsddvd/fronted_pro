<template>
  <header class="blog-header">
    <h1 @click="$router.push('/')">我的博客</h1>
    <nav>
      <a href="/">首页</a>
      <a href="https://github.com/wilkinsddvd/fronted_pro" target="_blank">GitHub</a>
    </nav>
  </header>
</template>
<style scoped>
.blog-header { display:flex; justify-content:space-between; align-items:center; padding:1rem 0;}
nav a { margin: 0 1rem; color: var(--color-text);}
</style>