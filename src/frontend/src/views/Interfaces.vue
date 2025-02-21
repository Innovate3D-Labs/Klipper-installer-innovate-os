<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Wähle deine Benutzeroberfläche</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Fluidd -->
      <div class="card hover:shadow-lg transition-shadow duration-300">
        <img :src="fluiddLogo" alt="Fluidd Logo" class="h-20 mx-auto mb-4">
        <h2 class="text-2xl font-semibold text-center mb-4">Fluidd</h2>
        <p class="text-gray-600 mb-6">
          Eine moderne, responsive Benutzeroberfläche für Klipper mit vielen Features und einfacher Bedienung.
        </p>
        <button @click="selectInterface('fluidd')" class="btn btn-primary w-full">
          Fluidd auswählen
        </button>
      </div>

      <!-- Mainsail -->
      <div class="card hover:shadow-lg transition-shadow duration-300">
        <img :src="mainsailLogo" alt="Mainsail Logo" class="h-20 mx-auto mb-4">
        <h2 class="text-2xl font-semibold text-center mb-4">Mainsail</h2>
        <p class="text-gray-600 mb-6">
          Eine leistungsstarke und anpassbare Benutzeroberfläche mit umfangreichen Konfigurationsmöglichkeiten.
        </p>
        <button @click="selectInterface('mainsail')" class="btn btn-primary w-full">
          Mainsail auswählen
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Interfaces',
  setup() {
    const store = useStore()
    const router = useRouter()

    const fluiddLogo = 'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="15" fill="#0284c7"/><text x="50" y="60" text-anchor="middle" fill="white" font-family="Arial" font-size="20" font-weight="bold">Fluidd</text></svg>')
    const mainsailLogo = 'data:image/svg+xml;base64,' + btoa('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect x="10" y="10" width="80" height="80" rx="15" fill="#0369a1"/><text x="50" y="60" text-anchor="middle" fill="white" font-family="Arial" font-size="16" font-weight="bold">Mainsail</text></svg>')

    const selectInterface = (interface_type) => {
      store.commit('setSelectedInterface', interface_type)
      router.push('/printers')
    }

    return {
      selectInterface,
      fluiddLogo,
      mainsailLogo
    }
  }
}
</script>