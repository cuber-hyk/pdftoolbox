/**
 * ParamConfig - Dynamic Parameter Configuration Component
 * Dynamically generates form fields based on tool configuration
 */
<script setup lang="ts">
import { computed, watch } from 'vue'
import type { ToolOption } from '@/types'

interface Props {
  options: ToolOption[]
  modelValue: Record<string, any>
  toolId?: string
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
  if (option.visible_when) {
    return Object.entries(option.visible_when).every(([key, expectedValue]) => {
      return localValues.value[key] === expectedValue
    })
  }
  
  if (option.depends_on) {
    return Object.entries(option.depends_on).every(([key, expectedValue]) => {
      return localValues.value[key] === expectedValue
    })
  }

  return true
}

const visibleOptions = computed(() => {
  return props.options.filter(opt => isOptionVisible(opt))
})

const isPasswordField = (name: string): boolean => {
  return name.toLowerCase().includes('password')
}

const getSectionTitle = (optionName: string): string => {
  const sectionTitles: Record<string, string> = {
    'operation': 'Operation',
    'password': 'Password',
    'algorithm': 'Encryption',
    'allow_printing': 'Permissions',
    'allow_copying': '',
    'allow_modifying': ''
  }
  return sectionTitles[optionName] || ''
}

const shouldShowSectionTitle = (optionName: string): boolean => {
  return optionName === 'allow_printing'
}
</script>

<template>
  <div v-if="visibleOptions.length > 0" class="space-y-4">
    <div v-for="(option, index) in visibleOptions" :key="option.name" class="space-y-2">
      <!-- Section header for permissions -->
      <div v-if="shouldShowSectionTitle(option.name)" class="pt-2">
        <h4 class="text-sm font-semibold text-slate-900">Permissions</h4>
        <p class="text-xs text-amber-600 bg-amber-50 p-2 rounded mt-1">
          Note: Some PDF viewers (especially browsers) may ignore these restrictions. For full protection, use Adobe Acrobat.
        </p>
      </div>

      <!-- Label with required indicator -->
      <label v-if="!shouldShowSectionTitle(option.name)" class="flex items-center gap-1 text-sm font-medium text-slate-700">
        {{ option.label }}
        <span v-if="option.required" class="text-red-500">*</span>
      </label>

      <!-- Description (except for password fields) -->
      <p v-if="option.description && !isPasswordField(option.name) && !shouldShowSectionTitle(option.name)" class="text-xs text-slate-500">
        {{ option.description }}
      </p>

      <!-- String Input (supports password type) -->
      <input
        v-if="option.type === 'string'"
        :type="isPasswordField(option.name) ? 'password' : 'text'"
        :value="localValues[option.name]"
        :placeholder="option.placeholder"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
        @input="(e) => updateValue(option.name, (e.target as HTMLInputElement).value)"
      />

      <!-- Number Input -->
      <div v-else-if="option.type === 'number'" class="space-y-2">
        <input
          type="number"
          :value="localValues[option.name]"
          :min="option.min"
          :max="option.max"
          class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
          @input="(e) => updateValue(option.name, Number((e.target as HTMLInputElement).value))"
        />
        <!-- Range slider for number inputs with min/max -->
        <div v-if="option.min !== undefined && option.max !== undefined" class="flex items-center gap-3">
          <input
            type="range"
            :min="option.min"
            :max="option.max"
            :value="localValues[option.name]"
            class="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            @input="(e) => updateValue(option.name, Number((e.target as HTMLInputElement).value))"
          />
          <span class="text-sm font-medium text-slate-700 w-12 text-center">
            {{ localValues[option.name] }}{{ option.suffix || '' }}
          </span>
        </div>
      </div>

      <!-- Select Dropdown -->
      <select
        v-else-if="option.type === 'select'"
        :value="localValues[option.name]"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
        @change="(e) => updateValue(option.name, (e.target as HTMLSelectElement).value)"
      >
        <option v-for="opt in option.options" :key="opt.value" :value="opt.value">
          {{ opt.label }}
        </option>
      </select>

      <!-- Boolean Checkbox -->
      <label v-else-if="option.type === 'boolean'" class="flex items-center gap-3 cursor-pointer">
        <input
          type="checkbox"
          :checked="localValues[option.name]"
          class="w-4 h-4 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 flex-shrink-0"
          @change="(e) => updateValue(option.name, (e.target as HTMLInputElement).checked)"
        />
        <span class="text-sm text-slate-700">{{ option.label }}</span>
      </label>

      <!-- Array Input (comma-separated) -->
      <input
        v-else-if="option.type === 'array'"
        type="text"
        :value="Array.isArray(localValues[option.name]) ? localValues[option.name].join(', ') : localValues[option.name]"
        :placeholder="option.placeholder || 'Comma-separated values'"
        class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 bg-white text-sm"
        @input="(e) => {
          const value = (e.target as HTMLInputElement).value
          updateValue(option.name, value ? value.split(',').map((v: string) => v.trim()) : [])
        }"
      />

      <!-- File Input -->
      <div v-else-if="option.type === 'file'" class="space-y-2">
        <input
          type="file"
          :accept="option.accept?.join(',') || '.pdf,.jpg,.png'"
          class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100"
          @change="(e) => {
            const file = (e.target as HTMLInputElement).files?.[0]
            updateValue(option.name, file)
          }"
        />
      </div>
    </div>
  </div>
</template>
