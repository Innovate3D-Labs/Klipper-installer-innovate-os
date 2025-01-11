export default {
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
