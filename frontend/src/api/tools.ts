// Tools API - 工具相关接口
import { apiClient } from './client'
import type { Tool } from '@/types'

export const toolsApi = {
  /**
   * 获取所有工具列表
   */
  getAll: async (): Promise<{ data: Tool[] }> => {
    const response: any = await apiClient.get('/v1/tools')
    return response
  },

  /**
   * 获取单个工具详情
   */
  getById: async (id: string): Promise<{ data: Tool }> => {
    const response: any = await apiClient.get(`/v1/tools/${id}`)
    return response
  }
}
