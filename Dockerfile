# 使用 Node.js 20 LTS 版本作为基础镜像
FROM node:20 AS build-stage

# 设置容器中的工作目录
WORKDIR /app

# 将 package.json 和 package-lock.json 复制到容器中
COPY package.json package-lock.json ./

# 安装项目依赖
RUN npm install

# 将项目源文件复制到容器中
COPY . .

# 构建项目（生产环境）
RUN npm run build

# 第二阶段：使用 Nginx 作为服务器
FROM nginx:stable AS production-stage

# 复制第一阶段生成的构建文件到 Nginx 静态内容目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx 服务
CMD ["nginx", "-g", "daemon off;"]