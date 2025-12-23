<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  if (document.getElementById('giscus-script')) return
  const script = document.createElement('script')
  script.src = 'https://giscus.app/client.js'
  script.setAttribute('data-repo', 'wilkinsddvd/fronted_pro')
  script.setAttribute('data-repo-id', 'REPO_ID') // <-- 请替换你的repo id
  script.setAttribute('data-category', 'General')
  script.setAttribute('data-mapping', 'pathname')
  script.setAttribute('data-reactions-enabled', '1')
  script.setAttribute('data-theme', 'light')
  script.crossOrigin = 'anonymous'
  script.async = true
  script.id = 'giscus-script'
  document.getElementById('giscus-container')?.appendChild(script)
})
</script>

<template>
  <section style="margin-top:2rem">
    <h3>欢迎留言</h3>
    <div id="giscus-container"></div>
    <noscript>请启用JavaScript留言</noscript>
  </section>
</template>