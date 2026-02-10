<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { api } from '@/api/client'
import type { Job } from '@/types'
import { generateWatermarkImage, parseColorWithOpacity } from '@/utils/watermark'
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
const pendingFiles = ref<File[]>([])
const isUploading = ref(false)
const uploadProgress = ref(0)
const fileInputRef = ref<HTMLInputElement | null>(null)
const previewContainerRef = ref<HTMLElement | null>(null)

// 水印配置
const watermarkText = ref('Watermark')
const watermarkColor = ref('#808080')
const watermarkOpacity = ref(70)
const watermarkRotation = ref(45)
const watermarkFontSize = ref(16)
const watermarkWidth = ref(100)
const watermarkHeight = ref(100)

// 水印间距 - 使用百分比模式（相对于水印尺寸的百分比）
// 0% = 紧凑排列（保留最小5%间距避免重叠），100% = 间距等于水印尺寸
const watermarkSpacingPercent = ref(30) // 默认 30%

// 计算实际间距像素值（用于后端）
const watermarkSpacingPx = computed(() => {
  // 最小间距为水印宽度的 5%（避免重叠）
  const minSpacing = watermarkWidth.value * 0.05
  // 实际间距 = 最小间距 + (百分比 * 水印宽度)
  return Math.round(minSpacing + (watermarkSpacingPercent.value / 100) * watermarkWidth.value)
})

// 预览相关
const watermarkImage = ref<string | null>(null) // 用于 PDF 覆盖层的水印（不包含旋转，旋转通过 CSS 应用）
const pdfPreviewImages = ref<PDFPageImage[]>([])
const currentPreviewPage = ref(0)
const pdfScale = ref(0.7) // 默认缩放
const pageWidth = ref(0) // PDF 页面宽度，用于计算水印预览缩放
const actualPageWidth = ref(0) // 实际 PDF 页面宽度（未缩放），用于确保预览与下载一致

// 单元预览的固定字体大小 - 完全不受用户设置影响
const UNIT_PREVIEW_FIXED_FONT_SIZE = 16
const unitPreviewRotation = ref(45) // 单独追踪预览区的旋转角度

// 平移相关状态
const isPanning = ref(false)
const panX = ref(0)
const panY = ref(0)
const panStartX = ref(0)
const panStartY = ref(0)
const initialPanX = ref(0)
const initialPanY = ref(0)

// 是否显示缩略图侧边栏
const showThumbnailSidebar = ref(true)

// 拖拽上传状态
const isDragOver = ref(false)
const isDragging = ref(false)

// 水印预览缩放比例（相对于实际 PDF 页面宽度）
// 计算包含间距的单元格大小，用于预览显示
// CSS 通过 background-size 控制单元格大小，空白处自然形成间距效果
const watermarkPreviewScale = computed(() => {
  if (actualPageWidth.value > 0 && watermarkWidth.value > 0) {
    // 单元格宽度 = 水印宽度 + 间距（与后端逻辑一致）
    const cellWidth = watermarkWidth.value + watermarkSpacingPx.value
    // 返回单元格相对于页面宽度的百分比
    return (cellWidth / actualPageWidth.value) * 100
  }
  return 20 // 默认值
})

// 同步单元预览的旋转角度与主旋转设置
watch(watermarkRotation, (newVal) => {
  unitPreviewRotation.value = newVal
})

// 是否显示预览
const showPreview = computed(() => pdfPreviewImages.value.length > 0)

// 生成水印图像 - 不包含旋转，旋转通过 CSS 实时应用以实现平滑效果
const generateWatermark = async () => {
  try {
    // 生成水印图像（不包含旋转，旋转通过 CSS 应用以实现平滑实时旋转）
    // 不在图像中包含间距，间距由 CSS 和后端分别处理
    watermarkImage.value = await generateWatermarkImage({
      text: watermarkText.value,
      fontSize: watermarkFontSize.value,
      fontFamily: 'Arial, sans-serif',
      color: parseColorWithOpacity(watermarkColor.value, watermarkOpacity.value / 100),
      opacity: watermarkOpacity.value / 100,
      rotation: 0, // 不在图像中嵌入旋转，通过 CSS 实现平滑旋转
      width: watermarkWidth.value,
      height: watermarkHeight.value
    })
  } catch (error) {
    console.error('Failed to generate watermark:', error)
  }
}

// 监听水印配置变化，自动重新生成（旋转和间距变化不触发重新生成）
watch([watermarkText, watermarkColor, watermarkOpacity, watermarkFontSize, watermarkWidth, watermarkHeight], () => {
  generateWatermark()
})

// 文件上传处理
const handleFileUpload = async (files: FileList) => {
  if (files.length === 0) return

  const file = files[0]
  if (!file.type.includes('pdf')) {
    alert('Please upload a PDF file')
    return
  }

  try {
    // 先上传文件到后端
    await uploadFile(file)

    // 渲染 PDF 预览 - 使用较高的 scale 以获得清晰预览
    const images = await renderPDFToImages(file, 10, 1.5)
    pdfPreviewImages.value = images

    // 记录 PDF 页面宽度
    if (images.length > 0) {
      pageWidth.value = images[0].width
      actualPageWidth.value = images[0].actualWidth // 实际页面尺寸（未缩放）
    }

    // 计算合适的缩放比例
    await nextTick()
    pdfScale.value = calculateScale()
  } catch (error: any) {
    console.error('Failed to render PDF:', error)
    const errorMsg = error?.message || error?.toString() || '未知错误'
    alert(`PDF 渲染失败: ${errorMsg}\n请检查控制台获取更多信息`)
  }
}

const uploadFile = async (file: File) => {
  isUploading.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    formData.append('files', file)
    formData.append('tool_id', props.tool.id)

    const response = await api.files.upload(formData, (progress) => {
      uploadProgress.value = progress
    })

    if (response?.data) {
      uploadId.value = response.data.upload_id
      selectedFiles.value = response.data.files
    }
  } catch (error: any) {
    console.error('Upload failed:', error)
    alert(error.error?.message || 'Upload failed')
  } finally {
    isUploading.value = false
  }
}

const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

// 取消上传
const cancelUpload = () => {
  isUploading.value = false
  uploadProgress.value = 0
}

const removeFile = () => {
  selectedFiles.value = []
  pendingFiles.value = []
  uploadId.value = null
  pdfPreviewImages.value = []
  currentPreviewPage.value = 0
  watermarkImage.value = null
  pdfScale.value = 0.7
  pageWidth.value = 0
  actualPageWidth.value = 0
  resetPan()
  showThumbnailSidebar.value = true
}

const onStartProcessing = async () => {
  if (!uploadId.value) return

  try {
    // 为下载生成包含旋转角度的水印图像
    const downloadWatermarkImage = await generateWatermarkImage({
    text: watermarkText.value,
    fontSize: watermarkFontSize.value,
    fontFamily: 'Arial, sans-serif',
    color: parseColorWithOpacity(watermarkColor.value, watermarkOpacity.value / 100),
    opacity: watermarkOpacity.value / 100,
    rotation: watermarkRotation.value, // 嵌入旋转角度用于下载
    width: watermarkWidth.value,
    height: watermarkHeight.value
  })

  // 发送完整的水印配置，确保后端使用与前端相同的参数
  const options = {
    type: 'text',
    text: watermarkText.value,
    opacity: watermarkOpacity.value,
    rotation: watermarkRotation.value,
    fontSize: watermarkFontSize.value,
    color: watermarkColor.value,
    watermark_image: downloadWatermarkImage, // 使用包含旋转的图像
    watermark_width: watermarkWidth.value,
    watermark_height: watermarkHeight.value,
    watermark_spacing: watermarkSpacingPx.value
  }

  props.onProcessingStart({ uploadId: uploadId.value, options })
  } catch (error) {
    console.error('Failed to generate watermark for download:', error)
    alert('生成水印失败，请重试')
  }
}

const isProcessing = computed(() =>
  props.currentJob?.status === 'queued' || props.currentJob?.status === 'processing'
)

const isCompleted = computed(() => props.currentJob?.status === 'completed')

const downloadFile = () => {
  props.onDownload?.()
}

const resetAndRetry = () => {
  props.onReset?.()
}

// 缩放控制 - 使用百分比 (25%-400%)
const ZOOM_MIN = 0.25 // 25%
const ZOOM_MAX = 4.0 // 400%
const ZOOM_STEP = 0.1 // 10% 步进

const zoomIn = () => {
  pdfScale.value = Math.min(pdfScale.value + ZOOM_STEP, ZOOM_MAX)
}

const zoomOut = () => {
  pdfScale.value = Math.max(pdfScale.value - ZOOM_STEP, ZOOM_MIN)
}

const resetZoom = () => {
  pdfScale.value = calculateScale()
  resetPan()
}

// 鼠标滚轮缩放处理
const onWheel = (e: WheelEvent) => {
  e.preventDefault()
  // 向前滚动 (deltaY < 0) 放大，向后滚动 (deltaY > 0) 缩小
  const delta = e.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP
  pdfScale.value = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, pdfScale.value + delta))
}

// 缩放百分比显示
const zoomPercent = computed(() => Math.round(pdfScale.value * 100))

// 平移控制
const resetPan = () => {
  panX.value = 0
  panY.value = 0
}

const startPan = (e: MouseEvent) => {
  if (pdfScale.value <= 0.5) return // 缩小时不需要平移
  isPanning.value = true
  panStartX.value = e.clientX
  panStartY.value = e.clientY
  initialPanX.value = panX.value
  initialPanY.value = panY.value

  // 添加全局事件监听
  document.addEventListener('mousemove', onPan)
  document.addEventListener('mouseup', endPan)
  document.addEventListener('mouseleave', endPan)
}

const onPan = (e: MouseEvent) => {
  if (!isPanning.value) return
  e.preventDefault()
  const dx = e.clientX - panStartX.value
  const dy = e.clientY - panStartY.value
  panX.value = initialPanX.value + dx
  panY.value = initialPanY.value + dy
}

const endPan = () => {
  isPanning.value = false
  document.removeEventListener('mousemove', onPan)
  document.removeEventListener('mouseup', endPan)
  document.removeEventListener('mouseleave', endPan)
}

// 水印间距控制（基于百分比）
const adjustSpacing = (delta: number) => {
  watermarkSpacingPercent.value = Math.max(0, Math.min(200, watermarkSpacingPercent.value + delta))
}

const resetSpacing = () => {
  watermarkSpacingPercent.value = 30 // 默认 30%
}

// 切换缩略图侧边栏
const toggleThumbnailSidebar = () => {
  showThumbnailSidebar.value = !showThumbnailSidebar.value
  // 切换后重新计算缩放
  nextTick(() => {
    pdfScale.value = calculateScale()
  })
}

// 选择缩略图页面
const selectPage = (index: number) => {
  currentPreviewPage.value = index
  resetPan()
}

// 拖拽上传处理
const onDragEnter = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = true
}

const onDragLeave = (e: DragEvent) => {
  e.preventDefault()
  // 只有当离开整个区域时才设置为 false
  const rect = (e.currentTarget as HTMLElement).getBoundingClientRect()
  const x = e.clientX
  const y = e.clientY
  if (x < rect.left || x > rect.right || y < rect.top || y > rect.bottom) {
    isDragOver.value = false
  }
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
}

const onDrop = async (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = false

  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    await handleFileUpload(files)
  }
}

const onFileInputChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    handleFileUpload(target.files)
  }
}

// 计算合适的 PDF 缩放比例
const calculateScale = () => {
  if (!previewContainerRef.value || pdfPreviewImages.value.length === 0) return 0.7

  const container = previewContainerRef.value
  const containerWidth = container.clientWidth - 32
  const containerHeight = container.clientHeight - 32

  const currentPage = pdfPreviewImages.value[currentPreviewPage.value]
  if (!currentPage) return 0.7

  const widthRatio = containerWidth / currentPage.width
  const heightRatio = containerHeight / currentPage.height

  return Math.min(widthRatio, heightRatio, 1.5)
}

// 响应式布局常量
const LAYOUT_CONFIG = {
  // 外层容器固定高度（100vh - header - main padding - footer - buffer）
  // header: 56px (h-14), main padding: 16px (py-2), footer: ~16px (py-2 + one-line content), buffer: 14px
  // 固定为 calc(100vh - 102px)
  containerHeight: 'calc(100vh - 102px)'
} as const
</script>

<template>
  <!-- 未上传文件时：居中的上传区域 -->
  <div
    v-if="!showPreview"
    class="h-full flex items-center justify-center p-8"
  >
    <div
      class="w-full max-w-2xl border-2 border-dashed rounded-2xl p-12 flex flex-col items-center justify-center gap-4 transition-all"
      :class="[
        isDragOver
          ? 'border-primary-500 bg-primary-50 scale-[1.01]'
          : 'border-slate-300 bg-white hover:border-primary-400'
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
        @change="onFileInputChange"
      />
      <div
        class="p-6 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50
                    w-28 h-28 flex items-center justify-center shadow-lg shadow-primary-100"
        :class="{ 'scale-110': isDragOver }"
      >
        <svg class="w-14 h-14 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </div>
      <p class="text-xl font-semibold text-slate-700">
        {{ isDragOver ? 'Drop file to upload' : 'Drag PDF file here' }}
      </p>
      <p class="text-base text-slate-500">Preview watermark effect in real-time</p>
      <div class="flex items-center gap-4 w-full max-w-xs">
        <div class="h-px flex-1 bg-slate-300"></div>
        <span class="text-sm text-slate-400">or</span>
        <div class="h-px flex-1 bg-slate-300"></div>
      </div>
      <button
        @click="triggerFileSelect"
        class="px-8 py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors text-base font-semibold shadow-lg shadow-primary-200">
        Select File
      </button>
    </div>
  </div>

  <!-- 上传中状态：居中显示 -->
  <div
    v-else-if="isUploading"
    class="h-full flex items-center justify-center"
  >
    <div class="text-center">
      <div class="w-24 h-24 rounded-full bg-primary-100 flex items-center justify-center mx-auto mb-6">
        <svg class="w-12 h-12 text-primary-600 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
      <p class="text-lg font-semibold text-slate-900 mb-1">Uploading...</p>
      <p class="text-base text-slate-500 mb-4">{{ uploadProgress }}%</p>
      <!-- 进度条 -->
      <div class="w-80 bg-slate-200 rounded-full h-3 mx-auto">
        <div
          class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-300"
          :style="{ width: `${uploadProgress}%` }"
        ></div>
      </div>
    </div>
  </div>

  <!-- 已上传文件：分栏视图 -->
  <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0" :style="{ height: LAYOUT_CONFIG.containerHeight }">
    <!-- 左侧预览区域 -->
    <div class="lg:col-span-3 flex gap-3 h-full min-h-0">
      <!-- 缩略图侧边栏 -->
      <div
        v-if="showPreview && showThumbnailSidebar && pdfPreviewImages.length > 1"
        class="w-28 flex-shrink-0 bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        <div class="px-3 py-2 border-b border-slate-200 bg-slate-50 flex-shrink-0">
          <span class="text-xs font-medium text-slate-600">Pages</span>
        </div>
        <div class="flex-1 overflow-y-auto p-2 space-y-2">
          <div
            v-for="(page, index) in pdfPreviewImages"
            :key="index"
            @click="selectPage(index)"
            :class="[
              'cursor-pointer rounded-lg overflow-hidden border-2 transition-all',
              currentPreviewPage === index
                ? 'border-primary-500 ring-1 ring-primary-200'
                : 'border-slate-200 hover:border-slate-300'
            ]">
            <img
              :src="page.dataUrl"
              :alt="`Page ${index + 1}`"
              class="w-full h-auto block"
            />
            <div class="text-center py-1 bg-slate-50">
              <span class="text-xs text-slate-500">{{ index + 1 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- PDF预览 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
        <div class="px-3 py-2 border-b border-slate-200 flex-shrink-0 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <h3 class="font-semibold text-slate-900 text-sm">PDF Preview</h3>
            <!-- 缩略图开关 -->
            <button
              v-if="showPreview && pdfPreviewImages.length > 1"
              @click="toggleThumbnailSidebar"
              :class="[
                'p-1.5 rounded-lg transition-colors text-xs flex items-center gap-1',
                showThumbnailSidebar
                  ? 'bg-primary-100 text-primary-700'
                  : 'hover:bg-slate-200 text-slate-600'
              ]"
              :title="showThumbnailSidebar ? 'Hide thumbnails' : 'Show thumbnails'">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
              </svg>
              <span class="hidden sm:inline">{{ pdfPreviewImages.length }} pages</span>
            </button>
          </div>
          <!-- 页码切换和缩放控制 -->
          <div v-if="showPreview" class="flex items-center gap-2">
            <!-- 页码切换 -->
            <template v-if="pdfPreviewImages.length > 1">
              <button
                @click="currentPreviewPage = Math.max(0, currentPreviewPage - 1); resetPan()"
                :disabled="currentPreviewPage === 0"
                class="p-1.5 hover:bg-slate-200 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Previous page">
                <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <span class="text-xs text-slate-600 font-medium min-w-[50px] text-center">
                {{ currentPreviewPage + 1 }} / {{ pdfPreviewImages.length }}
              </span>
              <button
                @click="currentPreviewPage = Math.min(pdfPreviewImages.length - 1, currentPreviewPage + 1); resetPan()"
                :disabled="currentPreviewPage === pdfPreviewImages.length - 1"
                class="p-1.5 hover:bg-slate-200 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                title="Next page">
                <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
              <div class="w-px h-4 bg-slate-300 mx-1"></div>
            </template>
            <!-- 缩放控制 -->
            <button
              @click="zoomOut"
              class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors"
              title="Zoom out">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>
            <span class="text-xs text-slate-500 font-medium min-w-[40px] text-center">{{ zoomPercent }}%</span>
            <button
              @click="zoomIn"
              class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors"
              title="Zoom in">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
            <button
              @click="resetZoom"
              class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors"
              title="Reset">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
            </button>
          </div>
        </div>

        <div class="p-3 flex-1 flex flex-col min-h-0">
          <!-- 预览区域 -->
          <div class="flex-1 flex flex-col min-h-0">
            <!-- PDF预览容器 -->
            <div
              ref="previewContainerRef"
              class="relative rounded-lg overflow-hidden bg-slate-100 flex-1 min-h-0 flex items-center justify-center"
              :class="[
                { 'cursor-grab': pdfScale > 0.5 && !isPanning, 'cursor-grabbing': isPanning }
              ]"
              @mousedown="startPan"
              @wheel.passive="onWheel"
            >
              <!-- PDF页面图像 - 使用缩放和平移 -->
              <div
                v-if="pdfPreviewImages[currentPreviewPage]"
                class="relative transition-transform duration-75"
                :style="{
                  transform: `scale(${pdfScale}) translate(${panX / pdfScale}px, ${panY / pdfScale}px)`,
                  transformOrigin: 'center'
                }"
              >
                <img
                  :src="pdfPreviewImages[currentPreviewPage].dataUrl"
                  :alt="`Page ${currentPreviewPage + 1}`"
                  class="block shadow-lg"
                  draggable="false"
                />

                <!-- 水印预览覆盖层 - 使用 backgroundSize 控制缩放，CSS 实现平滑旋转 -->
                <div
                  v-if="watermarkImage"
                  class="absolute inset-0 pointer-events-none transition-transform duration-75 ease-linear"
                  :style="{
                    backgroundImage: `url(${watermarkImage})`,
                    backgroundRepeat: 'repeat',
                    backgroundPosition: '0px 0px',
                    backgroundSize: `${watermarkPreviewScale}% auto`,
                    opacity: watermarkOpacity / 100,
                    transform: `rotate(${watermarkRotation}deg)`,
                    transformOrigin: 'center'
                  }"
                >
                </div>
              </div>
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
              <button
                @click="removeFile"
                v-if="!isProcessing"
                class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors"
                title="Remove file">
                <svg class="w-3.5 h-3.5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧配置区域 -->
    <div class="flex flex-col gap-3 h-full min-h-0 overflow-y-auto pr-1">
      <!-- Watermark Content -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-3 py-2 flex items-center gap-3">
          <h3 class="font-semibold text-slate-900 text-sm whitespace-nowrap">Watermark Content</h3>
          <input
            v-model="watermarkText"
            type="text"
            placeholder="Enter watermark text"
            class="flex-1 min-w-0 px-3 py-1.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
          >
        </div>
      </div>

      <!-- Watermark Configuration -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">Watermark Settings</h3>
        </div>
        <div class="p-3 space-y-3">
          <!-- Font Size -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="text-sm font-medium text-slate-700">Font Size</label>
              <span class="text-xs text-slate-500">{{ watermarkFontSize }}px</span>
            </div>
            <input
              v-model.number="watermarkFontSize"
              type="range"
              min="12"
              max="100"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            >
          </div>

          <!-- Rotation -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="text-sm font-medium text-slate-700">Rotation</label>
              <span class="text-xs text-slate-500">{{ watermarkRotation }}°</span>
            </div>
            <input
              v-model.number="watermarkRotation"
              type="range"
              min="0"
              max="360"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            >
          </div>

          <!-- Opacity -->
          <div>
            <div class="flex items-center justify-between mb-1">
              <label class="text-sm font-medium text-slate-700">Opacity</label>
              <span class="text-xs text-slate-500">{{ watermarkOpacity }}%</span>
            </div>
            <input
              v-model.number="watermarkOpacity"
              type="range"
              min="0"
              max="100"
              class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            >
          </div>

          <!-- Color and Size in one row -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Color</label>
              <div class="flex items-center gap-1">
                <div class="relative w-8 h-7 rounded overflow-hidden border border-slate-300 cursor-pointer hover:border-slate-400">
                  <input
                    v-model="watermarkColor"
                    type="color"
                    class="absolute inset-0 w-full h-full cursor-pointer opacity-0"
                  >
                  <div
                    class="w-full h-full"
                    :style="{ backgroundColor: watermarkColor }"
                  ></div>
                </div>
                <span class="text-xs text-slate-500 font-mono">{{ watermarkColor }}</span>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">Size</label>
              <div class="flex items-center gap-1">
                <input
                  v-model.number="watermarkWidth"
                  type="number"
                  min="50"
                  max="300"
                  class="w-full px-2 py-1.5 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                >
                <span class="text-xs text-slate-400">×</span>
                <input
                  v-model.number="watermarkHeight"
                  type="number"
                  min="50"
                  max="300"
                  class="w-full px-2 py-1.5 border border-slate-300 rounded text-xs focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Watermark Spacing -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-3 py-2 border-b border-slate-200 flex items-center justify-between">
          <h3 class="font-semibold text-slate-900 text-sm">Watermark Spacing</h3>
          <button
            @click="resetSpacing"
            class="text-xs text-primary-600 hover:text-primary-700 transition-colors">
            Reset
          </button>
        </div>
        <div class="p-2 space-y-2">
          <input
            v-model.number="watermarkSpacingPercent"
            type="range"
            min="0"
            max="200"
            class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          >
          <div class="flex justify-between items-center mt-1">
            <span class="text-xs text-slate-400">0%</span>
            <span class="text-xs text-slate-600 font-medium">{{ watermarkSpacingPercent }}% (~{{ watermarkSpacingPx }}px)</span>
            <span class="text-xs text-slate-400">200%</span>
          </div>
        </div>
      </div>

      <!-- Watermark Preview -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">Watermark Preview</h3>
        </div>
        <div class="p-3">
          <div
            class="rounded-lg flex items-center justify-center overflow-hidden relative"
            :style="{
              height: '120px',
              boxShadow: 'inset 0 0 0 1px rgba(0, 0, 0, 0.1)',
              backgroundColor: '#fafafa'
            }"
          >
            <div
              v-if="watermarkText"
              class="whitespace-nowrap select-none"
              :style="{
                fontSize: `${UNIT_PREVIEW_FIXED_FONT_SIZE}px`,
                fontFamily: 'Arial, sans-serif',
                color: watermarkColor,
                opacity: watermarkOpacity / 100,
                transform: `rotate(${watermarkRotation}deg)`,
                transformOrigin: 'center',
                transition: 'transform 0.1s linear, color 0.2s, opacity 0.2s'
              }"
            >
              {{ watermarkText }}
            </div>
            <div v-else class="text-slate-400 text-xs">
              Configure to see preview
            </div>
          </div>
          <p class="text-xs text-slate-500 mt-2 text-center">
            Shows color, rotation, and opacity effects
          </p>
        </div>
      </div>

      <!-- Action Button -->
      <div class="flex flex-col gap-2">
        <button
          v-if="showPreview && !isProcessing && !isCompleted"
          @click="onStartProcessing"
          :disabled="!watermarkImage"
          class="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed">
          Add Watermark
        </button>

        <!-- Processing -->
        <div v-if="isProcessing" class="bg-white rounded-lg p-2.5 shadow-sm">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-medium text-slate-700">Processing...</span>
            <span class="text-xs font-semibold text-primary-600">{{ props.currentJob?.progress }}%</span>
          </div>
          <div class="w-full bg-slate-200 rounded-full h-1.5">
            <div
              class="h-full bg-gradient-to-r from-primary-500 to-primary-600 rounded-full transition-all duration-500"
              :style="{ width: `${props.currentJob?.progress || 0}%` }"
            />
          </div>
        </div>

        <!-- Completed -->
        <div v-if="isCompleted" class="bg-white rounded-lg p-2.5 shadow-sm border border-green-200">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-3.5 h-3.5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-slate-900 text-sm truncate">Processing Complete</p>
              <p class="text-xs text-slate-500 truncate">{{ props.currentJob?.result?.filename }}</p>
            </div>
          </div>
          <div class="flex gap-2">
            <button
              @click="downloadFile"
              class="flex-1 py-1.5 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-xs font-semibold">
              Download
            </button>
            <button
              @click="resetAndRetry"
              class="px-3 py-1.5 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors text-xs">
              Retry
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
