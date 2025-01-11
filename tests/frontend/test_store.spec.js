import { createStore } from 'vuex'
import { cloneDeep } from 'lodash'
import storeConfig from '@/js/store'

describe('Vuex Store', () => {
  let store

  beforeEach(() => {
    store = createStore(cloneDeep(storeConfig))
  })

  describe('Interface Management', () => {
    it('should update currentWebInterface', () => {
      store.commit('setCurrentWebInterface', 'fluidd')
      expect(store.state.currentWebInterface).toBe('fluidd')
    })

    it('should handle interface switching', async () => {
      const mockApi = {
        switchInterface: jest.fn().mockResolvedValue({ success: true })
      }
      store.$api = mockApi

      await store.dispatch('switchInterface', 'mainsail')
      
      expect(mockApi.switchInterface).toHaveBeenCalledWith('mainsail')
      expect(store.state.currentWebInterface).toBe('mainsail')
    })

    it('should handle interface switching errors', async () => {
      const mockApi = {
        switchInterface: jest.fn().mockRejectedValue(new Error('Switch failed'))
      }
      store.$api = mockApi

      await expect(store.dispatch('switchInterface', 'invalid'))
        .rejects.toThrow('Switch failed')
    })
  })

  describe('Installation Status', () => {
    it('should update installation status', () => {
      const status = {
        step: 'dependencies',
        progress: 50,
        message: 'Installing dependencies...'
      }
      
      store.commit('setInstallationStatus', status)
      
      expect(store.state.installationStatus).toEqual(status)
    })

    it('should track installation progress', () => {
      store.commit('setInstallationProgress', 75)
      expect(store.state.installationStatus.progress).toBe(75)
    })
  })

  describe('Error Handling', () => {
    it('should set and clear errors', () => {
      const error = {
        message: 'Test error',
        code: 'TEST_ERROR'
      }
      
      store.commit('setError', error)
      expect(store.state.error).toEqual(error)
      
      store.commit('clearError')
      expect(store.state.error).toBeNull()
    })
  })

  describe('Getters', () => {
    it('should get installation progress', () => {
      store.commit('setInstallationProgress', 60)
      expect(store.getters.installationProgress).toBe(60)
    })

    it('should check if installation is in progress', () => {
      store.commit('setInstallationStatus', { 
        step: 'installing',
        progress: 30
      })
      expect(store.getters.isInstalling).toBe(true)
      
      store.commit('setInstallationStatus', { 
        step: 'completed',
        progress: 100
      })
      expect(store.getters.isInstalling).toBe(false)
    })
  })
})
