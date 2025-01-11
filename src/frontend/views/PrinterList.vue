<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Verfügbare Drucker</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="printer in printers" 
        :key="printer.name"
        class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow"
      >
        <h2 class="text-xl font-semibold mb-2">{{ printer.model }}</h2>
        <p class="text-gray-600 mb-4">{{ printer.description || 'Keine Beschreibung verfügbar' }}</p>
        <router-link 
          :to="'/printers/' + printer.name + '/install'"
          class="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Installation starten
        </router-link>
      </div>
    </div>

    <div v-if="printers.length === 0" class="text-center py-8">
      <p class="text-gray-600">Keine Drucker gefunden.</p>
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
