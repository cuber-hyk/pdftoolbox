/**
 * Tools Store - 工具状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Tool } from '@/types'
import { toolsApi } from '@/api/tools'

export const useToolsStore = defineStore('tools', () => {
  const tools = ref<Tool[]>([])
  const selectedCategory = ref<string | null>(null)
  const searchQuery = ref('')
  const loading = ref(false)

  const filteredTools = computed(() => {
    let result = tools.value

    if (selectedCategory.value) {
      result = result.filter(t => t.category === selectedCategory.value)
    }

    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      result = result.filter(t =>
        t.name.toLowerCase().includes(query) ||
        t.description.toLowerCase().includes(query)
      )
    }

    return result
  })

  const categories = computed(() => {
    return [...new Set(tools.value.map(t => t.category))]
  })

  async function fetchTools() {
    loading.value = true
    try {
      const response = await toolsApi.getAll()
      tools.value = response.data
    } catch (error) {
      console.error('Failed to fetch tools:', error)
      tools.value = []
    } finally {
      loading.value = false
    }
  }

  function setCategory(category: string | null) {
    selectedCategory.value = category
  }

  function setSearch(query: string) {
    searchQuery.value = query
  }

  function getToolById(id: string): Tool | undefined {
    return tools.value.find(t => t.id === id)
  }

  return {
    tools,
    selectedCategory,
    searchQuery,
    loading,
    filteredTools,
    categories,
    fetchTools,
    setCategory,
    setSearch,
    getToolById
  }
})
