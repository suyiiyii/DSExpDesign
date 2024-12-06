# 使用 node:20-slim 作为基础镜像
FROM cr.suyiiyii.top/docker.io/library/node:22-alpine AS frontend-builder

WORKDIR /app

# setup pnpm
RUN npm config set registry https://registry.npmmirror.com && \
    npm install -g pnpm

# install dependencies
COPY ./frontend/package.json .
RUN pnpm install

# build frontend
COPY ./frontend/ .
RUN pnpm run build


# 使用官方的 Python 基础镜像
FROM cr.suyiiyii.top/docker.io/library/python:3.11-slim AS base

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 并安装依赖
FROM base AS builder
COPY requirements.txt /app/
RUN python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --no-cache-dir -r requirements.txt

FROM base AS final

# 复制前端构建结果
COPY --from=frontend-builder /app/build /app/app/static

# 复制后端代码
COPY ./data /app/data
COPY ./app /app/app

# 从 builder 镜像复制已安装的依赖
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 暴露应用的端口
EXPOSE 8000
# 启动应用
CMD ["python", "./app/main.py"]
