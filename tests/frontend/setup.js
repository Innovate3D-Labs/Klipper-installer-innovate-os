import { config } from '@vue/test-utils'
import { createStore } from 'vuex'

// Mock store für globale Verfügbarkeit in Tests
const store = createStore({
  state: {},
  mutations: {},
  actions: {}
})

// Globale Mocks
config.global.mocks = {
  $store: store
}

// Stubs für externe Komponenten
config.global.stubs = {
  'font-awesome-icon': true
}
