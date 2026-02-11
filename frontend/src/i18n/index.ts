import { createI18n } from 'vue-i18n'
import en from './locales/en-US'
import zh from './locales/zh-CN'

const i18n = createI18n({
  legacy: false,  // Use Composition API mode
  locale: localStorage.getItem('locale') || 'en-US',
  fallbackLocale: 'en-US',
  messages: {
    'en-US': en,
    'zh-CN': zh
  }
})

export default i18n
