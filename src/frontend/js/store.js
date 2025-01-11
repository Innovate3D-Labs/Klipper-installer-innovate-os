import { createStore } from 'vuex'

export default createStore({
  state: {
    printers: [],
    selectedPrinter: null,
    installationStatus: null,
    currentInterface: null
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
    setCurrentInterface(state, interface) {
      state.currentInterface = interface
    }
  },
  actions: {
    async fetchPrinters({ commit }) {
      try {
        const response = await fetch('/api/v1/printers')
        const printers = await response.json()
        commit('setPrinters', printers)
      } catch (error) {
        console.error('Fehler beim Abrufen der Drucker:', error)
      }
    },
    async startInstallation({ commit, state }) {
      if (!state.selectedPrinter) return

      const ws = new WebSocket(`ws://localhost:8000/api/v1/ws/install/${state.selectedPrinter.name}`)
      
      ws.onmessage = (event) => {
        const status = JSON.parse(event.data)
        commit('setInstallationStatus', status)
      }

      ws.onerror = (error) => {
        commit('setInstallationStatus', {
          status: 'error',
          error: 'WebSocket-Verbindungsfehler'
        })
      }
    },
    async switchInterface({ commit }, interface) {
      try {
        const response = await fetch('/api/v1/interfaces/switch', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ interface })
        })
        if (response.ok) {
          commit('setCurrentInterface', interface)
        }
      } catch (error) {
        console.error('Fehler beim Wechseln der Oberfläche:', error)
      }
    }
  }
})
