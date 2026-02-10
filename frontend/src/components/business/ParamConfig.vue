/**
 * ParamConfig - 动态参数配置组件
 * 根据工具配置动态生成表单
 */
<script setup lang="ts">
import { computed, watch } from 'vue'
import type { ToolOption } from '@/types'

interface Props {
  options: ToolOption[]
  modelValue: Record<string, any>
}

interface Emits {
  'update:modelValue': [value: Record<string, any>]
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const localValues = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 设置默认值
watch(() => props.options, (options) => {
  const values = { ...localValues.value }

  options.forEach(opt => {
    if (opt.default !== undefined && values[opt.name] === undefined) {
      values[opt.name] = opt.default
    }
  })

  localValues.value = values
}, { immediate: true })

const updateValue = (name: string, value: any) => {
  localValues.value = {
    ...localValues.value,
    [name]: value
  }
}

const isOptionVisible = (option: ToolOption): boolean => {
  if (!option.visible_when) return true

  return Object.entries(option.visible_when).every(([key, expectedValue]) => {
    const actualValue = localValues.value[key]
    return actualValue === expectedValue
  })
}

const visibleOptions = computed(() => {
  return props.options.filter(opt => isOptionVisible(opt))
})
</script>

<template>
  <div v-if="visibleOptions.length > 0" class="space-y-4">
    <h3 class="text-lg font-semibold text-slate-900">处理选项</h3>

    <div v-for="option in visibleOptions" :key="option.name" class="space-y-2">
      <!-- 标签 -->
      <label class="block text-sm font-medium text-slate-700">
        {{ option.label }}
        <span v-if="option.required" class="text-red-500">*</span>
      </label>

      <!-- 描述 -->
      <p v-if="option.description" class="text-xs text-slate-500">
        {{ option.description }}
      </p>

      <!-- 字符串输入 -->
      <input
        v-if="option.type === 'string'"
        :type="option.name.includes('password') ? 'password' : 'text'"
        :value="localValues[option.name]"
        :placeholder="option.placeholder"
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        @input="(e) => updateValue(option.name, (e.target as HTMLInputElement).value)"
      />

      <!-- 数字输入 -->
      <div v-else-if="option.type === 'number'" class="flex items-center gap-2">
        <input
          type="number"
          :value="localValues[option.name]"
          :min="option.min"
          :max="option.max"
          class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
          @input="(e) => updateValue(option.name, Number((e.target as HTMLInputElement).value))"
        />
        <span v-if="option.suffix" class="text-sm text-slate-500">{{ option.suffix }}</span>
      </div>

      <!-- 选择器 -->
      <select
        v-else-if="option.type === 'select'"
        :value="localValues[option.name]"
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        @change="(e) => updateValue(option.name, (e.target as HTMLSelectElement).value)"
      >
        <option v-for="opt in option.options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- 复选框 -->
      <label v-else-if="option.type === 'boolean'" class="flex items-center gap-2 cursor-pointer">
        <input
          type="checkbox"
          :checked="localValues[option.name]"
          class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500"
          @change="(e) => updateValue(option.name, (e.target as HTMLInputElement).checked)"
        />
        <span class="text-sm text-slate-700">
          {{ option.label }}
        </span>
      </label>

      <!-- 数组输入 (逗号分隔) -->
      <input
        v-else-if="option.type === 'array'"
        type="text"
        :value="Array.isArray(localValues[option.name]) ? localValues[option.name].join(', ') : localValues[option.name]"
        :placeholder="option.placeholder || '用逗号分隔多个值'"
        class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
        @input="(e) => {
          const value = (e.target as HTMLInputElement).value
          updateValue(option.name, value ? value.split(',').map(v => v.trim()) : [])
        }"
      />
    </div>
  </div>
</template>
