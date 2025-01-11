export default {
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
