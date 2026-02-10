/**
 * 文件 Store - 管理上传文件状态
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UploadedFile } from '@/types'

export const useFilesStore = defineStore('files', () => {
  const files = ref<Map<string, UploadedFile[]>>(new Map())
  const uploadIds = ref<Map<string, string>>(new Map()) // toolId -> uploadId

  // 获取工具的上传文件
  const getToolFiles = (toolId: string) => {
    return files.value.get(toolId) || []
  }

  // 设置工具的上传文件
  const setToolFiles = (toolId: string, uploadedFiles: UploadedFile[], ulId: string) => {
    files.value.set(toolId, uploadedFiles)
    uploadIds.value.set(toolId, ulId)
  }

  // 清空工具文件
  const clearToolFiles = (toolId: string) => {
    files.value.delete(toolId)
    uploadIds.value.delete(toolId)
  }

  // 获取 uploadId
  const getUploadId = (toolId: string) => {
    return uploadIds.value.get(toolId) || null
  }

  // 是否有文件
  const hasFiles = computed(() => (toolId: string) => {
    return (getToolFiles(toolId).length > 0)
  })

  return {
    files,
    uploadIds,
    getToolFiles,
    setToolFiles,
    clearToolFiles,
    getUploadId,
    hasFiles
  }
})
