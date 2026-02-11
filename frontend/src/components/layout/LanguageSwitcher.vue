<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const languages = [
  { code: 'en-US', name: 'English', flag: '🇺🇸' },
  { code: 'zh-CN', name: '中文', flag: '🇨🇳' }
]

function changeLanguage(code: string) {
  locale.value = code
  localStorage.setItem('locale', code)
}
</script>

<template>
  <div class="flex items-center gap-1">
    <button
      v-for="lang in languages"
      :key="lang.code"
      @click="changeLanguage(lang.code)"
      class="px-2 py-1 text-sm rounded transition-colors hover:bg-slate-100"
      :class="{ 'bg-slate-200 font-medium': locale === lang.code }"
      :aria-label="`Switch to ${lang.name}`"
    >
      {{ lang.flag }} {{ lang.name }}
    </button>
  </div>
</template>
