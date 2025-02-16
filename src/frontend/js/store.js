import { createStore } from 'vuex'
import axios from 'axios'

const settings = {
  namespaced: true,
  state: {
    settings: {
      language: 'de',
      theme: 'light'
    }
  },
  mutations: {
    setSettings(state, settings) {
      state.settings = { ...state.settings, ...settings }
    }
  },
  actions: {
    updateSettings({ commit }, settings) {
      commit('setSettings', settings)
    }
  },
  getters: {
    getSettings: state => state.settings
  }
}

const websocket = {
  namespaced: true,
  state: {
    socket: null,
    connected: false,
    messages: []
  },
  mutations: {
    setSocket(state, socket) {
      state.socket = socket
    },
    setConnected(state, status) {
      state.connected = status
    },
    addMessage(state, message) {
      state.messages.push(message)
    }
  },
  actions: {
    connect({ commit, state }, url) {
      if (state.socket) {
        state.socket.close()
      }
      
      const socket = new WebSocket(url)
      
      socket.onopen = () => {
        commit('setConnected', true)
      }
      
      socket.onclose = () => {
        commit('setConnected', false)
      }
      
      socket.onmessage = (event) => {
        const message = JSON.parse(event.data)
        commit('addMessage', message)
      }
      
      commit('setSocket', socket)
    },
    disconnect({ commit, state }) {
      if (state.socket) {
        state.socket.close()
        commit('setSocket', null)
        commit('setConnected', false)
      }
    }
  },
  getters: {
    isConnected: state => state.connected,
    getMessages: state => state.messages
  }
}

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
      commit('setError', {
        message,
        details
      })
      setTimeout(() => commit('clearError'), 5000)
    },

    showSuccess({ commit }, message) {
      commit('setSuccess', message)
      setTimeout(() => commit('clearSuccess'), 5000)
    },

    async fetchPrinters({ commit }) {
      commit('setLoading', { key: 'printers', value: true })
      try {
        const response = await axios.get('/api/v1/printers')
        commit('setPrinters', response.data)
      } catch (error) {
        commit('showError', {
          message: 'Fehler beim Laden der Drucker',
          details: error.message
        })
      } finally {
        commit('setLoading', { key: 'printers', value: false })
      }
    },

    async createPrinter({ commit, dispatch }, printerData) {
      try {
        await axios.post('/api/v1/printers', printerData)
        dispatch('showSuccess', 'Drucker erfolgreich erstellt')
        dispatch('fetchPrinters')
      } catch (error) {
        dispatch('showError', {
          message: 'Fehler beim Erstellen des Druckers',
          details: error.message
        })
      }
    },

    async updatePrinter({ commit, dispatch }, { id, data }) {
      try {
        await axios.put(`/api/v1/printers/${id}`, data)
        dispatch('showSuccess', 'Drucker erfolgreich aktualisiert')
        dispatch('fetchPrinters')
      } catch (error) {
        dispatch('showError', {
          message: 'Fehler beim Aktualisieren des Druckers',
          details: error.message
        })
      }
    },

    async deletePrinter({ commit, dispatch }, id) {
      try {
        await axios.delete(`/api/v1/printers/${id}`)
        dispatch('showSuccess', 'Drucker erfolgreich gelöscht')
        dispatch('fetchPrinters')
      } catch (error) {
        dispatch('showError', {
          message: 'Fehler beim Löschen des Druckers',
          details: error.message
        })
      }
    },

    async switchWebInterface({ commit }, webInterfaceName) {
      commit('setLoading', { key: 'interfaces', value: true })
      try {
        const response = await axios.post('/api/v1/interface/switch', {
          interface: webInterfaceName
        })
        commit('setCurrentWebInterface', webInterfaceName)
        return response.data
      } catch (error) {
        throw error
      } finally {
        commit('setLoading', { key: 'interfaces', value: false })
      }
    },

    async getCurrentWebInterface({ commit }) {
      try {
        const response = await axios.get('/api/v1/interface/current')
        commit('setCurrentWebInterface', response.data.interface)
        return response.data
      } catch (error) {
        console.error('Fehler beim Abrufen der aktuellen Web-Oberfläche:', error)
        throw error
      }
    }
  },

  modules: {
    settings,
    websocket
  }
})
