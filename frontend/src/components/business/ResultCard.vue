/**
 * ResultCard - 结果卡片组件
 * 显示处理结果，支持下载和重新处理
 */
<script setup lang="ts">
import { computed } from 'vue'
import type { Job } from '@/types'
import { filesApi } from '@/api/files'

interface Props {
  job: Job
}

interface Emits {
  retry: []
  back: []
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const result = computed(() => props.job.result)
const error = computed(() => props.job.error)

const fileSize = computed(() => {
  const size = result.value?.size || 0
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(2)} MB`
})

const handleDownload = () => {
  if (result.value?.output_file_id) {
    filesApi.download(result.value.output_file_id, result.value.filename)
  }
}
</script>

<template>
  <!-- 成功状态 -->
  <div
    v-if="result"
    class="bg-white rounded-2xl p-6 shadow-sm border border-green-200 animate-fade-in"
  >
    <!-- 成功图标 -->
    <div class="flex items-center gap-3 mb-6">
      <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
        <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
      </div>
      <div>
        <h2 class="text-xl font-semibold text-slate-900">处理完成!</h2>
        <p class="text-sm text-slate-500">您的文件已准备好下载</p>
      </div>
    </div>

    <!-- 文件信息 -->
    <div class="bg-slate-50 rounded-lg p-4 mb-6">
      <div class="flex items-center gap-3">
        <svg class="w-10 h-10 text-red-500" fill="currentColor" viewBox="0 0 20 20">
          <path
            fill-rule="evenodd"
            d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
            clip-rule="evenodd"
          />
        </svg>
        <div class="flex-1 min-w-0">
          <p class="font-medium text-slate-900 truncate">
            {{ result.filename }}
          </p>
          <p class="text-sm text-slate-500">
            {{ fileSize }}
          </p>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex gap-3">
      <button
        @click="handleDownload"
        class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:scale-[0.98] transition-all font-semibold"
      >
        下载文件
      </button>
      <button
        @click="emit('retry')"
        class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 active:scale-[0.98] transition-all"
      >
        再次处理
      </button>
    </div>

    <!-- 过期提示 -->
    <p class="text-xs text-slate-400 mt-4 text-center">
      文件将在 2 小时后自动删除
    </p>
  </div>

  <!-- 失败状态 -->
  <div
    v-else-if="error"
    class="bg-white rounded-2xl p-6 shadow-sm border border-red-200 animate-fade-in"
  >
    <!-- 错误图标 -->
    <div class="flex items-center gap-3 mb-4">
      <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
        <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </div>
      <div>
        <h2 class="text-xl font-semibold text-slate-900">处理失败</h2>
        <p class="text-sm text-slate-500">{{ error.message }}</p>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex gap-3">
      <button
        @click="emit('retry')"
        class="flex-1 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 active:scale-[0.98] transition-all font-semibold"
      >
        重试
      </button>
      <button
        @click="emit('back')"
        class="px-6 py-3 border border-slate-300 rounded-lg hover:bg-slate-50 active:scale-[0.98] transition-all"
      >
        返回首页
      </button>
    </div>
  </div>
</template>
