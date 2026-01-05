# front_pro

Vue 3 + Vite 博客前端项目，完全对接后端API，无静态数据。

## 功能特性

- ✅ 完全基于后端API的数据获取（文章、分类、标签、归档等）
- ✅ 用户认证系统（登录、注册、登出）
- ✅ 文章列表分页、搜索、过滤
- ✅ 文章详情展示与Markdown渲染
- ✅ 文章浏览量和点赞功能
- ✅ 响应式设计与主题切换
- ✅ 统一的API调用封装与错误处理

## 技术栈

- Vue 3 (Composition API)
- Vue Router 4
- Axios (HTTP客户端)
- Vite (构建工具)
- Marked (Markdown解析)
- Highlight.js (代码高亮)

## 项目结构

```
src/
├── api/              # API调用模块
│   └── index.js      # 统一的API接口封装
├── components/       # Vue组件
├── router/           # 路由配置
├── utils/            # 工具函数
├── assets/           # 静态资源
├── App.vue           # 根组件
└── main.js           # 入口文件
```

## 后端API配置

项目通过Vite的proxy功能代理后端API请求。默认配置：

```javascript
// vite.config.js
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // 后端API地址
      changeOrigin: true,
    }
  }
}
```

如需修改后端地址，请编辑 `vite.config.js` 中的 `target` 字段。

## 后端API要求

本项目依赖以下后端API端点（详见 https://github.com/wilkinsddvd/end_pro/tree/master/api）：

- `GET /api/posts` - 获取文章列表（支持分页、搜索、过滤）
- `GET /api/posts/:id` - 获取文章详情
- `POST /api/posts/:id/view` - 增加文章浏览量
- `POST /api/posts/:id/like` - 文章点赞
- `GET /api/categories` - 获取分类列表
- `GET /api/tags` - 获取标签列表
- `GET /api/archive` - 获取归档数据
- `GET /api/menus` - 获取菜单配置
- `GET /api/siteinfo` - 获取站点信息
- `POST /api/login` - 用户登录
- `POST /api/register` - 用户注册
- `POST /api/logout` - 用户登出

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd) 
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

确保后端API服务已启动（默认在 http://localhost:8000），然后运行：

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## 开发说明

### API调用

所有API调用都封装在 `src/api/index.js` 中。示例：

```javascript
import { getPosts, getPost, login } from '@/api/index.js'

// 获取文章列表
const result = await getPosts({ page: 1, size: 10 })

// 获取文章详情
const post = await getPost(postId)

// 用户登录
const user = await login({ username: 'user', password: 'pass' })
```

### 错误处理

API模块已内置统一的错误处理。所有API调用应该包裹在 try-catch 中：

```javascript
try {
  const res = await getPosts()
  // 处理成功响应
} catch (error) {
  // 处理错误
  console.error(error.message)
}
```

### 用户认证

用户信息存储在 `localStorage` 中，key为 `user`。登录后自动保存，登出后自动清除。
