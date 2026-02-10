export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed' | 'cancelled'

export interface Tool {
  id: string
  name: string
  description: string
  icon: string
  route: string
  category: string
  max_files: number
  max_size_mb: number
  max_total_size_mb: number
  options: ToolOption[]
}

export interface ToolOption {
  name: string
  type: 'string' | 'number' | 'boolean' | 'select' | 'array' | 'file'
  label: string
  description?: string
  placeholder?: string
  default?: any
  required?: boolean
  min?: number
  max?: number
  suffix?: string
  options?: Array<{ value: string; label: string }>
  visible_when?: Record<string, string>
  accept?: string[]
}

export interface UploadedFile {
  file_id: string
  name: string
  size: number
  pages?: number
  metadata?: {
    title?: string
    author?: string
    created?: string
  }
}

export interface Job {
  job_id: string
  tool_id: string
  upload_id: string
  status: JobStatus
  progress: number
  message: string
  input_files: string[]
  output_file?: string
  options: Record<string, any>
  created_at: string
  started_at?: string
  completed_at?: string
  expires_at?: string
  error?: {
    code: string
    message: string
    details?: any
  }
  result?: {
    output_file_id: string
    filename: string
    size: number
    pages?: number
    download_url: string
    expires_at: string
  }
}

export interface APIResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: any
  }
}
