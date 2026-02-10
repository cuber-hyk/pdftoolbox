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
const pendingFiles = ref<File[]>([])
const isUploading = ref(false)
const uploadProgress = ref(0)
const fileInputRef = ref<HTMLInputElement | null>(null)

// 除水印配置
const removalMode = ref('all') // all, range, every, single
const pageRanges = ref('')
const everyN = ref(2)
const singlePage = ref(1)

// 预览相关
const pdfPreviewImages = ref<PDFPageImage[]>([])
const currentPreviewPage = ref(0)
const pdfScale = ref(0.7)

// 响应式布局常量
const LAYOUT_CONFIG = {
  containerHeight: 'calc(100vh - 102px)'
} as const

// 同步文件上传处理
const handleFileUpload = async (files: FileList) => {
  if (files.length === 0) return

  const file = files[0]
  if (!file.type.includes('pdf')) {
    alert('请上传 PDF 文件')
    return
  }

  try {
    await uploadFile(file)

    // 渲染 PDF 预览
    const images = await renderPDFToImages(file, 10, 1.5)
    pdfPreviewImages.value = images

    // 计算合适的缩放比例
    await nextTick()
    pdfScale.value = calculateScale()
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
    formData.append('tool_id', 'remove_watermark')

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
  if (pdfPreviewImages.value.length === 0) return 0.7

  const container = document.querySelector('.pdf-preview-container') as HTMLElement
  if (!container) return 0.7

  const containerWidth = container.clientWidth - 32 // padding
  const pageWidth = pdfPreviewImages.value[0]?.width || 0

  if (pageWidth > 0) {
    return Math.min(1.5, (containerWidth / pageWidth) * 0.9)
  }
  return 0.7
}

// 开始处理
const onStartProcessing = async () => {
  if (!uploadId.value) return

  const options: any = {
    mode: removalMode.value
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

// 计算状态
const isProcessing = computed(() =>
  props.currentJob?.status === 'queued' || props.currentJob?.status === 'processing'
)

const isCompleted = computed(() => props.currentJob?.status === 'completed')

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
  // 清除本地状态
  uploadId.value = null
  selectedFiles.value = []
  pdfPreviewImages.value = []
  currentPreviewPage.value = 0
  pageRanges.value = ''
}

// 移除文件
const removeFile = () => {
  uploadId.value = null
  selectedFiles.value = []
  pdfPreviewImages.value = []
  currentPreviewPage.value = 0
}

// 触发文件选择
const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

// 是否显示预览
const showPreview = computed(() => pdfPreviewImages.value.length > 0)

// 计算缩放百分比
const zoomPercent = computed(() => Math.round(pdfScale.value * 100))

// 缩放控制
const ZOOM_MIN = 0.25
const ZOOM_MAX = 4.0
const ZOOM_STEP = 0.1

const zoomIn = () => {
  pdfScale.value = Math.min(pdfScale.value + ZOOM_STEP, ZOOM_MAX)
}

const zoomOut = () => {
  pdfScale.value = Math.max(pdfScale.value - ZOOM_STEP, ZOOM_MIN)
}

const resetZoom = () => {
  pdfScale.value = calculateScale()
}

// 鼠标滚轮缩放
const onWheel = (e: WheelEvent) => {
  e.preventDefault()
  const delta = e.deltaY < 0 ? ZOOM_STEP : -ZOOM_STEP
  pdfScale.value = Math.max(ZOOM_MIN, Math.min(ZOOM_MAX, pdfScale.value + delta))
}

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
        @change="(e) => handleFileUpload((e.target as HTMLInputElement).files!)"
      />

      <div
        class="p-6 rounded-2xl bg-gradient-to-br from-red-100 to-red-50
                    w-28 h-28 flex items-center justify-center shadow-lg shadow-red-100"
      >
        <svg class="w-14 h-14 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6" />
        </svg>
      </div>

      <p class="text-xl font-semibold text-slate-700">
        {{ isDragOver ? '释放文件开始上传' : '拖拽 PDF 文件到此处' }}
      </p>
      <p class="text-base text-slate-500">上传包含水印的 PDF，快速清除水印内容</p>

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

  <!-- 上传中状态 -->
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

  <!-- 已上传文件：预览和配置 -->
  <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-4 min-h-0" :style="{ height: LAYOUT_CONFIG.containerHeight }">
    <!-- 左侧预览区域 -->
    <div class="lg:col-span-3 flex gap-3 h-full min-h-0">
      <!-- PDF预览 -->
      <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden h-full flex flex-col">
        <div class="px-3 py-2 border-b border-slate-200 flex-shrink-0 flex items-center justify-between">
          <h3 class="font-semibold text-slate-900 text-sm">PDF 预览</h3>

          <!-- 缩放控制 -->
          <div v-if="showPreview" class="flex items-center gap-1">
            <button @click="zoomOut" class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors" title="缩小">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
              </svg>
            </button>
            <span class="text-xs text-slate-500 font-medium min-w-[40px] text-center">{{ zoomPercent }}%</span>
            <button @click="zoomIn" class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors" title="放大">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
            </button>
            <button @click="resetZoom" class="p-1.5 hover:bg-slate-200 rounded-lg transition-colors" title="重置">
              <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h4m-4 0l5 5M4 16v4m0 0h4m-4 0l5 5" />
              </svg>
            </button>
          </div>
        </div>

        <div class="p-3 flex-1 flex flex-col min-h-0">
          <!-- 预览区域 -->
          <div class="flex-1 flex flex-col min-h-0">
            <!-- 页面切换 -->
            <div v-if="pdfPreviewImages.length > 1"
                 class="flex items-center justify-center gap-2 mb-2 flex-shrink-0">
              <button
                @click="currentPreviewPage = Math.max(0, currentPreviewPage - 1)"
                :disabled="currentPreviewPage === 0"
                class="p-1.5 hover:bg-slate-200 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
                <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <span class="text-xs text-slate-600 font-medium">
                {{ currentPreviewPage + 1 }} / {{ pdfPreviewImages.length }}
              </span>
              <button
                @click="currentPreviewPage = Math.min(pdfPreviewImages.length - 1, currentPreviewPage + 1)"
                :disabled="currentPreviewPage === pdfPreviewImages.length - 1"
                class="p-1.5 hover:bg-slate-200 rounded-lg disabled:opacity-30 disabled:cursor-not-allowed transition-colors">
                <svg class="w-4 h-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>

            <!-- PDF预览容器 -->
            <div
              class="pdf-preview-container relative rounded-lg overflow-hidden bg-slate-100 flex-1 min-h-0 flex items-center justify-center"
              @wheel.passive="onWheel"
            >
              <div
                v-if="pdfPreviewImages[currentPreviewPage]"
                class="relative transition-transform duration-75"
                :style="{
                  transform: `scale(${pdfScale})`,
                  transformOrigin: 'center'
                }"
              >
                <img
                  :src="pdfPreviewImages[currentPreviewPage].dataUrl"
                  :alt="`Page ${currentPreviewPage + 1}`"
                  class="block shadow-lg"
                  draggable="false"
                />
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
                title="移除文件">
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
            <option value="all">清除所有页面</option>
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
          >
          <p class="text-xs text-slate-500 mt-2">
            支持格式：单页(5)、范围(1-3)、末页(1--1)
          </p>
        </div>
      </div>

      <!-- 每隔 N 页 -->
      <div v-if="removalMode === 'every'" class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">间隔页数</h3>
        </div>
        <div class="p-3">
          <input
            v-model.number="everyN"
            type="number"
            min="2"
            max="100"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm"
          >
          <p class="text-xs text-slate-500 mt-2">
            清除每 {{ everyN }} 页的内容
          </p>
        </div>
      </div>

      <!-- 指定单页 -->
      <div v-if="removalMode === 'single'" class="bg-white rounded-2xl shadow-sm border border-slate-200">
        <div class="px-4 py-2.5 border-b border-slate-200">
          <h3 class="font-semibold text-slate-900 text-sm">指定页码</h3>
        </div>
        <div class="p-3">
          <input
            v-model.number="singlePage"
            type="number"
            min="1"
            :max="pdfPreviewImages.length"
            class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 text-sm"
          >
          <p class="text-xs text-slate-500 mt-2">
            共 {{ pdfPreviewImages.length }} 页
          </p>
        </div>
      </div>

      <!-- 处理按钮 -->
      <div class="flex flex-col gap-2">
        <button
          v-if="showPreview && !isProcessing && !isCompleted"
          @click="onStartProcessing"
          class="w-full py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-semibold text-sm">
          清除水印
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
