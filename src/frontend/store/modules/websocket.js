export default {
  state: {
    isConnected: false,
    installationProgress: {
      step: null,
      progress: 0,
      message: null
    },
    printerStatuses: {},
    lastError: null
  },

  mutations: {
    setWebSocketStatus(state, isConnected) {
      state.isConnected = isConnected
    },

    setInstallationProgress(state, { step, progress, message }) {
      state.installationProgress = {
        step,
        progress,
        message
      }
    },

    updatePrinterStatus(state, { printer_id, status }) {
      state.printerStatuses = {
        ...state.printerStatuses,
        [printer_id]: status
      }
    },

    setWebSocketError(state, error) {
      state.lastError = error
    },

    clearWebSocketError(state) {
      state.lastError = null
    }
  },

  actions: {
    handleWebSocketMessage({ commit }, message) {
      switch (message.type) {
        case 'installation_progress':
          commit('setInstallationProgress', message.data)
          break

        case 'printer_status':
          commit('updatePrinterStatus', message.data)
          break

        case 'error':
          commit('setWebSocketError', message.data)
          break

        default:
          console.warn('Unknown WebSocket message type:', message.type)
      }
    }
  },

  getters: {
    isWebSocketConnected: state => state.isConnected,
    currentInstallationProgress: state => state.installationProgress,
    getPrinterStatus: state => (printerId) => state.printerStatuses[printerId],
    webSocketError: state => state.lastError
  }
}
