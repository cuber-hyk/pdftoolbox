import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createTestingPinia } from '@/tests/utils/pinia'
import { useToolsStore } from '@/stores/modules/tools'
import { toolsApi } from '@/api/tools'

// Mock API
vi.mock('@/api/tools', () => ({
  toolsApi: {
    getAll: vi.fn(),
    getById: vi.fn()
  }
}))

describe('Tools Store', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should initialize with empty state', () => {
    const pinia = createTestingPinia()
    const store = useToolsStore()

    expect(store.tools).toEqual([])
    expect(store.selectedCategory).toBe(null)
    expect(store.searchQuery).toBe('')
    expect(store.loading).toBe(false)
  })

  it('should fetch tools successfully', async () => {
    const mockTools = [
      { id: 'merge', name: 'PDF Merge', description: 'Merge PDFs', icon: 'merge', route: '/tools/merge', category: 'Basic Tools', max_files: 20, max_size_mb: 100, max_total_size_mb: 200, options: [] },
      { id: 'split', name: 'PDF Split', description: 'Split PDFs', icon: 'scissors', route: '/tools/split', category: 'Basic Tools', max_files: 1, max_size_mb: 100, max_total_size_mb: 100, options: [] }
    ]

    vi.mocked(toolsApi.getAll).mockResolvedValue({ data: mockTools })

    const pinia = createTestingPinia()
    const store = useToolsStore()

    await store.fetchTools()

    expect(store.loading).toBe(false)
    expect(store.tools).toEqual(mockTools)
    expect(toolsApi.getAll).toHaveBeenCalledOnce()
  })

  it('should filter tools by category', () => {
    const pinia = createTestingPinia()
    const store = useToolsStore()

    store.tools = [
      { id: 'merge', name: 'PDF Merge', description: 'Merge PDFs', icon: 'merge', route: '/tools/merge', category: 'Basic Tools', max_files: 20, max_size_mb: 100, max_total_size_mb: 200, options: [] },
      { id: 'split', name: 'PDF Split', description: 'Split PDFs', icon: 'scissors', route: '/tools/split', category: 'Extract Tools', max_files: 1, max_size_mb: 100, max_total_size_mb: 100, options: [] }
    ]

    store.setCategory('Basic Tools')

    expect(store.filteredTools).toHaveLength(1)
    expect(store.filteredTools[0].id).toBe('merge')
  })

  it('should filter tools by search query', () => {
    const pinia = createTestingPinia()
    const store = useToolsStore()

    store.tools = [
      { id: 'merge', name: 'PDF Merge', description: 'Merge PDFs', icon: 'merge', route: '/tools/merge', category: 'Basic Tools', max_files: 20, max_size_mb: 100, max_total_size_mb: 200, options: [] },
      { id: 'split', name: 'PDF Split', description: 'Split PDFs', icon: 'scissors', route: '/tools/split', category: 'Basic Tools', max_files: 1, max_size_mb: 100, max_total_size_mb: 100, options: [] }
    ]

    store.setSearch('merge')

    expect(store.filteredTools).toHaveLength(1)
    expect(store.filteredTools[0].id).toBe('merge')
  })

  it('should get unique categories', () => {
    const pinia = createTestingPinia()
    const store = useToolsStore()

    store.tools = [
      { id: 'merge', name: 'PDF Merge', description: 'Merge PDFs', icon: 'merge', route: '/tools/merge', category: 'Basic Tools', max_files: 20, max_size_mb: 100, max_total_size_mb: 200, options: [] },
      { id: 'split', name: 'PDF Split', description: 'Split PDFs', icon: 'scissors', route: '/tools/split', category: 'Basic Tools', max_files: 1, max_size_mb: 100, max_total_size_mb: 100, options: [] },
      { id: 'extract', name: 'Extract', description: 'Extract pages', icon: 'file-text', route: '/tools/extract', category: 'Extract Tools', max_files: 1, max_size_mb: 100, max_total_size_mb: 100, options: [] }
    ]

    expect(store.categories).toEqual(['Basic Tools', 'Extract Tools'])
  })

  it('should get tool by id', () => {
    const pinia = createTestingPinia()
    const store = useToolsStore()

    const mockTool = { id: 'merge', name: 'PDF Merge', description: 'Merge PDFs', icon: 'merge', route: '/tools/merge', category: 'Basic Tools', max_files: 20, max_size_mb: 100, max_total_size_mb: 200, options: [] }
    store.tools = [mockTool]

    expect(store.getToolById('merge')).toEqual(mockTool)
    expect(store.getToolById('nonexistent')).toBeUndefined()
  })
})
