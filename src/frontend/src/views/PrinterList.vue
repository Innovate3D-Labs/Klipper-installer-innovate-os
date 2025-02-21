<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Gefundene Drucker</h1>
      <p class="text-gray-600">Wähle deinen 3D-Drucker aus der Liste</p>
    </div>

    <!-- Drucker-Liste -->
    <div class="space-y-4">
      <div v-if="loading" class="text-center py-8">
        <i class="fas fa-spinner fa-spin text-4xl text-primary-600"></i>
        <p class="mt-4 text-gray-600">Suche nach Druckern...</p>
      </div>

      <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p class="font-bold">Fehler beim Laden der Drucker</p>
        <p>{{ error }}</p>
      </div>

      <div v-else-if="printers.length === 0" class="text-center py-8">
        <i class="fas fa-exclamation-circle text-4xl text-gray-400"></i>
        <p class="mt-4 text-gray-600">Keine Drucker gefunden</p>
        <button @click="refreshPrinters" class="btn btn-primary mt-4">
          Erneut suchen
        </button>
      </div>

      <div v-else v-for="printer in printers" :key="printer.id" class="card hover:shadow-lg transition-shadow duration-300">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-xl font-semibold text-gray-900">{{ printer.name }}</h3>
            <div class="mt-2 text-sm text-gray-500">
              <p><span class="font-medium">Port:</span> {{ printer.port }}</p>
              <p><span class="font-medium">Hardware ID:</span> {{ printer.hardware_id }}</p>
              <p v-if="printer.manufacturer"><span class="font-medium">Hersteller:</span> {{ printer.manufacturer }}</p>
            </div>
          </div>
          <router-link :to="'/install/' + printer.id" class="btn btn-primary">
            Installieren
          </router-link>
        </div>
      </div>
    </div>

    <!-- Aktionen -->
    <div class="mt-8 flex justify-between">
      <router-link to="/" class="btn btn-secondary">
        Zurück
      </router-link>
      <button @click="refreshPrinters" class="btn btn-primary" :disabled="loading">
        <i class="fas fa-sync-alt mr-2" :class="{ 'fa-spin': loading }"></i>
        Aktualisieren
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'PrinterList',
  
  setup() {
    const store = useStore()
    const loading = ref(false)
    const error = ref(null)
    const printers = ref([])

    const fetchPrinters = async () => {
      loading.value = true
      error.value = null
      
      try {
        const response = await fetch('/api/v1/printers')
        const data = await response.json()
        printers.value = data
      } catch (err) {
        error.value = 'Fehler beim Laden der Drucker'
        console.error('Error loading printers:', err)
      } finally {
        loading.value = false
      }
    }

    const refreshPrinters = () => {
      fetchPrinters()
    }

    onMounted(() => {
      fetchPrinters()
    })

    return {
      loading,
      error,
      printers,
      refreshPrinters
    }
  }
}
</script>
