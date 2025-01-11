import axios from 'axios'

export default {
  state: {
    settings: {
      language: 'de',
      theme: 'light',
      autoUpdate: true,
      debugMode: false
    },
    backups: [],
    loading: false,
    error: null
  },

  mutations: {
    setSettings(state, settings) {
      state.settings = settings
    },
    setBackups(state, backups) {
      state.backups = backups
    },
    setLoading(state, loading) {
      state.loading = loading
    },
    setError(state, error) {
      state.error = error
    }
  },

  actions: {
    async fetchSettings({ commit }) {
      commit('setLoading', true)
      try {
        const { data } = await axios.get('/api/settings')
        commit('setSettings', data)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Laden der Einstellungen',
          details: error.response?.data?.detail || error.message
        })
      } finally {
        commit('setLoading', false)
      }
    },

    async updateSettings({ commit }, settings) {
      commit('setLoading', true)
      try {
        const { data } = await axios.patch('/api/settings', settings)
        commit('setSettings', data)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Speichern der Einstellungen',
          details: error.response?.data?.detail || error.message
        })
        throw error
      } finally {
        commit('setLoading', false)
      }
    },

    async createBackup({ commit }) {
      commit('setLoading', true)
      try {
        await axios.post('/api/settings/backup')
        await this.dispatch('fetchBackups')
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Erstellen des Backups',
          details: error.response?.data?.detail || error.message
        })
        throw error
      } finally {
        commit('setLoading', false)
      }
    },

    async fetchBackups({ commit }) {
      commit('setLoading', true)
      try {
        const { data } = await axios.get('/api/settings/backups')
        commit('setBackups', data.backups)
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Laden der Backups',
          details: error.response?.data?.detail || error.message
        })
      } finally {
        commit('setLoading', false)
      }
    },

    async restoreBackup({ commit }, backupId) {
      commit('setLoading', true)
      try {
        await axios.post(`/api/settings/restore/${backupId}`)
        await this.dispatch('fetchSettings')
      } catch (error) {
        commit('setError', {
          message: 'Fehler beim Wiederherstellen des Backups',
          details: error.response?.data?.detail || error.message
        })
        throw error
      } finally {
        commit('setLoading', false)
      }
    }
  },

  getters: {
    currentSettings: state => state.settings,
    availableBackups: state => state.backups,
    isLoading: state => state.loading
  }
}
