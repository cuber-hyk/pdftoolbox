# PDF 文档工具网站 - API 接口规范

> **版本**: 1.0
> **日期**: 2026-02-05
> **Base URL**: `https://api.pdftoolbox.example.com/api/v1`

---

## 目录

1. [概述](#概述)
2. [通用规范](#通用规范)
3. [认证授权](#认证授权)
4. [工具 API](#工具-api)
5. [文件 API](#文件-api)
6. [任务 API](#任务-api)
7. [错误处理](#错误处理)
8. [速率限制](#速率限制)
9. [Webhook (可选)](#webhook-可选)

---

## 概述

### API 版本

当前版本: `v1`

版本策略: URL 路径版本控制

示例: `/api/v1/tools`, `/api/v2/tools` (未来)

### 通信协议

- **协议**: HTTPS
- **格式**: JSON
- **字符编码**: UTF-8

### 基础 URL

```
开发环境: http://localhost:8000/api/v1
生产环境: https://api.pdftoolbox.example.com/api/v1
```

---

## 通用规范

### 请求格式

#### Headers

```http
Content-Type: application/json
Accept: application/json
User-Agent: PDFToolbox-Frontend/1.0
```

#### 请求体

```json
{
  "field1": "value1",
  "field2": "value2"
}
```

### 响应格式

#### 成功响应

```json
{
  "success": true,
  "data": {
    // 响应数据
  },
  "message": "操作成功"  // 可选
}
```

#### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "ERR_INVALID_FILE",
    "message": "无效的 PDF 文件",
    "details": {
      "file_id": "f_xxxxx",
      "reason": "文件头签名不匹配"
    }
  }
}
```

### HTTP 状态码

| 状态码 | 说明 | 使用场景 |
|--------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功 |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未授权 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 413 | Payload Too Large | 文件过大 |
| 415 | Unsupported Media Type | 不支持的文件类型 |
| 422 | Unprocessable Entity | 验证失败 |
| 429 | Too Many Requests | 速率限制 |
| 500 | Internal Server Error | 服务器错误 |
| 503 | Service Unavailable | 服务不可用 |

### 时间格式

所有时间字段使用 ISO 8601 格式 (UTC):

```json
{
  "created_at": "2026-02-05T10:00:00Z",
  "expires_at": "2026-02-05T12:00:00Z"
}
```

### 分页

```http
GET /api/v1/jobs?page=1&limit=20

Response:
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

---

## 认证授权

> 注意: 当前版本为公开服务，无需认证。未来版本可能添加用户系统。

### 公开访问

大部分 API 端点为公开访问，无需 Token。

### 速率限制

基于 IP 地址的速率限制:

| 端点类型 | 限制 | 时间窗口 |
|----------|------|----------|
| 文件上传 | 10 次 | 1 分钟 |
| 创建任务 | 20 次 | 1 分钟 |
| 查询任务 | 60 次 | 1 分钟 |
| 文件下载 | 30 次 | 1 分钟 |

响应头:

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1707110400
```

---

## 工具 API

### 获取工具列表

获取所有可用的 PDF 工具。

**请求**

```http
GET /api/v1/tools
```

**响应**

```json
{
  "success": true,
  "data": [
    {
      "id": "merge",
      "name": "PDF 合并",
      "description": "将多个 PDF 文件合并为一个文件，支持拖拽调整顺序",
      "icon": "merge",
      "route": "/tools/merge",
      "category": "基础工具",
      "max_files": 20,
      "max_size_mb": 100,
      "max_total_size_mb": 200,
      "options": [
        {
          "name": "output_filename",
          "type": "string",
          "label": "输出文件名",
          "default": "merged.pdf",
          "required": false
        }
      ]
    },
    {
      "id": "split",
      "name": "PDF 拆分",
      "description": "将一个 PDF 文件拆分为多个文件",
      "icon": "scissors",
      "route": "/tools/split",
      "category": "基础工具",
      "max_files": 1,
      "max_size_mb": 100,
      "max_total_size_mb": 100,
      "options": [
        {
          "name": "mode",
          "type": "select",
          "label": "拆分模式",
          "options": [
            { "value": "range", "label": "页码范围" },
            { "value": "every", "label": "每隔 N 页" },
            { "value": "single", "label": "每页单独文件" }
          ],
          "default": "range"
        },
        {
          "name": "ranges",
          "type": "array",
          "label": "页码范围",
          "description": "例如: [[1, 3], [5, 7]] 表示 1-3 页, 5-7 页",
          "required": false,
          "visible_when": { "mode": "range" }
        }
      ]
    },
    {
      "id": "extract_pages",
      "name": "页面提取",
      "description": "从 PDF 中提取指定页面生成新文件",
      "icon": "file-text",
      "route": "/tools/extract-pages",
      "category": "提取工具",
      "max_files": 1,
      "max_size_mb": 100,
      "max_total_size_mb": 100,
      "options": [
        {
          "name": "pages",
          "type": "string",
          "label": "页码",
          "description": "例如: 1,3,5-7,9",
          "placeholder": "1,3,5-7,9",
          "required": true
        }
      ]
    },
    {
      "id": "extract_text",
      "name": "文本提取",
      "description": "提取 PDF 中的文本内容",
      "icon": "type",
      "route": "/tools/extract-text",
      "category": "提取工具",
      "max_files": 1,
      "max_size_mb": 50,
      "max_total_size_mb": 50,
      "options": [
        {
          "name": "format",
          "type": "select",
          "label": "输出格式",
          "options": [
            { "value": "txt", "label": "纯文本 (.txt)" },
            { "value": "json", "label": "JSON (.json)" }
          ],
          "default": "txt"
        }
      ]
    },
    {
      "id": "extract_images",
      "name": "图片提取",
      "description": "提取 PDF 中的所有图片",
      "icon": "image",
      "route": "/tools/extract-images",
      "category": "提取工具",
      "max_files": 1,
      "max_size_mb": 100,
      "max_total_size_mb": 100,
      "options": [
        {
          "name": "format",
          "type": "select",
          "label": "输出格式",
          "options": [
            { "value": "original", "label": "保持原格式" },
            { "value": "png", "label": "转换为 PNG" },
            { "value": "jpg", "label": "转换为 JPG" }
          ],
          "default": "original"
        },
        {
          "name": "zip",
          "type": "boolean",
          "label": "打包为 ZIP",
          "default": true
        }
      ]
    },
    {
      "id": "add_watermark",
      "name": "添加水印",
      "description": "为 PDF 添加文字或图片水印",
      "icon": "droplet",
      "route": "/tools/add-watermark",
      "category": "水印工具",
      "max_files": 1,
      "max_size_mb": 100,
      "max_total_size_mb": 100,
      "options": [
        {
          "name": "type",
          "type": "select",
          "label": "水印类型",
          "options": [
            { "value": "text", "label": "文字水印" },
            { "value": "image", "label": "图片水印" }
          ],
          "default": "text"
        },
        {
          "name": "text",
          "type": "string",
          "label": "水印文字",
          "placeholder": "输入水印文字",
          "required": false,
          "visible_when": { "type": "text" }
        },
        {
          "name": "opacity",
          "type": "number",
          "label": "透明度",
          "min": 0,
          "max": 100,
          "default": 30,
          "suffix": "%"
        },
        {
          "name": "rotation",
          "type": "number",
          "label": "旋转角度",
          "min": 0,
          "max": 360,
          "default": 45,
          "suffix": "°"
        },
        {
          "name": "image_file",
          "type": "file",
          "label": "水印图片",
          "accept": ["image/png", "image/jpeg"],
          "required": false,
          "visible_when": { "type": "image" }
        }
      ]
    },
    {
      "id": "remove_watermark",
      "name": "去除水印",
      "description": "尝试去除 PDF 中的水印 (非 100% 成功)",
      "icon": "eraser",
      "route": "/tools/remove-watermark",
      "category": "水印工具",
      "max_files": 1,
      "max_size_mb": 50,
      "max_total_size_mb": 50,
      "options": [],
      "warning": "此功能基于启发式算法，不能保证完全去除水印"
    },
    {
      "id": "pdf_to_images",
      "name": "PDF 转图片",
      "description": "将 PDF 页面转换为图片",
      "icon": "image",
      "route": "/tools/pdf-to-images",
      "category": "转换工具",
      "max_files": 1,
      "max_size_mb": 100,
      "max_total_size_mb": 100,
      "options": [
        {
          "name": "format",
          "type": "select",
          "label": "输出格式",
          "options": [
            { "value": "png", "label": "PNG" },
            { "value": "jpg", "label": "JPG" },
            { "value": "webp", "label": "WebP" }
          ],
          "default": "png"
        },
        {
          "name": "dpi",
          "type": "select",
          "label": "分辨率",
          "options": [
            { "value": 72, "label": "72 DPI (屏幕)" },
            { "value": 150, "label": "150 DPI (高清)" },
            { "value": 300, "label": "300 DPI (打印)" }
          ],
          "default": 150
        },
        {
          "name": "pages",
          "type": "string",
          "label": "页码",
          "description": "留空表示全部页面，例如: 1,3,5-7",
          "placeholder": "留空表示全部",
          "required": false
        },
        {
          "name": "zip",
          "type": "boolean",
          "label": "打包为 ZIP",
          "default": true
        }
      ]
    }
  ]
}
```

### 获取单个工具

获取指定工具的详细信息。

**请求**

```http
GET /api/v1/tools/{tool_id}
```

**路径参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| tool_id | string | 是 | 工具 ID |

**响应**

```json
{
  "success": true,
  "data": {
    "id": "merge",
    "name": "PDF 合并",
    "description": "将多个 PDF 文件合并为一个文件",
    "icon": "merge",
    "route": "/tools/merge",
    "category": "基础工具",
    "max_files": 20,
    "max_size_mb": 100,
    "max_total_size_mb": 200,
    "options": [...],
    "examples": [
      {
        "name": "合并两个文件",
        "options": {
          "output_filename": "merged.pdf"
        }
      }
    ]
  }
}
```

---

## 文件 API

### 上传文件

上传一个或多个 PDF 文件。

**请求**

```http
POST /api/v1/files/upload
Content-Type: multipart/form-data
```

**表单数据**

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| files | File[] | 是 | PDF 文件列表 (最多 20 个) |
| tool_id | string | 是 | 目标工具 ID |

**请求示例**

```bash
curl -X POST https://api.pdftoolbox.example.com/api/v1/files/upload \
  -F "files=@document1.pdf" \
  -F "files=@document2.pdf" \
  -F "tool_id=merge"
```

**响应**

```json
{
  "success": true,
  "data": {
    "upload_id": "ul_a1b2c3d4e5f6",
    "files": [
      {
        "file_id": "f_abc123",
        "name": "document1.pdf",
        "size": 2048576,
        "pages": 10,
        "metadata": {
          "title": "Document 1",
          "author": "Unknown",
          "created": "2026-01-01T00:00:00Z"
        }
      },
      {
        "file_id": "f_def456",
        "name": "document2.pdf",
        "size": 1048576,
        "pages": 5,
        "metadata": {
          "title": "Document 2",
          "author": "Unknown",
          "created": "2026-01-02T00:00:00Z"
        }
      }
    ],
    "total_size": 3096576,
    "expires_at": "2026-02-05T12:00:00Z"
  }
}
```

**错误响应**

```json
{
  "success": false,
  "error": {
    "code": "ERR_FILE_TOO_LARGE",
    "message": "文件超过大小限制",
    "details": {
      "file": "large_document.pdf",
      "size": 157286400,
      "max_size": 104857600
    }
  }
}
```

### 下载文件

下载处理结果文件。

**请求**

```http
GET /api/v1/files/download/{file_id}
```

**路径参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| file_id | string | 是 | 文件 ID |

**响应**

- **状态码**: 200 OK
- **Content-Type**: `application/pdf` 或 `application/zip`
- **Content-Disposition**: `attachment; filename="result.pdf"`
- **Content-Length**: 文件大小

**请求示例**

```bash
curl -O https://api.pdftoolbox.example.com/api/v1/files/download/f_result123
```

**支持 Range 请求** (断点续传):

```http
GET /api/v1/files/download/{file_id}
Range: bytes=0-1048575

Response:
HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1048575/2097152
Content-Length: 1048576
```

### 删除文件

删除上传的文件 (手动清理)。

**请求**

```http
DELETE /api/v1/files/{file_id}
```

**响应**

```json
{
  "success": true,
  "message": "文件已删除"
}
```

---

## 任务 API

### 创建任务

创建一个 PDF 处理任务。

**请求**

```http
POST /api/v1/jobs
Content-Type: application/json
```

**请求体**

```json
{
  "tool_id": "merge",
  "upload_id": "ul_a1b2c3d4e5f6",
  "options": {
    "output_filename": "merged.pdf"
  }
}
```

**字段说明**

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| tool_id | string | 是 | 工具 ID |
| upload_id | string | 是 | 上传 ID |
| options | object | 否 | 处理选项 (工具特定) |

**响应**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "upload_id": "ul_a1b2c3d4e5f6",
    "status": "queued",
    "progress": 0,
    "message": "任务已加入队列",
    "created_at": "2026-02-05T10:00:00Z",
    "estimated_time": 30
  }
}
```

### 查询任务状态

查询任务的当前状态和进度。

**请求**

```http
GET /api/v1/jobs/{job_id}
```

**路径参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| job_id | string | 是 | 任务 ID |

**响应 (队列中)**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "upload_id": "ul_a1b2c3d4e5f6",
    "status": "queued",
    "progress": 0,
    "message": "等待处理中...",
    "queue_position": 3,
    "created_at": "2026-02-05T10:00:00Z"
  }
}
```

**响应 (处理中)**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "upload_id": "ul_a1b2c3d4e5f6",
    "status": "processing",
    "progress": 50,
    "message": "正在合并第 5 页，共 10 页",
    "created_at": "2026-02-05T10:00:00Z",
    "started_at": "2026-02-05T10:01:00Z",
    "estimated_remaining": 15
  }
}
```

**响应 (已完成)**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "upload_id": "ul_a1b2c3d4e5f6",
    "status": "completed",
    "progress": 100,
    "message": "处理完成",
    "created_at": "2026-02-05T10:00:00Z",
    "started_at": "2026-02-05T10:01:00Z",
    "completed_at": "2026-02-05T10:02:00Z",
    "processing_time_ms": 60000,
    "result": {
      "output_file_id": "f_result123",
      "filename": "merged.pdf",
      "size": 3096576,
      "pages": 15,
      "download_url": "/api/v1/files/download/f_result123",
      "expires_at": "2026-02-05T12:00:00Z"
    },
    "statistics": {
      "input_files": 2,
      "input_pages": 15,
      "output_pages": 15
    }
  }
}
```

**响应 (失败)**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "upload_id": "ul_a1b2c3d4e5f6",
    "status": "failed",
    "progress": 0,
    "message": "处理失败",
    "created_at": "2026-02-05T10:00:00Z",
    "started_at": "2026-02-05T10:01:00Z",
    "completed_at": "2026-02-05T10:01:30Z",
    "error": {
      "code": "ERR_ENCRYPTED_PDF",
      "message": "PDF 文件已加密，无法处理",
      "details": {
        "file": "document2.pdf",
        "suggestion": "请先移除密码保护后重试"
      }
    }
  }
}
```

### 取消任务

取消正在处理或排队中的任务。

**请求**

```http
DELETE /api/v1/jobs/{job_id}
```

**响应**

```json
{
  "success": true,
  "data": {
    "job_id": "job_xyz789",
    "status": "cancelled",
    "message": "任务已取消"
  }
}
```

**错误响应** (任务已完成)

```json
{
  "success": false,
  "error": {
    "code": "ERR_CANNOT_CANCEL",
    "message": "无法取消已完成的任务"
  }
}
```

### 批量查询任务状态

批量查询多个任务的状态。

**请求**

```http
POST /api/v1/jobs/batch-status
Content-Type: application/json
```

**请求体**

```json
{
  "job_ids": ["job_123", "job_456", "job_789"]
}
```

**响应**

```json
{
  "success": true,
  "data": {
    "jobs": [
      {
        "job_id": "job_123",
        "status": "completed",
        "progress": 100
      },
      {
        "job_id": "job_456",
        "status": "processing",
        "progress": 50
      },
      {
        "job_id": "job_789",
        "status": "queued",
        "progress": 0
      }
    ]
  }
}
```

### 任务列表 (可选 - 需要认证)

获取用户的任务历史记录。

**请求**

```http
GET /api/v1/jobs?page=1&limit=20&status=completed
```

**查询参数**

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码 (默认 1) |
| limit | integer | 否 | 每页数量 (默认 20) |
| status | string | 否 | 状态筛选 (queued/processing/completed/failed) |
| tool_id | string | 否 | 工具 ID 筛选 |

**响应**

```json
{
  "success": true,
  "data": {
    "items": [
      {
        "job_id": "job_123",
        "tool_id": "merge",
        "status": "completed",
        "created_at": "2026-02-05T10:00:00Z",
        "completed_at": "2026-02-05T10:02:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

---

## 错误处理

### 错误码列表

| 错误码 | HTTP 状态 | 说明 |
|--------|----------|------|
| `ERR_INVALID_REQUEST` | 400 | 请求参数无效 |
| `ERR_INVALID_FILE` | 400 | 无效的 PDF 文件 |
| `ERR_FILE_TOO_LARGE` | 413 | 文件超过大小限制 |
| `ERR_TOO_MANY_FILES` | 400 | 文件数量超过限制 |
| `ERR_FILE_CORRUPTED` | 400 | 文件损坏 |
| `ERR_ENCRYPTED_PDF` | 400 | PDF 已加密 |
| `ERR_INVALID_PAGES` | 400 | 页码范围无效 |
| `ERR_MISSING_FILE` | 400 | 缺少必需的文件 |
| `ERR_UNSUPPORTED_OPERATION` | 400 | 不支持的操作 |
| `ERR_TOOL_NOT_FOUND` | 404 | 工具不存在 |
| `ERR_JOB_NOT_FOUND` | 404 | 任务不存在 |
| `ERR_FILE_NOT_FOUND` | 404 | 文件不存在 |
| `ERR_FILE_EXPIRED` | 410 | 文件已过期 |
| `ERR_UPLOAD_FAILED` | 500 | 上传失败 |
| `ERR_PROCESSING_FAILED` | 500 | 处理失败 |
| `ERR_STORAGE_ERROR` | 500 | 存储错误 |
| `ERR_RATE_LIMIT_EXCEEDED` | 429 | 超过速率限制 |
| `ERR_SERVICE_UNAVAILABLE` | 503 | 服务不可用 |

### 错误响应示例

```json
{
  "success": false,
  "error": {
    "code": "ERR_ENCRYPTED_PDF",
    "message": "PDF 文件已加密，无法处理",
    "details": {
      "file": "document.pdf",
      "suggestion": "请先移除密码保护后重试",
      "help_url": "https://pdftoolbox.example.com/help/encrypted-pdf"
    }
  }
}
```

---

## 速率限制

### 限制策略

| 端点类型 | 限制 | 时间窗口 |
|----------|------|----------|
| 文件上传 | 10 次 | 1 分钟 |
| 创建任务 | 20 次 | 1 分钟 |
| 查询任务 | 60 次 | 1 分钟 |
| 文件下载 | 30 次 | 1 分钟 |
| 批量查询 | 10 次 | 1 分钟 |

### 响应头

```http
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 7
X-RateLimit-Reset: 1707110400
```

### 超限响应

```json
{
  "success": false,
  "error": {
    "code": "ERR_RATE_LIMIT_EXCEEDED",
    "message": "超过速率限制",
    "details": {
      "limit": 10,
      "window": "1 minute",
      "retry_after": 45
    }
  }
}
```

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 45
```

---

## Webhook (可选)

> 可选功能，用于任务完成时通知客户端。

### 注册 Webhook

**请求**

```http
POST /api/v1/webhooks
Content-Type: application/json
```

**请求体**

```json
{
  "url": "https://example.com/webhook/pdf",
  "events": ["job.completed", "job.failed"],
  "secret": "webhook_secret_key"
}
```

**响应**

```json
{
  "success": true,
  "data": {
    "webhook_id": "wh_abc123",
    "url": "https://example.com/webhook/pdf",
    "events": ["job.completed", "job.failed"],
    "secret": "webhook_secret_key",
    "created_at": "2026-02-05T10:00:00Z"
  }
}
```

### Webhook 事件

#### job.completed

```json
{
  "event": "job.completed",
  "timestamp": "2026-02-05T10:02:00Z",
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "result": {
      "output_file_id": "f_result123",
      "download_url": "/api/v1/files/download/f_result123"
    }
  }
}
```

#### job.failed

```json
{
  "event": "job.failed",
  "timestamp": "2026-02-05T10:01:30Z",
  "data": {
    "job_id": "job_xyz789",
    "tool_id": "merge",
    "error": {
      "code": "ERR_ENCRYPTED_PDF",
      "message": "PDF 文件已加密"
    }
  }
}
```

---

## 附录

### 数据类型

#### ToolOption

```typescript
interface ToolOption {
  name: string
  type: 'string' | 'number' | 'boolean' | 'select' | 'array' | 'file'
  label: string
  description?: string
  placeholder?: string
  default?: any
  required?: boolean
  min?: number
  max?: number
  suffix?: string
  options?: Array<{ value: string; label: string }>
  visible_when?: Record<string, string>
  accept?: string[]
}
```

#### JobStatus

```typescript
type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled'
```

#### FileInfo

```typescript
interface FileInfo {
  file_id: string
  name: string
  size: number
  pages: number
  metadata?: {
    title?: string
    author?: string
    subject?: string
    keywords?: string
    creator?: string
    created?: string
  }
}
```

### 工具选项示例

#### 合并 PDF

```json
{
  "tool_id": "merge",
  "options": {
    "output_filename": "merged.pdf"
  }
}
```

#### 拆分 PDF (页码范围)

```json
{
  "tool_id": "split",
  "options": {
    "mode": "range",
    "ranges": [[1, 5], [6, 10]]
  }
}
```

#### 拆分 PDF (每隔 N 页)

```json
{
  "tool_id": "split",
  "options": {
    "mode": "every",
    "every_n": 3
  }
}
```

#### 提取页面

```json
{
  "tool_id": "extract_pages",
  "options": {
    "pages": "1,3,5-7,9"
  }
}
```

#### 添加文字水印

```json
{
  "tool_id": "add_watermark",
  "options": {
    "type": "text",
    "text": "机密文件",
    "opacity": 30,
    "rotation": 45,
    "font_size": 48,
    "color": "#FF0000"
  }
}
```

#### PDF 转图片

```json
{
  "tool_id": "pdf_to_images",
  "options": {
    "format": "png",
    "dpi": 150,
    "pages": "1,3,5-7",
    "zip": true
  }
}
```

---

**文档结束**
