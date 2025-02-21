import { createApp } from 'vue'
import { createStore } from 'vuex'
import router from './router'
import App from './App.vue'
import './assets/main.css'
import './style.css'  // Füge globales CSS hinzu

// Font Awesome
import '@fortawesome/fontawesome-free/css/all.css'

// Vuex Store
const store = createStore({
  state() {
    return {
      printers: [],
      selectedPrinter: null,
      installationStatus: null,
      selectedInterface: null
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
    },
    setSelectedInterface(state, interface_type) {
      state.selectedInterface = interface_type
    }
  },
  actions: {
    async fetchPrinters({ commit }) {
      try {
        const response = await fetch('/api/v1/printers')
        const data = await response.json()
        commit('setPrinters', data)
      } catch (error) {
        console.error('Error fetching printers:', error)
      }
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(store)
app.mount('#app')
