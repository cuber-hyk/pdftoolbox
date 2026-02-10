import { setActivePinia, createPinia } from 'pinia'
import { createApp } from 'vue'

/**
 * 创建测试用的 Pinia 实例
 */
export function createTestingPinia() {
  const pinia = createPinia()
  setActivePinia(pinia)
  return pinia
}
