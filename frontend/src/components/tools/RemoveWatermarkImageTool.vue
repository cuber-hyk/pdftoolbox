<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { api } from '@/api/client'
import type { Job } from '@/types'
import { renderPDFToImages, type PDFPageImage } from '@/utils/pdf'

interface Props {
  tool: any
  currentJob: Job | null
  onProcessingStart: (data: { uploadId: string, options: any }) => void
  onDownload?: () => void
  onReset?: () => void
}

const props = defineProps<Props>()

// 状态
const uploadId = ref<string | null>(null)
const selectedFiles = ref<any[]>([])
const isUploading = ref(false)
const uploadProgress = ref(0)
const fileInputRef = ref<HTMLInputElement | null>(null)

// 水印去除配置
const watermarkColorHex = ref('#c8c8c8')  // 使用 hex 格式
const tolerance = ref(30)
const backgroundColorHex = ref('#ffffff')  // 使用 hex 格式
const removalMode = ref('all')
const pageRanges = ref('')
const everyN = ref(2)
const singlePage = ref(1)
const dpi = ref(200)

// 预览相关
const pdfPreviewImages = ref<PDFPageImage[]>([])
const currentPreviewPage = ref(0)
const pdfScale = ref(0.5)
const previewCanvas = ref<HTMLCanvasElement | null>(null)
const isHoveringCanvas = ref(false)
const pickedColor = ref<string | null>(null)

// 响应式布局
const LAYOUT_CONFIG = {
  containerHeight: 'calc(100vh - 102px)'
} as const

// 辅助函数：hex 转 rgb 数组
const hexToRgb = (hex: string): [number, number, number] => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? [
    parseInt(result[1], 16),
    parseInt(result[2], 16),
    parseInt(result[3], 16)
  ] : [200, 200, 200]
}

// 辅助函数：rgb 数组转 hex
const rgbToHex = (r: number, g: number, b: number): string => {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

// 辅助函数：获取 RGB 值数组（用于发送到后端）
const getWatermarkColorRgb = (): [number, number, number] => {
  return hexToRgb(watermarkColorHex.value)
}

const getBackgroundColorRgb = (): [number, number, number] => {
  return hexToRgb(backgroundColorHex.value)
}

// 同步文件上传
const handleFileUpload = async (files: FileList) => {
  if (files.length === 0) return

  const file = files[0]
  if (!file.type.includes('pdf')) {
    alert('请上传 PDF 文件')
    return
  }

  try {
    await uploadFile(file)

    // 渲染第一页作为预览
    const images = await renderPDFToImages(file, 1, 1.0)
    pdfPreviewImages.value = images
    currentPreviewPage.value = 0

    await nextTick()
    pdfScale.value = calculateScale()
    showPreview.value = true

    // 初始化画布显示 PDF
    await initCanvas()
  } catch (error: any) {
    console.error('Failed to render PDF:', error)
    alert(`PDF 预览失败: ${error.message || error}`)
  }
}

// 上传文件
const uploadFile = async (file: File): Promise<void> => {
  isUploading.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('files', file)
    formData.append('tool_id', 'remove_watermark_image')

    const response = await api.files.upload(formData, (progress) => {
      uploadProgress.value = progress
    })

    if (response?.data?.upload_id) {
      uploadId.value = response.data.upload_id
      selectedFiles.value = response.data.files.map((f: any, i: number) => ({
        ...f,
        name: response.data.files[i]?.name || file.name
      }))
    }
  } catch (error: any) {
    console.error('Upload failed:', error)
    alert(error.error?.message || 'Upload failed')
    throw error
  } finally {
    isUploading.value = false
  }
}

// 计算缩放比例
const calculateScale = () => {
  if (pdfPreviewImages.value.length === 0) return 0.5
  const container = document.querySelector('.pdf-preview-container') as HTMLElement
  if (!container) return 0.5
  const containerWidth = container.clientWidth - 32
  const pageWidth = pdfPreviewImages.value[0]?.width || 0
  if (pageWidth > 0) {
    return Math.min(1.0, (containerWidth / pageWidth) * 0.95)
  }
  return 0.5
}

// 初始化画布 - 绘制 PDF 到 canvas
const initCanvas = async () => {
  await nextTick()

  const canvas = previewCanvas.value
  if (!canvas || pdfPreviewImages.value.length === 0) return

  const img = pdfPreviewImages.value[currentPreviewPage.value]
  const tempImg = new Image()
  tempImg.src = img.dataUrl

  await new Promise(resolve => {
    tempImg.onload = resolve
    tempImg.onerror = resolve
  })

  // 设置 canvas 尺寸为实际图片尺寸
  canvas.width = img.width
  canvas.height = img.height

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  // 绘制原始图片
  ctx.drawImage(tempImg, 0, 0)
}

// 从画布拾取颜色
const pickColorFromCanvas = (event: MouseEvent) => {
  const canvas = previewCanvas.value
  if (!canvas) return

  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height

  const x = (event.clientX - rect.left) * scaleX
  const y = (event.clientY - rect.top) * scaleY

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  const imageData = ctx.getImageData(x, y, 1, 1)
  const r = imageData.data[0]
  const g = imageData.data[1]
  const b = imageData.data[2]

  // 转换为 hex 并更新
  const hex = rgbToHex(r, g, b)
  watermarkColorHex.value = hex
  pickedColor.value = hex
}

// 鼠标悬停显示颜色
const onCanvasMouseMove = (event: MouseEvent) => {
  const canvas = previewCanvas.value
  if (!canvas) return

  const rect = canvas.getBoundingClientRect()
  const scaleX = canvas.width / rect.width
  const scaleY = canvas.height / rect.height
  const x = (event.clientX - rect.left) * scaleX
  const y = (event.clientY - rect.top) * scaleY

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  try {
    const imageData = ctx.getImageData(x, y, 1, 1)
    const r = imageData.data[0]
    const g = imageData.data[1]
    const b = imageData.data[2]
    pickedColor.value = rgbToHex(r, g, b)
  } catch {
    pickedColor.value = null
  }
}

// 计算状态
const isProcessing = computed(() =>
  props.currentJob?.status === 'queued' || props.currentJob?.status === 'processing'
)

const isCompleted = computed(() => props.currentJob?.status === 'completed')

const showPreview = computed(() => pdfPreviewImages.value.length > 0)

// 下载文件
const downloadFile = () => {
  if (props.currentJob?.result?.download_url) {
    window.open(props.currentJob.result.download_url, '_self')
  } else if (props.onDownload) {
    props.onDownload()
  }
}

// 重置并重试
const resetAndRetry = () => {
  if (props.onReset) {
    props.onReset()
  }
  uploadId.value = null
  selectedFiles.value = []
  pdfPreviewImages.value = []
  currentPreviewPage.value = 0
  pageRanges.value = ''
  pickedColor.value = null
}

// 移除文件
const removeFile = () => {
  uploadId.value = null
  selectedFiles.value = []
  pdfPreviewImages.value = []
  currentPreviewPage.value = 0
  pickedColor.value = null
}

// 触发文件选择
const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

// 颜色格式化显示
const formatRgbDisplay = (hex: string) => {
  const [r, g, b] = hexToRgb(hex)
  return `RGB(${r}, ${g}, ${b})`
}

// 缩放控制
const zoomPercent = computed(() => Math.round(pdfScale.value * 100))
const ZOOM_MIN = 0.25
const ZOOM_MAX = 2.0
const ZOOM_STEP = 0.1

const zoomIn = () => { pdfScale.value = Math.min(pdfScale.value + ZOOM_STEP, ZOOM_MAX) }
const zoomOut = () => { pdfScale.value = Math.max(pdfScale.value - ZOOM_STEP, ZOOM_MIN) }
const resetZoom = () => { pdfScale.value = calculateScale() }

// 拖拽上传状态
const isDragOver = ref(false)

const onDragEnter = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = true
}

const onDragLeave = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = false
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const onDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = false
  if (e.dataTransfer?.files?.length) {
    handleFileUpload(e.dataTransfer.files)
  }
}

// 开始处理
const onStartProcessing = async () => {
  if (!uploadId.value) return

  const rgbColor = getWatermarkColorRgb()
  const bgRgbColor = getBackgroundColorRgb()

  console.log('[DEBUG] Sending watermark_color:', rgbColor)
  console.log('[DEBUG] Sending tolerance:', tolerance.value)
  console.log('[DEBUG] Sending background_color:', bgRgbColor)

  const options: any = {
    watermark_color: rgbColor,
    tolerance: tolerance.value,
    background_color: bgRgbColor,
    mode: removalMode.value,
    dpi: dpi.value
  }

  if (removalMode.value === 'range') {
    if (!pageRanges.value.trim()) {
      alert('请输入页面范围')
      return
    }
    options.ranges = pageRanges.value
  } else if (removalMode.value === 'every') {
    options.every_n = everyN.value
  } else if (removalMode.value === 'single') {
    options.page = singlePage.value
  }

  props.onProcessingStart({ uploadId: uploadId.value, options })
}

// 监听 showPreview 变化，初始化 canvas
watch(showPreview, async (newValue) => {
  if (newValue) {
    await nextTick()
    await initCanvas()
  }
})
</script>

<template>
  <!-- 未上传文件时 -->
  <div
    v-if="!showPreview"
    class="h-full flex items-center justify-center p-8"
  >
    <div
      class="w-full max-w-2xl border-2 border-dashed rounded-2xl p-12 flex flex-col items-center justify-center gap-4 transition-all"
      :class="[
        isDragOver
          ? 'border-red-500 bg-red-50 scale-[1.01]'
          : 'border-slate-300 bg-white hover:border-red-400'
      ]"
      @dragenter="onDragEnter"
      @dragleave="onDragLeave"
      @dragover="onDragOver"
      @drop="onDrop"
    >
      <input
        ref="fileInputRef"
        type="file"
        accept="application/pdf"
        class="hidden"
        @change="(e) => handleFileUpload((e.target as HTMLInputElement).files!)"
      />

      <div
        class="p-6 rounded-2xl bg-gradient-to-br from-red-100 to-red-50
                    w-28 h-28 flex items-center justify-center shadow-lg shadow-red-100"
      >
        <svg class="w-14 h-14 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
      </div>

      <p class="text-xl font-semibold text-slate-700">
        {{ isDragOver ? '释放文件开始上传' : '上传含水印的 PDF' }}
      </p>
      <p class="text-base text-slate-500">点击预览中的水印区域选择颜色进行去除</p>

      <div class="flex items-center gap-4 w-full max-w-xs">
        <div class="h-px flex-1 bg-slate-300"></div>
        <span class="text-sm text-slate-400">或</span>
        <div class="h-px flex-1 bg-slate-300"></div>
      </div>

      <button
        @click="triggerFileSelect"
        class="px-8 py-3 bg-red-600 text-white rounded-xl hover:bg-red-700 transition-colors text-base font-semibold shadow-lg shadow-red-200">
        选择文件
      </button>
    </div>
  </div>

  <!-- 上传中 -->
  <div
    v-else-if="isUploading"
    class="h-full flex items-center justify-center"
  >
    <div class="text-center">
      <div class="w-24 h-24 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-6">
        <svg class="w-12 h-12 text-red-600 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 0 12 0h4zm1 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
      <p class="text-lg font-semibold text-slate-900 mb-1">上传中...</p>
      <p class="text-base text-slate-500 mb-4">{{ uploadProgress }}%</p>
      <div class="w-80 bg-slate-200 rounded-full h-3 mx-auto">
        <div
          class="h-full bg-gradient-to-r from-red-500 to-red-600 rounded-full transition-all duration-300"
          :style="{ width: `${uploadProgress}%` }"
        ></div>
      </div>
    </div>
  </div>

  <!-- 预览和配置 -->
  <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0" :style="{ height: LAYOUT_CONFIG.containerHeight }">
    <!-- 左侧预览区域 -->
    <div class="lg:col-span-3 flex gap-3 h-full min-h-0">
      <!-- PDF预览 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col flex-1">
        <div class="px-3 py-2 border-b border-slate-200 flex-shrink-0 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <h3 class="font-semibold text-slate-900 text-sm">PDF 预览</h3>
            <span v-if="pickedColor" class="text-xs px-2 py-0.5 rounded-full text-white" :style="{ backgroundColor: pickedColor }">
              {{ pickedColor?.toUpperCase() }}
            </span>
            <span v-if="pickedColor" class="text-xs text-slate-500">
              {{ formatRgbDisplay(pickedColor) }}
            </span>
          </div>

          <div class="flex items-center gap-1">
            <button @click="zoomOut" class="p-1.5 hover:bg-slate-200 rounded-lg" title="缩小">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>
            <span class="text-xs text-slate-500 font-medium min-w-[40px] text-center">{{ zoomPercent }}%</span>
            <button @click="zoomIn" class="p-1.5 hover:bg-slate-200 rounded-lg" title="放大">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
            <button @click="resetZoom" class="p-1.5 hover:bg-slate-200 rounded-lg" title="重置">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h4m-4 0l5 5M4 16v4m0 0h4m-4 0l5 5" />
              </svg>
            </button>
          </div>
        </div>

        <div class="p-3 flex-1 flex flex-col min-h-0">
          <div
            class="pdf-preview-container relative rounded-lg overflow-hidden bg-slate-100 flex-1 min-h-0 flex items-center justify-center cursor-crosshair"
            @wheel.prevent="(e: WheelEvent) => {
              const delta = e.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP
              pdfScale = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, pdfScale + delta))
            }"
          >
            <canvas
              ref="previewCanvas"
              class="max-w-full max-h-full"
              :style="{ transform: `scale(${pdfScale})`, transformOrigin: 'center' }"
              @click="pickColorFromCanvas"
              @mousemove="onCanvasMouseMove"
              @mouseenter="isHoveringCanvas = true"
              @mouseleave="isHoveringCanvas = false"
            />
          </div>

          <!-- 文件信息 -->
          <div class="flex items-center justify-between p-2 bg-slate-50 rounded-lg mt-2 flex-shrink-0">
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
              </svg>
              <span class="text-slate-700 text-sm">{{ selectedFiles[0]?.name }}</span>
              <span class="text-xs text-slate-400">({{ ((selectedFiles[0]?.size || 0) / 1024 / 1024).toFixed(2) }} MB)</span>
            </div>
            <div v-if="isHoveringCanvas && pickedColor" class="flex items-center gap-2">
              <span class="w-3 h-3 rounded border border-slate-300" :style="{ backgroundColor: pickedColor }"></span>
              <span class="text-xs text-slate-600">点击选择此颜色</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧配置区域 -->
    <div class="flex flex-col gap-3 h-full min-h-0 overflow-y-auto pr-1">
      <!-- 颜色选择 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">水印颜色</h3>
        </div>
        <div class="p-3">
          <div class="flex items-center gap-3">
            <input
              v-model="watermarkColorHex"
              type="color"
              class="w-12 h-12 rounded-lg cursor-pointer border-2 border-slate-200"
            />
            <div class="flex-1">
              <label class="text-xs text-slate-500">选中颜色</label>
              <div class="flex items-center gap-2 mt-1">
                <span class="text-sm font-mono">{{ watermarkColorHex.toUpperCase() }}</span>
                <span class="text-xs text-slate-500">{{ formatRgbDisplay(watermarkColorHex) }}</span>
              </div>
            </div>
          </div>
          <p class="text-xs text-slate-500 mt-2">点击预览图中的水印区域自动选择颜色</p>
        </div>
      </div>

      <!-- 容差设置 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">颜色容差</h3>
        </div>
        <div class="p-3">
          <div class="flex items-center gap-3">
            <input
              v-model.number="tolerance"
              type="range"
              min="10"
              max="100"
              class="flex-1"
            />
            <span class="text-sm font-medium text-slate-700 w-12 text-center">{{ tolerance }}</span>
          </div>
          <p class="text-xs text-slate-500 mt-2">值越大，匹配颜色范围越广</p>
        </div>
      </div>

      <!-- 背景颜色 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">替换颜色</h3>
        </div>
        <div class="p-3">
          <div class="flex items-center gap-3">
            <input
              v-model="backgroundColorHex"
              type="color"
              class="w-12 h-12 rounded-lg cursor-pointer border-2 border-slate-200"
            />
            <div class="flex-1">
              <label class="text-xs text-slate-500">背景颜色</label>
              <div class="flex items-center gap-2 mt-1">
                <span class="text-sm font-mono">{{ backgroundColorHex.toUpperCase() }}</span>
                <span class="text-xs text-slate-500">{{ formatRgbDisplay(backgroundColorHex) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 清除模式 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">清除模式</h3>
        </div>
        <div class="p-3">
          <select
            v-model="removalMode"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white text-sm"
          >
            <option value="all">所有页面</option>
            <option value="range">指定页面范围</option>
            <option value="every">每隔 N 页</option>
            <option value="single">指定单页</option>
          </select>
        </div>
      </div>

      <!-- 页面范围 -->
      <div v-if="removalMode === 'range'" class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">页面范围</h3>
        </div>
        <div class="p-3">
          <input
            v-model="pageRanges"
            type="text"
            placeholder="例如: 1-3, 5, 7-9"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm"
          />
        </div>
      </div>

      <!-- 渲染质量 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">渲染质量</h3>
        </div>
        <div class="p-3">
          <select
            v-model.number="dpi"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 bg-white text-sm"
          >
            <option :value="150">150 DPI (快速)</option>
            <option :value="200">200 DPI (平衡)</option>
            <option :value="300">300 DPI (高质量)</option>
          </select>
          <p class="text-xs text-slate-500 mt-2">更高的质量需要更长的处理时间</p>
        </div>
      </div>

      <!-- 处理按钮 -->
      <div class="flex flex-col gap-2">
        <button
          v-if="!isProcessing && !isCompleted"
          @click="onStartProcessing"
          class="w-full py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold text-sm">
          去除水印
        </button>

        <!-- 处理中 -->
        <div v-if="isProcessing" class="bg-white rounded-lg p-2.5 shadow-sm border border-slate-200">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-medium text-slate-700">处理中...</span>
            <span class="text-xs font-semibold text-red-600">{{ props.currentJob?.progress }}%</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-1.5">
            <div
              class="h-full bg-gradient-to-r from-red-500 to-red-600 rounded-full transition-all duration-500"
              :style="{ width: `${props.currentJob?.progress || 0}%` }"
            />
          </div>
        </div>

        <!-- 完成状态 -->
        <div v-if="isCompleted" class="bg-white rounded-lg p-2.5 shadow-sm border border-green-200">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-slate-900 text-sm truncate">处理完成</p>
              <p class="text-xs text-slate-500 truncate">{{ props.currentJob?.result?.filename }}</p>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              @click="downloadFile"
              class="flex-1 py-1.5 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-xs font-semibold">
              下载
            </button>
            <button
              @click="resetAndRetry"
              class="px-3 py-1.5 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors text-xs">
              重试
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
