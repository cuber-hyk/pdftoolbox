// Files API - 文件上传下载接口
import { apiClient } from './client'
import type { UploadedFile } from '@/types'

export interface UploadResponse {
  upload_id: string
  files: UploadedFile[]
  total_size: number
  expires_at: string
}

export const filesApi = {
  /**
   * 上传文件
   */
  upload: async (
    formData: FormData,
    onProgress?: (progress: number) => void
  ): Promise<{ success: boolean; data: UploadResponse }> => {
    const response: any = await apiClient.post('/v1/files/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (progressEvent: any) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    })
    return response
  },

  /**
   * 获取文件下载 URL
   */
  getDownloadUrl: (fileId: string): string => {
    return `/api/v1/files/download/${fileId}`
  },

  /**
   * 下载文件
   */
  download: (fileId: string, filename?: string) => {
    const url = `/api/v1/files/download/${fileId}`

    const link = document.createElement('a')
    link.href = url
    if (filename) {
      link.download = filename
    }
    link.style.display = 'none'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}
