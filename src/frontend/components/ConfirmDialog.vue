<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-lg w-full max-w-md">
      <div class="p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">{{ title }}</h3>
        <p class="text-sm text-gray-500">{{ message }}</p>
        
        <div class="mt-6 flex justify-end space-x-4">
          <button
            type="button"
            @click="$emit('cancel')"
            class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Abbrechen
          </button>
          <button
            type="button"
            @click="$emit('confirm')"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Bestätigen
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  
  props: {
    title: {
      type: String,
      required: true
    },
    message: {
      type: String,
      required: true
    }
  },

  emits: ['confirm', 'cancel']
}
</script>
