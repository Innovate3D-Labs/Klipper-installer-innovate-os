<template>
  <div class="min-h-screen">
    <nav class="bg-blue-600 text-white p-4">
      <div class="container mx-auto flex justify-between items-center">
        <router-link to="/" class="text-xl font-bold">Klipper Installer</router-link>
        <div class="space-x-4">
          <router-link to="/printers" class="hover:text-blue-200">Drucker</router-link>
          <router-link to="/interfaces" class="hover:text-blue-200">Weboberflächen</router-link>
        </div>
      </div>
    </nav>

    <main class="container mx-auto p-4">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
