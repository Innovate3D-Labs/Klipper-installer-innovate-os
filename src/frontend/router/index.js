import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/printers',
    name: 'Printers',
    component: () => import('../views/Printers.vue'),
    meta: { title: 'Drucker' }
  },
  {
    path: '/interfaces',
    name: 'Interfaces',
    component: () => import('../views/Interfaces.vue'),
    meta: { title: 'Oberflächen' }
  },
  {
    path: '/install/:printerId?',
    name: 'Install',
    component: () => import('../views/Install.vue'),
    meta: { title: 'Installation' }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/Settings.vue'),
    meta: { title: 'Einstellungen' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: '404 - Nicht gefunden' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Titel für Browser-Tab setzen
router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | Klipper Installer`
  next()
})

export default router
