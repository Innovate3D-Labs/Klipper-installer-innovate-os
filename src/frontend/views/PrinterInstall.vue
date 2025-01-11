<template>
  <div class="max-w-4xl mx-auto">
    <div class="bg-white p-6 rounded-lg shadow-md">
      <h1 class="text-3xl font-bold mb-6">Installation: {{ selectedPrinter?.model }}</h1>

      <div class="mb-8">
        <div class="w-full bg-gray-200 rounded-full h-4">
          <div 
            class="bg-blue-600 h-4 rounded-full transition-all duration-500"
            :style="{ width: installationProgress + '%' }"
          ></div>
        </div>
        <p class="mt-2 text-gray-600">{{ currentStep }}</p>
      </div>

      <div class="bg-gray-100 p-4 rounded-lg font-mono text-sm h-64 overflow-y-auto">
        <div v-for="(log, index) in logs" :key="index" class="mb-1">
          <span :class="{'text-green-600': log.status === 'completed', 'text-red-600': log.status === 'error'}">
            {{ log.message }}
          </span>
        </div>
      </div>

      <div class="mt-6 flex justify-between">
        <router-link 
          to="/printers"
          class="bg-gray-500 text-white px-6 py-2 rounded hover:bg-gray-600"
        >
          Zurück
        </router-link>
        <button 
          @click="startInstallation"
          :disabled="isInstalling"
          class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ isInstalling ? 'Installation läuft...' : 'Installation starten' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'PrinterInstall',
  data() {
    return {
      logs: [],
      currentStep: 'Bereit zur Installation',
      installationProgress: 0,
      isInstalling: false
    }
  },
  computed: {
    ...mapState(['selectedPrinter', 'installationStatus'])
  },
  methods: {
    ...mapActions(['startInstallation']),
    async initializeInstallation() {
      this.isInstalling = true
      this.logs = []
      this.installationProgress = 0
      await this.startInstallation()
    }
  },
  watch: {
    installationStatus(status) {
      if (!status) return

      this.logs.push({
        status: status.status,
        message: status.status === 'error' ? status.error : status.output
      })

      if (status.status === 'completed') {
        this.installationProgress = 100
        this.currentStep = 'Installation abgeschlossen'
        this.isInstalling = false
      } else if (status.status === 'error') {
        this.currentStep = 'Fehler bei der Installation'
        this.isInstalling = false
      }
    }
  },
  created() {
    const printerName = this.$route.params.name
    if (!this.selectedPrinter || this.selectedPrinter.name !== printerName) {
      this.$router.push('/printers')
    }
  }
}
</script>
