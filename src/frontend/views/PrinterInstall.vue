<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Klipper Installation</h1>
      <p class="text-gray-600">Installiere Klipper für {{ printer.name }}</p>
    </div>

    <!-- Installation Status -->
    <div class="bg-white rounded-lg shadow-md p-6 mb-6">
      <h2 class="text-xl font-semibold mb-4">Installationsstatus</h2>
      
      <!-- Progress Steps -->
      <div class="space-y-4">
        <div class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center mr-3',
            status.klipper ? 'bg-green-500 text-white' : 'bg-gray-200'
          ]">
            <span v-if="status.klipper" class="fas fa-check"></span>
            <span v-else>1</span>
          </div>
          <div>
            <p class="font-medium">Klipper Installation</p>
            <p class="text-sm text-gray-500">Installation der Klipper Software</p>
          </div>
        </div>

        <div class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center mr-3',
            status.firmware ? 'bg-green-500 text-white' : 'bg-gray-200'
          ]">
            <span v-if="status.firmware" class="fas fa-check"></span>
            <span v-else>2</span>
          </div>
          <div>
            <p class="font-medium">Firmware Kompilierung</p>
            <p class="text-sm text-gray-500">Kompilierung der MCU Firmware</p>
          </div>
        </div>

        <div class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center mr-3',
            status.flashing ? 'bg-green-500 text-white' : 'bg-gray-200'
          ]">
            <span v-if="status.flashing" class="fas fa-check"></span>
            <span v-else>3</span>
          </div>
          <div>
            <p class="font-medium">Firmware Flashen</p>
            <p class="text-sm text-gray-500">Übertragung der Firmware auf den Drucker</p>
          </div>
        </div>

        <div class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center mr-3',
            status.service ? 'bg-green-500 text-white' : 'bg-gray-200'
          ]">
            <span v-if="status.service" class="fas fa-check"></span>
            <span v-else>4</span>
          </div>
          <div>
            <p class="font-medium">Klipper Service</p>
            <p class="text-sm text-gray-500">Einrichtung des Klipper System Service</p>
          </div>
        </div>

        <div class="flex items-center">
          <div :class="[
            'w-8 h-8 rounded-full flex items-center justify-center mr-3',
            status.config ? 'bg-green-500 text-white' : 'bg-gray-200'
          ]">
            <span v-if="status.config" class="fas fa-check"></span>
            <span v-else>5</span>
          </div>
          <div>
            <p class="font-medium">Konfiguration</p>
            <p class="text-sm text-gray-500">Erstellung der Drucker-Konfiguration</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
      <p class="font-bold">Installation fehlgeschlagen</p>
      <p>{{ error }}</p>
    </div>

    <!-- Success Message -->
    <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
      <p class="font-bold">Installation erfolgreich!</p>
      <p>Klipper wurde erfolgreich installiert und konfiguriert.</p>
    </div>

    <!-- Action Buttons -->
    <div class="flex justify-between">
      <button 
        @click="$router.push('/printers')"
        class="bg-gray-500 text-white px-6 py-2 rounded hover:bg-gray-600"
      >
        Zurück
      </button>
      
      <button 
        v-if="!installing"
        @click="startInstallation"
        class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        :disabled="installing"
      >
        Installation starten
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

export default {
  name: 'PrinterInstall',
  
  setup() {
    const route = useRoute()
    const printer = ref(null)
    const installing = ref(false)
    const error = ref(null)
    const success = ref(false)
    const status = ref({
      klipper: false,
      firmware: false,
      flashing: false,
      service: false,
      config: false
    })

    const loadPrinter = async () => {
      try {
        const response = await axios.get(`/api/v1/printers/${route.params.id}`)
        printer.value = response.data
      } catch (err) {
        error.value = 'Fehler beim Laden der Druckerinformationen'
        console.error('Error loading printer:', err)
      }
    }

    const startInstallation = async () => {
      installing.value = true
      error.value = null
      success.value = false
      
      try {
        const response = await axios.post(`/api/v1/install/${route.params.id}`)
        if (response.data.status === 'success') {
          success.value = true
          status.value = {
            klipper: true,
            firmware: true,
            flashing: true,
            service: true,
            config: true
          }
        } else {
          error.value = response.data.message
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ein unerwarteter Fehler ist aufgetreten'
        console.error('Installation error:', err)
      } finally {
        installing.value = false
      }
    }

    onMounted(() => {
      loadPrinter()
    })

    return {
      printer,
      installing,
      error,
      success,
      status,
      startInstallation
    }
  }
}
</script>
