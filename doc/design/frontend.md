# PDF 文档工具网站 - 前端设计文档

> **版本**: 1.0
> **日期**: 2026-02-05
> **设计方向**: 极简主义 + 现代科技感

---

## 目录

1. [设计概述](#设计概述)
2. [美学方向](#美学方向)
3. [设计规范](#设计规范)
4. [页面设计](#页面设计)
5. [组件设计](#组件设计)
6. [交互设计](#交互设计)
7. [路由设计](#路由设计)
8. [状态管理](#状态管理)
9. [响应式设计](#响应式设计)
10. [动效规范](#动效规范)
11. [可访问性](#可访问性)

---

## 设计概述

### 设计目标

1. **开门见山** - 用户打开网站立即看到可用工具，无需复杂导航
2. **专业可信** - 精致的视觉传达，建立用户信任
3. **高效操作** - 清晰的交互流程，最少的操作步骤
4. **即时反馈** - 每个操作都有明确的视觉反馈

### 目标用户

| 用户类型 | 特征 | 需求 |
|----------|------|------|
| 办公人员 | 经常处理 PDF 文档 | 快速、准确、批量处理 |
| 学生 | 需要整理学习资料 | 免费、简单、无广告 |
| 自由职业者 | 处理各种文档格式 | 多功能、高质量输出 |

### 设计原则

- **简洁优于复杂**: 减少视觉噪音，聚焦核心功能
- **清晰优于美观**: 功能优先，装饰服务于功能
- **一致优于多样**: 统一的设计语言，降低学习成本
- **快速优于花哨**: 轻量级实现，秒级加载

---

## 美学方向

### 设计风格

**现代极简 + 微科技感**

融合 Nordic 设计的克制与科技产品的精致，创造专业但不冰冷的视觉体验。

### 核心概念

1. **空气感布局**: 大量留白，让内容呼吸
2. **微妙层次**: 细腻的阴影和边框，建立深度
3. **功能色彩**: 色彩有明确语义，不滥用
4. **圆润几何**: 圆角柔和，但不过度可爱

### 差异化点

| 特征 | 常见设计 | 本设计 |
|------|----------|--------|
| 首屏 | 大 Banner + 滚动工具 | 工具直接展示，零滚动 |
| 工具卡片 | 齐平网格 | 微悬浮 + 动态阴影 |
| 上传区 | 纯色块 | 渐变边框 + 粒子效果 |
| 进度 | 纯进度条 | 动态消息 + 预估时间 |
| 结果 | 简单下载 | 文件预览 + 二维码 |

---

## 设计规范

### 配色方案

基于冷暖平衡的科技调色板，主色传达专业与信任，点缀色激发行动。

```css
:root {
  /* === 主色调 === */
  --primary-50: #eff6ff;
  --primary-100: #dbeafe;
  --primary-200: #bfdbfe;
  --primary-300: #93c5fd;
  --primary-400: #60a5fa;
  --primary-500: #3b82f6;  /* 主色 */
  --primary-600: #2563eb;
  --primary-700: #1d4ed8;
  --primary-800: #1e40af;
  --primary-900: #1e3a8a;

  /* === 中性色 === */
  --slate-50: #f8fafc;    /* 背景色 */
  --slate-100: #f1f5f9;   /* 次级背景 */
  --slate-200: #e2e8f0;   /* 边框 */
  --slate-300: #cbd5e1;   /* 分割线 */
  --slate-400: #94a3b8;   /* 禁用文本 */
  --slate-500: #64748b;   /* 次要文本 */
  --slate-600: #475569;   /* 正文 */
  --slate-700: #334155;   /* 标题 */
  --slate-800: #1e293b;   /* 深色背景 */
  --slate-900: #0f172a;   /* 主背景 */

  /* === 功能色 === */
  --success-50: #f0fdf4;
  --success-500: #22c55e;  /* 成功 */
  --success-700: #15803d;

  --warning-50: #fffbeb;
  --warning-500: #f59e0b;  /* 警告 */
  --warning-700: #b45309;

  --error-50: #fef2f2;
  --error-500: #ef4444;    /* 错误 */
  --error-700: #b91c1c;

  --info-50: #f0f9ff;
  --info-500: #0ea5e9;     /* 信息 */
  --info-700: #0369a1;

  /* === 特殊色 === */
  --accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --glass-bg: rgba(255, 255, 255, 0.8);
  --glass-border: rgba(255, 255, 255, 0.3);
}
```

### 排版系统

采用 Inter 作为主要字体，配合 JetBrains Mono 用于代码和数字。

```css
:root {
  /* === 字体家族 === */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'SF Mono', 'Monaco', 'Cascadia Code', monospace;

  /* === 字体尺度 (1.250 - Major Third) === */
  --text-xs: 0.75rem;      /* 12px */
  --text-sm: 0.875rem;     /* 14px */
  --text-base: 1rem;       /* 16px */
  --text-lg: 1.125rem;     /* 18px */
  --text-xl: 1.25rem;      /* 20px */
  --text-2xl: 1.5rem;      /* 24px */
  --text-3xl: 1.875rem;    /* 30px */
  --text-4xl: 2.25rem;     /* 36px */
  --text-5xl: 3rem;        /* 48px */

  /* === 行高 === */
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;

  /* === 字重 === */
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### 间距系统

基于 4px 网格的间距体系。

```css
:root {
  --spacing-0: 0;
  --spacing-1: 0.25rem;   /* 4px */
  --spacing-2: 0.5rem;    /* 8px */
  --spacing-3: 0.75rem;   /* 12px */
  --spacing-4: 1rem;      /* 16px */
  --spacing-5: 1.25rem;   /* 20px */
  --spacing-6: 1.5rem;    /* 24px */
  --spacing-8: 2rem;      /* 32px */
  --spacing-10: 2.5rem;   /* 40px */
  --spacing-12: 3rem;     /* 48px */
  --spacing-16: 4rem;     /* 64px */
  --spacing-20: 5rem;     /* 80px */
  --spacing-24: 6rem;     /* 96px */
}
```

### 圆角系统

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.25rem;    /* 4px */
  --radius-base: 0.375rem; /* 6px */
  --radius-md: 0.5rem;     /* 8px */
  --radius-lg: 0.75rem;    /* 12px */
  --radius-xl: 1rem;       /* 16px */
  --radius-2xl: 1.5rem;    /* 24px */
  --radius-full: 9999px;
}
```

### 阴影系统

多层次的微妙阴影，建立视觉深度。

```css
:root {
  --shadow-xs: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  --shadow-base: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-md: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 25px 50px -12px rgb(0 0 0 / 0.25);
  --shadow-inner: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);

  /* 彩色阴影 */
  --shadow-primary: 0 10px 40px -10px rgb(59 130 246 / 0.5);
  --shadow-success: 0 10px 40px -10px rgb(34 197 94 / 0.5);
  --shadow-error: 0 10px 40px -10px rgb(239 68 68 / 0.5);
}
```

---

## 页面设计

### 页面结构

```
E:\pdftoolbox\frontend\src\pages\
├── Home.vue                 # 首页（工具列表）
├── tools\
│   ├── MergePDF.vue         # PDF 合并
│   ├── SplitPDF.vue         # PDF 拆分
│   ├── ExtractPages.vue     # 页面提取
│   ├── ExtractText.vue      # 文本提取
│   ├── ExtractImages.vue    # 图片提取
│   ├── AddWatermark.vue     # 添加水印
│   ├── RemoveWatermark.vue  # 去除水印
│   ├── CompressPDF.vue      # PDF 压缩
│   └── PDFToImages.vue      # PDF 转图片
└── Error.vue                # 错误页
```

### 首页设计 (Home.vue)

#### 布局结构

```
┌────────────────────────────────────────────────────────────────┐
│                        AppHeader                               │
│  ┌──────────────┐  ┌──────────────────────┐  ┌──────────────┐ │
│  │   Logo +     │  │   PDF 工具箱          │  │   关于 +     │ │
│  │   品牌名      │  │   (搜索栏)            │  │   GitHub     │ │
│  └──────────────┘  └──────────────────────┘  └──────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                        Hero Section                            │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                   简单、快速的 PDF 工具                    │ │
│  │                   无需注册，完全免费，保护隐私              │ │
│  │                                                            │ │
│  │    ┌──────────┐  ┌──────────┐  ┌──────────┐              │ │
│  │    │  2M+     │  │  50K+    │  │  99.9%   │              │ │
│  │    │  处理文件  │  │  日活用户  │  │  成功率    │              │ │
│  │    └──────────┘  └──────────┘  └──────────┘              │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                     分类标签 (可滚动)                          │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐     │
│  │ 全部工具  │ │ 基础工具  │ │ 提取工具  │ │ 水印工具  │ │ 转换工具  │     │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘     │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      工具卡片网格                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │
│  │            │ │            │ │            │ │            │ │
│  │  [图标]    │ │  [图标]    │ │  [图标]    │ │  [图标]    │ │
│  │  PDF 合并  │ │  PDF 拆分  │ │  页面提取  │ │  添加水印  │ │
│  │  将多个...  │ │  将一个...  │ │  提取指...  │ │  为PDF...  │ │
│  │            │ │            │ │            │ │            │ │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘ │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │
│  │  文本提取  │ │  图片提取  │ │ PDF 转图片│ │  去除水印  │ │
│  └────────────┘ └────────────┘ └────────────┘ └────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                        AppFooter                               │
│  © 2026 PDF 工具箱 | 隐私政策 | 使用条款 | GitHub              │
└────────────────────────────────────────────────────────────────┘
```

#### 关键元素

**Hero Section**:
- 标题: 48px, Semibold, Slate-900
- 副标题: 18px, Regular, Slate-500
- 统计数字: 36px, Bold, Primary-600
- 背景: 极微妙的渐变 (Slate-50 → White)

**工具卡片**:
- 悬浮效果: Y 轴 -4px, 阴影增强
- 边框: 1px Slate-200 → Primary-300
- 图标背景: Primary-50, 图标 Primary-600
- 描述文本: 14px, Slate-500

### 工具页面设计

#### 通用布局

所有工具页面共享相同的布局结构，确保一致的交互体验。

```
┌────────────────────────────────────────────────────────────────┐
│                      ToolPageHeader                            │
│  ┌──────────┐  ┌──────────────────────┐  ┌──────────────────┐ │
│  │ ← 返回首页 │  │  PDF 合并             │  │                  │ │
│  │           │  │  (工具图标)            │  │                  │ │
│  └──────────┘  └──────────────────────┘  └──────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      ToolDescription                           │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 将多个 PDF 文件合并为一个文件。支持拖拽调整顺序。           │ │
│  │ 最多支持 20 个文件，单文件最大 100MB                       │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      FileUploadSection                         │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │         ┌─────────────────────────────────┐              │ │
│  │         │                                 │              │ │
│  │         │         [拖拽上传区域]           │              │ │
│  │         │                                 │              │ │
│  │         │    拖拽文件到此处，或点击选择     │              │ │
│  │         │                                 │              │ │
│  │         └─────────────────────────────────┘              │ │
│  │                                                           │ │
│  │           [选择文件] 按钮                                  │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │ 已选文件 (可拖拽排序):                                    │ │
│  │ ┌────────────────────────────────────────────────────┐   │ │
│  │ │ ☰  document1.pdf  (2.3 MB)              [×]       │   │ │
│  │ └────────────────────────────────────────────────────┘   │ │
│  │ ┌────────────────────────────────────────────────────┐   │ │
│  │ │ ☰  document2.pdf  (1.5 MB)              [×]       │   │ │
│  │ └────────────────────────────────────────────────────┘   │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      ParamConfigSection                        │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  处理选项:                                                │ │
│  │                                                           │ │
│  │  ┌─────────────────┐  ┌─────────────────┐               │ │
│  │  │  输出文件名      │  │  [高级选项 ▼]   │               │ │
│  │  │  [merged.pdf  ] │  │                 │               │ │
│  │  └─────────────────┘  └─────────────────┘               │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      ActionSection                             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │              ┌──────────────────────┐                    │ │
│  │              │    开始处理           │                    │ │
│  │              └──────────────────────┘                    │ │
│  │                                                           │ │
│  │              文件将在 2 小时后自动删除                      │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      ProgressSection (处理时)                  │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                                                           │ │
│  │  正在处理...                                    50%       │ │
│  │  ═══════════════════════════════════                    │ │
│  │  正在合并第 5 页，共 10 页                                │ │
│  │  预计剩余时间: 15 秒                                      │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
┌────────────────────────────────────────────────────────────────┐
│                      ResultSection (完成后)                    │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  ✓ 处理完成！                                             │ │
│  │                                                           │ │
│  │  ┌─────────────────────────────────────────────────┐     │ │
│  │  │  merged.pdf                                      │     │ │
│  │  │  3.8 MB · 15 页                                   │     │ │
│  │  │                                                   │     │ │
│  │  │  [下载文件]  [复制链接]  [二维码]                  │     │ │
│  │  └─────────────────────────────────────────────────┘     │ │
│  │                                                           │ │
│  │  文件链接将在 2 小时后失效                                │ │
│  │                                                           │ │
│  │  ┌──────────┐  ┌──────────┐                            │ │
│  │  │ 重新处理  │  │ 返回首页  │                            │ │
│  │  └──────────┘  └──────────┘                            │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

#### 状态流转

```
初始态 → 文件上传态 → 参数配置态 → 处理中态 → 完成态
  ↑                                        ↓
  └────────────── 错误态 ←──────────────────┘
```

---

## 组件设计

### 组件层次结构

```
src/components/
├── ui/                         # Shadcn/ui 基础组件
│   ├── button/
│   │   ├── Button.vue
│   │   └── index.ts
│   ├── card/
│   │   ├── Card.vue
│   │   ├── CardHeader.vue
│   │   ├── CardContent.vue
│   │   └── index.ts
│   ├── input/
│   ├── progress/
│   ├── dialog/
│   └── toast/
│
├── layout/                     # 布局组件
│   ├── AppHeader.vue
│   ├── AppFooter.vue
│   ├── ToolPageHeader.vue
│   └── MainLayout.vue
│
└── business/                  # 业务组件
    ├── ToolCard.vue           # 工具卡片
    ├── FileUploader.vue       # 文件上传器
    ├── FileList.vue           # 文件列表 (可拖拽排序)
    ├── ProgressBar.vue        # 进度条
    ├── ResultCard.vue         # 结果卡片
    ├── ParamConfig.vue        # 参数配置面板
    ├── CategoryFilter.vue     # 分类筛选
    └── SearchBar.vue          # 搜索栏
```

### AppHeader.vue

**用途**: 全站导航头部

**视觉**:
- 高度: 64px
- 背景: 白色 + 底部边框 1px Slate-200
- 模糊效果: backdrop-blur-md (滚动时)

**组件接口**:

```typescript
interface Props {
  showSearch?: boolean  // 是否显示搜索栏
}

interface Emits {
  search: [query: string]
}
```

**状态**:
- 搜索框展开/收起
- 移动端菜单展开/收起

### ToolCard.vue

**用途**: 首页工具卡片

**视觉**:
- 尺寸: 最小 280px 宽度
- 圆角: 16px
- 边框: 1px Slate-200
- 悬浮: Y -4px, 阴影 lg, 边框 Primary-300
- 过渡: 300ms cubic-bezier(0.4, 0, 0.2, 1)

**组件接口**:

```typescript
interface Tool {
  id: string
  name: string
  description: string
  icon: string
  route: string
  category: string
}

interface Props {
  tool: Tool
}

interface Emits {
  click: [tool: Tool]
}
```

**实现示例**:

```vue
<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { LucideIcon } from '@/components/ui/icon'
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
    class="group relative p-6 rounded-2xl border border-slate-200
           bg-white text-left
           hover:-translate-y-1 hover:shadow-lg hover:border-primary-300
           active:scale-[0.98]
           transition-all duration-300 ease-out"
  >
    <!-- 图标 -->
    <div class="flex items-center gap-3 mb-4">
      <div class="p-3 rounded-xl bg-primary-50 text-primary-600
                  group-hover:bg-primary-100 group-hover:scale-110
                  transition-all duration-300">
        <LucideIcon :name="tool.icon" :size="24" />
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
      <LucideIcon name="arrow-right" :size="16" class="text-primary-600" />
    </div>
  </button>
</template>
```

### FileUploader.vue

**用途**: 文件上传组件，支持拖拽和点击选择

**视觉**:
- 虚线边框: 2px dashed Slate-300
- 拖拽激活: 边框 Primary-500, 背景 Primary-50
- 上传中: 显示进度条
- 动画: 轻微脉冲效果

**组件接口**:

```typescript
interface Props {
  toolId: string
  maxFiles?: number
  maxSize?: number        // MB
  accept?: string
  disabled?: boolean
}

interface Emits {
  uploaded: [uploadId: string, files: UploadedFile[]]
  error: [message: string]
}

interface UploadedFile {
  file_id: string
  name: string
  size: number
  pages?: number
}
```

**实现示例**:

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useFileUpload } from '@/composables/useFileUpload'
import { Button } from '@/components/ui/button'
import { LucideIcon } from '@/components/ui/icon'

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

const {
  isDragging,
  isUploading,
  progress,
  selectedFiles,
  handleDrop,
  handleFileSelect,
  removeFile
} = useFileUpload(props.toolId, props.maxFiles, props.maxSize, emit)

const inputRef = ref<HTMLInputElement>()

const dropZoneClasses = computed(() => [
  'border-2 border-dashed rounded-2xl p-12 transition-all duration-300',
  'flex flex-col items-center justify-center gap-4 min-h-[240px]',
  isDragging.value ? 'border-primary-500 bg-primary-50 scale-[0.99]' : 'border-slate-300 bg-slate-50',
  isUploading.value ? 'opacity-50 pointer-events-none' : 'hover:border-primary-400 hover:bg-white'
].join(' '))

const selectFiles = () => {
  inputRef.value?.click()
}
</script>

<template>
  <div>
    <!-- 上传区域 -->
    <div
      class="drop-zone"
      :class="dropZoneClasses"
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
        @change="(e) => handleFileSelect(Array.from(e.target.files || []))"
      />

      <!-- 空状态 -->
      <div v-if="!isUploading && selectedFiles.length === 0" class="text-center">
        <div class="p-4 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50
                    w-20 h-20 flex items-center justify-center mx-auto mb-4
                    shadow-lg shadow-primary-100">
          <LucideIcon name="upload-cloud" :size="40" class="text-primary-600" />
        </div>

        <p class="text-lg font-medium text-slate-700 mb-2">
          拖拽文件到此处
        </p>
        <p class="text-sm text-slate-500 mb-6">
          或点击选择文件 (最多 {{ maxFiles }} 个)
        </p>

        <Button @click="selectFiles" size="lg">
          <LucideIcon name="folder-open" :size="18" class="mr-2" />
          选择文件
        </Button>

        <p class="text-xs text-slate-400 mt-4">
          支持 PDF 文件，单文件最大 {{ maxSize }}MB
        </p>
      </div>

      <!-- 上传进度 -->
      <div v-if="isUploading" class="text-center w-full max-w-sm">
        <div class="relative w-32 h-32 mx-auto mb-4">
          <!-- 环形进度 -->
          <svg class="w-full h-full -rotate-90">
            <circle
              cx="64" cy="64" r="56"
              fill="none"
              stroke="currentColor"
              stroke-width="8"
              class="text-slate-200"
            />
            <circle
              cx="64" cy="64" r="56"
              fill="none"
              stroke="currentColor"
              stroke-width="8"
              :stroke-dasharray="351.86"
              :stroke-dashoffset="351.86 * (1 - progress / 100)"
              class="text-primary-600 transition-all duration-300"
              stroke-linecap="round"
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
    <FileList
      v-if="selectedFiles.length > 0"
      :files="selectedFiles"
      :removable="!isUploading"
      @remove="removeFile"
      class="mt-4"
    />
  </div>
</template>
```

### FileList.vue

**用途**: 显示已上传文件列表，支持拖拽排序

**视觉**:
- 文件项: 白色背景, 圆角 12px, 边框 1px Slate-200
- 拖拽手柄: Slate-400, 悬浮时 Slate-600
- 文件图标: 红色 PDF 图标
- 大小标签: Slate-400, 13px

**组件接口**:

```typescript
interface FileItem {
  id: string
  name: string
  size: number
  pages?: number
}

interface Props {
  files: FileItem[]
  removable?: boolean
  sortable?: boolean
}

interface Emits {
  remove: [id: string]
  reorder: [fromIndex: number, toIndex: number]
}
```

### ProgressBar.vue

**用途**: 显示处理进度

**视觉**:
- 高度: 8px, 圆角 4px
- 背景: Slate-200
- 进度条: Primary-600, 带渐变效果
- 动画: 条纹动画 + 平滑过渡

**组件接口**:

```typescript
interface Props {
  value: number           // 0-100
  message?: string
  estimatedTime?: number  // 秒
  indeterminate?: boolean
}
```

**实现示例**:

```vue
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  value: number
  message?: string
  estimatedTime?: number
  indeterminate?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  indeterminate: false
})

const formatTime = (seconds: number) => {
  if (seconds < 60) return `${seconds} 秒`
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins} 分 ${secs} 秒`
}
</script>

<template>
  <div class="w-full">
    <!-- 头部信息 -->
    <div class="flex items-center justify-between mb-3">
      <span class="text-sm font-medium text-slate-700">
        {{ message || '正在处理...' }}
      </span>
      <span class="text-sm font-semibold text-primary-600">
        {{ indeterminate ? '...' : `${value}%` }}
      </span>
    </div>

    <!-- 进度条 -->
    <div class="relative h-2 bg-slate-200 rounded-full overflow-hidden">
      <!-- 动画条纹背景 -->
      <div
        v-if="indeterminate"
        class="absolute inset-0 bg-gradient-to-r from-primary-400 via-primary-500 to-primary-400
               animate-shimmer"
      />
      <!-- 确定进度 -->
      <div
        v-else
        class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full
               transition-all duration-500 ease-out"
        :style="{ width: `${value}%` }"
      >
        <!-- 条纹效果 -->
        <div
          class="h-full w-full opacity-20"
          style="background-image: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 10px,
            rgba(255,255,255,.3) 10px,
            rgba(255,255,255,.3) 20px
          )"
        />
      </div>
    </div>

    <!-- 预计时间 -->
    <p v-if="estimatedTime && !indeterminate" class="text-xs text-slate-500 mt-2">
      预计剩余时间: {{ formatTime(estimatedTime) }}
    </p>
  </div>
</template>

<style scoped>
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-shimmer {
  animation: shimmer 1.5s infinite;
}
</style>
```

### ResultCard.vue

**用途**: 显示处理结果，提供下载

**视觉**:
- 成功状态: 绿色边框 + 图标
- 文件预览: PDF 图标 + 文件名 + 大小
- 下载按钮: Primary 色主按钮
- 二维码: 悬浮显示

**组件接口**:

```typescript
interface Result {
  output_file_id: string
  filename: string
  size: number
  pages?: number
  download_url: string
  expires_at: string
}

interface Props {
  result: Result
}

interface Emits {
  download: []
  share: []
  reset: []
}
```

### ParamConfig.vue

**用途**: 动态参数配置面板

**组件接口**:

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

interface Props {
  options: ToolOption[]
  modelValue: Record<string, any>
}

interface Emits {
  'update:modelValue': [value: Record<string, any>]
}
```

---

## 交互设计

### 文件上传流程

```
1. 用户拖拽/点击选择文件
   ↓
2. 前端验证 (类型、大小、数量)
   ↓
3. 显示文件预览
   ↓
4. 上传到服务器 (显示进度)
   ↓
5. 接收 upload_id 和文件元数据
   ↓
6. 显示文件列表 (可删除/排序)
```

### 任务处理流程

```
1. 用户配置参数
   ↓
2. 点击"开始处理"
   ↓
3. 创建任务 (获取 job_id)
   ↓
4. 开始轮询任务状态 (1秒间隔)
   ↓
5. 显示进度和状态消息
   ↓
6. 完成后显示结果
```

### 错误处理

| 错误类型 | 显示方式 | 操作 |
|----------|----------|------|
| 文件类型错误 | Toast 提示 | 关闭提示 |
| 文件过大 | Toast 提示 | 关闭提示 |
| 上传失败 | 内联错误提示 | 重试按钮 |
| 处理失败 | 结果页面显示 | 返回/重新处理 |
| 网络错误 | 全局提示 | 重试 |

### 微交互

**按钮点击**:
- 默认: scale 1
- 悬浮: scale 1.02, 阴影增强
- 点击: scale 0.98
- 过渡: 150ms ease-out

**卡片悬浮**:
- 默认: Y 0, 阴影 sm
- 悬浮: Y -4px, 阴影 lg
- 过渡: 300ms cubic-bezier(0.4, 0, 0.2, 1)

**输入框聚焦**:
- 边框: Slate-300 → Primary-500
- 阴影: 0 0 0 3px Primary-100
- 过渡: 200ms ease-out

---

## 路由设计

### 路由结构

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/Home.vue'),
    meta: {
      title: 'PDF 工具箱 - 简单快速的在线 PDF 工具'
    }
  },
  {
    path: '/tools/:toolId',
    name: 'tool',
    component: () => import('@/pages/tools/ToolPage.vue'),
    props: true,
    meta: {
      title: 'PDF 工具'
    }
  },
  {
    path: '/result/:jobId',
    name: 'result',
    component: () => import('@/pages/Result.vue'),
    props: true,
    meta: {
      title: '处理结果'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/Error.vue'),
    meta: {
      title: '页面不存在'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title as string || 'PDF 工具箱'
  next()
})

export default router
```

### 路由守卫

```typescript
// 全局前置守卫
router.beforeEach((to, from, next) => {
  // 页面标题
  document.title = to.meta.title as string || 'PDF 工具箱'

  // 进度条开始
  NProgress.start()

  next()
})

// 全局后置钩子
router.afterEach(() => {
  // 进度条结束
  NProgress.done()
})
```

---

## 状态管理

### Store 结构

```typescript
// stores/index.ts
import { createPinia } from 'pinia'

const pinia = createPinia()

export default pinia

// stores/modules/tools.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Tool } from '@/types'

export const useToolsStore = defineStore('tools', () => {
  // State
  const tools = ref<Tool[]>([])
  const categories = ref<string[]>([])
  const selectedCategory = ref<string | null>(null)
  const searchQuery = ref('')

  // Getters
  const filteredTools = computed(() => {
    let result = tools.value

    // 分类筛选
    if (selectedCategory.value) {
      result = result.filter(t => t.category === selectedCategory.value)
    }

    // 搜索筛选
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(t =>
        t.name.toLowerCase().includes(query) ||
        t.description.toLowerCase().includes(query)
      )
    }

    return result
  })

  const allCategories = computed(() => {
    return [...new Set(tools.value.map(t => t.category))]
  })

  // Actions
  async function fetchTools() {
    const response = await apiClient.get('/tools')
    tools.value = response.data.data
  }

  function setCategory(category: string | null) {
    selectedCategory.value = category
  }

  function setSearch(query: string) {
    searchQuery.value = query
  }

  return {
    tools,
    categories,
    selectedCategory,
    searchQuery,
    filteredTools,
    allCategories,
    fetchTools,
    setCategory,
    setSearch
  }
})

// stores/modules/upload.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UploadedFile } from '@/types'

export const useUploadStore = defineStore('upload', () => {
  const uploadId = ref<string | null>(null)
  const files = ref<UploadedFile[]>([])
  const isUploading = ref(false)
  const progress = ref(0)

  function setUpload(id: string, uploadedFiles: UploadedFile[]) {
    uploadId.value = id
    files.value = uploadedFiles
  }

  function clearUpload() {
    uploadId.value = null
    files.value = []
    progress.value = 0
  }

  function removeFile(fileId: string) {
    files.value = files.value.filter(f => f.file_id !== fileId)
  }

  return {
    uploadId,
    files,
    isUploading,
    progress,
    setUpload,
    clearUpload,
    removeFile
  }
})

// stores/modules/job.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Job, JobStatus } from '@/types'

export const useJobStore = defineStore('job', () => {
  const currentJob = ref<Job | null>(null)
  const pollInterval = ref<number | null>(null)

  const isProcessing = computed(() =>
    currentJob.value?.status === 'queued' || currentJob.value?.status === 'processing'
  )

  const isCompleted = computed(() =>
    currentJob.value?.status === 'completed'
  )

  const isFailed = computed(() =>
    currentJob.value?.status === 'failed'
  )

  function setJob(job: Job) {
    currentJob.value = job
  }

  function updateJob(updates: Partial<Job>) {
    if (currentJob.value) {
      currentJob.value = { ...currentJob.value, ...updates }
    }
  }

  function clearJob() {
    currentJob.value = null
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
      pollInterval.value = null
    }
  }

  return {
    currentJob,
    isProcessing,
    isCompleted,
    isFailed,
    pollInterval,
    setJob,
    updateJob,
    clearJob
  }
})
```

---

## 响应式设计

### 断点系统

```css
:root {
  --breakpoint-sm: 640px;   /* 手机横屏 */
  --breakpoint-md: 768px;   /* 平板 */
  --breakpoint-lg: 1024px;  /* 小屏幕电脑 */
  --breakpoint-xl: 1280px;  /* 桌面 */
  --breakpoint-2xl: 1536px; /* 大屏幕 */
}
```

### Tailwind 配置

```javascript
// tailwind.config.js
export default {
  theme: {
    screens: {
      'sm': '640px',
      'md': '768px',
      'lg': '1024px',
      'xl': '1280px',
      '2xl': '1536px'
    }
  }
}
```

### 响应式布局

**首页工具网格**:

```vue
<template>
  <div class="grid gap-4 p-4
              sm:grid-cols-2
              md:grid-cols-3
              lg:grid-cols-4
              xl:gap-6 xl:p-6">
    <ToolCard
      v-for="tool in filteredTools"
      :key="tool.id"
      :tool="tool"
    />
  </div>
</template>
```

**导航栏**:

```vue
<template>
  <header class="h-16 px-4 flex items-center justify-between
                  md:px-6 lg:px-8">
    <!-- Logo -->
    <div class="flex items-center gap-2">
      <Logo class="w-8 h-8 sm:w-10 sm:h-10" />
      <span class="text-lg font-bold hidden sm:inline">PDF 工具箱</span>
    </div>

    <!-- 搜索 - 桌面端 -->
    <div class="hidden md:block flex-1 max-w-md mx-8">
      <SearchBar />
    </div>

    <!-- 右侧操作 -->
    <div class="flex items-center gap-2">
      <Button variant="ghost" size="icon" class="md:hidden">
        <SearchIcon />
      </Button>
      <Button variant="ghost" size="icon">
        <GithubIcon />
      </Button>
    </div>
  </header>
</template>
```

---

## 动效规范

### 过渡时长

| 场景 | 时长 | 缓动函数 |
|------|------|----------|
| 按钮点击 | 150ms | ease-out |
| 卡片悬浮 | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| 页面切换 | 400ms | cubic-bezier(0.4, 0, 0.2, 1) |
| 模态框 | 300ms | cubic-bezier(0.4, 0, 0.2, 1) |
| 进度条 | 500ms | ease-out |

### 页面切换动画

```vue
<!-- App.vue -->
<template>
  <router-view v-slot="{ Component, route }">
    <transition
      :name="route.meta.transition || 'fade'"
      mode="out-in"
      @before-enter="handleBeforeEnter"
      @after-enter="handleAfterEnter"
    >
      <component :is="Component" :key="route.path" />
    </transition>
  </router-view>
</template>

<style scoped>
/* 淡入淡出 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 滑动 */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* 缩放 */
.scale-enter-active,
.scale-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
```

### 元素进入动画

使用 VueUse 的 `useTransition` 或自定义动画:

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isVisible = ref(false)

onMounted(() => {
  // 延迟触发动画
  setTimeout(() => {
    isVisible.value = true
  }, 100)
})
</script>

<template>
  <div
    v-for="(item, index) in items"
    :key="index"
    class="transition-all duration-500 ease-out"
    :class="[
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
    ]"
    :style="{ transitionDelay: `${index * 50}ms` }"
  >
    {{ item }}
  </div>
</template>
```

### 加载动画

**骨架屏**:

```vue
<template>
  <div class="animate-pulse space-y-4">
    <div class="h-4 bg-slate-200 rounded w-3/4"></div>
    <div class="h-4 bg-slate-200 rounded"></div>
    <div class="h-4 bg-slate-200 rounded w-5/6"></div>
  </div>
</template>
```

**Spinner**:

```vue
<template>
  <div class="flex items-center justify-center">
    <div class="w-8 h-8 border-4 border-primary-200 border-t-primary-600
                rounded-full animate-spin"></div>
  </div>
</template>
```

---

## 可访问性

### ARIA 属性

```vue
<!-- 按钮 -->
<button
  aria-label="关闭对话框"
  @click="close"
>
  <XIcon />
</button>

<!-- 进度条 -->
<div
  role="progressbar"
  :aria-valuenow="progress"
  aria-valuemin="0"
  aria-valuemax="100"
  :aria-label="`处理进度: ${progress}%`"
>
  ...
</div>

<!-- 文件上传 -->
<div
  role="button"
  tabindex="0"
  aria-label="上传文件"
  @keydown.enter="selectFiles"
  @click="selectFiles"
>
  ...
</div>
```

### 键盘导航

| 按键 | 功能 |
|------|------|
| Tab | 焦点移动 |
| Shift + Tab | 反向焦点移动 |
| Enter / Space | 激活按钮/链接 |
| Escape | 关闭对话框/取消操作 |
| Arrow Keys | 在列表中导航 |

### 焦点管理

```vue
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useFocusTrap } from '@vueuse/integrations/useFocusTrap'

const modalRef = ref<HTMLElement>()
const { hasFocus, activate, deactivate } = useFocusTrap(modalRef)

watch(isOpen, (open) => {
  if (open) {
    activate()
  } else {
    deactivate()
  }
})
</script>

<template>
  <div ref="modalRef" v-if="isOpen">
    <!-- 模态框内容 -->
  </div>
</template>
```

### 颜色对比度

确保文本与背景对比度符合 WCAG AA 标准:

- 正常文本: 至少 4.5:1
- 大文本 (18px+): 至少 3:1
- 图标/图形: 至少 3:1

当前配色方案对比度:

| 组合 | 对比度 | 等级 |
|------|--------|------|
| Slate-900 on White | 16.4:1 | AAA |
| Slate-600 on White | 7.1:1 | AAA |
| Primary-600 on White | 5.1:1 | AA |
| Primary-600 on Primary-50 | 4.6:1 | AA |

---

## 实现指南

### 技术栈

```json
{
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "@vueuse/core": "^10.7.0",
    "axios": "^1.6.2",
    "lucide-vue-next": "^0.303.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "typescript": "^5.3.3",
    "vite": "^5.0.8",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "@vueuse/core": "^10.7.0",
    "@vueuse/motion": "^2.0.0"
  }
}
```

### Tailwind 配置

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'shimmer': 'shimmer 1.5s infinite',
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
```

### Vite 配置

```typescript
// vite.config.ts
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
  },
  build: {
    target: 'es2020',
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia'],
          'ui': ['@vueuse/core'],
        }
      }
    }
  }
})
```

### TypeScript 类型定义

```typescript
// src/types/index.ts

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

### API 客户端

```typescript
// src/api/client.ts
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
  (config) => {
    // 可以在这里添加认证 token
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      // 服务器返回错误
      return Promise.reject(error.response.data)
    } else if (error.request) {
      // 网络错误
      return Promise.reject({
        error: {
          code: 'NETWORK_ERROR',
          message: '网络连接失败，请检查您的网络'
        }
      })
    } else {
      return Promise.reject(error)
    }
  }
)

// API 方法
export const api = {
  tools: {
    getAll: () => apiClient.get<any, Tool[]>('/tools'),
    getById: (id: string) => apiClient.get<any, Tool>(`/tools/${id}`),
  },
  files: {
    upload: (formData: FormData) => {
      return apiClient.post<any, { upload_id: string; files: UploadedFile[] }>(
        '/files/upload',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' },
          onUploadProgress: (progressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded * 100) / (progressEvent.total || 1)
            )
            // 可以通过回调返回进度
          }
        }
      )
    },
    download: (fileId: string) => `/api/files/download/${fileId}`,
  },
  jobs: {
    create: (data: { tool_id: string; upload_id: string; options: any }) =>
      apiClient.post<any, Job>('/jobs', data),
    getStatus: (jobId: string) => apiClient.get<any, Job>(`/jobs/${jobId}`),
    cancel: (jobId: string) => apiClient.delete(`/jobs/${jobId}`),
  },
}
```

### Composables

```typescript
// src/composables/useFileUpload.ts
import { ref, computed } from 'vue'
import { api } from '@/api/client'
import type { UploadedFile } from '@/types'

export function useFileUpload(
  toolId: string,
  maxFiles: number,
  maxSizeMB: number,
  emit?: any
) {
  const isDragging = ref(false)
  const isUploading = ref(false)
  const progress = ref(0)
  const selectedFiles = ref<UploadedFile[]>([])

  const maxSizeBytes = maxSizeMB * 1024 * 1024

  const validateFiles = (files: File[]): { valid: File[]; errors: string[] } => {
    const valid: File[] = []
    const errors: string[] = []

    files.forEach(file => {
      // 检查文件类型
      if (file.type !== 'application/pdf') {
        errors.push(`${file.name} 不是 PDF 文件`)
        return
      }

      // 检查文件大小
      if (file.size > maxSizeBytes) {
        errors.push(`${file.name} 超过 ${maxSizeMB}MB 限制`)
        return
      }

      valid.push(file)
    })

    // 检查文件数量
    if (selectedFiles.value.length + valid.length > maxFiles) {
      errors.push(`最多只能上传 ${maxFiles} 个文件`)
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

    // 显示错误
    errors.forEach(error => {
      emit?.('error', error)
    })

    if (valid.length === 0) return

    // 上传文件
    await uploadFiles(valid)
  }

  const uploadFiles = async (files: File[]) => {
    isUploading.value = true
    progress.value = 0

    try {
      const formData = new FormData()
      files.forEach(file => formData.append('files', file))
      formData.append('tool_id', toolId)

      const response = await api.files.upload(formData, {
        onUploadProgress: (progressEvent) => {
          progress.value = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || 1)
          )
        }
      })

      selectedFiles.value = [...selectedFiles.value, ...response.files]
      emit?.('uploaded', response.upload_id, response.files)
    } catch (error: any) {
      emit?.('error', error.error?.message || '上传失败')
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
    handleDrop,
    handleFileSelect,
    removeFile,
  }
}
```

```typescript
// src/composables/usePolling.ts
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
      result.value = data.result
      error.value = data.error || null

      // 检查是否完成
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
    stopPolling,
  }
}
```

---

## 参考资料

### 设计灵感

- [Linear](https://linear.app) - 极简主义和微交互
- [Vercel](https://vercel.com) - 现代科技感设计
- [Raycast](https://raycast.com) - 高效的界面设计
- [Notion](https://notion.so) - 空气感布局

### 图标库

- [Lucide Icons](https://lucide.dev) - 使用的主要图标库
- [Heroicons](https://heroicons.com) - 备用图标

### 字体资源

- [Inter](https://rsms.me/inter/) - 主要字体
- [JetBrains Mono](https://www.jetbrains.com/lp/mono/) - 等宽字体

### 设计系统参考

- [Shadcn/ui](https://ui.shadcn.com) - 组件设计
- [Radix UI](https://www.radix-ui.com) - 无障碍组件
- [Headless UI](https://headlessui.com) - 无样式组件

---

**文档结束**

本设计文档定义了 PDF 文档工具网站的完整前端设计规范，包括美学方向、组件设计、交互流程和实现指南。按照此规范实施，可以构建一个专业、高效、美观的 PDF 处理平台。
