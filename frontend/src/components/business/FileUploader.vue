/**
 * FileUploader - 文件上传组件
 * 支持拖拽、多文件上传、进度显示
 */
<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useFileUpload } from '@/composables/useFileUpload'
import FileList from './FileList.vue'

interface Props {
  toolId: string
  maxFiles?: number
  maxSize?: number
  accept?: string
  disabled?: boolean
}

interface Emits {
  uploaded: [uploadId: string, files: any[]]
  error: [message: string]
}

const props = withDefaults(defineProps<Props>(), {
  maxFiles: 1,
  maxSize: 100,
  accept: 'application/pdf',
  disabled: false
})

const emit = defineEmits<Emits>()

const fileInput = ref<HTMLInputElement | null>(null)

const {
  isDragging,
  isUploading,
  progress,
  selectedFiles,
  uploadId,
  canUploadMore,
  handleDrop,
  handleFileSelect,
  removeFile,
  resetDrag
} = useFileUpload({
  toolId: props.toolId,
  maxFiles: props.maxFiles,
  maxSizeMB: props.maxSize,
  accept: props.accept
})

const maxSizeBytes = computed(() => props.maxSize * 1024 * 1024)

// 监听上传完成
watch(() => uploadId.value, (newUploadId) => {
  if (newUploadId && selectedFiles.value.length > 0) {
    emit('uploaded', newUploadId, selectedFiles.value)
  }
})

const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  if (!props.disabled) {
    isDragging.value = true
  }
}

const handleDragLeave = () => {
  resetDrag()
}

const triggerFileSelect = () => {
  fileInput.value?.click()
}

const onFileInputChange = (e: Event) => {
  const input = e.target as HTMLInputElement
  const files = Array.from(input.files || [])
  handleFileSelect(files)
  // 重置 input 以允许重复选择同一文件
  input.value = ''
}

const handleRemove = (fileId: string) => {
  removeFile(fileId)
}

const handleDragDrop = async (e: DragEvent) => {
  if (props.disabled) return
  await handleDrop(e)
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
        isUploading || disabled ? 'opacity-50 pointer-events-none' : 'hover:border-primary-400 hover:bg-white cursor-pointer'
      ]"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDragDrop"
      @click="triggerFileSelect"
    >
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :multiple="maxFiles > 1"
        class="hidden"
        @change="onFileInputChange"
      />

      <!-- 空状态 -->
      <template v-if="!isUploading && selectedFiles.length === 0">
        <!-- 上传图标 -->
        <div class="p-4 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50
                    w-20 h-20 flex items-center justify-center shadow-lg shadow-primary-100">
          <svg class="w-10 h-10 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>

        <!-- 提示文字 -->
        <p class="text-lg font-medium text-slate-700">拖拽文件到此处</p>
        <p class="text-sm text-slate-500">或点击选择文件 (最多 {{ maxFiles }} 个)</p>

        <!-- 选择按钮 -->
        <button
          class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:scale-[0.98] transition-all font-medium"
        >
          选择文件
        </button>

        <!-- 限制提示 -->
        <p class="text-xs text-slate-400">
          支持 PDF 文件，单文件最大 {{ maxSize }}MB
        </p>
      </template>

      <!-- 上传中状态 -->
      <div v-else-if="isUploading" class="text-center">
        <!-- 进度环 -->
        <div class="relative w-32 h-32 mx-auto mb-4">
          <svg class="w-full h-full -rotate-90">
            <circle
              cx="64"
              cy="64"
              r="56"
              fill="none"
              stroke="currentColor"
              class="text-slate-200"
              stroke-width="8"
            />
            <circle
              cx="64"
              cy="64"
              r="56"
              fill="none"
              stroke="currentColor"
              class="text-primary-600 transition-all duration-300"
              :stroke-dasharray="351.86"
              :stroke-dashoffset="351.86 * (1 - progress / 100)"
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
      @remove="handleRemove"
    />
  </div>
</template>
