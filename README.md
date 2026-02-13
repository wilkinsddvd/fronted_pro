# front_pro

Vue 3 + Vite 工单管理系统前端项目，完全对接后端API。

## 功能特性

- ✅ 完全基于后端API的数据获取（工单、快速回复、仪表盘、统计等）
- ✅ 用户认证系统（登录、注册、登出）with JWT Bearer Token
- ✅ 工单管理（创建、编辑、删除、状态管理）
- ✅ 快速回复模板管理
- ✅ 数据统计与可视化（工单趋势、状态分布、优先级分布等）
- ✅ 个人设置（基本信息、安全设置、隐私设置等）
- ✅ 响应式设计
- ✅ 统一的API调用封装与错误处理
- ✅ 401未授权自动跳转登录

## 技术栈

- Vue 3 (Composition API)
- Vue Router 4
- Element Plus (UI组件库)
- Axios (HTTP客户端)
- ECharts (数据可视化)
- Vite (构建工具)

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

本项目依赖以下后端API端点（详见 https://github.com/wilkinsddvd/end_pro）：

**认证要求：** 除了 `/api/login` 和 `/api/register` 外，所有API端点都需要JWT Bearer Token认证。

### 认证相关
- `POST /api/login` - 用户登录（返回token）
- `POST /api/register` - 用户注册（返回token）
- `POST /api/logout` - 用户登出（需要认证）
- `GET /api/self` - 获取当前用户信息（需要认证）

### 工单管理
- `GET /api/tickets` - 获取工单列表（需要认证，支持分页、搜索、过滤）
- `GET /api/tickets/:id` - 获取工单详情（需要认证）
- `POST /api/tickets` - 创建工单（需要认证）
- `PUT /api/tickets/:id` - 更新工单（需要认证）
- `DELETE /api/tickets/:id` - 删除工单（需要认证）

### 快速回复
- `GET /api/quick-replies` - 获取快速回复列表（需要认证）
- `POST /api/quick-replies` - 创建快速回复（需要认证）
- `PUT /api/quick-replies/:id` - 更新快速回复（需要认证）
- `DELETE /api/quick-replies/:id` - 删除快速回复（需要认证）

### 仪表盘
- `GET /api/dashboard/stats` - 获取仪表盘统计数据（需要认证）
- `GET /api/dashboard/trend` - 获取工单趋势数据（需要认证）
- `GET /api/dashboard/category-stats` - 获取工单分类统计（需要认证）

### 统计数据
- `GET /api/statistics/overview` - 获取详细统计数据（需要认证）
- `GET /api/statistics/status-distribution` - 获取工单状态分布（需要认证）
- `GET /api/statistics/priority-distribution` - 获取工单优先级分布（需要认证）
- `GET /api/statistics/user-handling` - 获取用户处理统计（需要认证）
- `GET /api/statistics/response-time` - 获取响应时间统计（需要认证）

### 站点配置
- `GET /api/menus` - 获取菜单配置（需要认证）
- `GET /api/siteinfo` - 获取站点信息（需要认证）

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
import { getTickets, getTicket, createTicket, login } from '@/api/index.js'

// 获取工单列表
const result = await getTickets({ page: 1, size: 10 })

// 获取工单详情
const ticket = await getTicket(ticketId)

// 创建工单
const newTicket = await createTicket({ title: 'Issue', description: 'Details' })

// 用户登录
const user = await login({ username: 'user', password: 'pass' })
```

### 认证机制

- 登录成功后，后端返回的 `data` 中包含 `token` 字段
- Token自动存储在 `localStorage` 中的 `user` 对象里
- 请求拦截器自动在请求头中添加 `Authorization: Bearer {token}`
- 响应拦截器检测401状态码，自动清除token并跳转到登录页

### 错误处理

API模块已内置统一的错误处理。所有API调用应该包裹在 try-catch 中：

```javascript
try {
  const res = await getTickets()
  // 处理成功响应
} catch (error) {
  // 处理错误
  console.error(error.message)
}
```

### 用户认证

用户信息存储在 `localStorage` 中，key为 `user`。登录后自动保存，登出后自动清除。
