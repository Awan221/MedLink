<template>
  <div class="min-h-screen flex flex-col">
    <PublicNavbar />
    <main class="flex-grow">
      <router-view />
    </main>
    <PublicFooter />
    
    <!-- Notifications -->
    <AppNotification />
  </div>
</template>

<script setup>
import PublicNavbar from '@/components/public/PublicNavbar.vue';
import PublicFooter from '@/components/public/PublicFooter.vue';
import AppNotification from '@/components/common/AppNotification.vue'

defineOptions({
  name: 'PublicLayout'
});
</script>