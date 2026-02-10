// File Upload Composable
import { ref, computed, type Ref, type ComputedRef } from 'vue'
import { filesApi } from '@/api/files'
import type { UploadedFile } from '@/types'

export interface UseFileUploadOptions {
  toolId: string
  maxFiles?: number
  maxSizeMB?: number
  accept?: string
}

export interface UseFileUploadReturn {
  isDragging: Ref<boolean>
  isUploading: Ref<boolean>
  progress: Ref<number>
  selectedFiles: Ref<UploadedFile[]>
  uploadId: Ref<string | null>
  canUploadMore: ComputedRef<boolean>
  uploadProgress: ComputedRef<number>
  handleDrop: (e: DragEvent) => Promise<void>
  handleFileSelect: (files: File[]) => Promise<void>
  removeFile: (fileId: string) => void
  clearAll: () => void
  resetDrag: () => void
}

export function useFileUpload(options: UseFileUploadOptions): UseFileUploadReturn {
  const {
    toolId,
    maxFiles = 1,
    maxSizeMB = 100,
    accept = 'application/pdf'
  } = options

  const isDragging = ref(false)
  const isUploading = ref(false)
  const progress = ref(0)
  const selectedFiles = ref<UploadedFile[]>([])
  const uploadId = ref<string | null>(null)

  const maxSizeBytes = maxSizeMB * 1024 * 1024

  const canUploadMore = computed(() => selectedFiles.value.length < maxFiles)
  const uploadProgress = computed(() => progress.value)

  const validateFiles = (files: File[]): { valid: File[]; errors: string[] } => {
    const valid: File[] = []
    const errors: string[] = []

    files.forEach(file => {
      if (!file.type.includes('pdf')) {
        errors.push(`${file.name} 不是 PDF 文件`)
        return
      }

      if (file.size > maxSizeBytes) {
        errors.push(`${file.name} 超过 ${maxSizeMB}MB 限制`)
        return
      }

      valid.push(file)
    })

    if (selectedFiles.value.length + valid.length > maxFiles) {
      errors.push(`最多只能上传 ${maxFiles} 个文件`)
      return { valid: [], errors }
    }

    return { valid, errors }
  }

  const uploadFiles = async (files: File[]) => {
    isUploading.value = true
    progress.value = 0

    try {
      const formData = new FormData()
      files.forEach(file => formData.append('files', file))
      formData.append('tool_id', toolId)

      const response = await filesApi.upload(formData, (p) => {
        progress.value = p
      })

      // 后端返回: {success: true, data: {upload_id: "...", files: [...]}}
      // API拦截器返回: response.data，所以这里 response 就是 {success: true, data: {...}}
      if (response?.data) {
        uploadId.value = response.data.upload_id
        selectedFiles.value = [...selectedFiles.value, ...response.data.files]
      }
    } catch (error: any) {
      console.error('Upload failed:', error)
      const errorMessage = error.error?.message || error.message || '上传失败'
      throw new Error(errorMessage)
    } finally {
      isUploading.value = false
      progress.value = 0
    }
  }

  const handleDrop = async (e: DragEvent) => {
    e.preventDefault()
    isDragging.value = false

    const files = Array.from(e.dataTransfer?.files || [])
    await processFiles(files)
  }

  const handleFileSelect = async (files: File[]) => {
    await processFiles(files)
  }

  const processFiles = async (files: File[]) => {
    const { valid, errors } = validateFiles(files)

    if (errors.length > 0) {
      console.warn('Upload errors:', errors)
    }

    if (valid.length === 0) return

    await uploadFiles(valid)
  }

  const removeFile = (fileId: string) => {
    selectedFiles.value = selectedFiles.value.filter(f => f.file_id !== fileId)

    if (selectedFiles.value.length === 0) {
      uploadId.value = null
    }
  }

  const clearAll = () => {
    selectedFiles.value = []
    uploadId.value = null
    progress.value = 0
    isUploading.value = false
  }

  const resetDrag = () => {
    isDragging.value = false
  }

  return {
    isDragging,
    isUploading,
    progress,
    selectedFiles,
    uploadId,
    canUploadMore,
    uploadProgress,
    handleDrop,
    handleFileSelect,
    removeFile,
    clearAll,
    resetDrag
  }
}
