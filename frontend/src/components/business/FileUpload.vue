<script setup lang="ts">
import { ref, computed } from 'vue'

interface FileItem {
  file_id: string
  name: string
  size: number
  index?: number
}

interface Props {
  tool: {
    id: string
    name: string
    max_files: number
    max_size_mb: number
    description?: string
  }
  files: FileItem[]
  isUploading: boolean
  uploadProgress: number
  accept?: string
  multiple?: boolean
  showDragReorder?: boolean
  draggedIndex: number | null
}

interface Emits {
  (e: 'fileSelect', files: FileList): void
  (e: 'fileRemove', fileId: string): void
  (e: 'dragStart', index: number): void
  (e: 'dragOver', e: DragEvent): void
  (e: 'drop', index: number): void
}

const props = withDefaults(defineProps<Props>(), {
  accept: 'application/pdf',
  multiple: false,
  showDragReorder: false,
  draggedIndex: null
})

const emit = defineEmits<Emits>()

const fileInputRef = ref<HTMLInputElement | null>(null)

const isMaxFilesReached = computed(() => props.files.length >= props.tool.max_files)

const canAddMore = computed(() => props.files.length < props.tool.max_files)

const formatFileSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

const triggerFileSelect = () => {
  fileInputRef.value?.click()
}

const onFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    emit('fileSelect', target.files)
    target.value = ''
  }
}

const onDragEnter = (e: DragEvent) => {
  e.preventDefault()
}

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
  emit('dragOver', e)
}

const onDrop = (e: DragEvent, targetIndex: number) => {
  e.preventDefault()
  emit('drop', targetIndex)
}

const onDragStart = (index: number) => {
  emit('dragStart', index)
}

const removeFile = (fileId: string) => {
  emit('fileRemove', fileId)
}
</script>

<template>
  <div
    class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden"
    :class="{ 'opacity-50': isUploading }"
  >
    <!-- Upload Area -->
    <div
      v-if="!isUploading && !isMaxFilesReached"
      class="border-2 border-dashed m-4 rounded-2xl p-8 transition-all duration-300 flex flex-col items-center justify-center gap-3"
      :class="[
        'border-slate-300 bg-slate-50 hover:border-primary-400 hover:bg-white'
      ]"
      @dragenter="onDragEnter"
      @dragover="onDragOver"
      @drop="onDrop($event, files.length)"
    >
      <input
        ref="fileInputRef"
        type="file"
        :accept="accept"
        :multiple="multiple || tool.max_files > 1"
        class="hidden"
        @change="onFileChange"
      />

      <!-- Icon -->
      <div class="p-4 rounded-2xl bg-gradient-to-br from-primary-100 to-primary-50 w-16 h-16 flex items-center justify-center shadow-lg shadow-primary-100">
        <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
      </div>

      <!-- Text -->
      <div class="text-center">
        <p class="text-lg font-medium text-slate-700">Drag & drop files here</p>
        <p class="text-sm text-slate-500 mt-1">
          {{ multiple || tool.max_files > 1 ? `Max ${tool.max_files} files` : 'Select a file' }}
        </p>
      </div>

      <!-- Divider -->
      <div class="flex items-center gap-4 w-full max-w-xs">
        <div class="h-px flex-1 bg-slate-300"></div>
        <span class="text-sm text-slate-400">or</span>
        <div class="h-px flex-1 bg-slate-300"></div>
      </div>

      <!-- Button -->
      <button
        @click="triggerFileSelect"
        class="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-medium"
      >
        Select Files
      </button>

      <p class="text-xs text-slate-400">
        Supports PDF, max {{ tool.max_size_mb }}MB per file
      </p>
    </div>

    <!-- Max Files Reached State -->
    <div
      v-else-if="!isUploading && isMaxFilesReached"
      class="border-2 border-dashed m-4 rounded-2xl p-8 transition-all duration-300 flex flex-col items-center justify-center gap-3"
      :class="[
        'border-blue-300 bg-blue-50'
      ]"
    >
      <div class="p-4 rounded-2xl bg-gradient-to-br from-blue-100 to-blue-50 w-16 h-16 flex items-center justify-center shadow-lg shadow-blue-100">
        <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 0 0118 0z" />
        </svg>
      </div>
      <div class="text-center">
        <p class="text-lg font-medium text-slate-700">Maximum files reached</p>
        <p class="text-sm text-slate-500 mt-1">{{ files.length }}/{{ tool.max_files }} files selected</p>
      </div>
      <p class="text-xs text-slate-400">Remove files to add different ones</p>
    </div>

    <!-- Uploading State -->
    <div v-else-if="isUploading" class="p-8">
      <div class="flex flex-col items-center justify-center">
        <div class="relative w-24 h-24 mb-4">
          <svg class="w-full h-full -rotate-90">
            <circle
              cx="48"
              cy="48"
              r="42"
              fill="none"
              stroke="currentColor"
              class="text-slate-200"
              stroke-width="6"
            />
            <circle
              cx="48"
              cy="48"
              r="42"
              fill="none"
              stroke="currentColor"
              class="text-primary-600 transition-all duration-300"
              :stroke-dasharray="264"
              :stroke-dashoffset="264 * (1 - uploadProgress / 100)"
              stroke-linecap="round"
              stroke-width="6"
            />
          </svg>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-xl font-bold text-slate-700">{{ uploadProgress }}%</span>
          </div>
        </div>
        <p class="text-slate-600 font-medium">Uploading...</p>
      </div>
    </div>

    <!-- Files List -->
    <div v-if="files.length > 0" class="px-4 pb-4">
      <div class="flex items-center justify-between mb-2">
        <p class="text-sm font-medium text-slate-700">Selected files:</p>
        <p v-if="showDragReorder" class="text-xs text-slate-500">
          Drag to reorder • Files will be merged in this order
        </p>
      </div>
      
      <div class="space-y-2 max-h-[200px] overflow-y-auto">
        <div
          v-for="(file, index) in files"
          :key="file.file_id"
          class="flex items-center justify-between p-3 rounded-lg border transition-all duration-200"
          :class="{
            'bg-slate-50 border-slate-200': draggedIndex !== index,
            'bg-white border-primary-400 shadow-md': draggedIndex === index,
            'ring-2 ring-primary-300': showDragReorder && draggedIndex !== index
          }"
          :draggable="showDragReorder && !isUploading"
          @dragstart="onDragStart(index)"
          @dragover="onDragOver"
          @drop="onDrop($event, index)"
        >
          <div class="flex items-center gap-3">
            <!-- Drag Handle (for merge tool) -->
            <svg
              v-if="showDragReorder"
              class="w-5 h-5 text-slate-400 cursor-move"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16" />
            </svg>
            
            <!-- Order Number (for merge tool) -->
            <span
              v-if="showDragReorder"
              class="w-6 h-6 flex items-center justify-center bg-primary-600 text-white text-sm font-semibold rounded-full"
            >
              {{ index + 1 }}
            </span>
            
            <!-- File Icon -->
            <svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd" />
            </svg>
            
            <!-- File Info -->
            <div class="flex flex-col">
              <span class="text-slate-700 truncate max-w-[200px] text-sm">{{ file.name }}</span>
              <span class="text-xs text-slate-400">{{ formatFileSize(file.size) }}</span>
            </div>
          </div>
          
          <!-- Remove Button -->
          <button
            v-if="!isUploading"
            @click="removeFile(file.file_id)"
            class="p-1.5 hover:bg-slate-200 rounded transition-colors"
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
</template>
