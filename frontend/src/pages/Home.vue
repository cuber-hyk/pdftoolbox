<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useToolsStore } from '@/stores/modules/tools'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'

const toolsStore = useToolsStore()

onMounted(() => {
  toolsStore.fetchTools()
})

const categories = computed(() => ['All Tools', ...toolsStore.categories])
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <AppHeader />

    <main class="max-w-7xl mx-auto px-4 py-12">
      <!-- Hero Section -->
      <section class="text-center mb-12">
        <h1 class="text-4xl md:text-5xl font-bold text-slate-900 mb-4 text-balance">
          Simple & Fast PDF Tools
        </h1>
        <p class="text-lg text-slate-500 mb-8">
          No registration required, completely free, protect your privacy
        </p>
      </section>

      <!-- Category Filter -->
      <section class="mb-8 flex gap-2 overflow-x-auto pb-2">
        <button
          v-for="category in categories"
          :key="category"
          @click="toolsStore.setCategory(category === 'All Tools' ? null : category)"
          class="px-4 py-2 rounded-lg whitespace-nowrap transition-colors"
          :class="
            (toolsStore.selectedCategory || 'All Tools') === category
              ? 'bg-primary-600 text-white'
              : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
          "
        >
          {{ category }}
        </button>
      </section>

      <!-- Loading State -->
      <div v-if="toolsStore.loading" class="flex justify-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>

      <!-- Tools Grid -->
      <section v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div
          v-for="tool in toolsStore.filteredTools"
          :key="tool.id"
          @click="$router.push(`/tools/${tool.id}`)"
          class="group relative p-6 rounded-2xl border border-slate-200 bg-white text-left
                 hover:-translate-y-1 hover:shadow-lg hover:border-primary-300
                 active:scale-[0.98]
                 transition-all duration-300 ease-out cursor-pointer min-w-[280px]"
        >
          <!-- Icon -->
          <div class="flex items-center gap-3 mb-4">
            <div class="p-3 rounded-xl bg-primary-50 text-primary-600
                        group-hover:bg-primary-100 group-hover:scale-110
                        transition-all duration-300">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="tool.icon === 'merge'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                <path v-else-if="tool.icon === 'scissors'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.121 14.121L19 19m-7-7l7-7m-7 7l-2.879 2.879M12 12L9.121 9.121m0 5.758a3 3 0 10-4.243 4.243 3 3 0 004.243-4.243zm0-5.758a3 3 0 10-4.243-4.243 3 3 0 004.243 4.243z" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-900">
              {{ tool.name }}
            </h3>
          </div>

          <!-- Description -->
          <p class="text-sm text-slate-500 leading-relaxed">
            {{ tool.description }}
          </p>

          <!-- Hover indicator -->
          <div class="absolute top-4 right-4 opacity-0 group-hover:opacity-100
                      transition-opacity duration-300">
            <svg class="w-4 h-4 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>
