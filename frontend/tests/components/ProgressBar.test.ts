import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createTestingPinia } from '@/tests/utils/pinia'
import ProgressBar from '@/components/business/ProgressBar.vue'

describe('ProgressBar Component', () => {
  it('should render progress bar with given progress', () => {
    const wrapper = mount(ProgressBar, {
      props: {
        progress: 50,
        message: 'Processing...',
        status: 'processing'
      }
    })

    expect(wrapper.find('.bg-gradient-to-r').attributes('style')).toContain('width: 50%')
    expect(wrapper.text()).toContain('Processing...')
    expect(wrapper.text()).toContain('50%')
  })

  it('should show completed state', () => {
    const wrapper = mount(ProgressBar, {
      props: {
        progress: 100,
        message: 'Complete',
        status: 'completed'
      }
    })

    expect(wrapper.find('.bg-green-500').exists()).toBe(true)
  })

  it('should show error state', () => {
    const wrapper = mount(ProgressBar, {
      props: {
        progress: 50,
        message: 'Error',
        status: 'error'
      }
    })

    expect(wrapper.find('.bg-red-500').exists()).toBe(true)
  })

  it('should hide percentage when showPercentage is false', () => {
    const wrapper = mount(ProgressBar, {
      props: {
        progress: 50,
        message: 'Processing',
        status: 'processing',
        showPercentage: false
      }
    })

    expect(wrapper.text()).not.toContain('50%')
  })

  it('should clamp progress between 0 and 100', () => {
    const wrapper = mount(ProgressBar, {
      props: {
        progress: 150,
        status: 'processing'
      }
    })

    expect(wrapper.find('.bg-gradient-to-r').attributes('style')).toContain('width: 100%')
  })
})
