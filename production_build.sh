#!/bin/bash

mkdir -p ~/storage
mkdir -p ~/applog
# 切换到src目录
cd src

# 停止并删除现有的Docker容器(如果存在)
docker stop blogbackendi
docker rm blogbackendi

# 删除旧的Docker镜像
docker rmi blogapi

# 构建新的Docker镜像
docker build -t blogapi . 

# 运行新的Docker容器
docker run -d \
  --name blogbackendi \
  --network host \
  --privileged \
  -v ~/storage:/app/storage \
  -v ~/applog:/app/log \
  -e GITHUB_TOKEN=$SYS_GITHUB_TOKEN \
  -e BLOG_REPO=$SYS_BLOG_REPO \
  -e LOGIN_USERNAME=$SYS_LOGIN_USERNAME \
  -e LOGIN_PASSWORD=$SYS_LOGIN_PASSWORD \
  -e SMTP_HOST=$SYS_SMTP_HOST \
  -e SMTP_USER=$SYS_SMTP_USER \
  -e SMTP_PASSWORD=$SYS_SMTP_PASSWORD \
  -e SMTP_PORT=$SYS_SMTP_PORT \
  -e EMAILS_FROM_EMAIL=$SYS_EMAILS_FROM_EMAIL \
  -p 1588:1588 \
  blogapi
