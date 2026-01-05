import { createRouter, createWebHistory } from 'vue-router'
import BlogPostList from '../components/BlogPostList.vue'
import BlogPostDetail from '../components/BlogPostDetail.vue'
import CategoryList from '../components/CategoryList.vue'
import TagList from '../components/TagList.vue'
import ArchiveList from '../components/ArchiveList.vue'
import AboutMe from '../components/AboutMe.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'

const routes = [
  { path: '/', name: 'Home', component: BlogPostList },
  { path: '/post/:slug', name: 'PostDetail', component: BlogPostDetail, props: true }, // slug实际为id
  { path: '/categories', name: 'Categories', component: CategoryList },
  { path: '/tags', name: 'Tags', component: TagList },
  { path: '/archives', name: 'Archives', component: ArchiveList },
  { path: '/about', name: 'About', component: AboutMe },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})