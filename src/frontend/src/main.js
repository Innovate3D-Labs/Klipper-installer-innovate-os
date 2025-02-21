import { createApp } from 'vue'
import { createStore } from 'vuex'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './assets/main.css'

// Router-Konfiguration
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/printers',
      name: 'PrinterList',
      component: () => import('./views/PrinterList.vue')
    },
    {
      path: '/install/:id',
      name: 'PrinterInstall',
      component: () => import('./views/PrinterInstall.vue')
    }
  ]
})

// Vuex Store
const store = createStore({
  state() {
    return {
      printers: [],
      selectedPrinter: null,
      installationStatus: null
    }
  },
  mutations: {
    setPrinters(state, printers) {
      state.printers = printers
    },
    setSelectedPrinter(state, printer) {
      state.selectedPrinter = printer
    },
    setInstallationStatus(state, status) {
      state.installationStatus = status
    }
  },
  actions: {
    async fetchPrinters({ commit }) {
      try {
        const response = await fetch('/api/v1/printers')
        const data = await response.json()
        commit('setPrinters', data)
      } catch (error) {
        console.error('Fehler beim Laden der Drucker:', error)
      }
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
