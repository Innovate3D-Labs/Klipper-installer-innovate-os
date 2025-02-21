<template>
  <div class="max-w-4xl mx-auto p-6">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Willkommen beim Klipper Installer</h1>
      <p class="text-xl text-gray-600">Installiere und konfiguriere Klipper für deinen 3D-Drucker</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Drucker erkennen -->
      <div class="card hover:shadow-lg transition-shadow duration-300">
        <div class="text-center mb-6">
          <i class="fas fa-search text-4xl text-primary-600"></i>
          <h2 class="text-2xl font-semibold mt-4">Drucker erkennen</h2>
          <p class="text-gray-600 mt-2">Automatische Erkennung deines 3D-Druckers</p>
        </div>
        <router-link to="/printers" class="btn btn-primary w-full text-center">
          Drucker suchen
        </router-link>
      </div>

      <!-- Dokumentation -->
      <div class="card hover:shadow-lg transition-shadow duration-300">
        <div class="text-center mb-6">
          <i class="fas fa-book text-4xl text-primary-600"></i>
          <h2 class="text-2xl font-semibold mt-4">Dokumentation</h2>
          <p class="text-gray-600 mt-2">Hilfe und Anleitungen zur Installation</p>
        </div>
        <a href="https://www.klipper3d.org/Installation.html" target="_blank" class="btn btn-primary w-full text-center">
          Dokumentation öffnen
        </a>
      </div>
    </div>

    <!-- Features -->
    <div class="mt-16">
      <h2 class="text-3xl font-bold text-center mb-8">Features</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="card text-center">
          <i class="fas fa-bolt text-3xl text-primary-600 mb-4"></i>
          <h3 class="text-xl font-semibold mb-2">Schnelle Installation</h3>
          <p class="text-gray-600">Automatisierte Installation und Konfiguration</p>
        </div>
        <div class="card text-center">
          <i class="fas fa-cogs text-3xl text-primary-600 mb-4"></i>
          <h3 class="text-xl font-semibold mb-2">Einfache Konfiguration</h3>
          <p class="text-gray-600">Vorkonfigurierte Einstellungen für deinen Drucker</p>
        </div>
        <div class="card text-center">
          <i class="fas fa-check-circle text-3xl text-primary-600 mb-4"></i>
          <h3 class="text-xl font-semibold mb-2">Kompatibilitätsprüfung</h3>
          <p class="text-gray-600">Automatische Erkennung der Hardware</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home'
}
</script>
