/**
 * ProgressBar - 进度条组件
 * 显示任务处理进度，带动画效果
 */
<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  progress: number  // 0-100
  message?: string
  status?: 'processing' | 'completed' | 'error'
  showPercentage?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  status: 'processing',
  showPercentage: true
})

const barColor = computed(() => {
  switch (props.status) {
    case 'completed':
      return 'bg-green-500'
    case 'error':
      return 'bg-red-500'
    default:
      return 'bg-gradient-to-r from-blue-500 to-blue-600'
  }
})

const containerColor = computed(() => {
  switch (props.status) {
    case 'completed':
      return 'bg-green-100'
    case 'error':
      return 'bg-red-100'
    default:
      return 'bg-slate-200'
  }
})
</script>

<template>
  <div class="w-full">
    <!-- 进度条容器 -->
    <div class="relative h-3 rounded-full overflow-hidden" :class="containerColor">
      <!-- 进度条 -->
      <div
        class="h-full rounded-full transition-all duration-500 ease-out"
        :class="barColor"
        :style="{ width: `${Math.min(100, Math.max(0, progress))}%` }"
      />
    </div>

    <!-- 状态信息 -->
    <div class="flex items-center justify-between mt-2">
      <!-- 消息 -->
      <p class="text-sm text-slate-600">
        {{ message }}
      </p>

      <!-- 百分比 -->
      <p v-if="showPercentage" class="text-sm font-semibold" :class="status === 'error' ? 'text-red-600' : 'text-slate-700'">
        {{ progress }}%
      </p>
    </div>
  </div>
</template>
