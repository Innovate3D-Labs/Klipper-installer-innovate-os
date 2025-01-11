<template>
  <transition
    enter-active-class="transform ease-out duration-300 transition"
    enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition ease-in duration-100"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div v-if="show" class="fixed inset-0 flex items-end px-4 py-6 pointer-events-none sm:p-6 sm:items-start z-50">
      <div class="w-full flex flex-col items-center space-y-4 sm:items-end">
        <div class="max-w-sm w-full bg-white shadow-lg rounded-lg pointer-events-auto ring-1 ring-black ring-opacity-5">
          <div class="p-4">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-red-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div class="ml-3 w-0 flex-1 pt-0.5">
                <p class="text-sm font-medium text-gray-900">
                  {{ title }}
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  {{ message }}
                </p>
                <div v-if="details" class="mt-2">
                  <button
                    type="button"
                    class="text-sm text-gray-600 hover:text-gray-800"
                    @click="showDetails = !showDetails"
                  >
                    {{ showDetails ? 'Details ausblenden' : 'Details anzeigen' }}
                  </button>
                  <pre v-if="showDetails" class="mt-2 text-xs text-gray-500 bg-gray-50 p-2 rounded">{{ details }}</pre>
                </div>
              </div>
              <div class="ml-4 flex-shrink-0 flex">
                <button
                  class="bg-white rounded-md inline-flex text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  @click="dismiss"
                >
                  <span class="sr-only">Schließen</span>
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'ErrorNotification',
  
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Fehler'
    },
    message: {
      type: String,
      required: true
    },
    details: {
      type: String,
      default: null
    },
    duration: {
      type: Number,
      default: 5000 // 5 Sekunden
    },
    persistent: {
      type: Boolean,
      default: false
    }
  },

  emits: ['dismiss'],

  setup(props, { emit }) {
    const showDetails = ref(false)
    let timer = null

    onMounted(() => {
      if (!props.persistent && props.duration > 0) {
        timer = setTimeout(() => {
          emit('dismiss')
        }, props.duration)
      }
    })

    onUnmounted(() => {
      if (timer) {
        clearTimeout(timer)
      }
    })

    const dismiss = () => {
      if (timer) {
        clearTimeout(timer)
      }
      emit('dismiss')
    }

    return {
      showDetails,
      dismiss
    }
  }
}
</script>
