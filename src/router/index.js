import { createRouter, createWebHistory } from 'vue-router'
import BlogPostList from '../components/BlogPostList.vue'
import BlogPostDetail from '../components/BlogPostDetail.vue'

const routes = [
  { path: '/', name: 'Home', component: BlogPostList },
  { path: '/post/:slug', name: 'PostDetail', component: BlogPostDetail, props: true },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})