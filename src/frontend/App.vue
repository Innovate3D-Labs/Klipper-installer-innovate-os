<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Logo und Navigation Links -->
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <img class="h-8 w-auto" src="/logo.svg" alt="Klipper Installer" />
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link
                v-for="item in navigationItems"
                :key="item.name"
                :to="item.to"
                :class="[
                  $route.name === item.name
                    ? 'border-primary-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700',
                  'inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium'
                ]"
              >
                {{ item.text }}
              </router-link>
            </div>
          </div>

          <!-- Mobile Menu Button -->
          <div class="flex items-center sm:hidden">
            <button
              @click="mobileMenuOpen = !mobileMenuOpen"
              class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
            >
              <span class="sr-only">Menü öffnen</span>
              <svg
                :class="[mobileMenuOpen ? 'hidden' : 'block', 'h-6 w-6']"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <svg
                :class="[mobileMenuOpen ? 'block' : 'hidden', 'h-6 w-6']"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div :class="[mobileMenuOpen ? 'block' : 'hidden', 'sm:hidden']">
        <div class="pt-2 pb-3 space-y-1">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.to"
            :class="[
              $route.name === item.name
                ? 'bg-primary-50 border-primary-500 text-primary-700'
                : 'border-transparent text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800',
              'block pl-3 pr-4 py-2 border-l-4 text-base font-medium'
            ]"
            @click="mobileMenuOpen = false"
          >
            {{ item.text }}
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Globale Fehlermeldung -->
      <div
        v-if="error"
        class="mb-4 rounded-md bg-red-50 p-4"
      >
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              {{ error.message }}
            </h3>
            <div v-if="error.details" class="mt-2 text-sm text-red-700">
              {{ error.details }}
            </div>
          </div>
          <div class="ml-auto pl-3">
            <div class="-mx-1.5 -my-1.5">
              <button
                @click="clearError"
                class="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100"
              >
                <span class="sr-only">Schließen</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Router View -->
      <router-view v-slot="{ Component }">
        <transition
          name="fade"
          mode="out-in"
        >
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'App',

  setup() {
    const store = useStore()
    const router = useRouter()
    const mobileMenuOpen = ref(false)

    const navigationItems = [
      { name: 'Home', to: '/', text: 'Home' },
      { name: 'Printers', to: '/printers', text: 'Drucker' },
      { name: 'Interfaces', to: '/interfaces', text: 'Oberflächen' },
      { name: 'Settings', to: '/settings', text: 'Einstellungen' }
    ]

    const error = computed(() => store.state.error)

    const clearError = () => {
      store.commit('clearError')
    }

    // Lade aktuelle Web-Interface beim Start
    store.dispatch('getCurrentWebInterface')

    return {
      navigationItems,
      mobileMenuOpen,
      error,
      clearError
    }
  }
}
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
