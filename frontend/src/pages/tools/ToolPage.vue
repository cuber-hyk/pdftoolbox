<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import type { Tool, Job } from '@/types'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import { generateWatermarkImage, parseColorWithOpacity } from '@/utils/watermark'
import WatermarkTool from '@/components/tools/WatermarkTool.vue'
import RemoveWatermarkTool from '@/components/tools/RemoveWatermarkTool.vue'
import RemoveWatermarkImageTool from '@/components/tools/RemoveWatermarkImageTool.vue'

const route = useRoute()
const router = useRouter()

const tool = ref<Tool | null>(null)
const uploadId = ref<string | null>(null)
const currentJob = ref<Job | null>(null)
const options = ref<Record<string, any>>({})
const selectedFiles = ref<any[]>([])
const pendingFiles = ref<File[]>([])  // 本地存储待上传的文件
const isUploading = ref(false)
const uploadProgress = ref(0)
const pollInterval = ref<number | null>(null)
const fileInputRef = ref<HTMLInputElement | null>(null)
const draggedIndex = ref<number | null>(null)  // 拖拽的文件索引

const toolId = computed(() => route.params.toolId as string)

// 判断是否是水印工具
const isWatermarkTool = computed(() => toolId.value === 'add_watermark')

// 判断是否是除水印工具
const isRemoveWatermarkTool = computed(() => toolId.value === 'remove_watermark')

// 判断是否是图片颜色除水印工具
const isRemoveWatermarkImageTool = computed(() => toolId.value === 'remove_watermark_image')

onMounted(async () => {
  try {
    const response = await api.tools.getById(toolId.value)
    tool.value = response.data

    // Set default options
    if (tool.value?.options) {
      tool.value.options.forEach(opt => {
        if (opt.default !== undefined) {
          options.value[opt.name] = opt.default
        }
      })
    }
  } catch (error: any) {
    console.error('Failed to load tool:', error)
    router.push('/')
  }
})

onUnmounted(() => {
  if (pollInterval.value) {
    clearInterval(pollInterval.value)
  }
})

// 处理来自 WatermarkTool 组件的处理请求
const handleWatermarkProcessing = async ({ uploadId, options }: { uploadId: string, options: any }) => {
  try {
    const response = await api.jobs.create({
      tool_id: toolId.value,
      upload_id: uploadId,
      options: options
    })

    currentJob.value = response.data
    startPolling()
  } catch (error: any) {
    console.error('Failed to create job:', error)
    alert(error.error?.message || 'Failed to start processing')
  }
}

// 处理来自 RemoveWatermarkTool 组件的处理请求
const handleRemoveWatermarkProcessing = async ({ uploadId, options }: { uploadId: string, options: any }) => {
  try {
    const response = await api.jobs.create({
      tool_id: toolId.value,
      upload_id: uploadId,
      options: options
    })

    currentJob.value = response.data
    startPolling()
  } catch (error: any) {
    console.error('Failed to create job:', error)
    alert(error.error?.message || 'Failed to start processing')
  }
}

// 处理来自 RemoveWatermarkImageTool 组件的处理请求
const handleRemoveWatermarkImageProcessing = async ({ uploadId, options }: { uploadId: string, options: any }) => {
  try {
    const response = await api.jobs.create({
      tool_id: toolId.value,
      upload_id: uploadId,
      options: options
    })

    currentJob.value = response.data
    startPolling()
  } catch (error: any) {
    console.error('Failed to create job:', error)
    alert(error.error?.message || 'Failed to start processing')
  }
}

const onStartProcessing = async () => {
  // 如果还没有上传文件，先上传所有文件
  const uid = uploadId.value || await uploadAllFiles()
  if (!uid) return

  try {
    let finalOptions = { ...options.value }

    // For add_watermark tool, generate watermark image on frontend
    if (toolId.value === 'add_watermark' && options.value.type === 'text') {
      const watermarkImage = await generateWatermarkImage({
        text: options.value.text || 'Watermark',
        fontSize: 50,
        fontFamily: 'Arial, sans-serif',
        color: parseColorWithOpacity('#808080', options.value.opacity / 100),
        opacity: (options.value.opacity || 30) / 100,
        rotation: parseInt(options.value.rotation || '0')
      })
      // Add the generated image to options
      finalOptions = {
        ...finalOptions,
        watermark_image: watermarkImage
      }
    }

    const response = await api.jobs.create({
      tool_id: toolId.value,
      upload_id: uid,
      options: finalOptions
    })

    currentJob.value = response.data
    startPolling()
  } catch (error: any) {
    console.error('Failed to create job:', error)
    alert(error.error?.message || 'Failed to start processing')
  }
}

const startPolling = () => {
  pollInterval.value = window.setInterval(async () => {
    if (!currentJob.value) return

    try {
      const response = await api.jobs.getStatus(currentJob.value.job_id)
      currentJob.value = response.data

      if (response.data.status === 'completed' || response.data.status === 'failed') {
        if (pollInterval.value) {
          clearInterval(pollInterval.value)
          pollInterval.value = null
        }
      }
    } catch (error: any) {
      console.error('Failed to poll job status:', error)
    }
  }, 1000)
}

const handleFileUpload = (files: FileList) => {
  if (!tool.value || files.length === 0) return

  // 计算还能添加多少个文件
  const remainingSlots = tool.value.max_files - pendingFiles.value.length

  // 检查是否超过最大文件数
  if (files.length > remainingSlots) {
    alert(`只能再添加 ${remainingSlots} 个文件（当前 ${pendingFiles.value.length}/${tool.value.max_files}）\n请一次选择更多文件，或者删除部分文件后再添加。`)
    return
  }

  // 验证文件类型和大小
  const maxSizeBytes = tool.value.max_size_mb * 1024 * 1024
  const validFiles: File[] = []
  const invalidFiles: string[] = []

  for (const file of Array.from(files)) {
    if (!file.type.includes('pdf')) {
      invalidFiles.push(`${file.name} (不是PDF文件)`)
      continue
    }
    if (file.size > maxSizeBytes) {
      invalidFiles.push(`${file.name} (超过${tool.value.max_size_mb}MB限制)`)
      continue
    }
    validFiles.push(file)
  }

  // 如果有无效文件，显示提示
  if (invalidFiles.length > 0) {
    alert(`以下文件无法添加:\n${invalidFiles.join('\n')}`)
  }

  // 如果没有有效文件，直接返回
  if (validFiles.length === 0) {
    return
  }

  // 添加到待上传列表
  pendingFiles.value = [...pendingFiles.value, ...validFiles]

  // 更新显示的文件列表（使用本地文件信息）
  selectedFiles.value = pendingFiles.value.map((file, index) => ({
    file_id: `pending-${index}`,
    name: file.name,
    size: file.size
  }))
}

const uploadAllFiles = async () => {
  if (pendingFiles.value.length === 0 || !tool.value) return null

  isUploading.value = true
  uploadProgress.value = 0

  try {
    const formData = new FormData()
    // 按照当前 pendingFiles 的顺序上传
    pendingFiles.value.forEach(file => formData.append('files', file))
    formData.append('tool_id', tool.value.id)

    const response = await api.files.upload(formData, (progress) => {
      uploadProgress.value = progress
    })

    // 后端返回: {success: true, data: {upload_id: "...", files: [...]}}
    if (response?.data) {
      uploadId.value = response.data.upload_id
      // 清空 pendingFiles（已上传）
      pendingFiles.value = []
      // 更新 selectedFiles，保持文件名映射关系
      selectedFiles.value = response.data.files.map((serverFile: any, index: number) => ({
        ...serverFile,
        name: serverFile.name || selectedFiles.value[index]?.name || `file_${index + 1}.pdf`
      }))
      return response.data.upload_id
    }
    return null
  } catch (error: any) {
    console.error('Upload failed:', error)
    alert(error.error?.message || 'Upload failed')
    return null
  } finally {
    isUploading.value = false
  }
}

const isProcessing = computed(() =>
  currentJob.value?.status === 'queued' || currentJob.value?.status === 'processing'
)

const isCompleted = computed(() => currentJob.value?.status === 'completed')

const isFailed = computed(() => currentJob.value?.status === 'failed')

const removeFile = (fileId: string) => {
  // 如果文件ID是pending格式，从pendingFiles中移除
  if (fileId.startsWith('pending-')) {
    const index = parseInt(fileId.replace('pending-', ''))
    pendingFiles.value = pendingFiles.value.filter((_, i) => i !== index)
    // 重新生成文件列表
    regenerateFileIds()
  } else {
    // 已上传的文件，直接从 selectedFiles 移除
    selectedFiles.value = selectedFiles.value.filter(f => f.file_id !== fileId)
  }

  if (selectedFiles.value.length === 0) {
    uploadId.value = null
  }
}

const resetAndRetry = () => {
  currentJob.value = null
  uploadId.value = null
  selectedFiles.value = []
  pendingFiles.value = []
}

const downloadFile = () => {
  if (currentJob.value?.result?.download_url) {
    window.open(currentJob.value.result.download_url, '_self')
  }
}

const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

// 拖拽处理函数
const onDragStart = (index: number) => {
  draggedIndex.value = index
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()  // 允许放置
}

const onDrop = (targetIndex: number) => {
  if (draggedIndex.value === null || draggedIndex.value === targetIndex) {
    draggedIndex.value = null
    return
  }

  // 从 pendingFiles 中移除拖拽的文件
  const [movedFile] = pendingFiles.value.splice(draggedIndex.value, 1)
  // 插入到目标位置
  pendingFiles.value.splice(targetIndex, 0, movedFile)

  // 重新生成 file_id 映射
  regenerateFileIds()

  draggedIndex.value = null
}

const regenerateFileIds = () => {
  // 根据 pendingFiles 的顺序重新生成 selectedFiles 的 file_id
  selectedFiles.value = pendingFiles.value.map((file, i) => ({
    file_id: `pending-${i}`,
    name: file.name,
    size: file.size
  }))
}

// 获取工具选项
const getOption = (name: string) => {
  return tool.value?.options?.find((o: any) => o.name === name)
}

// 判断选项是否应该显示（处理依赖关系）
const shouldShowOption = (name: string) => {
  const opt = getOption(name)
  if (!opt) return false

  // 检查是否有依赖条件 depends_on
  if (opt.depends_on) {
    for (const [key, value] of Object.entries(opt.depends_on)) {
      if (options.value[key] !== value) {
        return false
      }
    }
  }

  return true
}

// 监听 mode 变化，重置相关选项
const handleModeChange = () => {
  // 当 mode 改变时，清除可能冲突的选项
  if (options.value.mode === 'single') {
    // 单页模式不需要额外选项
  } else if (options.value.mode === 'range') {
    // 清空 every_n
    delete options.value.every_n
  } else if (options.value.mode === 'every') {
    // 清空 ranges
    delete options.value.ranges
  }
}

// 监听 mode 变化
watch(() => options.value.mode, (newMode) => {
  if (newMode === 'range') {
    options.value.every_n = undefined
  } else if (newMode === 'every') {
    options.value.ranges = undefined
  } else if (newMode === 'single') {
    options.value.ranges = undefined
    options.value.every_n = undefined
  }
})
</script>

<template>
  <div class="h-screen bg-slate-50 overflow-hidden flex flex-col">
    <AppHeader :tool-title="tool?.name" />

    <main :class="isWatermarkTool || isRemoveWatermarkTool || isRemoveWatermarkImageTool ? 'max-w-7xl mx-auto px-4 py-2 flex flex-col min-h-0' : 'max-w-7xl mx-auto px-4 py-2 flex flex-col min-h-0'">
      <div v-if="tool">
        <!-- Watermark Tool - Special Layout -->
        <div v-if="isWatermarkTool" class="flex-1 min-h-0">
          <WatermarkTool
            :tool="tool"
            :current-job="currentJob"
            :on-processing-start="handleWatermarkProcessing"
            :on-download="downloadFile"
            :on-reset="resetAndRetry"
          />
        </div>

        <!-- Remove Watermark Tool - Special Layout -->
        <div v-if="isRemoveWatermarkTool" class="flex-1 min-h-0">
          <RemoveWatermarkTool
            :tool="tool"
            :current-job="currentJob"
            :on-processing-start="handleRemoveWatermarkProcessing"
            :on-download="downloadFile"
            :on-reset="resetAndRetry"
          />
        </div>

        <!-- Remove Watermark Image Tool - Special Layout -->
        <div v-if="isRemoveWatermarkImageTool" class="flex-1 min-h-0">
          <RemoveWatermarkImageTool
            :tool="tool"
            :current-job="currentJob"
            :on-processing-start="handleRemoveWatermarkImageProcessing"
            :on-download="downloadFile"
            :on-reset="resetAndRetry"
          />
        </div>

        <!-- Standard Tool Layout (for non-watermark tools) -->
        <div v-if="!isWatermarkTool && !isRemoveWatermarkTool && !isRemoveWatermarkImageTool" class="flex-1 min-h-0">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
            <!-- Left Panel: Upload & Files (2/3) -->
            <div class="lg:col-span-2 flex flex-col gap-4 h-full min-h-0">
        <!-- Upload area -->
        <div v-if="!isProcessing && !isCompleted && !isFailed" class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div
            class="border-2 border-dashed m-4 rounded-2xl p-12 transition-all duration-300
                   flex flex-col items-center justify-center gap-4 min-h-[240px]"
            :class="isUploading ? 'border-slate-300 bg-slate-50 opacity-50' : 'border-slate-300 bg-slate-50 hover:border-primary-400 hover:bg-white'"
          >
            <input
              ref="fileInputRef"
              type="file"
              :accept="'application/pdf'"
              :multiple="tool.max_files > 1"
              class="hidden"
              @change="(e) => handleFileUpload((e.target as HTMLInputElement).files!)"
              :disabled="isUploading"
            />

            <!-- Initial upload state - no files selected -->
            <template v-if="!isUploading && selectedFiles.length === 0">
              <div class="p-4 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50
                          w-20 h-20 flex items-center justify-center shadow-lg shadow-primary-100">
                <svg class="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
              </div>

              <p class="text-lg font-medium text-slate-700">Drag & drop files here</p>
              <p class="text-sm text-slate-500">or click to select files (max {{ tool.max_files }})</p>

              <button
                @click="triggerFileSelect"
                class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Select Files
              </button>

              <p class="text-xs text-slate-400">Supports PDF files, max {{ tool.max_size_mb }}MB per file</p>
            </template>

            <!-- Add more files state - some files selected but can add more -->
            <template v-else-if="!isUploading && selectedFiles.length > 0 && selectedFiles.length < tool.max_files">
              <div class="p-4 rounded-2xl bg-gradient-to-br from-green-100 to-green-50
                          w-20 h-20 flex items-center justify-center shadow-lg shadow-green-100">
                <svg class="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
              </div>

              <p class="text-lg font-medium text-slate-700">Add more files</p>
              <p class="text-sm text-slate-500">{{ selectedFiles.length }}/{{ tool.max_files }} files selected</p>

              <button
                @click="triggerFileSelect"
                class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Add More Files
              </button>

              <p class="text-xs text-slate-400">Supports PDF files, max {{ tool.max_size_mb }}MB per file</p>
            </template>

            <!-- Max files reached state -->
            <template v-else-if="!isUploading && selectedFiles.length >= tool.max_files">
              <div class="p-4 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-50
                          w-20 h-20 flex items-center justify-center shadow-lg shadow-blue-100">
                <svg class="w-10 h-10 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>

              <p class="text-lg font-medium text-slate-700">Maximum files reached</p>
              <p class="text-sm text-slate-500">{{ selectedFiles.length }}/{{ tool.max_files }} files selected</p>
              <p class="text-sm text-slate-400">Remove files to add different ones</p>
            </template>

            <div v-else-if="isUploading" class="text-center">
              <div class="relative w-32 h-32 mx-auto mb-4">
                <svg class="w-full h-full -rotate-90">
                  <circle cx="64" cy="64" r="56" fill="none" stroke="currentColor" class="text-slate-200" stroke-width="8" />
                  <circle
                    cx="64" cy="64" r="56" fill="none" stroke="currentColor" class="text-primary-600 transition-all duration-300"
                    :stroke-dasharray="351.86" :stroke-dashoffset="351.86 * (1 - uploadProgress / 100)" stroke-linecap="round"
                  />
                </svg>
                <div class="absolute inset-0 flex items-center justify-center">
                  <span class="text-2xl font-bold text-slate-700">{{ uploadProgress }}%</span>
                </div>
              </div>
              <p class="text-slate-600">Uploading...</p>
            </div>
          </div>

          <!-- Selected files list -->
          <div v-if="selectedFiles.length > 0" class="px-4 pb-4">
            <div class="flex items-center justify-between mb-2">
              <p class="text-sm font-medium text-slate-700">Selected files:</p>
              <p v-if="tool?.id === 'merge'" class="text-xs text-slate-500">
                Drag to reorder • Files will be merged in this order
              </p>
            </div>
            <div class="space-y-2 max-h-[200px] overflow-y-auto">
              <div
                v-for="(file, index) in selectedFiles"
                :key="file.file_id"
                class="flex items-center justify-between p-3 rounded-lg border transition-all duration-200"
                :class="{
                  'bg-slate-50 border-slate-200': draggedIndex !== index,
                  'bg-white border-primary-400 shadow-md': draggedIndex === index,
                  'ring-2 ring-primary-300': tool?.id === 'merge' && draggedIndex !== index
                }"
                :draggable="tool?.id === 'merge' && !isUploading"
                @dragstart="onDragStart(index)"
                @dragover="onDragOver"
                @drop="onDrop(index)"
              >
                <div class="flex items-center gap-3">
                  <!-- 拖拽把手 -->
                  <svg
                    v-if="tool?.id === 'merge'"
                    class="w-5 h-5 text-slate-400 cursor-move"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
                  </svg>
                  <!-- 序号 -->
                  <span
                    v-if="tool?.id === 'merge'"
                    class="w-6 h-6 flex items-center justify-center bg-primary-600 text-white text-sm font-semibold rounded-full"
                  >
                    {{ index + 1 }}
                  </span>
                  <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
                  </svg>
                  <span class="text-slate-700 truncate max-w-[200px]">{{ file.name }}</span>
                  <span class="text-sm text-slate-400">({{ (file.size / 1024 / 1024).toFixed(2) }} MB)</span>
                </div>
                <!-- 删除按钮 -->
                <button
                  v-if="!isUploading"
                  @click="removeFile(file.file_id)"
                  class="p-1 hover:bg-slate-200 rounded transition-colors"
                  title="Remove file"
                >
                  <svg class="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Progress -->
        <div v-if="isProcessing" class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
          <div class="mb-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-slate-700">Processing...</span>
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

        <!-- Result -->
        <div v-if="isCompleted" class="bg-white rounded-2xl shadow-sm border border-green-200 p-6">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-slate-900">Processing Complete!</h2>
              <p class="text-sm text-slate-500">Your file is ready for download</p>
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
            <button
              @click="downloadFile"
              class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
            >
              Download File
            </button>
            <button
              @click="resetAndRetry"
              class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
            >
              Process Again
            </button>
          </div>

          <p class="text-xs text-slate-400 mt-4 text-center">
            Files will be automatically deleted after 2 hours
          </p>
        </div>

        <!-- Error -->
        <div v-if="isFailed" class="bg-white rounded-2xl shadow-sm border border-red-200 p-6">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-slate-900">Processing Failed</h2>
              <p class="text-sm text-slate-500">{{ currentJob?.error?.message }}</p>
            </div>
          </div>

          <div class="flex gap-3">
            <button
              @click="resetAndRetry"
              class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
            >
              Retry
            </button>
            <button
              @click="router.push('/')"
              class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
            >
              Back to Home
            </button>
          </div>
        </div>
            </div>

            <!-- Right Panel: Options & Actions (1/3) -->
            <div class="flex flex-col gap-4 h-full min-h-0">
              <!-- Tool Options -->
              <div v-if="tool?.options && tool.options.length > 0" class="bg-white rounded-2xl shadow-sm border border-slate-200 flex flex-col overflow-hidden">
                <div class="px-4 py-3 border-b border-slate-200 bg-slate-50">
                  <h3 class="text-sm font-semibold text-slate-900">Processing Options</h3>
                </div>
                <div class="p-4 space-y-4 overflow-y-auto flex-1">
                  <!-- Split Mode Select -->
                  <div v-if="getOption('mode')" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('mode').label }}</label>
                    <select
                      v-model="options.mode"
                      @change="handleModeChange"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
                    >
                      <option v-for="opt in getOption('mode').options" :key="opt.value" :value="opt.value">
                        {{ opt.label }}
                      </option>
                    </select>
                    <p v-if="getOption('mode').description" class="text-xs text-slate-500">{{ getOption('mode').description }}</p>
                  </div>

                  <!-- Page Ranges Input - Only show when mode is 'range' -->
                  <div v-if="tool?.id === 'split' && options.mode === 'range'" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('ranges')?.label || 'Page Ranges' }}</label>
                    <input
                      v-model="options.ranges"
                      type="text"
                      :placeholder="getOption('ranges')?.placeholder || '1-3, 5-7'"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
                    >
                    <p v-if="getOption('ranges')?.description" class="text-xs text-slate-500">{{ getOption('ranges')?.description }}</p>
                    <p class="text-xs text-slate-400">Examples: <code class="bg-slate-200 px-1 rounded">1-3</code> <code class="bg-slate-200 px-1 rounded">5-7</code> <code class="bg-slate-200 px-1 rounded">1-3, 5-7</code></p>
                  </div>

                  <!-- Every N Pages Input - Only show when mode is 'every' -->
                  <div v-if="tool?.id === 'split' && options.mode === 'every'" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('every_n')?.label || 'Pages per File' }}</label>
                    <input
                      v-model.number="options.every_n"
                      type="number"
                      :min="getOption('every_n')?.min || 1"
                      :max="getOption('every_n')?.max || 100"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
                    >
                    <p v-if="getOption('every_n')?.description" class="text-xs text-slate-500">{{ getOption('every_n')?.description }}</p>
                    <div class="flex items-center gap-2 mt-2">
                      <button
                        v-for="n in [1, 2, 3, 5, 10]"
                        :key="n"
                        @click="options.every_n = n"
                        class="px-3 py-1 text-sm rounded-md border transition-colors"
                        :class="options.every_n === n ? 'bg-primary-100 border-primary-500 text-primary-700' : 'bg-white border-slate-300 text-slate-600 hover:bg-slate-50'"
                      >
                        {{ n }}
                      </button>
                    </div>
                  </div>

                  <!-- Pages Input (for extract_pages) -->
                  <div v-if="shouldShowOption('pages')" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('pages').label }}</label>
                    <input
                      v-model="options.pages"
                      type="text"
                      :placeholder="getOption('pages').placeholder"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
                    >
                    <p v-if="getOption('pages').description" class="text-xs text-slate-500">{{ getOption('pages').description }}</p>
                  </div>

                  <!-- Watermark Text Input -->
                  <div v-if="shouldShowOption('text')" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('text').label }}</label>
                    <input
                      v-model="options.text"
                      type="text"
                      :placeholder="getOption('text').placeholder"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 text-sm"
                    >
                  </div>

                  <!-- Number Input (for opacity, rotation, etc.) -->
                  <div v-if="shouldShowOption('opacity')" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('opacity').label }}</label>
                    <div class="flex items-center gap-3">
                      <input
                        v-model.number="options.opacity"
                        type="range"
                        :min="getOption('opacity').min"
                        :max="getOption('opacity').max"
                        class="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                      >
                      <span class="text-sm font-medium text-slate-700 w-12 text-center">{{ options.opacity }}%</span>
                    </div>
                  </div>

                  <div v-if="shouldShowOption('rotation')" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ getOption('rotation').label }}</label>
                    <div class="flex items-center gap-3">
                      <input
                        v-model.number="options.rotation"
                        type="range"
                        :min="getOption('rotation').min"
                        :max="getOption('rotation').max"
                        class="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
                      >
                      <span class="text-sm font-medium text-slate-700 w-12 text-center">{{ options.rotation }}°</span>
                    </div>
                  </div>

                  <!-- Generic Select -->
                  <div v-for="opt in tool.options.filter(o => o.type === 'select' && o.name !== 'mode')" :key="opt.name" class="space-y-2">
                    <label class="text-sm font-medium text-slate-700">{{ opt.label }}</label>
                    <select
                      v-model="options[opt.name]"
                      class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
                    >
                      <option v-for="choice in opt.options" :key="choice.value" :value="choice.value">
                        {{ choice.label }}
                      </option>
                    </select>
                    <p v-if="opt.description" class="text-xs text-slate-500">{{ opt.description }}</p>
                  </div>
                </div>
              </div>

              <!-- Action Button -->
              <button
                v-if="selectedFiles.length > 0 && !isUploading && !isProcessing && !isCompleted && !isFailed"
                @click="onStartProcessing"
                class="w-full py-3 bg-primary-600 text-white rounded-xl hover:bg-primary-700 transition-colors font-semibold shadow-lg shadow-primary-200 flex items-center justify-center gap-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Start Processing
              </button>

              <!-- Info Card -->
              <div class="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl p-4 border border-slate-200">
                <div class="flex items-start gap-3">
                  <svg class="w-5 h-5 text-slate-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div>
                    <p class="text-sm font-medium text-slate-700">About this tool</p>
                    <p class="text-xs text-slate-500 mt-1">{{ tool?.description }}</p>
                    <p class="text-xs text-slate-400 mt-2">Max files: {{ tool?.max_files }} • Max size: {{ tool?.max_size_mb }}MB each</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- End Standard Tool Layout -->
      </div>
    </main>

    <AppFooter />
  </div>
</template>
