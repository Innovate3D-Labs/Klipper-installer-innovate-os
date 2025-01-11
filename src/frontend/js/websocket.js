import { ref } from 'vue'
import { useStore } from 'vuex'

export class WebSocketClient {
  constructor() {
    this.store = useStore()
    this.ws = null
    this.isConnected = ref(false)
    this.reconnectAttempts = 0
    this.maxReconnectAttempts = 5
    this.reconnectTimeout = null
    this.pingInterval = null
    this.clientId = this._generateClientId()
  }

  connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws/${this.clientId}`

    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      this.isConnected.value = true
      this.reconnectAttempts = 0
      this._startPingInterval()
      this.store.commit('setWebSocketStatus', true)
    }

    this.ws.onclose = () => {
      this.isConnected.value = false
      this._cleanup()
      this._attemptReconnect()
      this.store.commit('setWebSocketStatus', false)
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      this.store.commit('setError', {
        message: 'WebSocket Verbindungsfehler',
        details: 'Die Verbindung zum Server wurde unterbrochen'
      })
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data)
        this._handleMessage(message)
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this._cleanup()
    }
  }

  _cleanup() {
    if (this.pingInterval) {
      clearInterval(this.pingInterval)
      this.pingInterval = null
    }
    this.isConnected.value = false
  }

  _startPingInterval() {
    this.pingInterval = setInterval(() => {
      if (this.isConnected.value) {
        this.send({
          type: 'ping',
          timestamp: Date.now()
        })
      }
    }, 30000) // Ping alle 30 Sekunden
  }

  _attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000)
      
      this.reconnectTimeout = setTimeout(() => {
        console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`)
        this.connect()
      }, delay)
    } else {
      this.store.commit('setError', {
        message: 'Verbindung fehlgeschlagen',
        details: 'Die maximale Anzahl an Verbindungsversuchen wurde erreicht'
      })
    }
  }

  _handleMessage(message) {
    switch (message.type) {
      case 'installation_progress':
        this.store.commit('setInstallationProgress', message.data)
        break

      case 'printer_status':
        this.store.commit('updatePrinterStatus', message.data)
        break

      case 'error':
        this.store.commit('setError', {
          message: message.data.message,
          details: message.data.details
        })
        break

      case 'pong':
        // Handle pong response if needed
        break

      default:
        console.warn('Unknown message type:', message.type)
    }
  }

  send(data) {
    if (this.isConnected.value) {
      this.ws.send(JSON.stringify(data))
    }
  }

  _generateClientId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      const r = Math.random() * 16 | 0
      const v = c === 'x' ? r : (r & 0x3 | 0x8)
      return v.toString(16)
    })
  }
}

// Singleton-Instanz
export const wsClient = new WebSocketClient()
