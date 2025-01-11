import { createStore } from 'vuex'
import axios from 'axios'

export default createStore({
  state: {
    currentWebInterface: null,
    installationStatus: {
      step: null,
      progress: 0,
      message: ''
    },
    error: null,
    printers: [],
    selectedPrinter: null,
    loading: {
      printers: false,
      interfaces: false
    }
  },

  mutations: {
    setCurrentWebInterface(state, webInterface) {
      state.currentWebInterface = webInterface
    },
    setInstallationStatus(state, status) {
      state.installationStatus = status
    },
    setInstallationProgress(state, progress) {
      state.installationStatus.progress = progress
    },
    setError(state, error) {
      state.error = error
    },
    clearError(state) {
      state.error = null
    },
    setPrinters(state, printers) {
      state.printers = printers
    },
    setSelectedPrinter(state, printer) {
      state.selectedPrinter = printer
    },
    setLoading(state, { type, value }) {
      state.loading[type] = value
    }
  },

  actions: {
    async fetchPrinters({ commit }) {
      commit('setLoading', { type: 'printers', value: true })
      try {
        const response = await axios.get('/api/printers')
        commit('setPrinters', response.data)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Laden der Drucker',
          details: error.message
        })
      } finally {
        commit('setLoading', { type: 'printers', value: false })
      }
    },

    async createPrinter({ commit, dispatch }, printerData) {
      try {
        await axios.post('/api/printers', printerData)
        dispatch('fetchPrinters')
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Erstellen des Druckers',
          details: error.message
        })
        throw error
      }
    },

    async updatePrinter({ commit, dispatch }, { id, data }) {
      try {
        await axios.put(`/api/printers/${id}`, data)
        dispatch('fetchPrinters')
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Aktualisieren des Druckers',
          details: error.message
        })
        throw error
      }
    },

    async deletePrinter({ commit, dispatch }, id) {
      try {
        await axios.delete(`/api/printers/${id}`)
        dispatch('fetchPrinters')
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Löschen des Druckers',
          details: error.message
        })
        throw error
      }
    },

    async switchWebInterface({ commit }, webInterfaceName) {
      try {
        const response = await axios.post('/api/interface/switch', {
          interface: webInterfaceName
        })
        if (response.data.success) {
          commit('setCurrentWebInterface', webInterfaceName)
        }
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Wechseln des Interfaces',
          details: error.message
        })
        throw error
      }
    },

    async getCurrentWebInterface({ commit }) {
      try {
        const response = await axios.get('/api/interface/current')
        commit('setCurrentWebInterface', response.data.interface)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Laden des aktuellen Interfaces',
          details: error.message
        })
      }
    }
  },

  getters: {
    installationProgress: state => state.installationStatus.progress,
    isInstalling: state => state.installationStatus.step !== null,
    availablePrinters: state => state.printers,
    selectedPrinterConfig: state => state.selectedPrinter?.config || null,
    isLoading: state => type => state.loading[type]
  }
})
