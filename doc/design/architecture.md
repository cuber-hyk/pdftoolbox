# PDF 文档工具网站 - 架构设计文档

> **版本**: 1.0
> **日期**: 2026-02-05
> **作者**: 架构团队

---

## 目录

1. [项目概述](#项目概述)
2. [技术栈选型](#技术栈选型)
3. [系统架构设计](#系统架构设计)
4. [目录结构](#目录结构)
5. [API 接口设计](#api-接口设计)
6. [数据模型设计](#数据模型设计)
7. [前端组件设计](#前端组件设计)
8. [PDF 处理库选型](#pdf-处理库选型)
9. [安全性设计](#安全性设计)
10. [性能优化策略](#性能优化策略)
11. [部署架构](#部署架构)
12. [监控与日志](#监控与日志)

---

## 项目概述

### 功能定位

PDF 文档工具网站是一个在线 PDF 处理服务平台，提供多种 PDF 操作功能，用户无需安装软件即可通过浏览器完成 PDF 文件处理。

### 核心功能

| 功能 | 描述 | 优先级 |
|------|------|--------|
| PDF 合并 | 将多个 PDF 文件合并为一个 | P0 |
| PDF 拆分 | 将一个 PDF 拆分为多个文件 | P0 |
| 页面提取 | 提取指定页面生成新 PDF | P0 |
| 文本提取 | 提取 PDF 中的文本内容 | P1 |
| 图片提取 | 提取 PDF 中的图片 | P1 |
| 添加水印 | 为 PDF 添加文字/图片水印 | P0 |
| 去除水印 | 尝试去除 PDF 中的水印 | P2 |
| PDF 转图片 | 将 PDF 页面转换为图片 | P1 |

### 设计原则

1. **简洁优先**: 开门见山，用户无需导航即可看到可用工具
2. **性能导向**: 前端轻量，后端高效处理
3. **可扩展性**: 易于添加新工具，支持未来扩展
4. **安全可靠**: 文件自动清理，隐私保护
5. **渐进增强**: 基础功能优先，高级功能逐步添加

---

## 技术栈选型

### 前端技术栈

#### Vue 3 + TypeScript

**选择理由**:

- **Vue 3**: 性能优秀，Composition API 提供更好的代码组织
- **TypeScript**: 类型安全，减少运行时错误
- **Vite**: 极快的开发体验，生产优化出色
- **成熟生态**: Shadcn/ui 提供优雅的组件库

**技术组合**:

```typescript
// 核心框架
Vue 3.4+              // 渐进式框架
TypeScript 5.3+       // 类型系统

// 构建工具
Vite 5.0+             // 构建工具

// UI 组件
Shadcn/ui             // 无样式组件库
TailwindCSS 3.4+      // 原子化 CSS
Lucide Icons          // 图标库

// 状态管理
Pinia 2.1+            // 官方状态管理

// 路由
Vue Router 4.2+       // 官方路由

// 工具库
VueUse 10.0+          // Composition 工具集
```

#### 为什么选择 Shadcn/ui

1. **可定制性强**: 组件代码直接复制到项目中，完全控制
2. **设计系统**: 基于 Radix UI，无障碍访问支持好
3. **美观现代**: 预设设计简洁专业，符合项目风格要求
4. **Tree-shaking**: 按需导入，打包体积小
5. **TypeScript**: 完整类型支持

### 后端技术栈

#### FastAPI + Python

**选择理由**:

- **FastAPI**: 现代、快速的 Web 框架，自动 API 文档
- **异步支持**: 原生 async/await，适合 I/O 密集型任务
- **类型验证**: Pydantic 提供强大的数据验证
- **Python 生态**: PDF 处理库丰富

**技术组合**:

```python
# 核心框架
FastAPI 0.104+        # Web 框架
Python 3.11+          # 运行时
Pydantic 2.4+         # 数据验证
Uvicorn 0.24+         # ASGI 服务器

# PDF 处理
PyMuPDF 1.23+         # 核心处理库（fitz）
Pillow 10.1+          # 图片处理
PyPDF2 3.0+           # 辅助操作

# 任务队列
Celery 5.3+           # 异步任务队列
Redis 5.0+            # 消息代理/缓存

# 数据库
PostgreSQL 15+        # 关系型数据库（可选）
SQLite                # 轻量级替代方案

# 文件存储
本地存储              # 简单部署
云存储 (OSS/S3)       # 生产环境推荐

# 工具库
python-multipart      # 文件上传
aiofiles 23.2+        # 异步文件操作
```

### 为什么选择 FastAPI

| 特性 | 优势 | 对项目的影响 |
|------|------|-------------|
| **自动文档** | Swagger UI 开箱即用 | 减少文档维护成本 |
| **异步支持** | 高并发处理能力 | 提升文件处理吞吐量 |
| **类型验证** | Pydantic 自动验证 | 减少数据验证代码 |
| **依赖注入** | 优雅的依赖管理 | 代码更易测试 |
| **WebSocket** | 实时进度推送 | 提升用户体验 |

---

## 系统架构设计

### 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户浏览器                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Vue 3 前端应用                           │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │ │
│  │  │工具列表页│  │操作页面  │  │上传组件  │  │进度显示  │  │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTPS + REST API
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Nginx (可选)                              │
│                    静态资源 + 反向代理                            │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI 后端服务                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    API 路由层                               │ │
│  │  /api/v1/tools /api/v1/files /api/v1/jobs                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    业务逻辑层                               │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ │
│  │  │文件服务  │  │任务服务  │  │工具服务  │  │清理服务  │       │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ▼                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    PDF 处理层                               │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │ │
│  │  │合并模块  │  │拆分模块  │  │提取模块  │  │水印模块  │       │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│    Redis     │    │  文件存储     │    │  PostgreSQL  │
│ (任务队列/   │    │ (临时文件/    │    │  (用户/日志/  │
│   缓存)      │    │  结果文件)    │    │   统计)      │
└──────────────┘    └──────────────┘    └──────────────┘
```

### 架构分层说明

#### 1. 前端层 (Vue 3)

**职责**:
- 用户界面渲染
- 文件上传处理
- 进度展示
- 结果下载

**关键组件**:
```
pages/
├── Home.vue              # 工具首页（工具列表）
├── tools/
│   ├── MergePDF.vue      # PDF 合并
│   ├── SplitPDF.vue      # PDF 拆分
│   ├── ExtractPages.vue  # 页面提取
│   ├── ExtractText.vue   # 文本提取
│   ├── ExtractImages.vue # 图片提取
│   ├── AddWatermark.vue  # 添加水印
│   └── RemoveWatermark.vue # 去除水印
└── Result.vue            # 处理结果页
```

#### 2. API 网关层 (Nginx - 可选)

**职责**:
- 静态资源服务
- 反向代理
- SSL 终止
- 负载均衡（多实例部署时）

#### 3. 后端层 (FastAPI)

**职责**:
- RESTful API 提供
- 请求验证
- 业务逻辑协调
- 文件处理调度

**分层架构**:

```
api/
├── __init__.py
├── deps.py               # 依赖注入
├── v1/
│   ├── __init__.py
│   ├── router.py         # 路由聚合
│   ├── tools.py          # 工具相关 API
│   ├── files.py          # 文件上传/下载 API
│   └── jobs.py           # 任务状态 API
├── middleware/
│   ├── cors.py           # CORS 处理
│   ├── rate_limit.py     # 速率限制
│   └── security.py       # 安全头
└── schemas/
    ├── tools.py          # 工具请求/响应模型
    ├── files.py          # 文件模型
    └── jobs.py           # 任务模型
```

#### 4. 业务逻辑层

**核心服务**:

```python
services/
├── __init__.py
├── file_service.py       # 文件存储服务
├── job_service.py        # 任务管理服务
├── tool_service.py       # 工具注册/调度
└── cleanup_service.py    # 定时清理服务
```

#### 5. PDF 处理层

**处理模块**:

```python
processors/
├── __init__.py
├── base.py               # 基础处理器类
├── merge.py              # 合并处理器
├── split.py              # 拆分处理器
├── extract.py            # 提取处理器
└── watermark.py          # 水印处理器
```

#### 6. 数据存储层

**存储方案**:
- **Redis**: 任务队列、缓存、会话
- **文件系统**: 临时文件、结果文件
- **PostgreSQL** (可选): 用户数据、使用统计、日志

---

## 目录结构

### 完整项目结构

```
pdftoolbox/
├── frontend/                    # 前端项目 (Vue 3)
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/
│   │   │   ├── styles/
│   │   │   │   └── main.css     # 全局样式
│   │   │   └── images/
│   │   ├── components/
│   │   │   ├── ui/              # Shadcn/ui 组件
│   │   │   │   ├── button/
│   │   │   │   ├── card/
│   │   │   │   ├── dialog/
│   │   │   │   ├── progress/
│   │   │   │   └── ...
│   │   │   └── business/        # 业务组件
│   │   │       ├── ToolCard.vue # 工具卡片
│   │   │       ├── FileUploader.vue # 文件上传
│   │   │       ├── ProgressBar.vue # 进度条
│   │   │       └── ResultDownload.vue # 结果下载
│   │   ├── composables/
│   │   │   ├── useFileUpload.ts # 文件上传逻辑
│   │   │   ├── usePolling.ts    # 轮询任务状态
│   │   │   └── useApi.ts        # API 调用
│   │   ├── pages/
│   │   │   ├── Home.vue         # 工具首页
│   │   │   └── tools/           # 各工具页面
│   │   │       ├── MergePDF.vue
│   │   │       ├── SplitPDF.vue
│   │   │       ├── ExtractPages.vue
│   │   │       ├── ExtractText.vue
│   │   │       ├── ExtractImages.vue
│   │   │       ├── AddWatermark.vue
│   │   │       └── RemoveWatermark.vue
│   │   ├── router/
│   │   │   └── index.ts         # 路由配置
│   │   ├── stores/
│   │   │   └── modules/
│   │   │       ├── upload.ts    # 上传状态
│   │   │       └── job.ts       # 任务状态
│   │   ├── api/
│   │   │   ├── client.ts        # API 客户端
│   │   │   └── types.ts         # API 类型
│   │   ├── utils/
│   │   │   ├── file.ts          # 文件工具
│   │   │   └── format.ts        # 格式化工具
│   │   ├── App.vue
│   │   └── main.ts
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   ├── .eslintrc.cjs
│   ├── .prettierrc
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
│
├── backend/                     # 后端项目 (FastAPI)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py              # 依赖注入
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py        # API 路由聚合
│   │   │   ├── tools.py         # 工具 API
│   │   │   ├── files.py         # 文件 API
│   │   │   └── jobs.py          # 任务 API
│   │   └── middleware/
│   │       ├── cors.py
│   │       ├── rate_limit.py
│   │       └── security.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # 配置管理
│   │   ├── security.py          # 安全工具
│   │   └── logging.py           # 日志配置
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py              # 任务模型
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── tools.py             # 工具请求/响应
│   │   ├── files.py             # 文件模型
│   │   └── jobs.py              # 任务模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_service.py      # 文件服务
│   │   ├── job_service.py       # 任务服务
│   │   ├── tool_service.py      # 工具服务
│   │   └── cleanup_service.py   # 清理服务
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── base.py              # 基础处理器
│   │   ├── merge.py             # 合并处理器
│   │   ├── split.py             # 拆分处理器
│   │   ├── extract.py           # 提取处理器
│   │   └── watermark.py         # 水印处理器
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file.py              # 文件工具
│   │   └── validation.py        # 验证工具
│   ├── tests/
│   │   ├── unit/
│   │   ├── integration/
│   │   └── conftest.py
│   ├── storage/
│   │   ├── uploads/             # 上传文件
│   │   ├── results/             # 结果文件
│   │   └── temp/                # 临时文件
│   ├── .env.example
│   ├── .gitignore
│   ├── alembic.ini              # 数据库迁移（可选）
│   ├── app.py                   # 应用入口
│   ├── pyproject.toml
│   └── requirements.txt
│
├── deployment/                  # 部署配置
│   ├── docker/
│   │   ├── Dockerfile.frontend
│   │   ├── Dockerfile.backend
│   │   └── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── kubernetes/              # K8s 配置（可选）
│
├── doc/                         # 文档
│   ├── design/
│   │   ├── architecture.md      # 本文档
│   │   ├── api.md               # API 文档
│   │   └── database.md          # 数据库设计（可选）
│   ├── development/
│   │   ├── frontend-guide.md
│   │   └── backend-guide.md
│   └── deployment/
│       └── deployment-guide.md
│
├── .gitignore
└── README.md
```

### 目录设计原则

1. **前后端分离**: frontend 和 backend 独立目录
2. **分层清晰**: API 层、服务层、处理层分离
3. **易于扩展**: 新增工具只需添加处理器和路由
4. **测试独立**: 测试代码与源码分离
5. **文档完善**: 设计、开发、部署文档齐全

---

## API 接口设计

### RESTful 设计原则

- **资源导向**: URL 表示资源，HTTP 方法表示操作
- **统一响应**: 标准化的响应格式
- **版本控制**: 通过 URL 路径进行版本控制 (`/api/v1/`)
- **幂等性**: GET、PUT、DELETE 操作幂等

### 通用响应格式

```typescript
// 成功响应
interface SuccessResponse<T> {
  success: true
  data: T
  message?: string
}

// 错误响应
interface ErrorResponse {
  success: false
  error: {
    code: string
    message: string
    details?: any
  }
}
```

### API 端点列表

#### 1. 工具相关 API

```python
# 获取可用工具列表
GET /api/v1/tools

Response:
{
  "success": true,
  "data": [
    {
      "id": "merge",
      "name": "PDF 合并",
      "description": "将多个 PDF 文件合并为一个",
      "icon": "merge",
      "route": "/tools/merge",
      "max_files": 20,
      "max_size_mb": 100
    },
    {
      "id": "split",
      "name": "PDF 拆分",
      "description": "将一个 PDF 拆分为多个文件",
      "icon": "scissors",
      "route": "/tools/split",
      "max_files": 1,
      "max_size_mb": 100
    }
    // ... 更多工具
  ]
}
```

#### 2. 文件上传 API

```python
# 上传文件
POST /api/v1/files/upload
Content-Type: multipart/form-data

Form Data:
- files: List[File]    # 文件列表
- tool_id: str         # 工具 ID

Response:
{
  "success": true,
  "data": {
    "upload_id": "ul_xxxxx",
    "files": [
      {
        "file_id": "f_xxxxx",
        "name": "document.pdf",
        "size": 1024000,
        "pages": 10
      }
    ]
  }
}

# 限制：
# - 单文件最大 100MB
# - 总大小最大 200MB
# - 支持断点续传（可选）
```

#### 3. 任务处理 API

```python
# 创建处理任务
POST /api/v1/jobs

Request:
{
  "tool_id": "merge",
  "upload_id": "ul_xxxxx",
  "options": {
    "output_filename": "merged.pdf"
    // 工具特定选项
  }
}

Response:
{
  "success": true,
  "data": {
    "job_id": "job_xxxxx",
    "status": "queued",
    "created_at": "2026-02-05T10:00:00Z"
  }
}

# 查询任务状态
GET /api/v1/jobs/{job_id}

Response:
{
  "success": true,
  "data": {
    "job_id": "job_xxxxx",
    "status": "processing",  # queued | processing | completed | failed
    "progress": 50,          # 0-100
    "message": "正在处理第 3 页，共 10 页",
    "created_at": "2026-02-05T10:00:00Z",
    "started_at": "2026-02-05T10:01:00Z",
    "completed_at": null,
    "result": null           # 完成后包含结果信息
  }
}

# 完成状态响应
{
  "success": true,
  "data": {
    "job_id": "job_xxxxx",
    "status": "completed",
    "progress": 100,
    "message": "处理完成",
    "created_at": "2026-02-05T10:00:00Z",
    "started_at": "2026-02-05T10:01:00Z",
    "completed_at": "2026-02-05T10:02:00Z",
    "result": {
      "download_url": "/api/v1/files/download/result_xxxxx.pdf",
      "filename": "result.pdf",
      "size": 2048000,
      "expires_at": "2026-02-05T12:00:00Z"
    }
  }
}

# 取消任务
DELETE /api/v1/jobs/{job_id}
```

#### 4. 文件下载 API

```python
# 下载处理结果
GET /api/v1/files/download/{file_id}

# 注意：
# - 需要验证权限
# - 设置正确的 Content-Type
# - 支持 Range 请求（断点续传）
# - 文件链接有时效性（默认 2 小时）
```

### API 错误码

```python
# HTTP 状态码
400 Bad Request         # 请求参数错误
401 Unauthorized        # 未授权（如需要认证）
403 Forbidden           # 无权限
404 Not Found           # 资源不存在
413 Payload Too Large   # 文件过大
415 Unsupported Media   # 不支持的文件类型
422 Unprocessable Entity # 验证失败
429 Too Many Requests   # 速率限制
500 Internal Server Error # 服务器错误
503 Service Unavailable # 服务不可用

# 业务错误码
ERR_INVALID_FILE       # 无效的 PDF 文件
ERR_FILE_TOO_LARGE     # 文件超过大小限制
ERR_FILE_CORRUPTED     # 文件损坏
ERR_ENCRYPTED_PDF      # PDF 已加密
ERR_INVALID_PAGES      # 页码范围错误
ERR_PROCESSING_FAILED  # 处理失败
ERR_JOB_NOT_FOUND      # 任务不存在
ERR_FILE_EXPIRED       # 文件已过期
```

### API 速率限制

```python
# 速率限制策略
UPLOAD_LIMIT = "10/minute"      # 上传：每分钟 10 次
JOB_LIMIT = "20/minute"         # 创建任务：每分钟 20 次
DOWNLOAD_LIMIT = "30/minute"    # 下载：每分钟 30 次

# 基于 IP 地址和用户（如支持认证）
# 使用 Redis 存储计数器
```

---

## 数据模型设计

### 核心数据模型

#### 1. 任务模型 (Job)

```python
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Job(BaseModel):
    """任务模型"""
    job_id: str = Field(..., description="任务 ID")
    tool_id: str = Field(..., description="工具 ID")
    upload_id: str = Field(..., description="上传 ID")
    status: JobStatus = Field(default=JobStatus.QUEUED, description="任务状态")
    progress: int = Field(default=0, ge=0, le=100, description="进度百分比")
    message: str = Field(default="", description="状态消息")

    # 文件信息
    input_files: list[str] = Field(default_factory=list, description="输入文件 ID 列表")
    output_file: Optional[str] = Field(None, description="输出文件 ID")

    # 处理选项
    options: Dict[str, Any] = Field(default_factory=dict, description="处理选项")

    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

    # 错误信息
    error: Optional[str] = Field(None, description="错误信息")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### 2. 文件模型 (File)

```python
class FileStatus(str, Enum):
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    DELETED = "deleted"

class FileMetadata(BaseModel):
    """文件元数据"""
    name: str
    size: int
    mime_type: str
    pages: Optional[int] = None  # PDF 页数
    encrypted: bool = False      # 是否加密

class File(BaseModel):
    """文件模型"""
    file_id: str
    upload_id: str
    status: FileStatus = FileStatus.UPLOADING
    metadata: FileMetadata

    # 存储信息
    storage_path: str
    storage_type: str = "local"  # local | s3 | oss

    # 时间戳
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

#### 3. 工具模型 (Tool)

```python
class Tool(BaseModel):
    """工具模型"""
    id: str
    name: str
    description: str
    icon: str
    route: str

    # 配置
    max_files: int = Field(default=1, description="最大文件数")
    max_size_mb: int = Field(default=100, description="单文件最大大小 (MB)")
    max_total_size_mb: int = Field(default=200, description="总大小限制 (MB)")

    # 选项配置
    options_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="选项 JSON Schema"
    )
```

### 数据库设计 (PostgreSQL - 可选)

```sql
-- 任务表
CREATE TABLE jobs (
    job_id VARCHAR(64) PRIMARY KEY,
    tool_id VARCHAR(32) NOT NULL,
    upload_id VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'queued',
    progress INTEGER NOT NULL DEFAULT 0,
    message TEXT,
    input_files JSONB,
    output_file VARCHAR(64),
    options JSONB,
    error TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    expires_at TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_upload_id (upload_id)
);

-- 文件表
CREATE TABLE files (
    file_id VARCHAR(64) PRIMARY KEY,
    upload_id VARCHAR(64) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'uploading',
    metadata JSONB NOT NULL,
    storage_path TEXT NOT NULL,
    storage_type VARCHAR(20) NOT NULL DEFAULT 'local',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    INDEX idx_upload_id (upload_id),
    INDEX idx_expires_at (expires_at)
);

-- 使用统计表（可选）
CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    tool_id VARCHAR(32) NOT NULL,
    job_id VARCHAR(64),
    status VARCHAR(20) NOT NULL,
    processing_time_ms INTEGER,
    file_count INTEGER,
    total_size_bytes BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tool_id (tool_id),
    INDEX idx_created_at (created_at)
);
```

---

## 前端组件设计

### 页面布局

#### 主页布局 (Home.vue)

```
┌─────────────────────────────────────────────────────────┐
│                      Header                              │
│  ┌──────────────┐  ┌──────────────────────────────┐     │
│  │    Logo      │  │         PDF 工具箱           │     │
│  └──────────────┘  └──────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                       Hero                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │     简单、快速的在线 PDF 工具                    │    │
│  │     无需注册，完全免费，保护隐私                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                    工具列表                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │  PDF合并  │ │  PDF拆分  │ │ 页面提取  │ │ 添加水印  │  │
│  │ [图标]   │ │ [图标]   │ │ [图标]   │ │ [图标]   │  │
│  │ 将多个... │ │ 将一个... │ │ 提取指... │ │ 为PDF... │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│  │ 文本提取  │ │ 图片提取  │ │ PDF转图片│ │ 去除水印  │  │
│  │ [图标]   │ │ [图标]   │ │ [图标]   │ │ [图标]   │  │
│  │ 提取PDF...│ │ 提取PDF...│ │ 将PDF... │ │ 尝试去除...│  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘  │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                      Footer                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │  © 2026 PDF 工具箱 | 隐私政策 | 使用条款         │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

#### 工具页面布局

```
┌─────────────────────────────────────────────────────────┐
│                      Header                              │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ← 返回   │  │  PDF 合并     │  │              │      │
│  └──────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                     说明区域                              │
│  ┌─────────────────────────────────────────────────┐    │
│  │ 将多个 PDF 文件合并为一个文件。支持拖拽调整顺序。 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                    操作区域                               │
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                   │    │
│  │   ┌─────────────────────────────────────────┐   │    │
│  │   │                                         │   │    │
│  │   │         [拖拽上传文件]                  │   │    │
│  │   │                                         │   │    │
│  │   │     或点击选择文件 (最多 20 个)          │   │    │
│  │   │                                         │   │    │
│  │   └─────────────────────────────────────────┘   │    │
│  │                                                   │    │
│  │   已选文件 (可拖拽排序):                          │    │
│  │   ┌───────────────────────────────────────────┐  │    │
│  │   │ ☰ document1.pdf (2.3 MB)        [×]      │  │    │
│  │   │ ☰ document2.pdf (1.5 MB)        [×]      │  │    │
│  │   └───────────────────────────────────────────┘  │    │
│  │                                                   │    │
│  │   ┌─────────────────┐  ┌─────────────────┐       │    │
│  │   │   输出文件名    │  │   [开始合并]    │       │    │
│  │   └─────────────────┘  └─────────────────┘       │    │
│  │                                                   │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   进度显示 (处理时)                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │  正在处理...  [=========>        ] 50%          │    │
│  │  正在合并第 5 页，共 10 页                        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                   结果显示 (完成后)                       │
│  ┌─────────────────────────────────────────────────┐    │
│  │  ✓ 处理完成！                                    │    │
│  │                                                  │    │
│  │  ┌───────────────┐   ┌─────────────────────┐   │    │
│  │  │  [下载结果]   │   │  [重新处理]         │   │    │
│  │  └───────────────┘   └─────────────────────┘   │    │
│  │                                                  │    │
│  │  文件将在 2 小时后自动删除                        │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

### 核心组件设计

#### 1. ToolCard.vue (工具卡片)

```vue
<script setup lang="ts">
interface Tool {
  id: string
  name: string
  description: string
  icon: string
  route: string
}

interface Props {
  tool: Tool
}

const props = defineProps<Props>()
</script>

<template>
  <router-link
    :to="tool.route"
    class="group block p-6 rounded-xl border border-gray-200
           hover:border-blue-500 hover:shadow-lg
           transition-all duration-200"
  >
    <div class="flex items-center gap-3 mb-3">
      <div class="p-2 rounded-lg bg-blue-50 text-blue-600">
        <LucideIcon :name="tool.icon" :size="24" />
      </div>
      <h3 class="text-lg font-semibold text-gray-900">
        {{ tool.name }}
      </h3>
    </div>
    <p class="text-sm text-gray-600">
      {{ tool.description }}
    </p>
  </router-link>
</template>
```

#### 2. FileUploader.vue (文件上传)

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { useFileUpload } from '@/composables/useFileUpload'

interface Props {
  toolId: string
  maxFiles?: number
  maxSize?: number  // MB
  accept?: string
}

const props = withDefaults(defineProps<Props>(), {
  maxFiles: 1,
  maxSize: 100,
  accept: 'application/pdf'
})

const emit = defineEmits<{
  uploaded: [uploadId: string, files: UploadedFile[]]
}>()

const {
  isUploading,
  progress,
  selectedFiles,
  handleFileSelect,
  uploadFiles
} = useFileUpload(props.toolId, props.maxFiles, props.maxSize)

const onDrop = (e: DragEvent) => {
  e.preventDefault()
  const files = Array.from(e.dataTransfer?.files || [])
  handleFileSelect(files)
}
</script>

<template>
  <div
    class="border-2 border-dashed rounded-xl p-8
           transition-colors"
    :class="isUploading ? 'border-gray-300 bg-gray-50' :
           'border-gray-300 hover:border-blue-400'"
    @drop.prevent="onDrop"
    @dragover.prevent
  >
    <div v-if="!isUploading" class="text-center">
      <UploadIcon :size="48" class="mx-auto text-gray-400 mb-4" />
      <p class="text-gray-600 mb-2">
        拖拽文件到此处，或点击选择
      </p>
      <p class="text-sm text-gray-400">
        支持 PDF 文件，单文件最大 {{ maxSize }}MB
      </p>
      <input
        type="file"
        :accept="accept"
        :multiple="maxFiles > 1"
        class="hidden"
        @change="(e) => handleFileSelect(Array.from(e.target.files || []))"
      />
      <Button
        @click="$el.querySelector('input').click()"
        class="mt-4"
      >
        选择文件
      </Button>
    </div>

    <div v-else class="text-center">
      <ProgressBar :value="progress" />
      <p class="text-gray-600 mt-2">上传中... {{ progress }}%</p>
    </div>
  </div>

  <!-- 已选文件列表 -->
  <div v-if="selectedFiles.length > 0" class="mt-4 space-y-2">
    <div
      v-for="file in selectedFiles"
      :key="file.id"
      class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
    >
      <div class="flex items-center gap-3">
        <FileIcon :size="20" class="text-gray-400" />
        <span class="text-gray-700">{{ file.name }}</span>
        <span class="text-sm text-gray-400">
          ({{ formatSize(file.size) }})
        </span>
      </div>
      <Button
        variant="ghost"
        size="sm"
        @click="removeFile(file.id)"
      >
        <XIcon :size="16" />
      </Button>
    </div>
  </div>
</template>
```

#### 3. ProgressBar.vue (进度条)

```vue
<script setup lang="ts">
interface Props {
  value: number  // 0-100
  message?: string
}

withDefaults(defineProps<Props>(), {
  message: ''
})
</script>

<template>
  <div class="w-full">
    <div class="flex items-center justify-between mb-2">
      <span class="text-sm text-gray-600">
        {{ message || '正在处理...' }}
      </span>
      <span class="text-sm font-medium text-gray-900">
        {{ value }}%
      </span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2">
      <div
        class="bg-blue-600 h-2 rounded-full transition-all duration-300"
        :style="{ width: `${value}%` }"
      />
    </div>
  </div>
</template>
```

### Composables 设计

#### useFileUpload.ts

```typescript
import { ref, computed } from 'vue'
import { apiClient } from '@/api/client'

interface UploadFile {
  id: string
  name: string
  size: number
}

export function useFileUpload(
  toolId: string,
  maxFiles: number,
  maxSizeMB: number
) {
  const isUploading = ref(false)
  const progress = ref(0)
  const selectedFiles = ref<UploadFile[]>([])

  const maxSizeBytes = maxSizeMB * 1024 * 1024

  const handleFileSelect = async (files: File[]) => {
    // 验证文件
    const validFiles = files.filter(file => {
      if (file.type !== 'application/pdf') {
        alert('请选择 PDF 文件')
        return false
      }
      if (file.size > maxSizeBytes) {
        alert(`文件 ${file.name} 超过大小限制`)
        return false
      }
      return true
    })

    if (selectedFiles.value.length + validFiles.length > maxFiles) {
      alert(`最多只能上传 ${maxFiles} 个文件`)
      return
    }

    // 添加到已选列表
    const newFiles: UploadFile[] = validFiles.map(file => ({
      id: Math.random().toString(36),
      name: file.name,
      size: file.size
    }))

    selectedFiles.value.push(...newFiles)

    // 自动上传
    await uploadFiles(validFiles)
  }

  const uploadFiles = async (files: File[]) => {
    isUploading.value = true
    progress.value = 0

    try {
      const formData = new FormData()
      files.forEach(file => formData.append('files', file))
      formData.append('tool_id', toolId)

      const response = await apiClient.post('/files/upload', formData, {
        onUploadProgress: (e) => {
          progress.value = Math.round((e.loaded * 100) / e.total)
        }
      })

      return response.data
    } finally {
      isUploading.value = false
    }
  }

  const removeFile = (id: string) => {
    selectedFiles.value = selectedFiles.value.filter(f => f.id !== id)
  }

  return {
    isUploading,
    progress,
    selectedFiles,
    handleFileSelect,
    uploadFiles,
    removeFile
  }
}
```

#### usePolling.ts

```typescript
import { ref, onUnmounted } from 'vue'
import { apiClient } from '@/api/client'

export function usePolling(jobId: string, interval = 1000) {
  const status = ref<JobStatus>('queued')
  const progress = ref(0)
  const message = ref('')
  const result = ref<Result | null>(null)
  const error = ref<string | null>(null)

  let timer: number | null = null

  const poll = async () => {
    try {
      const response = await apiClient.get(`/jobs/${jobId}`)
      const data = response.data.data

      status.value = data.status
      progress.value = data.progress
      message.value = data.message
      result.value = data.result

      if (data.status === 'completed' || data.status === 'failed') {
        if (timer) {
          clearInterval(timer)
          timer = null
        }
      }
    } catch (e) {
      error.value = '查询任务状态失败'
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    }
  }

  const startPolling = () => {
    timer = window.setInterval(poll, interval)
  }

  const stopPolling = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  onUnmounted(() => {
    stopPolling()
  })

  return {
    status,
    progress,
    message,
    result,
    error,
    startPolling,
    stopPolling
  }
}
```

---

## PDF 处理库选型

### PyMuPDF (fitz) - 主要选择

**选择理由**:

| 特性 | 说明 |
|------|------|
| **性能优秀** | 基于 MuPDF C 库，处理速度快 |
| **功能完整** | 支持合并、拆分、提取、水印等 |
| **内存友好** | 流式处理，适合大文件 |
| **维护活跃** | 持续更新，社区支持好 |
| **开源免费** | AGPL-3.0 许可证 |

**代码示例**:

```python
import fitz  # PyMuPDF

# 合并 PDF
def merge_pdfs(input_files: list[Path], output_path: Path) -> None:
    """合并多个 PDF 文件。"""
    result_doc = fitz.open()

    for file_path in input_files:
        with fitz.open(file_path) as doc:
            result_doc.insert_pdf(doc)

    result_doc.save(output_path)
    result_doc.close()

# 拆分 PDF
def split_pdf(
    input_path: Path,
    output_dir: Path,
    ranges: list[tuple[int, int]]
) -> list[Path]:
    """拆分 PDF 文件。"""
    output_files = []

    with fitz.open(input_path) as doc:
        for i, (start, end) in enumerate(ranges):
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start, to_page=end)

            output_path = output_dir / f"split_{i + 1}.pdf"
            new_doc.save(output_path)
            new_doc.close()

            output_files.append(output_path)

    return output_files

# 提取文本
def extract_text(input_path: Path) -> dict[int, str]:
    """提取 PDF 文本。"""
    text_by_page = {}

    with fitz.open(input_path) as doc:
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_by_page[page_num + 1] = page.get_text()

    return text_by_page

# 添加水印
def add_watermark(
    input_path: Path,
    output_path: Path,
    text: str,
    opacity: float = 0.3
) -> None:
    """为 PDF 添加文字水印。"""
    with fitz.open(input_path) as doc:
        for page in doc:
            # 创建水印页面
            rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
            page.insert_text(
                point=fitz.Point(page.rect.width / 2, page.rect.height / 2),
                text=text,
                fontsize=50,
                color=(0.5, 0.5, 0.5),
                fill_opacity=opacity,
                align=fitz.TEXT_ALIGN_CENTER
            )

        doc.save(output_path)

# 提取图片
def extract_images(input_path: Path, output_dir: Path) -> list[Path]:
    """提取 PDF 中的图片。"""
    output_files = []

    with fitz.open(input_path) as doc:
        image_count = 0

        for page_num, page in enumerate(doc):
            image_list = page.get_images()

            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)

                if base_image:
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    output_path = output_dir / f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                    output_path.write_bytes(image_bytes)
                    output_files.append(output_path)

                    image_count += 1

    return output_files
```

### pypdf - 辅助选择

**用途**: 简单操作、元数据提取

```python
from pypdf import PdfReader, PdfWriter

# 读取 PDF 信息
def get_pdf_info(file_path: Path) -> dict:
    """获取 PDF 信息。"""
    reader = PdfReader(file_path)

    return {
        "pages": len(reader.pages),
        "encrypted": reader.is_encrypted,
        "metadata": reader.metadata
    }
```

### Pillow - 图片处理

**用途**: 水印图片处理、PDF 转图片

```python
from PIL import Image, ImageDraw, ImageFont

def create_watermark_image(
    text: str,
    size: tuple[int, int] = (800, 600),
    opacity: int = 77  # 0-255
) -> Image.Image:
    """创建水印图片。"""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # 尝试使用系统字体
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    # 绘制旋转文字
    draw.text((100, 100), text, font=font, fill=(128, 128, 128, opacity))

    return img
```

### 库对比

| 库 | 优点 | 缺点 | 推荐用途 |
|----|------|------|----------|
| **PyMuPDF** | 性能高、功能全、文档好 | AGPL 许可证 | 主要处理库 |
| **pypdf** | 纯 Python、MIT 许可 | 性能较低 | 元数据读取 |
| **PyPDF2** | 简单易用 | 维护不活跃 | 简单操作 |
| **pdfplumber** | 文本提取精确 | 较慢 | 文本分析 |
| **Pillow** | 图片处理强大 | 非 PDF 专用 | 水印图片 |

**最终选择**: PyMuPDF (fitz) 作为主要处理库，pypdf 用于元数据读取，Pillow 用于图片水印。

---

## 安全性设计

### 文件安全

#### 1. 文件验证

```python
import magic
from pathlib import Path

ALLOWED_MIME_TYPES = {
    'application/pdf',
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

async def validate_file(file: UploadFile) -> bool:
    """验证上传文件。"""
    # 检查文件扩展名
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, '只支持 PDF 文件')

    # 检查 MIME 类型
    contents = await file.read()
    await file.seek(0)

    mime = magic.from_buffer(contents, mime=True)
    if mime not in ALLOWED_MIME_TYPES:
        raise HTTPException(400, '无效的文件类型')

    # 检查文件大小
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(413, '文件超过大小限制')

    # 检查是否为有效 PDF
    try:
        import fitz
        doc = fitz.open(stream=contents, filetype="pdf")
        doc.close()
    except Exception as e:
        raise HTTPException(400, '无效的 PDF 文件')

    return True
```

#### 2. 文件隔离

```python
# 每个上传使用唯一目录
def get_upload_dir(upload_id: str) -> Path:
    """获取上传目录。"""
    upload_dir = STORAGE_DIR / 'uploads' / upload_id
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir

# 文件名混淆
def sanitize_filename(filename: str) -> str:
    """清理文件名。"""
    # 保留扩展名，替换其他字符
    name = Path(filename).stem
    ext = Path(filename).suffix

    # 生成安全文件名
    safe_name = secrets.token_urlsafe(16)
    return f"{safe_name}{ext}"
```

#### 3. 自动清理

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def cleanup_expired_files():
    """清理过期文件。"""
    now = datetime.utcnow()

    # 清理上传文件
    for file_dir in (STORAGE_DIR / 'uploads').iterdir():
        if file_dir.is_dir():
            # 检查目录修改时间
            mtime = datetime.fromtimestamp(file_dir.stat().st_mtime)
            if (now - mtime) > timedelta(hours=2):
                shutil.rmtree(file_dir)

    # 清理结果文件
    for file_path in (STORAGE_DIR / 'results').iterdir():
        if file_path.is_file():
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if (now - mtime) > timedelta(hours=2):
                file_path.unlink()

# 定时任务
scheduler = AsyncIOScheduler()
scheduler.add_job(cleanup_expired_files, 'interval', minutes=30)
scheduler.start()
```

### API 安全

#### 1. 速率限制

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/files/upload")
@limiter.limit("10/minute")
async def upload_file(request: Request):
    ...
```

#### 2. CORS 配置

```python
from fastapi.middleware.cors import CORSMiddleware

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://pdftoolbox.example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

#### 3. 安全头

```python
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"

    return response
```

---

## 性能优化策略

### 后端优化

#### 1. 异步处理

```python
from fastapi import BackgroundTasks
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def process_pdf_task(job_id: str, tool_id: str, options: dict):
    """异步处理 PDF。"""
    processor = get_processor(tool_id)
    processor.process(job_id, options)

@app.post("/api/v1/jobs")
async def create_job(
    request: JobCreate,
    background_tasks: BackgroundTasks
):
    job = await job_service.create(request)
    background_tasks.add_task(process_pdf_task.delay, job.job_id, request.tool_id, request.options)
    return job
```

#### 2. 流式响应

```python
from fastapi.responses import StreamingResponse

@app.get("/api/v1/files/download/{file_id}")
async def download_file(file_id: str):
    file = await file_service.get(file_id)

    def iter_file():
        with open(file.path, 'rb') as f:
            while chunk := f.read(8192):
                yield chunk

    return StreamingResponse(
        iter_file(),
        media_type='application/pdf',
        headers={
            'Content-Disposition': f'attachment; filename="{file.name}"'
        }
    )
```

#### 3. 缓存策略

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@app.get("/api/v1/tools")
@cache(expire=3600)  # 缓存 1 小时
async def get_tools():
    return tool_service.get_all()
```

### 前端优化

#### 1. 代码分割

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/pages/Home.vue')
    },
    {
      path: '/tools/merge',
      component: () => import('@/pages/tools/MergePDF.vue')
    }
    // 其他路由
  ]
})
```

#### 2. 懒加载组件

```vue
<script setup lang="ts">
import { defineAsyncComponent } from 'vue'

const ToolCard = defineAsyncComponent(() =>
  import('@/components/business/ToolCard.vue')
)
</script>
```

#### 3. 图片优化

```vue
<template>
  <img
    :src="imageUrl"
    :srcset="`${imageUrl}?w=400 400w, ${imageUrl}?w=800 800w`"
    sizes="(max-width: 600px) 400px, 800px"
    loading="lazy"
    alt="..."
  />
</template>
```

---

## 部署架构

### 开发环境

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    command: pnpm dev

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./test.db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 生产环境

```
                                    ┌─────────────┐
                                    │    用户     │
                                    └──────┬──────┘
                                           │
                                           ▼
                              ┌────────────────────────┐
                              │     CloudFlare CDN     │
                              │    (静态资源 + DDoS)   │
                              └────────────┬───────────┘
                                           │
                              ┌────────────▼───────────┐
                              │      负载均衡器        │
                              └────────────┬───────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
           ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
           │  Nginx #1      │    │  Nginx #2      │    │  Nginx #3      │
           │  (静态文件)    │    │  (静态文件)    │    │  (静态文件)    │
           └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
                   │                      │                      │
                   └──────────────────────┼──────────────────────┘
                                          ▼
                              ┌────────────────────────┐
                              │      API 网关          │
                              └────────────┬───────────┘
                                           │
                    ┌──────────────────────┼──────────────────────┐
                    ▼                      ▼                      ▼
           ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
           │ FastAPI Worker │    │ FastAPI Worker │    │ FastAPI Worker │
           │   (Uvicorn)    │    │   (Uvicorn)    │    │   (Uvicorn)    │
           └───────┬────────┘    └───────┬────────┘    └───────┬────────┘
                   │                      │                      │
                   └──────────────────────┼──────────────────────┘
                                          ▼
           ┌────────────────────────────────────────────────────────┐
           │                       服务层                           │
           │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
           │  │ 文件服务  │  │ 任务服务  │  │ 工具服务  │           │
           │  └──────────┘  └──────────┘  └──────────┘           │
           └────────────────────────────────────────────────────────┘
                    │                      │                      │
                    ▼                      ▼                      ▼
           ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
           │    Redis #1    │    │    Redis #2    │    │   PostgreSQL   │
           │   (主节点)     │    │   (从节点)     │    │   (主从复制)   │
           └────────────────┘    └────────────────┘    └────────────────┘
```

### Docker 配置

#### Dockerfile.backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    libmupdf-dev \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN uv pip install --system -r requirements.txt

# 复制代码
COPY . .

# 创建存储目录
RUN mkdir -p storage/uploads storage/results storage/temp

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

#### Dockerfile.frontend

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# 安装 pnpm
RUN npm install -g pnpm

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install

# 复制代码
COPY . .

# 构建
RUN pnpm build

# 生产环境
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## 监控与日志

### 日志配置

```python
# core/logging.py
import logging
from pathlib import Path

def setup_logging():
    """配置日志。"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 配置格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 文件处理器
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
```

### 性能监控

```python
from prometheus_client import Counter, Histogram, generate_latest

# 指标
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# 中间件
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response

# 指标端点
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

---

## 附录

### A. 环境变量配置

```bash
# backend/.env.example

# 应用配置
APP_NAME=PDF工具箱
APP_ENV=production
APP_DEBUG=false
APP_URL=https://pdftoolbox.example.com

# 数据库
DATABASE_URL=postgresql://user:password@localhost/pdftoolbox

# Redis
REDIS_URL=redis://localhost:6379/0

# 文件存储
STORAGE_TYPE=local  # local | s3 | oss
STORAGE_PATH=./storage
MAX_FILE_SIZE=104857600  # 100MB
UPLOAD_EXPIRE_HOURS=2

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# 安全
SECRET_KEY=your-secret-key-here
ALLOWED_ORIGINS=https://pdftoolbox.example.com

# 日志
LOG_LEVEL=INFO

# OSS (可选)
OSS_ACCESS_KEY_ID=
OSS_ACCESS_KEY_SECRET=
OSS_BUCKET=
OSS_ENDPOINT=
```

### B. 技术栈版本锁定

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
PyMuPDF==1.23.8
Pillow==10.1.0
celery==5.3.4
redis==5.0.1
aiofiles==23.2.1
python-magic==0.4.27
python-dotenv==1.0.0
httpx==0.25.2
slowapi==0.1.9
prometheus-client==0.19.0
```

```json
// frontend/package.json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "@vueuse/core": "^10.7.0",
    "axios": "^1.6.2"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.3.3",
    "vite": "^5.0.8",
    "vitest": "^1.1.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

---

**文档结束**

本架构设计文档定义了 PDF 文档工具网站的完整技术架构，包括技术栈选型、系统设计、API 规范、数据模型、前端组件和部署方案。按照此架构实施，可以构建一个高性能、可扩展、安全的 PDF 处理服务平台。
