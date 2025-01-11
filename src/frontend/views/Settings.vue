<template>
  <div>
    <div class="md:flex md:items-center md:justify-between mb-8">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Einstellungen
        </h2>
      </div>
    </div>

    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <!-- Allgemeine Einstellungen -->
        <div class="space-y-6">
          <div>
            <h3 class="text-lg leading-6 font-medium text-gray-900">Allgemein</h3>
            <div class="mt-2 max-w-xl text-sm text-gray-500">
              <p>Grundlegende Einstellungen für den Klipper Installer.</p>
            </div>
            <div class="mt-5 space-y-4">
              <!-- Sprache -->
              <div>
                <label for="language" class="block text-sm font-medium text-gray-700">
                  Sprache
                </label>
                <select
                  id="language"
                  v-model="settings.language"
                  class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
                >
                  <option value="de">Deutsch</option>
                  <option value="en">English</option>
                </select>
              </div>

              <!-- Theme -->
              <div>
                <label for="theme" class="block text-sm font-medium text-gray-700">
                  Theme
                </label>
                <select
                  id="theme"
                  v-model="settings.theme"
                  class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
                >
                  <option value="light">Hell</option>
                  <option value="dark">Dunkel</option>
                  <option value="system">System</option>
                </select>
              </div>

              <!-- Auto-Update -->
              <div class="relative flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id="autoUpdate"
                    v-model="settings.autoUpdate"
                    type="checkbox"
                    class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                  >
                </div>
                <div class="ml-3 text-sm">
                  <label for="autoUpdate" class="font-medium text-gray-700">Automatische Updates</label>
                  <p class="text-gray-500">Automatisch nach Updates suchen und installieren</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Backup -->
          <div class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-lg leading-6 font-medium text-gray-900">Backup</h3>
                <div class="mt-2 max-w-xl text-sm text-gray-500">
                  <p>Verwalten Sie Ihre Backups und stellen Sie Konfigurationen wieder her.</p>
                </div>
              </div>
              <button
                type="button"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                @click="createBackup"
              >
                Backup erstellen
              </button>
            </div>
          </div>

          <!-- Entwickler -->
          <div class="pt-6">
            <h3 class="text-lg leading-6 font-medium text-gray-900">Entwickler</h3>
            <div class="mt-2 max-w-xl text-sm text-gray-500">
              <p>Erweiterte Einstellungen für Entwickler.</p>
            </div>
            <div class="mt-5 space-y-4">
              <div class="relative flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id="debugMode"
                    v-model="settings.debugMode"
                    type="checkbox"
                    class="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                  >
                </div>
                <div class="ml-3 text-sm">
                  <label for="debugMode" class="font-medium text-gray-700">Debug-Modus</label>
                  <p class="text-gray-500">Zusätzliche Logging-Informationen anzeigen</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
        <button
          type="button"
          class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          @click="saveSettings"
          :disabled="saving"
        >
          <span v-if="saving">Speichern...</span>
          <span v-else>Speichern</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'Settings',

  setup() {
    const store = useStore()
    const saving = ref(false)
    const settings = ref({
      language: 'de',
      theme: 'light',
      autoUpdate: true,
      debugMode: false
    })

    onMounted(async () => {
      // Lade gespeicherte Einstellungen
      const savedSettings = await store.dispatch('getSettings')
      if (savedSettings) {
        settings.value = { ...settings.value, ...savedSettings }
      }
    })

    const saveSettings = async () => {
      saving.value = true
      try {
        await store.dispatch('updateSettings', settings.value)
        store.commit('setSuccess', 'Einstellungen wurden gespeichert')
      } catch (error) {
        store.commit('setError', {
          message: 'Fehler beim Speichern der Einstellungen',
          details: error.message
        })
      } finally {
        saving.value = false
      }
    }

    const createBackup = async () => {
      try {
        await store.dispatch('createBackup')
        store.commit('setSuccess', 'Backup wurde erstellt')
      } catch (error) {
        store.commit('setError', {
          message: 'Fehler beim Erstellen des Backups',
          details: error.message
        })
      }
    }

    return {
      settings,
      saving,
      saveSettings,
      createBackup
    }
  }
}
</script>
