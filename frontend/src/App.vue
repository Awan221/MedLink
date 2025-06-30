<template>
  <div id="app" class="min-h-screen bg-gray-100">
    <Navbar v-if="isAuthenticated" />
    <div class="container mx-auto px-4 py-6">
      <router-view />
    </div>
    <FooterView />
  </div>
</template>

<script>
import Navbar from '@/components/layout/Navbar.vue'
import FooterView from '@/components/layout/Footer.vue'
import { mapGetters } from 'vuex'
//import AppHeader from './components/common/AppHeader.vue'

export default {
  name: 'App',
  components: {
    Navbar,
    FooterView,
  },
  computed: {
    ...mapGetters('auth', ['isAuthenticated'])
  },
  created() {
    // Vérifier l'authentification au chargement de l'application
    this.$store.dispatch('auth/checkAuth')
  }
}
</script>

<style>
#app {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>