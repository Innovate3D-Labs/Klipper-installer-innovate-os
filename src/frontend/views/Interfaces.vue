<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Weboberfläche auswählen</h1>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Fluidd -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-semibold">Fluidd</h2>
          <img src="/images/fluidd-logo.png" alt="Fluidd Logo" class="h-12">
        </div>
        <p class="text-gray-600 mb-4">
          Moderne und intuitive Weboberfläche für Klipper mit Fokus auf Benutzerfreundlichkeit.
        </p>
        <button 
          @click="switchTo('fluidd')"
          :class="[
            'w-full py-2 px-4 rounded',
            currentInterface === 'fluidd'
              ? 'bg-green-600 text-white'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          ]"
        >
          {{ currentInterface === 'fluidd' ? 'Aktiv' : 'Aktivieren' }}
        </button>
      </div>

      <!-- Mainsail -->
      <div class="bg-white p-6 rounded-lg shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-2xl font-semibold">Mainsail</h2>
          <img src="/images/mainsail-logo.png" alt="Mainsail Logo" class="h-12">
        </div>
        <p class="text-gray-600 mb-4">
          Leistungsstarke Weboberfläche mit erweiterten Funktionen und Anpassungsmöglichkeiten.
        </p>
        <button 
          @click="switchTo('mainsail')"
          :class="[
            'w-full py-2 px-4 rounded',
            currentInterface === 'mainsail'
              ? 'bg-green-600 text-white'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          ]"
        >
          {{ currentInterface === 'mainsail' ? 'Aktiv' : 'Aktivieren' }}
        </button>
      </div>
    </div>

    <!-- Status Message -->
    <div 
      v-if="statusMessage"
      :class="[
        'mt-6 p-4 rounded',
        statusMessage.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
      ]"
    >
      {{ statusMessage.text }}
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'Interfaces',
  data() {
    return {
      statusMessage: null
    }
  },
  computed: {
    ...mapState(['currentInterface'])
  },
  methods: {
    ...mapActions(['switchInterface']),
    async switchTo(interface) {
      try {
        await this.switchInterface(interface)
        this.statusMessage = {
          type: 'success',
          text: `Erfolgreich zu ${interface} gewechselt`
        }
      } catch (error) {
        this.statusMessage = {
          type: 'error',
          text: `Fehler beim Wechsel zu ${interface}`
        }
      }
      
      setTimeout(() => {
        this.statusMessage = null
      }, 3000)
    }
  }
}
</script>
