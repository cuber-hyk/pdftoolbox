import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/pages/Home.vue'),
    meta: {
      title: 'PDF Toolbox - Simple & Fast Online PDF Tools'
    }
  },
  {
    path: '/tools/:toolId',
    name: 'tool',
    component: () => import('@/pages/tools/ToolPage.vue'),
    props: true,
    meta: {
      title: 'PDF Tool'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/pages/Error.vue'),
    meta: {
      title: 'Page Not Found'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0, behavior: 'smooth' }
  }
})

router.beforeEach((to, from, next) => {
  // Set page title
  document.title = to.meta.title as string || 'PDF Toolbox'
  next()
})

export default router
