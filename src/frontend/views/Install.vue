<template>
  <div>
    <div class="md:flex md:items-center md:justify-between mb-8">
      <div class="flex-1 min-w-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
          Klipper Installation
        </h2>
      </div>
    </div>

    <!-- Installation Steps -->
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <nav aria-label="Progress">
          <ol role="list" class="overflow-hidden">
            <li
              v-for="(step, index) in steps"
              :key="step.name"
              :class="[index !== steps.length - 1 ? 'pb-10' : '', 'relative']"
            >
              <!-- Step Connector Line -->
              <div
                v-if="index !== steps.length - 1"
                class="absolute left-4 top-4 -ml-px mt-0.5 h-full w-0.5"
                :class="step.status === 'complete' ? 'bg-primary-600' : 'bg-gray-300'"
                aria-hidden="true"
              />

              <div class="relative flex items-start group">
                <!-- Step Circle -->
                <span class="h-9 flex items-center">
                  <span
                    class="relative z-10 w-8 h-8 flex items-center justify-center rounded-full"
                    :class="[
                      step.status === 'complete' ? 'bg-primary-600' : 
                      step.status === 'current' ? 'border-2 border-primary-600' : 
                      'border-2 border-gray-300',
                    ]"
                  >
                    <template v-if="step.status === 'complete'">
                      <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                      </svg>
                    </template>
                    <template v-else>
                      <span
                        :class="[
                          step.status === 'current' ? 'text-primary-600' : 'text-gray-500',
                        ]"
                      >
                        {{ index + 1 }}
                      </span>
                    </template>
                  </span>
                </span>

                <!-- Step Content -->
                <div class="ml-4 min-w-0 flex-1">
                  <div class="text-sm font-medium text-gray-900">
                    {{ step.name }}
                  </div>
                  <div class="mt-2 text-sm text-gray-500">
                    {{ step.description }}
                  </div>

                  <!-- Step Action -->
                  <div v-if="step.status === 'current'" class="mt-4">
                    <div v-if="step.component" class="space-y-4">
                      <component
                        :is="step.component"
                        v-bind="step.props || {}"
                        @complete="completeStep"
                        @error="handleError"
                      />
                    </div>
                    <div v-else class="flex space-x-4">
                      <button
                        type="button"
                        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
                        @click="startStep"
                        :disabled="installing"
                      >
                        <span v-if="installing">
                          <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Installiere...
                        </span>
                        <span v-else>Starten</span>
                      </button>
                    </div>
                  </div>

                  <!-- Step Output -->
                  <div
                    v-if="step.output"
                    class="mt-4 bg-gray-50 rounded-md p-4 font-mono text-sm text-gray-900 whitespace-pre-wrap"
                  >
                    {{ step.output }}
                  </div>

                  <!-- Step Error -->
                  <div
                    v-if="step.error"
                    class="mt-4 bg-red-50 border-l-4 border-red-400 p-4"
                  >
                    <div class="flex">
                      <div class="flex-shrink-0">
                        <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                        </svg>
                      </div>
                      <div class="ml-3">
                        <p class="text-sm text-red-700">
                          {{ step.error }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </li>
          </ol>
        </nav>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Install',

  setup() {
    const store = useStore()
    const route = useRoute()
    const router = useRouter()
    const installing = ref(false)

    const steps = ref([
      {
        name: 'Vorbereitung',
        description: 'Überprüfe System-Voraussetzungen und bereite Installation vor',
        status: 'current',
        output: null,
        error: null
      },
      {
        name: 'Klipper Installation',
        description: 'Installiere Klipper und seine Abhängigkeiten',
        status: 'upcoming',
        output: null,
        error: null
      },
      {
        name: 'Firmware Kompilierung',
        description: 'Kompiliere und flashe die Firmware für deinen 3D-Drucker',
        status: 'upcoming',
        output: null,
        error: null
      },
      {
        name: 'Konfiguration',
        description: 'Konfiguriere Klipper für deinen 3D-Drucker',
        status: 'upcoming',
        output: null,
        error: null
      },
      {
        name: 'Abschluss',
        description: 'Überprüfe die Installation und starte die Dienste',
        status: 'upcoming',
        output: null,
        error: null
      }
    ])

    onMounted(async () => {
      if (route.params.printerId) {
        try {
          const printer = await store.dispatch('getPrinter', route.params.printerId)
          // Setze Drucker-spezifische Informationen
        } catch (error) {
          store.commit('setError', {
            message: 'Drucker nicht gefunden',
            details: error.message
          })
          router.push('/printers')
        }
      }
    })

    const getCurrentStep = () => {
      return steps.value.find(step => step.status === 'current')
    }

    const startStep = async () => {
      const currentStep = getCurrentStep()
      if (!currentStep) return

      installing.value = true
      currentStep.error = null
      currentStep.output = ''

      try {
        // Führe den aktuellen Installationsschritt aus
        await store.dispatch('executeInstallStep', {
          step: currentStep.name,
          printerId: route.params.printerId,
          onOutput: (output) => {
            currentStep.output = (currentStep.output || '') + output + '\n'
          }
        })

        completeStep()
      } catch (error) {
        handleError(error)
      } finally {
        installing.value = false
      }
    }

    const completeStep = () => {
      const currentIndex = steps.value.findIndex(step => step.status === 'current')
      if (currentIndex === -1) return

      // Markiere aktuellen Schritt als abgeschlossen
      steps.value[currentIndex].status = 'complete'

      // Setze nächsten Schritt als aktuell
      if (currentIndex < steps.value.length - 1) {
        steps.value[currentIndex + 1].status = 'current'
      } else {
        // Installation abgeschlossen
        store.commit('setSuccess', 'Installation erfolgreich abgeschlossen')
        router.push('/printers')
      }
    }

    const handleError = (error) => {
      const currentStep = getCurrentStep()
      if (currentStep) {
        currentStep.error = error.message || 'Ein unerwarteter Fehler ist aufgetreten'
      }
      store.commit('setError', {
        message: 'Installationsfehler',
        details: error.message
      })
    }

    return {
      steps,
      installing,
      startStep,
      completeStep,
      handleError
    }
  }
}
</script>
