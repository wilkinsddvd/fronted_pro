<script setup>
import { ref, onMounted } from 'vue'
import { getSiteInfo } from '@/api/index.js'

const siteInfo = ref({
  title: 'wilkinsddvd',
  description: '',
  icp: '鲁ICP备2025198092号-1',
  footer: '© 2025 wilkinsddvd. Power by Vue 3 + Vite'
})

async function loadSiteInfo() {
  try {
    const res = await getSiteInfo()
    if (res.data) {
      siteInfo.value = {
        title: res.data.title || siteInfo.value.title,
        description: res.data.description || siteInfo.value.description,
        icp: res.data.icp || siteInfo.value.icp,
        footer: res.data.footer || siteInfo.value.footer
      }
    }
  } catch (e) {
    console.log('使用默认站点信息')
  }
}

onMounted(() => {
  loadSiteInfo()
})
</script>

<template>
  <footer class="blog-footer">
    <small>
      {{ siteInfo.footer }} |
      <a
        href="https://beian.miit.gov.cn/#/Integrated/index"
        target="_blank"
        rel="noopener"
        class="beian-link"
      >{{ siteInfo.icp }}</a>
    </small>
  </footer>
</template>

<style scoped>
.blog-footer {
  margin-top: 2rem;
  text-align: center;
  color: #999;
}
.beian-link {
  color: #999;
  text-decoration: underline;
  margin-left: 0.5em;
}
.beian-link:hover {
  color: hsla(160, 100%, 37%, 1);
}
</style>