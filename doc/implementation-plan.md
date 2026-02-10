# PDF 文档工具网站 - 实施计划

> **版本**: 1.0
> **日期**: 2026-02-05
> **预计工期**: 6 周 (40 工作日)
> **优先级**: 按功能优先级排序

---

## 目录

1. [项目初始化](#1-项目初始化-3-天)
2. [后端开发](#2-后端开发-10-天)
3. [前端开发](#3-前端开发-10-天)
4. [集成测试](#4-集成测试-3-天)
5. [部署准备](#5-部署准备-2-天)
6. [里程碑](#里程碑)
7. [风险评估](#风险评估)

---

## 1. 项目初始化 (3 天)

### 1.1 目录结构设计 (Day 1 - 2h)

**负责人**: 开发者

**交付物**:
- 完整的项目目录结构
- README 文件
- .gitignore 配置

**任务列表**:

```bash
# 创建项目根目录结构
E:\pdftoolbox\
├── frontend/              # 前端项目 (Vue 3)
├── backend/               # 后端项目 (FastAPI)
├── deployment/            # 部署配置
├── doc/                   # 文档
│   ├── design/           # 设计文档 ✓
│   ├── plans/            # 实施计划
│   └── api/              # API 文档
└── README.md
```

**验收标准**:
- [ ] 所有目录创建完成
- [ ] .gitignore 配置正确 (包含 node_modules, .venv, storage/)
- [ ] README.md 包含项目概述和快速开始指南

---

### 1.2 前端项目脚手架 (Day 1 - 3h)

**负责人**: 前端开发者

**技术栈**:
- Vue 3 + TypeScript
- Vite 5.0
- Pinia 2.1
- Vue Router 4.2
- Shadcn/ui + Tailwind CSS

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 初始化 Vite 项目 (Vue 3 + TS) | 30min | - | P0 |
| 配置 Tailwind CSS | 30min | 初始化完成 | P0 |
| 配置 Shadcn/ui | 1h | Tailwind 完成 | P0 |
| 配置 Vue Router | 30min | 初始化完成 | P0 |
| 配置 Pinia | 30min | 初始化完成 | P0 |
| 配置 ESLint + Prettier | 30min | 初始化完成 | P1 |
| 配置 Vite 别名 (@/src) | 15min | 初始化完成 | P1 |

**命令**:

```bash
# 使用 pnpm (禁止使用 npm)
cd E:\pdftoolbox
pnpm create vite@latest frontend -- --template vue-ts
cd frontend
pnpm install

# 安装核心依赖
pnpm add vue@^3.4.0 vue-router@^4.2.5 pinia@^2.1.7 @vueuse/core@^10.7.0 axios@^1.6.2

# 安装开发依赖
pnpm add -D @vitejs/plugin-vue@^5.0.0 typescript@^5.3.3 vite@^5.0.8
pnpm add -D tailwindcss@^3.4.0 autoprefixer@^10.4.16 postcss@^8.4.32
pnpm add -D @vueuse/core@^10.7.0

# 初始化 Tailwind
pnpm exec tailwindcss init -p

# 配置 Shadcn/ui
pnpm dlx shadcn-vue@latest init
```

**验收标准**:
- [ ] `pnpm dev` 启动成功，无报错
- [ ] 访问 http://localhost:5173 显示默认页面
- [ ] Tailwind CSS 类名生效
- [ ] TypeScript 无类型错误

---

### 1.3 后端项目脚手架 (Day 1 - 2h)

**负责人**: 后端开发者

**技术栈**:
- FastAPI 0.104+
- Python 3.11+
- Pydantic 2.4+
- Uvicorn 0.24+

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 创建虚拟环境 (uv) | 15min | - | P0 |
| 初始化 FastAPI 项目 | 30min | 虚拟环境 | P0 |
| 配置 Pydantic Schemas | 1h | FastAPI 完成 | P0 |
| 配置目录结构 | 30min | - | P0 |
| 配置日志系统 | 30min | 目录结构 | P1 |
| 配置环境变量 | 15min | - | P0 |

**命令**:

```bash
# 使用 uv (禁止使用系统 Python)
cd E:\pdftoolbox\backend
uv venv
.venv\Scripts\activate  # Windows

# 安装核心依赖
uv pip install fastapi==0.104.1 uvicorn[standard]==0.24.0
uv pip install pydantic==2.5.0 python-multipart==0.0.6
uv pip install PyMuPDF==1.23.8 Pillow==10.1.0
uv pip install aiofiles==23.2.1 python-dotenv==1.0.0

# 保存依赖到 requirements.txt
uv pip freeze > requirements.txt
```

**目录结构**:

```
backend/
├── api/
│   ├── __init__.py
│   ├── deps.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── tools.py
│   │   ├── files.py
│   │   └── jobs.py
│   └── middleware/
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── logging.py
├── schemas/
│   ├── __init__.py
│   ├── tools.py
│   ├── files.py
│   └── jobs.py
├── services/
│   └── __init__.py
├── processors/
│   └── __init__.py
├── storage/
│   ├── uploads/
│   ├── results/
│   └── temp/
├── .env.example
├── app.py
├── pyproject.toml
└── requirements.txt
```

**验收标准**:
- [ ] `uvicorn app:app --reload` 启动成功
- [ ] 访问 http://localhost:8000 显示 FastAPI 欢迎页
- [ ] 访问 http://localhost:8000/docs 显示 Swagger UI
- [ ] Python 代码无 lint 错误

---

### 1.4 开发环境配置 (Day 1 - 1h)

**负责人**: 全栈开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 配置前后端代理 (Vite) | 30min | 前后端脚手架 | P0 |
| 配置环境变量文件 | 15min | - | P0 |
| 配置启动脚本 | 15min | - | P1 |

**前端 Vite 配置** (`frontend/vite.config.ts`):

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**后端环境变量** (`backend/.env.example`):

```env
# 应用配置
APP_NAME=PDF工具箱
APP_ENV=development
APP_DEBUG=true
APP_URL=http://localhost:8000

# CORS
ALLOWED_ORIGINS=http://localhost:5173

# 文件存储
STORAGE_PATH=./storage
MAX_FILE_SIZE=104857600
UPLOAD_EXPIRE_HOURS=2

# 日志
LOG_LEVEL=INFO
```

**验收标准**:
- [ ] 前端可以访问后端 API (/api/v1/tools)
- [ ] 环境变量正确加载
- [ ] CORS 配置生效

---

### 1.5 TypeScript/Python 类型定义 (Day 2 - 4h)

**负责人**: 全栈开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 定义前端 TypeScript 类型 | 2h | 前端脚手架 | P0 |
| 定义后端 Pydantic Schemas | 2h | 后端脚手架 | P0 |

**前端类型定义** (`frontend/src/types/index.ts`):

```typescript
export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled'

export interface Tool {
  id: string
  name: string
  description: string
  icon: string
  route: string
  category: string
  max_files: number
  max_size_mb: number
  max_total_size_mb: number
  options: ToolOption[]
}

export interface ToolOption {
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

export interface UploadedFile {
  file_id: string
  name: string
  size: number
  pages?: number
  metadata?: {
    title?: string
    author?: string
    created?: string
  }
}

export interface Job {
  job_id: string
  tool_id: string
  upload_id: string
  status: JobStatus
  progress: number
  message: string
  input_files: string[]
  output_file?: string
  options: Record<string, any>
  created_at: string
  started_at?: string
  completed_at?: string
  expires_at?: string
  error?: {
    code: string
    message: string
    details?: any
  }
  result?: {
    output_file_id: string
    filename: string
    size: number
    pages?: number
    download_url: string
    expires_at: string
  }
}

export interface APIResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: any
  }
}
```

**后端 Schemas** (`backend/schemas/`):

```python
# schemas/tools.py
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class ToolOption(BaseModel):
    name: str
    type: str
    label: str
    description: Optional[str] = None
    placeholder: Optional[str] = None
    default: Optional[Any] = None
    required: bool = False
    min: Optional[float] = None
    max: Optional[float] = None
    suffix: Optional[str] = None
    options: Optional[List[Dict[str, str]]] = None
    visible_when: Optional[Dict[str, str]] = None
    accept: Optional[List[str]] = None

class Tool(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    route: str
    category: str
    max_files: int
    max_size_mb: int
    max_total_size_mb: int
    options: List[ToolOption] = []

# schemas/jobs.py
from enum import Enum
from datetime import datetime

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobCreate(BaseModel):
    tool_id: str
    upload_id: str
    options: Dict[str, Any] = {}

class JobResponse(BaseModel):
    job_id: str
    tool_id: str
    upload_id: str
    status: JobStatus
    progress: int
    message: str
    input_files: List[str] = []
    output_file: Optional[str] = None
    options: Dict[str, Any] = {}
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    error: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
```

**验收标准**:
- [ ] TypeScript 类型定义完整
- [ ] Pydantic Schemas 验证通过
- [ ] 前后端类型一致

---

## 2. 后端开发 (10 天)

### 2.1 核心服务层 (Day 3 - 4h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现文件服务 (file_service.py) | 1.5h | 类型定义 | P0 |
| 实现任务服务 (job_service.py) | 1.5h | 文件服务 | P0 |
| 实现工具服务 (tool_service.py) | 1h | - | P0 |

**文件服务** (`backend/services/file_service.py`):

```python
import aiofiles
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

class FileService:
    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.uploads_dir = self.storage_path / "uploads"
        self.results_dir = self.storage_path / "results"
        self.temp_dir = self.storage_path / "temp"

        # 创建目录
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def get_upload_dir(self, upload_id: str) -> Path:
        """获取上传目录。"""
        upload_dir = self.uploads_dir / upload_id
        upload_dir.mkdir(parents=True, exist_ok=True)
        return upload_dir

    def generate_file_id(self) -> str:
        """生成文件 ID。"""
        return f"f_{secrets.token_urlsafe(16)}"

    def generate_upload_id(self) -> str:
        """生成上传 ID。"""
        return f"ul_{secrets.token_urlsafe(16)}"

    def get_expires_at(self, hours: int = 2) -> datetime:
        """获取过期时间。"""
        return datetime.utcnow() + timedelta(hours=hours)

    async def save_file(self, upload_id: str, file_id: str, content: bytes, filename: str) -> Path:
        """保存文件。"""
        upload_dir = self.get_upload_dir(upload_id)
        file_path = upload_dir / f"{file_id}.pdf"
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        return file_path

    async def get_file(self, file_path: Path) -> bytes:
        """读取文件。"""
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    def delete_file(self, file_path: Path) -> None:
        """删除文件。"""
        if file_path.exists():
            file_path.unlink()
```

**任务服务** (`backend/services/job_service.py`):

```python
from datetime import datetime
from typing import Optional, Dict, Any
from schemas.jobs import JobCreate, JobResponse, JobStatus

class JobService:
    def __init__(self):
        # 简单内存存储，生产环境使用 Redis 或 PostgreSQL
        self.jobs: Dict[str, JobResponse] = {}

    def create_job(self, job_data: JobCreate) -> JobResponse:
        """创建任务。"""
        job_id = f"job_{secrets.token_urlsafe(16)}"

        job = JobResponse(
            job_id=job_id,
            tool_id=job_data.tool_id,
            upload_id=job_data.upload_id,
            status=JobStatus.QUEUED,
            progress=0,
            message="任务已创建",
            options=job_data.options,
            created_at=datetime.utcnow()
        )

        self.jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[JobResponse]:
        """获取任务。"""
        return self.jobs.get(job_id)

    def update_job(self, job_id: str, **updates) -> Optional[JobResponse]:
        """更新任务。"""
        job = self.jobs.get(job_id)
        if job:
            for key, value in updates.items():
                setattr(job, key, value)
            return job
        return None

    def update_progress(self, job_id: str, progress: int, message: str) -> None:
        """更新进度。"""
        self.update_job(job_id, progress=progress, message=message)

    def complete_job(self, job_id: str, result: Dict[str, Any]) -> None:
        """完成任务。"""
        self.update_job(
            job_id,
            status=JobStatus.COMPLETED,
            progress=100,
            message="处理完成",
            completed_at=datetime.utcnow(),
            result=result
        )

    def fail_job(self, job_id: str, error: Dict[str, Any]) -> None:
        """标记任务失败。"""
        self.update_job(
            job_id,
            status=JobStatus.FAILED,
            completed_at=datetime.utcnow(),
            error=error
        )
```

**验收标准**:
- [ ] 文件服务可以保存和读取文件
- [ ] 任务服务可以创建和更新任务
- [ ] 服务层单元测试通过

---

### 2.2 PDF 处理器基类 (Day 3 - 2h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现 BaseProcessor | 1.5h | - | P0 |
| 实现工具注册机制 | 30min | BaseProcessor | P0 |

**基类** (`backend/processors/base.py`):

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import fitz

class BaseProcessor(ABC):
    """PDF 处理器基类。"""

    def __init__(self, job_service):
        self.job_service = job_service

    @abstractmethod
    async def process(self, job_id: str, files: list[Path], options: Dict[str, Any]) -> str:
        """处理 PDF 文件。

        Args:
            job_id: 任务 ID
            files: 输入文件列表
            options: 处理选项

        Returns:
            输出文件 ID
        """
        pass

    def validate_pdf(self, file_path: Path) -> fitz.Document:
        """验证 PDF 文件。"""
        try:
            doc = fitz.open(file_path)
            if doc.is_encrypted:
                raise ValueError("PDF 文件已加密")
            return doc
        except Exception as e:
            raise ValueError(f"无效的 PDF 文件: {e}")

    def get_page_count(self, file_path: Path) -> int:
        """获取 PDF 页数。"""
        doc = fitz.open(file_path)
        count = len(doc)
        doc.close()
        return count
```

**工具注册** (`backend/processors/__init__.py`):

```python
from typing import Dict, Type
from .base import BaseProcessor

class ProcessorRegistry:
    """处理器注册表。"""

    def __init__(self):
        self._processors: Dict[str, Type[BaseProcessor]] = {}

    def register(self, tool_id: str):
        """装饰器：注册处理器。"""
        def decorator(processor_class: Type[BaseProcessor]):
            self._processors[tool_id] = processor_class
            return processor_class
        return decorator

    def get(self, tool_id: str) -> Type[BaseProcessor]:
        """获取处理器。"""
        processor = self._processors.get(tool_id)
        if not processor:
            raise ValueError(f"未知的工具 ID: {tool_id}")
        return processor

    def list_all(self) -> Dict[str, Type[BaseProcessor]]:
        """列出所有处理器。"""
        return self._processors

# 全局注册表
registry = ProcessorRegistry()
```

**验收标准**:
- [ ] BaseProcessor 定义完整
- [ ] 工具注册机制正常工作
- [ ] 基类单元测试通过

---

### 2.3 核心 API 实现 (Day 4 - 5h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现工具 API | 1h | 工具服务 | P0 |
| 实现文件上传 API | 2h | 文件服务 | P0 |
| 实现任务 API | 2h | 任务服务 | P0 |

**工具 API** (`backend/api/v1/tools.py`):

```python
from fastapi import APIRouter, HTTPException
from schemas.tools import Tool

router = APIRouter(prefix="/tools", tags=["tools"])

# 工具列表 (硬编码，后续可从数据库读取)
TOOLS: list[Tool] = [
    Tool(
        id="merge",
        name="PDF 合并",
        description="将多个 PDF 文件合并为一个文件，支持拖拽调整顺序",
        icon="merge",
        route="/tools/merge",
        category="基础工具",
        max_files=20,
        max_size_mb=100,
        max_total_size_mb=200,
        options=[
            {
                "name": "output_filename",
                "type": "string",
                "label": "输出文件名",
                "default": "merged.pdf",
                "required": False
            }
        ]
    ),
    # ... 更多工具
]

@router.get("", response_model=list[Tool])
async def get_tools() -> list[Tool]:
    """获取所有工具。"""
    return TOOLS

@router.get("/{tool_id}", response_model=Tool)
async def get_tool(tool_id: str) -> Tool:
    """获取单个工具。"""
    for tool in TOOLS:
        if tool.id == tool_id:
            return tool
    raise HTTPException(status_code=404, detail="工具不存在")
```

**文件上传 API** (`backend/api/v1/files.py`):

```python
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from services.file_service import FileService
from schemas.files import UploadResponse, FileInfo
import fitz

router = APIRouter(prefix="/files", tags=["files"])
file_service = FileService()

@router.post("/upload", response_model=UploadResponse)
async def upload_files(
    files: List[UploadFile] = File(...),
    tool_id: str = Form(...)
):
    """上传文件。"""

    # 验证工具 ID
    # ... (略)

    upload_id = file_service.generate_upload_id()
    uploaded_files = []

    for file in files:
        # 验证文件类型
        if not file.filename.endswith('.pdf'):
            raise HTTPException(400, f"只支持 PDF 文件: {file.filename}")

        # 读取文件内容
        content = await file.read()

        # 验证 PDF
        try:
            doc = fitz.open(stream=content, filetype="pdf")
            page_count = len(doc)
            doc.close()
        except Exception as e:
            raise HTTPException(400, f"无效的 PDF 文件: {file.filename}")

        # 保存文件
        file_id = file_service.generate_file_id()
        await file_service.save_file(upload_id, file_id, content, file.filename)

        uploaded_files.append(FileInfo(
            file_id=file_id,
            name=file.filename,
            size=len(content),
            pages=page_count
        ))

    return UploadResponse(
        upload_id=upload_id,
        files=uploaded_files,
        expires_at=file_service.get_expires_at()
    )
```

**任务 API** (`backend/api/v1/jobs.py`):

```python
from fastapi import APIRouter, HTTPException, BackgroundTasks
from schemas.jobs import JobCreate, JobResponse
from services.job_service import JobService
from processors import registry

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_service = JobService()

@router.post("", response_model=JobResponse, status_code=201)
async def create_job(request: JobCreate, background_tasks: BackgroundTasks):
    """创建处理任务。"""

    # 创建任务
    job = job_service.create_job(request)

    # 后台处理
    processor_class = registry.get(request.tool_id)
    processor = processor_class(job_service)
    background_tasks.add_task(processor.process, job.job_id, [], request.options)

    return job

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """获取任务状态。"""
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(404, detail="任务不存在")
    return job

@router.delete("/{job_id}")
async def cancel_job(job_id: str):
    """取消任务。"""
    job = job_service.get_job(job_id)
    if not job:
        raise HTTPException(404, detail="任务不存在")
    # TODO: 实现取消逻辑
    return {"message": "任务已取消"}
```

**验收标准**:
- [ ] GET /api/v1/tools 返回工具列表
- [ ] POST /api/v1/files/upload 上传成功
- [ ] POST /api/v1/jobs 创建任务成功
- [ ] GET /api/v1/jobs/{job_id} 返回任务状态

---

### 2.4 PDF 处理器实现 (Day 5-7, 3 天)

**负责人**: 后端开发者

**优先级**: 按 Phase 1 功能顺序实现

#### 2.4.1 合并处理器 (Day 5 - 3h)

**文件**: `backend/processors/merge.py`

```python
from pathlib import Path
from processors.base import BaseProcessor, registry
import fitz

@registry.register("merge")
class MergeProcessor(BaseProcessor):
    """PDF 合并处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """合并 PDF 文件。"""

        # 更新状态
        self.job_service.update_job(job_id, status="processing", started_at=datetime.now())

        output_filename = options.get("output_filename", "merged.pdf")
        output_path = self.results_dir / f"{job_id}_{output_filename}"

        try:
            result_doc = fitz.open()
            total_files = len(files)

            for i, file_path in enumerate(files):
                # 更新进度
                progress = int((i / total_files) * 100)
                self.job_service.update_progress(
                    job_id,
                    progress,
                    f"正在合并第 {i + 1} 个文件，共 {total_files} 个"
                )

                # 打开并插入 PDF
                with fitz.open(file_path) as doc:
                    result_doc.insert_pdf(doc)

            # 保存结果
            result_doc.save(output_path)
            result_doc.close()

            # 完成任务
            self.job_service.complete_job(job_id, {
                "output_file_id": f"f_{job_id}",
                "filename": output_filename,
                "size": output_path.stat().st_size,
                "download_url": f"/api/v1/files/download/f_{job_id}",
                "expires_at": (datetime.now() + timedelta(hours=2)).isoformat()
            })

            return f"f_{job_id}"

        except Exception as e:
            self.job_service.fail_job(job_id, {
                "code": "ERR_MERGE_FAILED",
                "message": str(e)
            })
            raise
```

#### 2.4.2 拆分处理器 (Day 5 - 3h)

**文件**: `backend/processors/split.py`

```python
@registry.register("split")
class SplitProcessor(BaseProcessor):
    """PDF 拆分处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """拆分 PDF 文件。"""

        mode = options.get("mode", "range")

        if mode == "range":
            return await self._split_by_range(job_id, files[0], options)
        elif mode == "every":
            return await self._split_by_every(job_id, files[0], options)
        else:
            raise ValueError(f"不支持的拆分模式: {mode}")

    async def _split_by_range(self, job_id: str, file_path: Path, options: dict) -> str:
        """按页码范围拆分。"""
        ranges = options.get("ranges", [[1, -1]])  # -1 表示到最后一页

        doc = fitz.open(file_path)
        output_files = []

        for i, (start, end) in enumerate(ranges):
            # 创建新文档
            new_doc = fitz.open()
            new_doc.insert_pdf(doc, from_page=start - 1, to_page=end if end == -1 else end - 1)

            output_path = self.results_dir / f"{job_id}_part_{i + 1}.pdf"
            new_doc.save(output_path)
            new_doc.close()

            output_files.append(output_path)

        doc.close()

        # 如果是单个文件，直接返回
        if len(output_files) == 1:
            # ... (返回逻辑)
            pass
        else:
            # 多个文件，打包为 ZIP
            # ... (ZIP 打包逻辑)
            pass

    async def _split_by_every(self, job_id: str, file_path: Path, options: dict) -> str:
        """每隔 N 页拆分。"""
        # ... (实现)
        pass
```

#### 2.4.3 提取处理器 (Day 6 - 4h)

**文件**: `backend/processors/extract.py`

```python
@registry.register("extract_pages")
class ExtractPagesProcessor(BaseProcessor):
    """页面提取处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """提取指定页面。"""
        # ... (实现)
        pass

@registry.register("extract_text")
class ExtractTextProcessor(BaseProcessor):
    """文本提取处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """提取文本内容。"""
        # ... (实现)
        pass

@registry.register("extract_images")
class ExtractImagesProcessor(BaseProcessor):
    """图片提取处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """提取图片。"""
        # ... (实现)
        pass
```

#### 2.4.4 水印处理器 (Day 7 - 4h)

**文件**: `backend/processors/watermark.py`

```python
@registry.register("add_watermark")
class AddWatermarkProcessor(BaseProcessor):
    """添加水印处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """添加水印。"""
        # ... (实现)
        pass

@registry.register("remove_watermark")
class RemoveWatermarkProcessor(BaseProcessor):
    """去除水印处理器。"""

    async def process(self, job_id: str, files: list[Path], options: dict) -> str:
        """尝试去除水印 (启发式算法)。"""
        # ... (实现)
        pass
```

**验收标准**:
- [ ] 所有 Phase 1 处理器实现完成
- [ ] 处理器单元测试覆盖率 > 80%
- [ ] 处理器集成测试通过

---

### 2.5 中间件与安全 (Day 8 - 2h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现 CORS 中间件 | 30min | - | P0 |
| 实现速率限制 | 1h | - | P0 |
| 实现安全头中间件 | 30min | - | P0 |

**CORS 配置** (`backend/api/middleware/cors.py`):

```python
from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """添加 CORS 中间件。"""
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "DELETE"],
        allow_headers=["*"],
    )
```

**速率限制** (`backend/api/middleware/rate_limit.py`):

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# 使用示例
# @router.post("/upload")
# @limiter.limit("10/minute")
# async def upload_file(...):
#     ...
```

**安全头** (`backend/api/middleware/security.py`):

```python
from fastapi import Request

async def add_security_headers(request: Request, call_next):
    """添加安全头。"""
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"

    return response
```

**验收标准**:
- [ ] CORS 配置生效
- [ ] 速率限制生效 (超过限制返回 429)
- [ ] 安全头正确设置

---

### 2.6 文件清理服务 (Day 9 - 1h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现定时清理任务 | 1h | - | P1 |

**清理服务** (`backend/services/cleanup_service.py`):

```python
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler

class CleanupService:
    """文件清理服务。"""

    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.scheduler = AsyncIOScheduler()

    async def cleanup_expired_files(self):
        """清理过期文件。"""
        now = datetime.now()
        expire_delta = timedelta(hours=2)

        # 清理上传文件
        uploads_dir = self.storage_path / "uploads"
        for upload_dir in uploads_dir.iterdir():
            if upload_dir.is_dir():
                mtime = datetime.fromtimestamp(upload_dir.stat().st_mtime)
                if (now - mtime) > expire_delta:
                    shutil.rmtree(upload_dir)

        # 清理结果文件
        results_dir = self.storage_path / "results"
        for file_path in results_dir.iterdir():
            if file_path.is_file():
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if (now - mtime) > expire_delta:
                    file_path.unlink()

    def start(self):
        """启动定时任务。"""
        self.scheduler.add_job(
            self.cleanup_expired_files,
            'interval',
            minutes=30
        )
        self.scheduler.start()
```

**验收标准**:
- [ ] 定时任务启动成功
- [ ] 过期文件自动删除

---

### 2.7 后端测试 (Day 10 - 6h)

**负责人**: 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 编写单元测试 | 3h | 所有后端代码 | P0 |
| 编写集成测试 | 2h | 单元测试 | P0 |
| 测试覆盖率检查 | 1h | 所有测试 | P0 |

**测试结构**:

```
backend/tests/
├── unit/
│   ├── test_file_service.py
│   ├── test_job_service.py
│   └── test_processors/
│       ├── test_merge.py
│       └── test_split.py
├── integration/
│   ├── test_api_upload.py
│   └── test_api_jobs.py
└── conftest.py
```

**单元测试示例** (`backend/tests/unit/test_file_service.py`):

```python
import pytest
from services.file_service import FileService

@pytest.fixture
def file_service(tmp_path):
    return FileService(storage_path=str(tmp_path))

def test_generate_file_id(file_service):
    file_id = file_service.generate_file_id()
    assert file_id.startswith("f_")
    assert len(file_id) > 10

@pytest.mark.asyncio
async def test_save_and_get_file(file_service):
    upload_id = file_service.generate_upload_id()
    file_id = file_service.generate_file_id()
    content = b"test content"

    await file_service.save_file(upload_id, file_id, content, "test.pdf")
    retrieved = await file_service.get_file(file_service.get_upload_dir(upload_id) / f"{file_id}.pdf")

    assert retrieved == content
```

**验收标准**:
- [ ] 单元测试覆盖率 > 80%
- [ ] 所有集成测试通过
- [ ] pytest 运行无报错

---

## 3. 前端开发 (10 天)

### 3.1 基础组件搭建 (Day 11-12, 2 天)

**负责人**: 前端开发者

**优先级**: P0 - 核心组件优先

#### 3.1.1 Shadcn/ui 组件安装 (Day 11 - 2h)

```bash
cd frontend

# 安装核心组件
pnpm dlx shadcn-vue@latest add button
pnpm dlx shadcn-vue@latest add card
pnpm dlx shadcn-vue@latest add input
pnpm dlx shadcn-vue@latest add progress
pnpm dlx shadcn-vue@latest add toast
pnpm dlx shadcn-vue@latest add dialog
```

**验收标准**:
- [ ] 所有组件安装成功
- [ ] 组件可以正常导入使用

#### 3.1.2 布局组件 (Day 11 - 3h)

**AppHeader.vue** (`frontend/src/components/layout/AppHeader.vue`):

```vue
<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/')
}
</script>

<template>
  <header class="h-16 px-4 md:px-6 flex items-center justify-between border-b bg-white">
    <!-- Logo -->
    <div class="flex items-center gap-2 cursor-pointer" @click="goHome">
      <div class="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <span class="text-lg font-bold text-slate-900 hidden sm:inline">PDF 工具箱</span>
    </div>

    <!-- 右侧操作 -->
    <div class="flex items-center gap-2">
      <a href="https://github.com" target="_blank" rel="noopener" class="p-2 hover:bg-slate-100 rounded-lg transition-colors">
        <svg class="w-5 h-5 text-slate-600" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
      </a>
    </div>
  </header>
</template>
```

**AppFooter.vue** (`frontend/src/components/layout/AppFooter.vue`):

```vue
<template>
  <footer class="py-8 px-4 border-t bg-slate-50">
    <div class="max-w-6xl mx-auto text-center text-sm text-slate-500">
      <p class="mb-2">© 2026 PDF 工具箱. 简单、快速的在线 PDF 工具</p>
      <div class="flex items-center justify-center gap-4">
        <a href="/privacy" class="hover:text-slate-700">隐私政策</a>
        <span>·</span>
        <a href="/terms" class="hover:text-slate-700">使用条款</a>
        <span>·</span>
        <a href="https://github.com" target="_blank" class="hover:text-slate-700">GitHub</a>
      </div>
    </div>
  </footer>
</template>
```

#### 3.1.3 业务组件 (Day 12 - 5h)

**ToolCard.vue** (`frontend/src/components/business/ToolCard.vue`):

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import type { Tool } from '@/types'

interface Props {
  tool: Tool
}

const props = defineProps<Props>()
const router = useRouter()

const handleClick = () => {
  router.push(props.tool.route)
}
</script>

<template>
  <button
    @click="handleClick"
    class="group p-6 rounded-2xl border border-slate-200 bg-white text-left
           hover:-translate-y-1 hover:shadow-lg hover:border-primary-300
           active:scale-[0.98]
           transition-all duration-300 ease-out
           min-w-[280px]"
  >
    <!-- 图标 -->
    <div class="flex items-center gap-3 mb-4">
      <div class="p-3 rounded-xl bg-primary-50 text-primary-600
                  group-hover:bg-primary-100 group-hover:scale-110
                  transition-all duration-300">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="tool.icon === 'merge'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
          <path v-else-if="tool.icon === 'scissors'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z" />
          <!-- 其他图标... -->
        </svg>
      </div>
      <h3 class="text-lg font-semibold text-slate-900">
        {{ tool.name }}
      </h3>
    </div>

    <!-- 描述 -->
    <p class="text-sm text-slate-500 leading-relaxed">
      {{ tool.description }}
    </p>

    <!-- 悬浮指示器 -->
    <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100
                transition-opacity duration-300">
      <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </div>
  </button>
</template>
```

**FileUploader.vue** (`frontend/src/components/business/FileUploader.vue`):

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import type { UploadedFile } from '@/types'

interface Props {
  toolId: string
  maxFiles?: number
  maxSize?: number
  accept?: string
}

const props = withDefaults(defineProps<Props>(), {
  maxFiles: 1,
  maxSize: 100,
  accept: 'application/pdf'
})

const emit = defineEmits<{
  uploaded: [uploadId: string, files: UploadedFile[]]
  error: [message: string]
}>()

const isDragging = ref(false)
const isUploading = ref(false)
const progress = ref(0)
const selectedFiles = ref<UploadedFile[]>([])

const maxSizeBytes = props.maxSize * 1024 * 1024

const validateFiles = (files: File[]): { valid: File[]; errors: string[] } => {
  const valid: File[] = []
  const errors: string[] = []

  files.forEach(file => {
    if (file.type !== 'application/pdf') {
      errors.push(`${file.name} 不是 PDF 文件`)
      return
    }
    if (file.size > maxSizeBytes) {
      errors.push(`${file.name} 超过 ${props.maxSize}MB 限制`)
      return
    }
    valid.push(file)
  })

  if (selectedFiles.value.length + valid.length > props.maxFiles) {
    errors.push(`最多只能上传 ${props.maxFiles} 个文件`)
    return { valid: [], errors }
  }

  return { valid, errors }
}

const handleDrop = async (e: DragEvent) => {
  e.preventDefault()
  isDragging.value = false
  const files = Array.from(e.dataTransfer?.files || [])
  await processFiles(files)
}

const handleFileSelect = async (files: File[]) => {
  await processFiles(files)
}

const processFiles = async (files: File[]) => {
  const { valid, errors } = validateFiles(files)
  errors.forEach(error => emit('error', error))
  if (valid.length === 0) return
  await uploadFiles(valid)
}

const uploadFiles = async (files: File[]) => {
  isUploading.value = true
  progress.value = 0

  try {
    const formData = new FormData()
    files.forEach(file => formData.append('files', file))
    formData.append('tool_id', props.toolId)

    const response = await fetch('/api/v1/files/upload', {
      method: 'POST',
      body: formData
    })

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.error?.message || '上传失败')
    }

    selectedFiles.value = [...selectedFiles.value, ...data.data.files]
    emit('uploaded', data.data.upload_id, data.data.files)
  } catch (error: any) {
    emit('error', error.message || '上传失败')
  } finally {
    isUploading.value = false
  }
}

const removeFile = (fileId: string) => {
  selectedFiles.value = selectedFiles.value.filter(f => f.file_id !== fileId)
}
</script>

<template>
  <div>
    <!-- 上传区域 -->
    <div
      class="border-2 border-dashed rounded-2xl p-12 transition-all duration-300
             flex flex-col items-center justify-center gap-4 min-h-[240px]"
      :class="[
        isDragging ? 'border-primary-500 bg-primary-50 scale-[0.99]' : 'border-slate-300 bg-slate-50',
        isUploading ? 'opacity-50 pointer-events-none' : 'hover:border-primary-400 hover:bg-white'
      ]"
      @drop.prevent="handleDrop"
      @dragover.prevent
      @dragleave.prevent="isDragging = false"
      @dragenter.prevent="isDragging = true"
    >
      <input
        ref="inputRef"
        type="file"
        :accept="accept"
        :multiple="maxFiles > 1"
        class="hidden"
        @change="(e) => handleFileSelect(Array.from((e.target as HTMLInputElement).files || []))"
      />

      <template v-if="!isUploading && selectedFiles.length === 0">
        <div class="p-4 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50
                    w-20 h-20 flex items-center justify-center shadow-lg shadow-primary-100">
          <svg class="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>

        <p class="text-lg font-medium text-slate-700">拖拽文件到此处</p>
        <p class="text-sm text-slate-500">或点击选择文件 (最多 {{ maxFiles }} 个)</p>

        <button
          @click="inputRef?.click()"
          class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          选择文件
        </button>

        <p class="text-xs text-slate-400">支持 PDF 文件，单文件最大 {{ maxSize }}MB</p>
      </template>

      <div v-if="isUploading" class="text-center">
        <div class="relative w-32 h-32 mx-auto mb-4">
          <svg class="w-full h-full -rotate-90">
            <circle cx="64" cy="64" r="56" fill="none" stroke="currentColor" class="text-slate-200" stroke-width="8" />
            <circle
              cx="64" cy="64" r="56" fill="none" stroke="currentColor" class="text-primary-600 transition-all duration-300"
              :stroke-dasharray="351.86" :stroke-dashoffset="351.86 * (1 - progress / 100)" stroke-linecap="round"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-2xl font-bold text-slate-700">{{ progress }}%</span>
          </div>
        </div>
        <p class="text-slate-600">正在上传...</p>
      </div>
    </div>

    <!-- 已选文件列表 -->
    <div v-if="selectedFiles.length > 0" class="mt-4 space-y-2">
      <div
        v-for="file in selectedFiles"
        :key="file.file_id"
        class="flex items-center justify-between p-3 bg-white rounded-lg border border-slate-200"
      >
        <div class="flex items-center gap-3">
          <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
          </svg>
          <span class="text-slate-700">{{ file.name }}</span>
          <span class="text-sm text-slate-400">({{ (file.size / 1024 / 1024).toFixed(2) }} MB)</span>
        </div>
        <button
          v-if="!isUploading"
          @click="removeFile(file.file_id)"
          class="p-1 hover:bg-slate-100 rounded transition-colors"
        >
          <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
```

**验收标准**:
- [ ] AppHeader 和 AppFooter 正常显示
- [ ] ToolCard 点击跳转正确
- [ ] FileUploader 上传功能正常

---

### 3.2 API 客户端与状态管理 (Day 13 - 4h)

**负责人**: 前端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现 API 客户端 | 1.5h | 类型定义 | P0 |
| 实现 Pinia Stores | 2.5h | API 客户端 | P0 |

**API 客户端** (`frontend/src/api/client.ts`):

```typescript
import axios from 'axios'
import type { APIResponse } from '@/types'

const baseURL = import.meta.env.VITE_API_URL || '/api'

export const apiClient = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      return Promise.reject(error.response.data)
    } else if (error.request) {
      return Promise.reject({
        error: {
          code: 'NETWORK_ERROR',
          message: '网络连接失败，请检查您的网络'
        }
      })
    }
    return Promise.reject(error)
  }
)

// API 方法
export const api = {
  tools: {
    getAll: () => apiClient.get<any, any[]>('/v1/tools'),
    getById: (id: string) => apiClient.get<any, any>(`/v1/tools/${id}`),
  },
  files: {
    upload: (formData: FormData, onProgress?: (progress: number) => void) => {
      return apiClient.post<any, any>('/v1/files/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress(progress)
          }
        }
      })
    },
    download: (fileId: string) => `/api/v1/files/download/${fileId}`,
  },
  jobs: {
    create: (data: { tool_id: string; upload_id: string; options: any }) =>
      apiClient.post<any, any>('/v1/jobs', data),
    getStatus: (jobId: string) => apiClient.get<any, any>(`/v1/jobs/${jobId}`),
    cancel: (jobId: string) => apiClient.delete(`/v1/jobs/${jobId}`),
  },
}
```

**Pinia Stores** (`frontend/src/stores/modules/tools.ts`):

```typescript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Tool } from '@/types'
import { api } from '@/api/client'

export const useToolsStore = defineStore('tools', () => {
  const tools = ref<Tool[]>([])
  const selectedCategory = ref<string | null>(null)
  const searchQuery = ref('')
  const loading = ref(false)

  const filteredTools = computed(() => {
    let result = tools.value

    if (selectedCategory.value) {
      result = result.filter(t => t.category === selectedCategory.value)
    }

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(t =>
        t.name.toLowerCase().includes(query) ||
        t.description.toLowerCase().includes(query)
      )
    }

    return result
  })

  const categories = computed(() => {
    return [...new Set(tools.value.map(t => t.category))]
  })

  async function fetchTools() {
    loading.value = true
    try {
      const response = await api.tools.getAll()
      tools.value = response.data
    } finally {
      loading.value = false
    }
  }

  function setCategory(category: string | null) {
    selectedCategory.value = category
  }

  function setSearch(query: string) {
    searchQuery.value = query
  }

  return {
    tools,
    selectedCategory,
    searchQuery,
    loading,
    filteredTools,
    categories,
    fetchTools,
    setCategory,
    setSearch
  }
})
```

**验收标准**:
- [ ] API 客户端可以调用后端接口
- [ ] Stores 数据正确存储和更新

---

### 3.3 页面实现 (Day 14-17, 4 天)

**负责人**: 前端开发者

#### 3.3.1 首页 (Day 14 - 3h)

**Home.vue** (`frontend/src/pages/Home.vue`):

```vue
<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useToolsStore } from '@/stores/modules/tools'
import ToolCard from '@/components/business/ToolCard.vue'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const toolsStore = useToolsStore()

onMounted(() => {
  toolsStore.fetchTools()
})

const categories = computed(() => ['全部工具', ...toolsStore.categories])
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <AppHeader />

    <main class="max-w-7xl mx-auto px-4 py-12">
      <!-- Hero Section -->
      <section class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-slate-900 mb-4">
          简单、快速的 PDF 工具
        </h1>
        <p class="text-lg text-slate-500 mb-8">
          无需注册，完全免费，保护隐私
        </p>
      </section>

      <!-- 分类筛选 -->
      <section class="mb-8 flex gap-2 overflow-x-auto pb-2">
        <button
          v-for="category in categories"
          :key="category"
          @click="toolsStore.setCategory(category === '全部工具' ? null : category)"
          class="px-4 py-2 rounded-lg whitespace-nowrap transition-colors"
          :class="
            (toolsStore.selectedCategory || '全部工具') === category
              ? 'bg-primary-600 text-white'
              : 'bg-white text-slate-600 hover:bg-slate-100'
          "
        >
          {{ category }}
        </button>
      </section>

      <!-- 工具网格 -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <ToolCard
          v-for="tool in toolsStore.filteredTools"
          :key="tool.id"
          :tool="tool"
        />
      </section>
    </main>

    <AppFooter />
  </div>
</template>
```

#### 3.3.2 工具页面模板 (Day 15 - 4h)

**ToolPage.vue** (`frontend/src/pages/tools/ToolPage.vue`):

```vue
<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import type { Tool, Job } from '@/types'
import FileUploader from '@/components/business/FileUploader.vue'

const route = useRoute()
const router = useRouter()

const tool = ref<Tool | null>(null)
const uploadId = ref<string | null>(null)
const currentJob = ref<Job | null>(null)
const options = ref<Record<string, any>>({})
const pollInterval = ref<number | null>(null)

const toolId = computed(() => route.params.toolId as string)

onMounted(async () => {
  const response = await api.tools.getById(toolId.value)
  tool.value = response.data

  // 设置默认选项
  if (tool.value?.options) {
    tool.value.options.forEach(opt => {
      if (opt.default !== undefined) {
        options.value[opt.name] = opt.default
      }
    })
  }
})

onUnmounted(() => {
  if (pollInterval.value) {
    clearInterval(pollInterval.value)
  }
})

const onUploaded = (id: string, files: any[]) => {
  uploadId.value = id
}

const onStartProcessing = async () => {
  if (!uploadId.value) return

  const response = await api.jobs.create({
    tool_id: toolId.value,
    upload_id: uploadId.value,
    options: options.value
  })

  currentJob.value = response.data
  startPolling()
}

const startPolling = () => {
  pollInterval.value = window.setInterval(async () => {
    if (!currentJob.value) return

    const response = await api.jobs.getStatus(currentJob.value.job_id)
    currentJob.value = response.data

    if (response.data.status === 'completed' || response.data.status === 'failed') {
      if (pollInterval.value) {
        clearInterval(pollInterval.value)
        pollInterval.value = null
      }
    }
  }, 1000)
}

const isProcessing = computed(() =>
  currentJob.value?.status === 'queued' || currentJob.value?.status === 'processing'
)

const isCompleted = computed(() => currentJob.value?.status === 'completed')

const isFailed = computed(() => currentJob.value?.status === 'failed')
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <AppHeader />

    <main class="max-w-4xl mx-auto px-4 py-12">
      <!-- 返回按钮 -->
      <button
        @click="router.push('/')"
        class="flex items-center gap-2 text-slate-600 hover:text-slate-900 mb-8"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        返回首页
      </button>

      <div v-if="tool">
        <!-- 工具标题 -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-slate-900 mb-2">{{ tool.name }}</h1>
          <p class="text-slate-500">{{ tool.description }}</p>
        </div>

        <!-- 上传区域 -->
        <div v-if="!isProcessing && !isCompleted && !isFailed" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
          <FileUploader
            :tool-id="tool.id"
            :max-files="tool.max_files"
            :max-size="tool.max_size_mb"
            @uploaded="onUploaded"
            @error="console.error"
          />

          <!-- 选项配置 -->
          <div v-if="uploadId && tool.options.length > 0" class="mt-6 space-y-4">
            <h3 class="text-lg font-semibold text-slate-900">处理选项</h3>

            <div v-for="option in tool.options" :key="option.name" class="space-y-2">
              <label class="block text-sm font-medium text-slate-700">
                {{ option.label }}
              </label>

              <!-- 文本输入 -->
              <input
                v-if="option.type === 'string'"
                v-model="options[option.name]"
                type="text"
                :placeholder="option.placeholder"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />

              <!-- 数字输入 -->
              <input
                v-else-if="option.type === 'number'"
                v-model.number="options[option.name]"
                type="number"
                :min="option.min"
                :max="option.max"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              />

              <!-- 选择器 -->
              <select
                v-else-if="option.type === 'select'"
                v-model="options[option.name]"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option v-for="opt in option.options" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>
            </div>
          </div>

          <!-- 开始按钮 -->
          <button
            v-if="uploadId"
            @click="onStartProcessing"
            class="mt-6 w-full py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
          >
            开始处理
          </button>
        </div>

        <!-- 进度显示 -->
        <div v-if="isProcessing" class="bg-white rounded-2xl p-6 shadow-sm border border-slate-200">
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-slate-700">正在处理...</span>
              <span class="text-sm font-semibold text-primary-600">{{ currentJob?.progress }}%</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
              <div
                class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-500"
                :style="{ width: `${currentJob?.progress || 0}%` }"
              />
            </div>
          </div>
          <p class="text-sm text-slate-500">{{ currentJob?.message }}</p>
        </div>

        <!-- 结果显示 -->
        <div v-if="isCompleted" class="bg-white rounded-2xl p-6 shadow-sm border border-green-200">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-slate-900">处理完成！</h2>
              <p class="text-sm text-slate-500">您的文件已准备好下载</p>
            </div>
          </div>

          <div class="bg-slate-50 rounded-lg p-4 mb-6">
            <div class="flex items-center gap-3">
              <svg class="w-10 h-10 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
              </svg>
              <div>
                <p class="font-medium text-slate-900">{{ currentJob?.result?.filename }}</p>
                <p class="text-sm text-slate-500">
                  {{ ((currentJob?.result?.size || 0) / 1024 / 1024).toFixed(2) }} MB
                </p>
              </div>
            </div>
          </div>

          <div class="flex gap-3">
            <a
              :href="currentJob?.result?.download_url"
              download
              class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold text-center"
            >
              下载文件
            </a>
            <button
              @click="currentJob = null; uploadId = null"
              class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
            >
              重新处理
            </button>
          </div>

          <p class="text-xs text-slate-400 mt-4 text-center">
            文件链接将在 2 小时后失效
          </p>
        </div>

        <!-- 错误显示 -->
        <div v-if="isFailed" class="bg-white rounded-2xl p-6 shadow-sm border border-red-200">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-slate-900">处理失败</h2>
              <p class="text-sm text-slate-500">{{ currentJob?.error?.message }}</p>
            </div>
          </div>

          <div class="flex gap-3">
            <button
              @click="currentJob = null"
              class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
            >
              重试
            </button>
            <button
              @click="router.push('/')"
              class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
            >
              返回首页
            </button>
          </div>
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>
```

**验收标准**:
- [ ] 首页工具列表正确显示
- [ ] 工具页面完整流程可用
- [ ] 文件上传 → 处理 → 下载 流程畅通

---

### 3.4 Composables 实现 (Day 18 - 3h)

**负责人**: 前端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 实现 useFileUpload | 1.5h | API 客户端 | P0 |
| 实现 usePolling | 1.5h | API 客户端 | P0 |

**useFileUpload.ts** (`frontend/src/composables/useFileUpload.ts`):

```typescript
import { ref } from 'vue'
import { api } from '@/api/client'
import type { UploadedFile } from '@/types'

export function useFileUpload(toolId: string, maxFiles: number, maxSizeMB: number) {
  const isDragging = ref(false)
  const isUploading = ref(false)
  const progress = ref(0)
  const selectedFiles = ref<UploadedFile[]>([])

  const maxSizeBytes = maxSizeMB * 1024 * 1024

  const validateFiles = (files: File[]): { valid: File[]; errors: string[] } => {
    const valid: File[] = []
    const errors: string[] = []

    files.forEach(file => {
      if (file.type !== 'application/pdf') {
        errors.push(`${file.name} 不是 PDF 文件`)
        return
      }
      if (file.size > maxSizeBytes) {
        errors.push(`${file.name} 超过 ${maxSizeMB}MB 限制`)
        return
      }
      valid.push(file)
    })

    if (selectedFiles.value.length + valid.length > maxFiles) {
      errors.push(`最多只能上传 ${maxFiles} 个文件`)
      return { valid: [], errors }
    }

    return { valid, errors }
  }

  const uploadFiles = async (files: File[]) => {
    isUploading.value = true
    progress.value = 0

    try {
      const formData = new FormData()
      files.forEach(file => formData.append('files', file))
      formData.append('tool_id', toolId)

      const response = await api.files.upload(formData, (p) => {
        progress.value = p
      })

      selectedFiles.value = [...selectedFiles.value, ...response.files]
      return response
    } finally {
      isUploading.value = false
    }
  }

  const removeFile = (fileId: string) => {
    selectedFiles.value = selectedFiles.value.filter(f => f.file_id !== fileId)
  }

  return {
    isDragging,
    isUploading,
    progress,
    selectedFiles,
    validateFiles,
    uploadFiles,
    removeFile
  }
}
```

**usePolling.ts** (`frontend/src/composables/usePolling.ts`):

```typescript
import { ref, onUnmounted } from 'vue'
import { api } from '@/api/client'
import type { Job } from '@/types'

export function usePolling(jobId: string, interval = 1000) {
  const status = ref<Job['status']>('queued')
  const progress = ref(0)
  const message = ref('')
  const result = ref<Job['result'] | null>(null)
  const error = ref<Job['error'] | null>(null)

  let timer: number | null = null

  const poll = async () => {
    try {
      const response = await api.jobs.getStatus(jobId)
      const data = response as Job

      status.value = data.status
      progress.value = data.progress
      message.value = data.message
      result.value = data.result || null
      error.value = data.error || null

      if (data.status === 'completed' || data.status === 'failed') {
        stopPolling()
      }
    } catch (err: any) {
      error.value = {
        code: 'POLL_ERROR',
        message: err.error?.message || '查询状态失败'
      }
      stopPolling()
    }
  }

  const startPolling = () => {
    if (timer) return
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

**验收标准**:
- [ ] Composables 功能正常
- [ ] 组件可以正确使用 Composables

---

### 3.5 前端测试 (Day 19-20, 2 天)

**负责人**: 前端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 编写组件测试 | 4h | 组件实现 | P0 |
| 编写 Composables 测试 | 2h | Composables | P0 |
| 编写 E2E 测试 | 4h | 所有前端代码 | P0 |
| 测试覆盖率检查 | 2h | 所有测试 | P0 |

**测试配置** (`frontend/vitest.config.ts`):

```typescript
import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  test: {
    globals: true,
    environment: 'jsdom',
    coverage: {
      provider: 'c8',
      reporter: ['text', 'html', 'lcov'],
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

**组件测试示例** (`frontend/tests/unit/ToolCard.spec.ts`):

```typescript
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createMemoryHistory } from 'vue-router'
import ToolCard from '@/components/business/ToolCard.vue'
import type { Tool } from '@/types'

describe('ToolCard', () => {
  it('renders tool name and description', () => {
    const tool: Tool = {
      id: 'merge',
      name: 'PDF 合并',
      description: '将多个 PDF 文件合并为一个',
      icon: 'merge',
      route: '/tools/merge',
      category: '基础工具',
      max_files: 20,
      max_size_mb: 100,
      max_total_size_mb: 200,
      options: []
    }

    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/tools/:toolId', component: { template: '<div />' } }]
    })

    const wrapper = mount(ToolCard, {
      props: { tool },
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.text()).toContain('PDF 合并')
    expect(wrapper.text()).toContain('将多个 PDF 文件合并为一个')
  })

  it('navigates to tool route on click', async () => {
    const tool: Tool = {
      id: 'merge',
      name: 'PDF 合并',
      description: '描述',
      icon: 'merge',
      route: '/tools/merge',
      category: '基础工具',
      max_files: 20,
      max_size_mb: 100,
      max_total_size_mb: 200,
      options: []
    }

    const router = createRouter({
      history: createMemoryHistory(),
      routes: [{ path: '/tools/:toolId', component: { template: '<div />' } }]
    })

    await router.push('/')
    await router.isReady()

    const wrapper = mount(ToolCard, {
      props: { tool },
      global: {
        plugins: [router]
      }
    })

    await wrapper.find('button').trigger('click')
    expect(router.currentRoute.value.path).toBe('/tools/merge')
  })
})
```

**E2E 测试示例** (`frontend/tests/e2e/merge.spec.ts`):

```typescript
import { test, expect } from '@playwright/test'

test.describe('PDF Merge', () => {
  test('should merge two PDF files', async ({ page }) => {
    await page.goto('/')

    // 点击合并工具
    await page.click('text=PDF 合并')

    // 上传文件
    const fileInput = await page.locator('input[type="file"]')
    await fileInput.setInputFiles([
      'tests/fixtures/sample1.pdf',
      'tests/fixtures/sample2.pdf'
    ])

    // 等待上传完成
    await expect(page.locator('text=上传成功')).toBeVisible()

    // 点击开始处理
    await page.click('text=开始处理')

    // 等待处理完成
    await expect(page.locator('text=处理完成')).toBeVisible({ timeout: 30000 })

    // 验证下载链接存在
    const downloadButton = page.locator('a[href*="/api/v1/files/download/"]')
    await expect(downloadButton).toBeVisible()
  })
})
```

**验收标准**:
- [ ] 单元测试覆盖率 > 80%
- [ ] E2E 测试通过
- [ ] vitest 运行无报错

---

## 4. 集成测试 (3 天)

### 4.1 前后端集成测试 (Day 21-22, 2 天)

**负责人**: QA / 全栈开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 端到端流程测试 | 4h | 前后端完成 | P0 |
| API 集成测试 | 3h | 后端完成 | P0 |
| 性能测试 | 2h | 所有代码 | P1 |
| 安全测试 | 2h | 所有代码 | P0 |
| 兼容性测试 | 3h | 所有代码 | P0 |

**端到端测试用例**:

1. **PDF 合并流程**
   - [ ] 用户访问首页
   - [ ] 选择"PDF 合并"工具
   - [ ] 上传 2 个 PDF 文件
   - [ ] 配置输出文件名
   - [ ] 点击"开始处理"
   - [ ] 查看进度更新
   - [ ] 处理完成后下载文件
   - [ ] 验证下载文件有效

2. **文件验证**
   - [ ] 上传非 PDF 文件 → 显示错误
   - [ ] 上传超过大小限制的文件 → 显示错误
   - [ ] 上传加密的 PDF → 显示友好错误

3. **速率限制**
   - [ ] 短时间内多次上传 → 触发速率限制
   - [ ] 验证 429 响应

**性能测试**:

```bash
# 使用 locust 进行负载测试
locust -f tests/load/test_api.py --host=http://localhost:8000
```

**验收标准**:
- [ ] 所有 E2E 测试用例通过
- [ ] API 响应时间 < 500ms (P95)
- [ ] 并发 100 用户时系统稳定

---

### 4.2 Bug 修复与优化 (Day 23 - 1 天)

**负责人**: 全栈开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 修复测试发现的 Bug | 4h | 测试报告 | P0 |
| 性能优化 | 2h | 测试报告 | P1 |
| 代码审查 | 2h | 所有代码 | P0 |

**验收标准**:
- [ ] 所有 P0 Bug 修复
- [ ] 代码审查通过
- [ ] 性能指标达标

---

## 5. 部署准备 (2 天)

### 5.1 Docker 配置 (Day 24 - 4h)

**负责人**: DevOps / 后端开发者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 编写后端 Dockerfile | 1h | 后端代码 | P0 |
| 编写前端 Dockerfile | 1h | 前端代码 | P0 |
| 配置 docker-compose | 1h | Dockerfiles | P0 |
| 测试 Docker 构建 | 1h | docker-compose | P0 |

**后端 Dockerfile** (`backend/Dockerfile`):

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
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**前端 Dockerfile** (`frontend/Dockerfile`):

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# 安装 pnpm
RUN npm install -g pnpm

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN pnpm install --frozen-lockfile

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

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - APP_ENV=production
      - ALLOWED_ORIGINS=http://localhost
    volumes:
      - ./backend/storage:/app/storage

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

**验收标准**:
- [ ] `docker-compose up` 启动成功
- [ ] 前后端通信正常
- [ ] 文件存储持久化

---

### 5.2 环境变量与配置 (Day 24 - 2h)

**负责人**: DevOps

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 配置生产环境变量 | 1h | - | P0 |
| 编写部署文档 | 1h | 环境变量 | P0 |

**生产环境变量** (`.env.production`):

```env
# 后端
APP_ENV=production
APP_DEBUG=false
APP_URL=https://pdftoolbox.example.com
ALLOWED_ORIGINS=https://pdftoolbox.example.com

# 存储
STORAGE_PATH=/app/storage
MAX_FILE_SIZE=104857600

# Redis
REDIS_URL=redis://redis:6379/0

# 日志
LOG_LEVEL=WARNING
```

**验收标准**:
- [ ] 环境变量文档完整
- [ ] 生产配置正确

---

### 5.3 CI/CD 配置 (Day 25 - 4h)

**负责人**: DevOps

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 配置 GitHub Actions | 2h | - | P1 |
| 配置自动化测试 | 1h | GitHub Actions | P0 |
| 配置自动化部署 | 1h | GitHub Actions | P1 |

**GitHub Actions** (`.github/workflows/ci.yml`):

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        working-directory: ./backend
        run: |
          uv venv
          source .venv/bin/activate
          uv pip install -r requirements.txt

      - name: Run tests
        working-directory: ./backend
        run: |
          source .venv/bin/activate
          pytest

  frontend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: pnpm/action-setup@v2
        with:
          version: 8

      - uses: actions/setup-node@v3
        with:
          node-version: '20'
          cache: 'pnpm'
          cache-dependency-path: frontend/pnpm-lock.yaml

      - name: Install dependencies
        working-directory: ./frontend
        run: pnpm install

      - name: Run tests
        working-directory: ./frontend
        run: pnpm test

      - name: Build
        working-directory: ./frontend
        run: pnpm build
```

**验收标准**:
- [ ] CI 流水线运行成功
- [ ] 测试自动执行
- [ ] 构建产物生成

---

### 5.4 部署文档编写 (Day 25 - 2h)

**负责人**: 技术文档作者

**任务列表**:

| 任务 | 预估时间 | 依赖 | 优先级 |
|------|----------|------|--------|
| 编写部署指南 | 1h | - | P0 |
| 编写运维手册 | 1h | - | P1 |

**交付物**:
- `doc/deployment/deployment-guide.md`
- `doc/deployment/operations.md`

**验收标准**:
- [ ] 部署步骤清晰
- [ ] 运维指南完整

---

## 里程碑

| 里程碑 | 日期 | 交付物 |
|--------|------|--------|
| M1: 项目初始化完成 | Day 2 | 前后端脚手架，类型定义 |
| M2: 后端 API 完成 | Day 10 | 所有 Phase 1 API 可用 |
| M3: 前端页面完成 | Day 20 | 所有 Phase 1 页面可用 |
| M4: 集成测试通过 | Day 23 | 端到端流程测试通过 |
| M5: 部署准备完成 | Day 25 | Docker 配置，CI/CD 配置 |

---

## 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| PyMuPDF 许可证问题 | 中 | 高 | 确认 AGPL-3.0 合规性，考虑替代方案 |
| 大文件处理内存溢出 | 高 | 中 | 实现流式处理，限制并发 |
| Redis 单点故障 | 低 | 高 | 生产环境使用 Redis Cluster |
| 文件清理遗漏 | 中 | 中 | 实现双重清理机制 |
| CORS 配置错误 | 低 | 中 | 充分测试跨域场景 |
| 速率限制绕过 | 低 | 中 | 使用 Redis 存储计数器 |

---

## 附录

### A. 依赖版本清单

**前端** (`frontend/package.json`):

```json
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
    "@playwright/test": "^1.40.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32"
  }
}
```

**后端** (`backend/requirements.txt`):

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
PyMuPDF==1.23.8
Pillow==10.1.0
aiofiles==23.2.1
python-dotenv==1.0.0
slowapi==0.1.9
celery==5.3.4
redis==5.0.1
```

---

## 实施注意事项

### 开发规范

1. **Git 提交规范**
   - feat: 新功能
   - fix: Bug 修复
   - docs: 文档
   - test: 测试
   - refactor: 重构
   - chore: 构建/工具

2. **代码审查**
   - 所有代码必须经过审查
   - 使用 GitHub Pull Request
   - 至少一人批准

3. **测试要求**
   - 单元测试覆盖率 > 80%
   - 关键路径必须有 E2E 测试
   - 测试失败阻止合并

### 沟通机制

- **每日站会**: 同步进度和问题
- **周报**: 每周五总结本周完成情况
- **问题升级**: 阻塞问题立即上报

---

**文档结束**

本实施计划定义了 PDF 文档工具网站的详细开发任务和时间表。按照此计划执行，预计 6 周内可完成 Phase 1 功能的开发和部署。
