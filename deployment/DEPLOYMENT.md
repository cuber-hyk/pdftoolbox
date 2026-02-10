# PDF 部署指南

本文档提供 PDF 文档工具网站的部署说明。

## 环境要求

### 生产环境

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **CPU**: 2 核心以上
- **内存**: 4GB 以上
- **磁盘**: 20GB 以上可用空间

### 开发环境

- **Node.js**: 18+
- **Python**: 3.11+
- **pnpm**: 9.15+
- **uv**: 最新版本

## 环境变量配置

### 后端环境变量 (.env)

```bash
# API 配置
API_V1_STR=/api/v1
PROJECT_NAME=PDF Toolbox
VERSION=1.0.0

# CORS 配置（逗号分隔）
BACKEND_CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 文件配置
MAX_FILE_SIZE=104857600          # 100MB (字节)
MAX_FILES_PER_UPLOAD=20

# 存储配置
STORAGE_DIR=storage
UPLOAD_DIR=storage/uploads
RESULT_DIR=storage/results
FILE_EXPIRE_HOURS=2               # 文件自动删除时间（小时）

# 处理配置
MAX_WORKERS=4
TASK_TIMEOUT=300                  # 任务超时时间（秒）

# 生产环境（可选）
ENVIRONMENT=production
```

### 前端环境变量 (.env.production)

```bash
VITE_API_URL=/api
```

## 部署方式

### 方式一：Docker Compose 部署（推荐）

这是最简单和推荐的方式，适合大多数部署场景。

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd pdftoolbox
   ```

2. **配置环境变量**
   ```bash
   # 复制并编辑后端环境变量
   cp backend/.env.example backend/.env
   nano backend/.env
   ```

3. **构建并启动服务**
   ```bash
   docker-compose up -d
   ```

4. **检查服务状态**
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

5. **访问应用**
   - 前端: http://localhost
   - 后端 API: http://localhost:8000
   - API 文档: http://localhost:8000/docs

### 方式二：分别部署

适用于需要独立部署前端和后端的场景。

#### 后端部署

1. **构建 Docker 镜像**
   ```bash
   cd backend
   docker build -t pdftoolbox-backend:latest .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name pdftoolbox-backend \
     -p 8000:8000 \
     -v $(pwd)/storage:/app/storage \
     --env-file .env \
     pdftoolbox-backend:latest
   ```

#### 前端部署

1. **构建 Docker 镜像**
   ```bash
   cd frontend
   docker build -t pdftoolbox-frontend:latest .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name pdftoolbox-frontend \
     -p 80:80 \
     -e VITE_API_URL=http://your-backend-url:8000 \
     pdftoolbox-frontend:latest
   ```

### 方式三：Kubernetes 部署

适用于需要高可用和自动扩缩容的场景。

参考 `deployment/k8s/` 目录中的 Kubernetes 配置文件。

## 生产环境配置建议

### 1. 使用 HTTPS

推荐使用 Let's Encrypt 获取免费 SSL 证书。

```bash
# 使用 Certbot
certbot certonly --standalone -d yourdomain.com
```

在 Nginx 配置中添加 SSL:

```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # ... 其他配置
}
```

### 2. 配置反向代理

如果使用 Nginx 作为反向代理:

```nginx
upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://frontend:80;
    }

    location /api/ {
        proxy_pass http://backend;
    }
}
```

### 3. 设置防火墙

```bash
# 只允许必要端口
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

### 4. 配置日志轮转

```bash
# /etc/logrotate.d/pdftoolbox
/var/log/pdftoolbox/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        docker-compose restart backend
    endscript
}
```

### 5. 定期清理过期文件

创建定时任务清理过期文件:

```bash
# 添加到 crontab
0 */2 * * * find /path/to/storage/results -type f -mmin +120 -delete
0 */2 * * * find /path/to/storage/uploads -type f -mmin +120 -delete
```

### 6. 监控和告警

推荐使用以下工具进行监控:
- **Prometheus**: 指标收集
- **Grafana**: 可视化监控
- **Sentry**: 错误追踪

## 性能优化

### 1. 使用 CDN

将静态资源托管到 CDN:
- 阿里云 OSS + CDN
- 腾讯云 COS + CDN
- Cloudflare

### 2. 启用缓存

在 Nginx 中配置缓存:

```nginx
# 缓存 API 响应
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m;

location /api/v1/tools {
    proxy_cache api_cache;
    proxy_cache_valid 200 10m;
    proxy_pass http://backend;
}
```

### 3. 数据库优化

- 使用连接池
- 添加适当的索引
- 定期 VACUUM

## 备份策略

### 1. 数据库备份

```bash
# 每日备份
0 2 * * * pg_dump -U pdftoolbox pdftoolbox > backup_$(date +\%Y\%m\%d).sql
```

### 2. 存储备份

```bash
# 使用 rsync 同步到备份服务器
0 3 * * * rsync -avz /path/to/storage/ backup-server:/backup/storage/
```

## 故障排查

### 常见问题

1. **前端无法连接后端**
   - 检查 CORS 配置
   - 检查防火墙规则
   - 检查后端服务是否运行

2. **文件上传失败**
   - 检查文件大小限制
   - 检查磁盘空间
   - 查看后端日志

3. **任务处理卡住**
   - 检查 Redis 连接
   - 查看任务队列状态
   - 重启后端服务

### 查看日志

```bash
# Docker Compose
docker-compose logs -f backend
docker-compose logs -f frontend

# Docker
docker logs -f pdftoolbox-backend
docker logs -f pdftoolbox-frontend
```

## 更新部署

### 滚动更新（零停机）

```bash
# 拉取最新代码
git pull

# 重新构建
docker-compose build

# 滚动更新
docker-compose up -d --no-deps --build backend frontend
```

### 回滚

```bash
# 切换到之前的版本
git checkout <previous-tag>

# 重新构建并部署
docker-compose build
docker-compose up -d
```

## 安全检查清单

- [ ] 使用 HTTPS
- [ ] 配置 CORS 白名单
- [ ] 启用速率限制
- [ ] 定期更新依赖
- [ ] 配置防火墙
- [ ] 启用日志审计
- [ ] 定期备份数据
- [ ] 使用环境变量管理密钥
- [ ] 禁用 DEBUG 模式
- [ ] 配置 CSP 头

## 支持与联系

如有问题，请联系:
- GitHub Issues: <repository-url>/issues
- Email: support@yourdomain.com
