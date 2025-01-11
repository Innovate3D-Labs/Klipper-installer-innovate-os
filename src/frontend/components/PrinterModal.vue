<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg w-full max-w-2xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold">
            {{ isEdit ? 'Drucker bearbeiten' : 'Neuer Drucker' }}
          </h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Basis-Informationen -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input
                v-model="form.name"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Hersteller</label>
              <input
                v-model="form.manufacturer"
                type="text"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">Typ</label>
              <select
                v-model="form.type"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="cartesian">Cartesian</option>
                <option value="corexy">CoreXY</option>
                <option value="delta">Delta</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700">MCU Typ</label>
              <input
                v-model="form.mcu_type"
                type="text"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
          </div>

          <!-- Bauvolumen -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Bauvolumen (mm)</label>
            <div class="grid grid-cols-3 gap-4">
              <div>
                <label class="block text-xs text-gray-500">X</label>
                <input
                  v-model.number="form.build_volume.x"
                  type="number"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label class="block text-xs text-gray-500">Y</label>
                <input
                  v-model.number="form.build_volume.y"
                  type="number"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label class="block text-xs text-gray-500">Z</label>
                <input
                  v-model.number="form.build_volume.z"
                  type="number"
                  required
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            </div>
          </div>

          <!-- Features -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Features</label>
            <div class="space-y-2">
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  v-model="form.features"
                  value="auto_leveling"
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
                <span class="ml-2">Auto Leveling</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  v-model="form.features"
                  value="dual_extruder"
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
                <span class="ml-2">Dual Extruder</span>
              </label>
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  v-model="form.features"
                  value="heated_bed"
                  class="rounded border-gray-300 text-primary-600 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
                <span class="ml-2">Heated Bed</span>
              </label>
            </div>
          </div>

          <!-- Beschreibung -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Beschreibung</label>
            <textarea
              v-model="form.description"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            ></textarea>
          </div>

          <!-- Konfiguration -->
          <div>
            <label class="block text-sm font-medium text-gray-700">Klipper Konfiguration</label>
            <textarea
              v-model="form.config"
              rows="6"
              class="mt-1 block w-full font-mono text-sm rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
            ></textarea>
          </div>

          <div class="flex justify-end space-x-4">
            <button
              type="button"
              @click="$emit('close')"
              class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
              :disabled="loading"
            >
              <span v-if="loading" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Speichern...
              </span>
              <span v-else>
                Speichern
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'PrinterModal',
  
  props: {
    printer: {
      type: Object,
      default: null
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },

  emits: ['close', 'save'],

  setup(props) {
    const loading = ref(false)
    const form = ref({
      name: '',
      manufacturer: '',
      type: 'cartesian',
      mcu_type: '',
      build_volume: {
        x: 0,
        y: 0,
        z: 0
      },
      features: [],
      description: '',
      config: ''
    })

    onMounted(() => {
      if (props.printer) {
        form.value = {
          ...props.printer,
          build_volume: { ...props.printer.build_volume },
          features: [...(props.printer.features || [])]
        }
      }
    })

    const handleSubmit = async () => {
      loading.value = true
      try {
        await props.$emit('save', form.value)
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      handleSubmit
    }
  }
}
</script>
