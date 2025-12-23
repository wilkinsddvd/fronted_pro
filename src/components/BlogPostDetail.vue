<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-light.css'

const route = useRoute()
const content = ref('')
const title = ref('')
const date = ref('')

onMounted(async () => {
  const slug = route.params.slug
  try {
    // 这里直接import可能会被Vite优化，可以用fetch或import.meta.glob
    const res = await fetch(`/src/posts/${slug}.md`)
    const raw = await res.text()
    content.value = marked.parse(raw, {
      highlight: code => hljs.highlightAuto(code).value
    })
    // 简单处理标题和日期（建议用front-matter库做真正博客需解析meta，可后续优化）
    const headerMatch = raw.match(/^# (.+)$/m)
    if (headerMatch) title.value = headerMatch[1]
  } catch (e) {
    content.value = '<p>未找到此文章。</p>'
  }
})
</script>
<template>
  <article>
    <h1>{{ title }}</h1>
    <div v-html="content" class="markdown-body"></div>
  </article>
</template>
<style scoped>
.markdown-body img {max-width:100%;}
</style>