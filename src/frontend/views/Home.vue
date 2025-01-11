<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold mb-8">Willkommen beim Klipper Installer</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4">Drucker installieren</h2>
        <p class="mb-4">Wählen Sie Ihren 3D-Drucker aus und starten Sie die Installation von Klipper.</p>
        <router-link 
          to="/printers" 
          class="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Zur Druckerauswahl
        </router-link>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-md">
        <h2 class="text-2xl font-semibold mb-4">Weboberfläche wählen</h2>
        <p class="mb-4">Wechseln Sie zwischen Fluidd und Mainsail als Weboberfläche.</p>
        <router-link 
          to="/interfaces" 
          class="inline-block bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Zu den Weboberflächen
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>
