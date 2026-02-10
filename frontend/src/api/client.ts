import axios from 'axios'
import type { APIResponse } from '@/types'

const baseURL = import.meta.env.VITE_API_URL || '/api'

export const apiClient = axios.create({
  baseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response) {
      return Promise.reject(error.response.data)
    } else if (error.request) {
      return Promise.reject({
        error: {
          code: 'NETWORK_ERROR',
          message: 'Network connection failed. Please check your network.'
        }
      })
    }
    return Promise.reject(error)
  }
)

// API methods
export const api = {
  tools: {
    getAll: () => apiClient.get<any, any>('/v1/tools'),
    getById: (id: string) => apiClient.get<any, any>(`/v1/tools/${id}`),
  },
  files: {
    upload: (formData: FormData, onProgress?: (progress: number) => void) => {
      return apiClient.post<any, any>('/v1/files/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          if (onProgress && progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress(progress)
          }
        }
      })
    },
    download: (fileId: string) => `/api/v1/files/download/${fileId}`,
  },
  jobs: {
    create: (data: { tool_id: string; upload_id: string; options: any }) =>
      apiClient.post<any, any>('/v1/jobs', data),
    getStatus: (jobId: string) => apiClient.get<any, any>(`/v1/jobs/${jobId}`),
    cancel: (jobId: string) => apiClient.delete(`/v1/jobs/${jobId}`),
  },
}
