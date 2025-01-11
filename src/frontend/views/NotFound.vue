<template>
  <div class="min-h-[60vh] flex flex-col items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">404</h1>
      <p class="text-xl text-gray-600 mb-8">Seite nicht gefunden</p>
      <router-link
        to="/"
        class="inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
      >
        Zurück zur Startseite
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>
