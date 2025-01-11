import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import PrinterList from '../views/PrinterList.vue'
import PrinterInstall from '../views/PrinterInstall.vue'
import Interfaces from '../views/Interfaces.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/printers',
    name: 'PrinterList',
    component: PrinterList
  },
  {
    path: '/printers/:name/install',
    name: 'PrinterInstall',
    component: PrinterInstall
  },
  {
    path: '/interfaces',
    name: 'Interfaces',
    component: Interfaces
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
