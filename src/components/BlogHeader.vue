<template>
  <header class="blog-header">
    <h1 @click="$router.push('/')">我的博客</h1>
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/categories">分类</router-link>
      <router-link to="/tags">标签</router-link>
      <router-link to="/archives">归档</router-link>
      <router-link to="/about">关于</router-link>
      <router-link to="/login">登录</router-link>
      <ThemeToggle />
      <a href="https://github.com/wilkinsddvd/fronted_pro" target="_blank">GitHub</a>
     </nav>
  </header>
</template>
<style scoped>
.blog-header { display:flex; justify-content:space-between; align-items:center; padding:1rem 0;}
nav a { margin: 0 1rem; color: var(--color-text);}
</style>