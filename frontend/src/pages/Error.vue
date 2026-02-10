<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const router = useRouter()
</script>

<template>
  <div class="min-h-screen bg-slate-50 flex flex-col">
    <AppHeader />

    <main class="flex-1 flex items-center justify-center px-4">
      <div class="text-center">
        <h1 class="text-6xl font-bold text-slate-900 mb-4">404</h1>
        <h2 class="text-2xl font-semibold text-slate-700 mb-4">Page Not Found</h2>
        <p class="text-slate-500 mb-8">The page you are looking for does not exist.</p>
        <button
          @click="router.push('/')"
          class="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors font-semibold"
        >
          Back to Home
        </button>
      </div>
    </main>

    <AppFooter />
  </div>
</template>
