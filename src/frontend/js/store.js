import { createStore } from 'vuex'
import axios from 'axios'
import settings from './store/modules/settings'
import websocket from './store/modules/websocket'

export default createStore({
  state: {
    currentWebInterface: null,
    installationStatus: {
      step: null,
      progress: 0,
      message: ''
    },
    error: null,
    success: null,
    printers: [],
    selectedPrinter: null,
    loading: {
      printers: false,
      interfaces: false,
      installation: false
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
    setSuccess(state, message) {
      state.success = message
    },
    clearSuccess(state) {
      state.success = null
    },
    setPrinters(state, printers) {
      state.printers = printers
    },
    setSelectedPrinter(state, printer) {
      state.selectedPrinter = printer
    },
    setLoading(state, { key, value }) {
      state.loading[key] = value
    }
  },

  actions: {
    showError({ commit }, { message, details }) {
      commit('setError', { message, details })
      setTimeout(() => {
        commit('clearError')
      }, 5000)
    },

    showSuccess({ commit }, message) {
      commit('setSuccess', message)
      setTimeout(() => {
        commit('clearSuccess')
      }, 3000)
    },

    async fetchPrinters({ commit }) {
      commit('setLoading', { key: 'printers', value: true })
      try {
        const response = await axios.get('/api/printers')
        commit('setPrinters', response.data)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Laden der Drucker',
          details: error.message
        })
      } finally {
        commit('setLoading', { key: 'printers', value: false })
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

  modules: {
    settings,
    websocket
  },

  getters: {
    installationProgress: state => state.installationStatus.progress,
    isInstalling: state => state.installationStatus.step !== null,
    availablePrinters: state => state.printers,
    selectedPrinterConfig: state => state.selectedPrinter?.config || null,
    isLoading: state => key => state.loading[key]
  }
})
