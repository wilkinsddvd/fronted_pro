# 构建阶段：使用 Node 20（满足 Vite 要求）
FROM node:20-alpine AS build
WORKDIR /app

# 复制依赖并安装（优先使用 ci）
COPY package*.json ./
RUN npm ci --silent || npm install --silent

# 复制源码并构建
COPY . .
RUN npm run build

# 运行阶段：Nginx，容器内监听 3000（避免宿主 80/443 冲突）
FROM nginx:stable-alpine AS production
ENV FRONTEND_PORT=3000

# 安装 curl（可选，用于健康检查）
RUN apk add --no-cache curl

# 替换默认配置为监听 3000 的简单 SPA 配置
RUN rm -f /etc/nginx/conf.d/default.conf \
 && printf '%s\n' \
'server {' \
'    listen 3000 default_server;' \
'    listen [::]:3000 default_server;' \
'    server_name _;' \
'    root /usr/share/nginx/html;' \
'    index index.html;' \
'    location / {' \
'        try_files $uri $uri/ /index.html;' \
'    }' \
'    location ~* \.(?:css|js|json|xml|svg|ttf|woff|woff2|eot|otf|jpg|jpeg|png|gif|ico)$ {' \
'        expires 7d;' \
'        add_header Cache-Control "public, must-revalidate, proxy-revalidate";' \
'    }' \
'    gzip on;' \
'    gzip_types text/plain application/javascript text/css application/json image/svg+xml application/xml;' \
'}' \
> /etc/nginx/conf.d/default.conf

# 复制构建产物
COPY --from=build /app/dist /usr/share/nginx/html

# 暴露容器内部端口（运行时映射到宿主任意端口）
EXPOSE 3000

# 可选健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["nginx", "-g", "daemon off;"]