# PDF 文档工具网站

> 简单、快速的在线 PDF 工具 - 无需注册，完全免费，保护隐私

## 项目概述

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

## 技术栈

### 前端
- **Vue 3** + TypeScript
- **Vite** 5.0 - 构建工具
- **Pinia** - 状态管理
- **Vue Router** - 路由
- **Shadcn/ui** + Tailwind CSS - UI 组件

### 后端
- **FastAPI** - Web 框架
- **Python 3.11+**
- **PyMuPDF** - PDF 处理
- **Redis** - 任务队列/缓存

## 项目结构

```
pdftoolbox/
├── frontend/              # 前端项目 (Vue 3)
├── backend/               # 后端项目 (FastAPI)
├── deployment/            # 部署配置
├── doc/                   # 文档
└── README.md
```

## 快速开始

### 前置要求

- **Node.js** 18+
- **pnpm** (推荐) 或 cnpm
- **Python** 3.11+
- **uv** (Python 虚拟环境管理)

### 安装 pnpm

```bash
npm install -g pnpm
```

### 安装 uv

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 前端开发

```bash
cd frontend
pnpm install
pnpm dev
```

访问 http://localhost:5173

### 后端开发

```bash
cd backend
uv venv
.venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
uvicorn app:app --reload
```

访问 http://localhost:8000

### Docker 部署

```bash
docker-compose up -d
```

## 开发规范

### 代码风格
- **Python**: 遵循 PEP 8 + Black
- **TypeScript**: 遵循项目 ESLint 配置
- **Vue**: 使用 Composition API + `<script setup>`

### Git 提交规范
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档
- `test`: 测试
- `refactor`: 重构

## 文档

- [架构设计](doc/design/architecture.md)
- [API 设计](doc/design/api.md)
- [前端设计](doc/design/frontend.md)
- [实施计划](doc/implementation-plan.md)

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

**注意**: 本项目正在开发中，功能尚未完善。
