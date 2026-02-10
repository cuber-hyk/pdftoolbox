/**
 * 任务 Store - 管理 PDF 处理任务状态
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Job, JobStatus } from '@/types'
import { jobsApi } from '@/api/jobs'

export const useJobsStore = defineStore('jobs', () => {
  // 当前任务
  const currentJob = ref<Job | null>(null)
  const jobsHistory = ref<Map<string, Job>>(new Map())

  // 轮询定时器
  const pollInterval = ref<number | null>(null)

  // 计算属性
  const isProcessing = computed(() =>
    currentJob.value?.status === 'queued' || currentJob.value?.status === 'processing'
  )

  const isCompleted = computed(() => currentJob.value?.status === 'completed')

  const isFailed = computed(() => currentJob.value?.status === 'failed')

  /**
   * 创建任务
   */
  const createJob = async (
    toolId: string,
    uploadId: string,
    options: Record<string, any>
  ) => {
    try {
      const response = await jobsApi.create({
        tool_id: toolId,
        upload_id: uploadId,
        options
      })

      const job = response.data
      currentJob.value = job
      jobsHistory.value.set(job.job_id, job)

      return job
    } catch (error: any) {
      console.error('Failed to create job:', error)
      throw error
    }
  }

  /**
   * 更新任务
   */
  const updateJob = (updates: Partial<Job>) => {
    if (currentJob.value) {
      currentJob.value = { ...currentJob.value, ...updates }

      // 同步到历史记录
      if (currentJob.value.job_id) {
        jobsHistory.value.set(currentJob.value.job_id, currentJob.value)
      }
    }
  }

  /**
   * 开始轮询任务状态
   */
  const startPolling = (jobId: string) => {
    stopPolling()

    pollInterval.value = window.setInterval(async () => {
      if (!currentJob.value) return

      try {
        const response = await jobsApi.getStatus(jobId)
        const job = response.data

        updateJob(job)

        // 检查是否完成
        if (job.status === 'completed' || job.status === 'failed') {
          stopPolling()
        }
      } catch (error: any) {
        console.error('Failed to poll job status:', error)
        stopPolling()
      }
    }, 1000)
  }

  /**
   * 停止轮询
   */
  const stopPolling = () => {
    if (pollInterval.value) {
      clearInterval(pollInterval.value)
      pollInterval.value = null
    }
  }

  /**
   * 取消任务
   */
  const cancelJob = async (jobId: string) => {
    try {
      await jobsApi.cancel(jobId)
      updateJob({ status: 'cancelled' as JobStatus })
      stopPolling()
    } catch (error: any) {
      console.error('Failed to cancel job:', error)
      throw error
    }
  }

  /**
   * 清空当前任务
   */
  const clearCurrentJob = () => {
    currentJob.value = null
    stopPolling()
  }

  /**
   * 获取任务历史
   */
  const getJobFromHistory = (jobId: string) => {
    return jobsHistory.value.get(jobId)
  }

  return {
    currentJob,
    jobsHistory,
    isProcessing,
    isCompleted,
    isFailed,
    createJob,
    updateJob,
    startPolling,
    stopPolling,
    cancelJob,
    clearCurrentJob,
    getJobFromHistory
  }
})
