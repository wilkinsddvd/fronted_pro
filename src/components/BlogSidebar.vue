<template>
  <aside class="blog-sidebar">
    <div class="blog-title">我的博客</div>
    <nav>
      <router-link to="/">首页</router-link>
      <router-link to="/categories">分类</router-link>
      <router-link to="/tags">标签</router-link>
      <router-link to="/archives">归档</router-link>
      <router-link to="/about">关于</router-link>
    </nav>
    <router-link to="/login" class="login-btn">登录</router-link>
  </aside>
</template>

<style scoped>
.blog-sidebar {
  position: fixed;
  height: 100vh;
  width: 240px;
  background: #181818;
  padding: 2rem 1.5rem 1.5rem;
  box-shadow: 4px 0px 16px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.blog-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #eaeaea;
  margin-bottom: 2rem;
}

.blog-sidebar nav {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.blog-sidebar a {
  color: #a9b7c6;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
}

.blog-sidebar a:hover, .blog-sidebar a:focus {
  background: rgba(255,255,255,0.08);
  color: #37c999;
  font-weight: bold;
}

.login-btn {
  background: #ffe466;
  color: #181818;
  font-size: 1rem;
  text-align: center;
  padding: 0.5rem;
  border-radius: 6px;
  text-decoration: none;
  transition: background .18s;
}

.login-btn:hover {
  background: #f5d85a;
}
</style>