/**
 * FileList - 文件列表组件
 * 显示已上传的文件，支持拖拽排序（TODO）、删除
 */
<script setup lang="ts">
import { computed } from 'vue'
import type { UploadedFile } from '@/types'

interface Props {
  files: UploadedFile[]
  removable?: boolean
  sortable?: boolean
}

interface Emits {
  remove: [fileId: string]
  reorder: [fromIndex: number, toIndex: number]
}

const props = withDefaults(defineProps<Props>(), {
  removable: true,
  sortable: false
})

const emit = defineEmits<Emits>()

const totalSize = computed(() =>
  props.files.reduce((sum, file) => sum + file.size, 0)
)

const formatSize = (bytes: number): string => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(2)} MB`
}

const handleRemove = (fileId: string) => {
  emit('remove', fileId)
}
</script>

<template>
  <div v-if="files.length > 0" class="space-y-2">
    <p class="text-sm font-medium text-slate-700 mb-2">
      已选文件 ({{ files.length }} 个):
    </p>

    <div
      v-for="file in files"
      :key="file.file_id"
      class="flex items-center justify-between p-3 bg-white rounded-lg border border-slate-200 hover:border-slate-300 transition-colors"
    >
      <div class="flex items-center gap-3 flex-1 min-w-0">
        <!-- PDF 图标 -->
        <svg class="w-5 h-5 text-red-500 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
            clip-rule="evenodd"
          />
        </svg>

        <!-- 文件信息 -->
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium text-slate-900 truncate">
            {{ file.name }}
          </p>
          <p class="text-xs text-slate-400">
            {{ file.pages }} 页 · {{ formatSize(file.size) }}
          </p>
        </div>
      </div>

      <!-- 删除按钮 -->
      <button
        v-if="removable"
        @click="handleRemove(file.file_id)"
        class="p-1 hover:bg-slate-100 rounded-lg transition-colors flex-shrink-0"
        aria-label="删除文件"
      >
        <svg class="w-4 h-4 text-slate-400 hover:text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- 总计 -->
    <p class="text-xs text-slate-400 mt-2">
      总计: {{ formatSize(totalSize) }}
    </p>
  </div>
</template>
