<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex justify-between items-center mb-8">
      <h1 class="text-3xl font-bold">Druckerverwaltung</h1>
      <button
        @click="showAddPrinterModal = true"
        class="bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded"
      >
        Drucker hinzufügen
      </button>
    </div>

    <!-- Drucker-Liste -->
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="printers.length === 0" class="text-center py-8">
      <p class="text-gray-600">Keine Drucker verfügbar</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="printer in printers"
        :key="printer.id"
        class="bg-white rounded-lg shadow-md overflow-hidden"
      >
        <div class="p-6">
          <div class="flex justify-between items-start">
            <h2 class="text-xl font-semibold mb-2">{{ printer.name }}</h2>
            <div class="flex space-x-2">
              <button
                @click="editPrinter(printer)"
                class="text-gray-600 hover:text-primary-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button
                @click="confirmDelete(printer)"
                class="text-gray-600 hover:text-red-600"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="mt-4 space-y-2">
            <p class="text-gray-600">
              <span class="font-medium">Hersteller:</span> {{ printer.manufacturer }}
            </p>
            <p class="text-gray-600">
              <span class="font-medium">Typ:</span> {{ printer.type }}
            </p>
            <p class="text-gray-600">
              <span class="font-medium">Bauvolumen:</span>
              {{ `${printer.build_volume.x}x${printer.build_volume.y}x${printer.build_volume.z}mm` }}
            </p>
          </div>

          <div class="mt-4">
            <button
              @click="selectPrinter(printer)"
              class="w-full bg-primary-100 text-primary-700 hover:bg-primary-200 font-medium py-2 px-4 rounded"
            >
              Konfiguration anzeigen
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Drucker hinzufügen/bearbeiten Modal -->
    <PrinterModal
      v-if="showAddPrinterModal || showEditPrinterModal"
      :printer="selectedPrinter"
      :is-edit="showEditPrinterModal"
      @close="closeModal"
      @save="savePrinter"
    />

    <!-- Löschen Bestätigung Modal -->
    <ConfirmDialog
      v-if="showDeleteConfirm"
      :title="'Drucker löschen'"
      :message="'Möchten Sie diesen Drucker wirklich löschen?'"
      @confirm="deletePrinter"
      @cancel="showDeleteConfirm = false"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import PrinterModal from '../components/PrinterModal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'

export default {
  name: 'Printers',
  
  components: {
    PrinterModal,
    ConfirmDialog
  },

  setup() {
    const store = useStore()
    const showAddPrinterModal = ref(false)
    const showEditPrinterModal = ref(false)
    const showDeleteConfirm = ref(false)
    const selectedPrinter = ref(null)
    const printerToDelete = ref(null)

    const printers = computed(() => store.state.printers)
    const loading = computed(() => store.state.loading.printers)

    onMounted(() => {
      store.dispatch('fetchPrinters')
    })

    const editPrinter = (printer) => {
      selectedPrinter.value = { ...printer }
      showEditPrinterModal.value = true
    }

    const selectPrinter = (printer) => {
      store.commit('setSelectedPrinter', printer)
      // Hier könnte Navigation zur Konfigurationsansicht erfolgen
    }

    const confirmDelete = (printer) => {
      printerToDelete.value = printer
      showDeleteConfirm.value = true
    }

    const closeModal = () => {
      showAddPrinterModal.value = false
      showEditPrinterModal.value = false
      selectedPrinter.value = null
    }

    const savePrinter = async (printerData) => {
      try {
        if (showEditPrinterModal.value) {
          await store.dispatch('updatePrinter', {
            id: selectedPrinter.value.id,
            data: printerData
          })
        } else {
          await store.dispatch('createPrinter', printerData)
        }
        closeModal()
      } catch (error) {
        console.error('Fehler beim Speichern:', error)
      }
    }

    const deletePrinter = async () => {
      if (!printerToDelete.value) return

      try {
        await store.dispatch('deletePrinter', printerToDelete.value.id)
        showDeleteConfirm.value = false
        printerToDelete.value = null
      } catch (error) {
        console.error('Fehler beim Löschen:', error)
      }
    }

    return {
      printers,
      loading,
      showAddPrinterModal,
      showEditPrinterModal,
      showDeleteConfirm,
      selectedPrinter,
      editPrinter,
      selectPrinter,
      confirmDelete,
      closeModal,
      savePrinter,
      deletePrinter
    }
  }
}
</script>
