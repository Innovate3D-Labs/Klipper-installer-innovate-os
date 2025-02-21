<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Wähle deine Benutzeroberfläche</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Fluidd -->
      <div class="card hover:shadow-lg transition-shadow duration-300 p-6">
        <div class="w-20 h-20 mx-auto mb-4 bg-primary-600 rounded-lg flex items-center justify-center">
          <span class="text-white text-xl font-bold">Fluidd</span>
        </div>
        <h2 class="text-2xl font-semibold text-center mb-4">Fluidd</h2>
        <p class="text-gray-600 mb-6">
          Eine moderne, responsive Benutzeroberfläche für Klipper mit vielen Features und einfacher Bedienung.
        </p>
        <button @click="selectInterface('fluidd')" class="btn btn-primary w-full">
          Fluidd auswählen
        </button>
      </div>

      <!-- Mainsail -->
      <div class="card hover:shadow-lg transition-shadow duration-300 p-6">
        <div class="w-20 h-20 mx-auto mb-4 bg-primary-700 rounded-lg flex items-center justify-center">
          <span class="text-white text-xl font-bold">Mainsail</span>
        </div>
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

    const selectInterface = (interface_type) => {
      store.commit('setSelectedInterface', interface_type)
      router.push('/printers')
    }

    return {
      selectInterface
    }
  }
}
</script>