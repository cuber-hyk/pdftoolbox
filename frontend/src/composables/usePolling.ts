// Polling Composable
import { ref, onUnmounted, computed, type Ref, type ComputedRef } from 'vue'
import { jobsApi, POLLING_INTERVAL, MAX_POLLING_ATTEMPTS } from '@/api/jobs'
import type { Job, JobStatus } from '@/types'

export interface UsePollingOptions {
  interval?: number
  maxAttempts?: number
  autoStart?: boolean
}

export interface UsePollingReturn {
  status: Ref<JobStatus>
  progress: Ref<number>
  message: Ref<string>
  result: Ref<Job['result'] | null>
  error: Ref<Job['error'] | null>
  isProcessing: ComputedRef<boolean>
  isCompleted: ComputedRef<boolean>
  isFailed: ComputedRef<boolean>
  startPolling: () => void
  stopPolling: () => void
  reset: () => void
}

export function usePolling(jobId: string, options: UsePollingOptions = {}): UsePollingReturn {
  const {
    interval = POLLING_INTERVAL,
    maxAttempts = MAX_POLLING_ATTEMPTS,
    autoStart = false
  } = options

  const status = ref<JobStatus>('queued' as JobStatus)
  const progress = ref(0)
  const message = ref('')
  const result = ref<Job['result'] | null>(null)
  const error = ref<Job['error'] | null>(null)

  let timer: number | null = null
  let attempts = 0

  const poll = async () => {
    try {
      const response = await jobsApi.getStatus(jobId)
      const job = response.data

      status.value = job.status
      progress.value = job.progress || 0
      message.value = job.message || ''
      result.value = job.result || null
      error.value = job.error || null

      if (job.status === 'completed' || job.status === 'failed') {
        stopPolling()
      }
    } catch (err: any) {
      console.error('Polling error:', err)

      error.value = {
        code: 'POLL_ERROR',
        message: err.error?.message || err.message || '查询状态失败'
      }
      status.value = 'failed'
      stopPolling()
    }
  }

  const startPolling = () => {
    if (timer) return

    timer = window.setInterval(() => {
      attempts++

      if (attempts > maxAttempts) {
        stopPolling()
        error.value = {
          code: 'TIMEOUT',
          message: '请求超时，请稍后重试'
        }
        status.value = 'failed'
      } else {
        poll()
      }
    }, interval)

    poll()
  }

  const stopPolling = () => {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  const reset = () => {
    stopPolling()
    status.value = 'queued' as JobStatus
    progress.value = 0
    message.value = ''
    result.value = null
    error.value = null
    attempts = 0
  }

  if (autoStart) {
    startPolling()
  }

  onUnmounted(() => {
    stopPolling()
  })

  const isProcessing = computed(() =>
    status.value === 'queued' || status.value === 'processing'
  )

  const isCompleted = computed(() => status.value === 'completed')

  const isFailed = computed(() => status.value === 'failed')

  return {
    status,
    progress,
    message,
    result,
    error,
    isProcessing,
    isCompleted,
    isFailed,
    startPolling,
    stopPolling,
    reset
  }
}
