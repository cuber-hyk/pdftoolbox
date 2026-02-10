// Jobs API - 任务处理接口
import { apiClient } from './client'
import type { Job, JobStatus } from '@/types'

export interface JobCreateRequest {
  tool_id: string
  upload_id: string
  options: Record<string, any>
}

export const jobsApi = {
  /**
   * 创建处理任务
   */
  create: async (data: JobCreateRequest): Promise<{ success: boolean; data: Job }> => {
    const response: any = await apiClient.post('/v1/jobs', data)
    return response
  },

  /**
   * 获取任务状态
   */
  getStatus: async (jobId: string): Promise<{ success: boolean; data: Job }> => {
    const response: any = await apiClient.get(`/v1/jobs/${jobId}`)
    return response
  },

  /**
   * 取消任务
   */
  cancel: async (jobId: string): Promise<{ success: boolean; message: string }> => {
    const response: any = await apiClient.delete(`/v1/jobs/${jobId}`)
    return response
  }
}

export const POLLING_INTERVAL = 1000
export const MAX_POLLING_ATTEMPTS = 180
