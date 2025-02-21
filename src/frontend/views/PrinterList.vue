<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Verfügbare Drucker</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="printer in printers" 
        :key="printer.id"
        class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
      >
        <h2 class="text-xl font-semibold mb-2">{{ printer.name }}</h2>
        <p class="text-gray-600 mb-2">{{ printer.description || 'Keine Beschreibung verfügbar' }}</p>
        <p class="text-gray-500 text-sm mb-4">
          <span class="font-medium">Port:</span> {{ printer.port }}
          <br>
          <span v-if="printer.manufacturer" class="font-medium">Hersteller:</span> {{ printer.manufacturer }}
        </p>
        <router-link 
          :to="'/printers/' + printer.id + '/install'"
          class="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Installation starten
        </router-link>
      </div>
    </div>

    <div v-if="printers.length === 0" class="text-center py-8">
      <p class="text-gray-600">Keine Drucker gefunden. Bitte stellen Sie sicher, dass Ihr 3D-Drucker angeschlossen ist.</p>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'PrinterList',
  computed: {
    ...mapState(['printers'])
  },
  methods: {
    ...mapActions(['fetchPrinters'])
  },
  mounted() {
    this.fetchPrinters()
  }
}
</script>
