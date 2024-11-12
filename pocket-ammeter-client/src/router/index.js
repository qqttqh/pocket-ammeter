import { createRouter, createWebHistory } from 'vue-router'

import PowerInfo from '@/views/PowerInfo.vue'
import SelectRoom from '@/views/SelectRoom.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'PowerInfo',
      component: PowerInfo
    },
    {
      path: '/select',
      name: 'SelectRoom',
      component: SelectRoom
    },
    {
      path: '/demo',
      name: 'demo',
      component: import('@/views/Demo.vue')
    }
  ]
})

export default router
