import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest'
import { usePolling } from '@/composables/usePolling'
import { jobsApi } from '@/api/jobs'
import { ref } from 'vue'

// Mock API
vi.mock('@/api/jobs', () => ({
  jobsApi: {
    getStatus: vi.fn()
  },
  POLLING_INTERVAL: 100,
  MAX_POLLING_ATTEMPTS: 5
}))

describe('usePolling', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('should initialize with queued status', () => {
    const { status, progress, message, result, error } = usePolling('test-job')

    expect(status.value).toBe('queued')
    expect(progress.value).toBe(0)
    expect(message.value).toBe('')
    expect(result.value).toBeNull()
    expect(error.value).toBeNull()
  })

  it('should start polling when autoStart is true', async () => {
    const mockJob = {
      job_id: 'test-job',
      tool_id: 'merge',
      upload_id: 'ul-test',
      status: 'processing' as const,
      progress: 50,
      message: 'Processing...',
      created_at: new Date().toISOString(),
      expires_at: new Date().toISOString(),
      options: {}
    }

    vi.mocked(jobsApi.getStatus).mockResolvedValue({ data: mockJob })

    usePolling('test-job', { autoStart: true })

    // Wait for initial poll
    await vi.runAllTimersAsync()

    expect(jobsApi.getStatus).toHaveBeenCalledWith('test-job')
  })

  it('should update job status on poll', async () => {
    const mockJob = {
      job_id: 'test-job',
      tool_id: 'merge',
      upload_id: 'ul-test',
      status: 'completed' as const,
      progress: 100,
      message: 'Complete',
      created_at: new Date().toISOString(),
      expires_at: new Date().toISOString(),
      options: {},
      result: {
        output_file_id: 'f-result',
        filename: 'result.pdf',
        size: 1024,
        download_url: '/download/f-result',
        expires_at: new Date().toISOString()
      }
    }

    vi.mocked(jobsApi.getStatus).mockResolvedValue({ data: mockJob })

    const polling = usePolling('test-job')
    polling.startPolling()

    await vi.runAllTimersAsync()

    expect(polling.status.value).toBe('completed')
    expect(polling.progress.value).toBe(100)
    expect(polling.result.value).toEqual(mockJob.result)
  })

  it('should stop polling when job is completed', async () => {
    const mockJob = {
      job_id: 'test-job',
      tool_id: 'merge',
      upload_id: 'ul-test',
      status: 'completed' as const,
      progress: 100,
      message: 'Complete',
      created_at: new Date().toISOString(),
      expires_at: new Date().toISOString(),
      options: {}
    }

    vi.mocked(jobsApi.getStatus).mockResolvedValue({ data: mockJob })

    const polling = usePolling('test-job')
    polling.startPolling()

    await vi.runAllTimersAsync()

    // Should only call once (completed stops polling)
    expect(jobsApi.getStatus).toHaveBeenCalledTimes(1)
  })

  it('should handle polling errors', async () => {
    vi.mocked(jobsApi.getStatus).mockRejectedValue({
      error: { code: 'ERR', message: 'Network error' }
    })

    const polling = usePolling('test-job')
    polling.startPolling()

    await vi.runAllTimersAsync()

    expect(polling.status.value).toBe('failed')
    expect(polling.error.value).toEqual({
      code: 'POLL_ERROR',
      message: 'Network error'
    })
  })

  it('should reset state', () => {
    const polling = usePolling('test-job')

    polling.status.value = 'completed' as const
    polling.progress.value = 100

    polling.reset()

    expect(polling.status.value).toBe('queued')
    expect(polling.progress.value).toBe(0)
  })
})
