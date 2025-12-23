<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/atom-one-light.css'
import CommentBox from './CommentBox.vue'
import { parseFrontMatter } from '../utils/post-meta.js'

const route = useRoute()
const content = ref('')
const title = ref('')
const date = ref('')
const tags = ref([])
const category = ref('')

onMounted(async () => {
  const slug = route.params.slug
  try {
    const res = await fetch(`/src/posts/${slug}.md`)
    const raw = await res.text()
    // 解析front-matter元信息及正文
    const { meta, content: mdContent } = parseFrontMatter(raw)
    title.value = meta.title || extractTitle(mdContent) || ''
    date.value = meta.date || ''
    tags.value = meta.tags ? meta.tags.split(',').map(t => t.trim()) : []
    category.value = meta.category || ''
    content.value = marked.parse(mdContent, {
      highlight: code => hljs.highlightAuto(code).value
    })
  } catch (e) {
    content.value = '<p>未找到此文章。</p>'
    title.value = ''
    date.value = ''
    tags.value = []
    category.value = ''
  }
})

function extractTitle(md) {
  const m = md.match(/^# (.+)$/m)
  return m ? m[1] : ''
}
</script>

<template>
  <article>
    <h1>{{ title }}</h1>
    <div v-if="date || tags.length || category" class="meta">
      <time v-if="date">{{ date }}</time>
      <span v-if="category" class="category">{{ category }}</span>
      <ul class="tags" v-if="tags.length">
        <li v-for="t in tags" :key="t">#{{ t }}</li>
      </ul>
    </div>
    <div v-html="content" class="markdown-body"></div>
    <!-- 评论区（如需可以解除注释下面） -->
    <CommentBox />
  </article>
</template>

<style scoped>
.markdown-body img {max-width:100%;}
.meta {
  margin-bottom: 1rem;
  color: #888;
  font-size: .96em;
  display: flex;
  gap: 1.5em;
  align-items: center;
  flex-wrap: wrap;
}
.meta .tags {
  list-style: none;
  display: flex;
  gap: .5em;
  margin: 0;
  padding: 0;
}
.meta .category {
  background: #eef6f5;
  color: #249d8f;
  padding: 0 .5em;
  border-radius: .5em;
  font-size: .94em;
}
</style>