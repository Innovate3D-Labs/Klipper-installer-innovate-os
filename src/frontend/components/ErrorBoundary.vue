<template>
  <div>
    <slot v-if="!error" />
    
    <div v-else class="rounded-md bg-red-50 p-4">
      <div class="flex">
        <div class="flex-shrink-0">
          <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
        </div>
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">
            Ein Fehler ist aufgetreten
          </h3>
          <div class="mt-2 text-sm text-red-700">
            <p>{{ error.message }}</p>
            <p v-if="error.info" class="mt-1">
              {{ error.info }}
            </p>
          </div>
          <div class="mt-4">
            <button
              type="button"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              @click="reset"
            >
              Neu laden
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ErrorBoundary',
  
  data() {
    return {
      error: null
    }
  },

  errorCaptured(err, vm, info) {
    this.error = {
      message: err.message,
      info: info
    }
    return false // Verhindert Fehlerweiterleitung
  },

  methods: {
    reset() {
      this.error = null
      this.$emit('reset')
    }
  }
}
</script>
