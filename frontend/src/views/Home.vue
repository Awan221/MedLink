<template> 
  <div class="bg-white">
    <!-- Hero Section -->
    <div class="relative bg-gradient-to-r from-blue-600 to-indigo-800 text-white">
      <div class="container mx-auto px-4 pt-12 pb-24 md:pt-40 md:pb-60">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-2">
            <h1 class="text-4xl md:text-5xl font-bold mb-4">Plateforme d'imagerie médicale Orthanc</h1>
            <p class="text-xl mb-10">Une solution complète pour la gestion des images médicales, des patients et des diagnostics assistés par IA.</p>
            <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
              <router-link 
                to="/login" 
                class="z-50 bg-white text-blue-600 hover:bg-gray-100 px-6 py-3 rounded-lg font-semibold text-center"
              >
                Connexion
              </router-link>
              <router-link 
                to="/register" 
                class="z-50 bg-transparent hover:bg-blue-700 border border-white px-6 py-3 rounded-lg font-semibold text-center"
              >
                Inscription
              </router-link>
              <router-link
                to="/public"
                class="z-50 bg-yellow-400 text-blue-900 hover:bg-yellow-300 px-6 py-3 rounded-lg font-semibold text-center border border-yellow-500 transition"
                style="margin-top: 0.5em;"
              >
                Portail public
              </router-link>
            </div>
          </div>
          <!---<div class="md:w-1/2">
            <img src="@/assets/hero-image.png" alt="Imagerie médicale" class="rounded-lg shadow-xl">
          </div>-->
        </div>
      </div>
      
      <!-- Vague décorative -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" class="w-full h-auto">
          <path fill="#ffffff" fill-opacity="1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,149.3C960,160,1056,160,1152,138.7C1248,117,1344,75,1392,53.3L1440,32L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </div>
    </div>
    
    <!-- Fonctionnalités -->
    <div class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">Nos fonctionnalités</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Gestion des patients</h3>
            <p class="text-gray-600">Gérez efficacement les dossiers médicaux, les antécédents et les rendez-vous de vos patients.</p>
          </div>
          
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">Imagerie DICOM</h3>
            <p class="text-gray-600">Stockez, visualisez et partagez des images médicales au format DICOM avec notre visualiseur intégré.</p>
          </div>
          
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold mb-2">IA Diagnostic</h3>
            <p class="text-gray-600">Utilisez l'intelligence artificielle pour assister le diagnostic médical et améliorer la précision.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Chatbot -->
    <div class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center">
          <div class="md:w-1/2 mb-8 md:mb-0">
            <h2 class="text-3xl font-bold mb-4">Assistant médical virtuel</h2>
            <p class="text-xl text-gray-600 mb-6">Notre chatbot médical répond à vos questions et vous guide dans l'utilisation de la plateforme.</p>
            <router-link 
              to="/chat" 
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-semibold inline-block"
            >
              Essayer le chatbot
            </router-link>
          </div>
          <div class="md:w-1/2">
            <img src="@/assets/chatbot-image.png" alt="Chatbot médical" class="rounded-lg shadow-lg">
          </div>
        </div>
      </div>
    </div>
    
    <!-- Témoignages -->
    <div class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">Ce que disent nos utilisateurs</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span class="text-blue-600 font-bold">DR</span>
              </div>
              <div>
                <h4 class="font-semibold">Dr. Robert Martin</h4>
                <p class="text-gray-600 text-sm">Radiologue</p>
              </div>
            </div>
            <p class="text-gray-600">"La plateforme Orthanc a considérablement amélioré notre flux de travail. Le visualiseur DICOM est rapide et l'intégration de l'IA nous aide à détecter des anomalies que nous aurions pu manquer."</p>
          </div>
          
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span class="text-blue-600 font-bold">SL</span>
              </div>
              <div>
                <h4 class="font-semibold">Sophie Leclerc</h4>
                <p class="text-gray-600 text-sm">Secrétaire médicale</p>
              </div>
            </div>
            <p class="text-gray-600">"La gestion des rendez-vous et des dossiers patients est devenue beaucoup plus simple. Je peux facilement suivre les examens programmés et envoyer des rappels automatiques."</p>
          </div>
          
          <div class="bg-gray-50 p-6 rounded-lg shadow-md">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mr-4">
                <span class="text-blue-600 font-bold">JD</span>
              </div>
              <div>
                <h4 class="font-semibold">Dr. Julie Dupont</h4>
                <p class="text-gray-600 text-sm">Médecin généraliste</p>
              </div>
            </div>
            <p class="text-gray-600">"L'accès rapide aux images médicales et aux rapports de radiologie me permet de prendre des décisions plus éclairées pour mes patients. Le chatbot est également très utile pour répondre aux questions fréquentes."</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- CTA -->
    <div class="py-16 bg-gradient-to-r from-blue-600 to-indigo-800 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-4">Prêt à améliorer votre pratique médicale?</h2>
        <p class="text-xl mb-8 max-w-2xl mx-auto">Rejoignez notre plateforme d'imagerie médicale et découvrez comment l'IA peut transformer votre diagnostic.</p>
        <div class="flex flex-col sm:flex-row justify-center space-y-4 sm:space-y-0 sm:space-x-4">
          <router-link 
            to="/register" 
            class="bg-white text-blue-600 hover:bg-gray-100 px-6 py-3 rounded-lg font-semibold"
          >
            S'inscrire maintenant
          </router-link>
          <router-link 
            to="/contact" 
            class="bg-transparent hover:bg-blue-700 border border-white px-6 py-3 rounded-lg font-semibold"
          >
            Nous contacter
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>