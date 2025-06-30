<template>
  <footer class="bg-gray-800 text-white py-8 mt-12">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row justify-between">
        <div class="mb-6 md:mb-0">
          <h3 class="text-lg font-semibold mb-2">Orthanc Medical</h3>
          <p class="text-gray-400">Plateforme d'imagerie médicale et de gestion de patients</p>
        </div>
        
        <div class="grid grid-cols-2 md:grid-cols-3 gap-8">
          <div>
            <h4 class="text-sm font-semibold uppercase tracking-wider mb-3">Plateforme</h4>
            <ul class="space-y-2">
              <li><router-link to="/" class="text-gray-400 hover:text-white">Accueil</router-link></li>
              <li><router-link to="/features" class="text-gray-400 hover:text-white">Fonctionnalités</router-link></li>
              <li><router-link to="/pricing" class="text-gray-400 hover:text-white">Tarifs</router-link></li>
              <li><router-link to="/about" class="text-gray-400 hover:text-white">À propos</router-link></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-sm font-semibold uppercase tracking-wider mb-3">Support</h4>
            <ul class="space-y-2">
              <li><router-link to="/documentation" class="text-gray-400 hover:text-white">Documentation</router-link></li>
              <li><router-link to="/faq" class="text-gray-400 hover:text-white">FAQ</router-link></li>
              <li><router-link to="/contact" class="text-gray-400 hover:text-white">Contact</router-link></li>
            </ul>
          </div>
          
          <div>
            <h4 class="text-sm font-semibold uppercase tracking-wider mb-3">Légal</h4>
            <ul class="space-y-2">
              <li><router-link to="/privacy" class="text-gray-400 hover:text-white">Confidentialité</router-link></li>
              <li><router-link to="/terms" class="text-gray-400 hover:text-white">Conditions d'utilisation</router-link></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="mt-8 pt-8 border-t border-gray-700 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-400 text-sm">&copy; {{ currentYear }} Orthanc Medical. Tous droits réservés.</p>
        
        <div class="flex space-x-4 mt-4 md:mt-0">
          <a href="#" class="text-gray-400 hover:text-white">
            <span class="sr-only">Facebook</span>
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clip-rule="evenodd" />
            </svg>
          </a>
          
          <a href="#" class="text-gray-400 hover:text-white">
            <span class="sr-only">Twitter</span>
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
            </svg>
          </a>
          
          <a href="#" class="text-gray-400 hover:text-white">
            <span class="sr-only">LinkedIn</span>
            <svg class="h-6 w-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fill-rule="evenodd" d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z" clip-rule="evenodd" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterView',
  computed: {
    currentYear() {
      return new Date().getFullYear()
    }
  }
}
</script>