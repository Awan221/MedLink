<template>
  <div class="min-h-screen bg-gray-100">
    <div class="container px-4 py-6 mx-auto">
      <!-- En-tête du visualiseur -->
      <div class="flex items-center justify-between mb-4">
        <div>
          <h1 class="text-2xl font-bold text-gray-800">
            {{ study ? study.study_description || 'Visualiseur DICOM' : 'Chargement...' }}
          </h1>
          <p v-if="study" class="text-gray-600">
            Patient: {{ study.patient_name }} | 
            Date: {{ formatDate(study.study_date) }} | 
            Modalité: {{ study.modality }}
          </p>
        </div>
        <button 
          @click="goBack" 
          class="px-4 py-2 text-white transition-colors bg-blue-600 rounded hover:bg-blue-700"
        >
          Retour à la liste
        </button>
      </div>
      
      <!-- Conteneur principal -->
      <div class="overflow-hidden bg-white rounded-lg shadow-lg">
        <!-- Barre d'outils -->
        <div class="flex items-center p-2 bg-gray-100 border-b">
          <div class="flex space-x-2">
            <button 
              v-for="tool in tools" 
              :key="tool.id"
              @click="setActiveTool(tool.id)"
              :class="[
                'p-2 rounded',
                activeTool === tool.id 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-white hover:bg-gray-200'
              ]"
              :title="tool.label"
            >
              <component :is="tool.icon" class="w-5 h-5" />
            </button>
          </div>
          <div class="ml-4 text-sm text-gray-600">
            {{ activeTool ? `Outil actif: ${getToolLabel(activeTool)}` : '' }}
          </div>
        </div>

        <!-- Conteneur pour les images DICOM -->
        <div class="relative" style="height: 70vh;">
          <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
            <div class="text-center">
              <div class="w-12 h-12 mx-auto border-b-2 border-blue-500 rounded-full animate-spin"></div>
              <p class="mt-2 text-gray-600">Chargement des images DICOM...</p>
            </div>
          </div>
          
          <div v-else-if="error" class="p-4 bg-red-100 rounded">
            <p class="text-red-600">Erreur : {{ error }}</p>
            <p class="mt-2 text-sm text-gray-600">
              Assurez-vous que le serveur Orthanc est en cours d'exécution et accessible.
              <br>
              URL du serveur: http://localhost:8042
            </p>
            <button 
              @click="loadStudy" 
              class="px-4 py-2 mt-4 text-white bg-blue-600 rounded hover:bg-blue-700"
            >
              Réessayer
            </button>
          </div>
          
          <!-- Conteneur pour les images -->
          <div v-else class="grid grid-cols-1 gap-4 p-4 md:grid-cols-2 lg:grid-cols-3">
            <div 
              v-for="(instance, index) in instances" 
              :key="instance.ID"
              class="overflow-hidden bg-gray-100 rounded-lg shadow"
            >
              <div class="p-2 text-sm text-center text-gray-700 bg-gray-200">
                Instance {{ index + 1 }} - {{ instance.MainDicomTags.InstanceNumber || 'N/A' }}
              </div>
              <div class="relative" style="height: 200px;">
                <div 
                  :id="'dicom-canvas-' + instance.ID"
                  class="w-full h-full bg-black"
                ></div>
                <div v-if="!imageLoaded[instance.ID]" class="absolute inset-0 flex items-center justify-center">
                  <div class="w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                </div>
              </div>
              <div class="p-2 text-xs text-gray-600">
                <p>Type: {{ instance.MainDicomTags.SOPClassUID || 'N/A' }}</p>
                <p>UID: {{ instance.ID }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import * as cornerstone from 'cornerstone-core';
import * as cornerstoneTools from 'cornerstone-tools';
import * as cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';
import dicomParser from 'dicom-parser';
import { 
  HandThumbUpIcon as HandIcon,
  MagnifyingGlassIcon as SearchIcon,
  MinusIcon, 
  PlusIcon, 
  ArrowsPointingOutIcon as ArrowsExpandIcon,
  Squares2X2Icon as ViewGridIcon
} from '@heroicons/vue/24/outline';

// Configuration Orthanc via le proxy Django
const ORTHANC_URL = '/imaging/orthanc';
// Configuration de Cornerstone
cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
cornerstoneWADOImageLoader.external.dicomParser = dicomParser;

// Configuration du chargeur d'images WADO
const config = {
  webWorkerPath: 'https://unpkg.com/cornerstone-wado-image-loader/dist/cornerstoneWADOImageLoaderWebWorker.min.js',
  taskConfiguration: {
    'decodeTask': {
      codecsPath: 'https://unpkg.com/cornerstone-wado-image-loader/dist/cornerstoneWADOImageLoaderCodecs.js'
    }
  }
};

// Initialiser le gestionnaire de workers
cornerstoneWADOImageLoader.webWorkerManager.initialize(config);

// Configurer l'authentification pour les requêtes DICOM
cornerstoneWADOImageLoader.configure({
  beforeSend: function(xhr) {
    xhr.withCredentials = true;
  }
});

export default {
  name: 'StudyViewer',
  
  components: {
    HandIcon,
    SearchIcon,
    MinusIcon,
    PlusIcon,
    ArrowsExpandIcon,
    ViewGridIcon
  },
  
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const study = ref(null);
    const instances = ref([]);
    const loading = ref(true);
    const error = ref(null);
    const activeTool = ref('pan');
    const imageLoaded = ref({});
    const zoomLevel = ref(1);
    
    const tools = [
      { id: 'pan', label: 'Déplacer', icon: 'HandIcon' },
      { id: 'wwc', label: 'Fenêtrage', icon: 'SearchIcon' },
      { id: 'zoomIn', label: 'Zoom +', icon: 'PlusIcon' },
      { id: 'zoomOut', label: 'Zoom -', icon: 'MinusIcon' },
      { id: 'reset', label: 'Réinitialiser', icon: 'ArrowsExpandIcon' },
      { id: 'layout', label: 'Disposition', icon: 'ViewGridIcon' }
    ];
    
    const formatDate = (dateString) => {
      if (!dateString) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    };
    
    const goBack = () => {
      router.go(-1);
    };
    
    const getToolLabel = (toolId) => {
      const tool = tools.find(t => t.id === toolId);
      return tool ? tool.label : toolId;
    };
    
    const setActiveTool = (toolId) => {
      activeTool.value = toolId;
      // Implémenter la logique de l'outil sélectionné
      switch (toolId) {
        case 'pan':
          // Activer le déplacement
          break;
        case 'wwc':
          // Activer le fenêtrage
          break;
        case 'zoomIn':
          zoomLevel.value = Math.min(zoomLevel.value + 0.2, 3);
          break;
        case 'zoomOut':
          zoomLevel.value = Math.max(zoomLevel.value - 0.2, 0.5);
          break;
        case 'reset':
          zoomLevel.value = 1;
          // Réinitialiser la vue
          break;
      }
    };
    
    // Charger une instance DICOM
    const loadDicomInstance = async (instanceId, elementId) => {
      try {
        // Marquer l'image comme en cours de chargement
        imageLoaded.value = { ...imageLoaded.value, [instanceId]: false };
        
        // Récupérer l'instance DICOM via le proxy Django
        /*const response = await axios.get(`${ORTHANC_URL}/instances/${instanceId}/file`, {
          responseType: 'arraybuffer',
          withCredentials: true  // Important pour l'authentification de session
        });*/
        
        // Charger l'image avec Cornerstone
        const imageId = `wadouri:${ORTHANC_URL}/instances/${instanceId}/file`;
        const element = document.getElementById(elementId);
        
        // Activer l'élément pour Cornerstone
        cornerstone.enable(element);
        
        // Charger et afficher l'image
        const image = await cornerstone.loadAndCacheImage(imageId);
        cornerstone.displayImage(element, image);
        
        // Activer les outils de base
        cornerstoneTools.mouseInput.enable(element);
        cornerstoneTools.mouseWheelInput.enable(element);
        
        // Marquer comme chargé
        imageLoaded.value = { ...imageLoaded.value, [instanceId]: true };
        
      } catch (err) {
        console.error('Erreur lors du chargement de l\'instance DICOM:', err);
        error.value = 'Impossible de charger l\'image DICOM. ' + 
                     (err.response?.data?.message || err.message || '');
      }
    };
    
    // Charger les données de l'étude
    const loadStudy = async () => {
      try {
        loading.value = true;
        error.value = null;
        
        // 1. Récupérer les détails de l'étude
        const studyResponse = await axios.get(`/imaging/studies/${route.params.id}/`);
        study.value = studyResponse.data;
        
        if (!study.value?.study_instance_uid) {
          throw new Error('Aucune étude trouvée avec cet ID');
        }
        
        // 2. Récupérer les séries de l'étude via le proxy Django
        console.log(`Tentative de récupération des séries pour l'étude: ${study.value.study_instance_uid}`);
        console.log(`URL complète: ${ORTHANC_URL}/studies/${study.value.study_instance_uid}/series`);
        
        const seriesResponse = await axios.get(
          `${ORTHANC_URL}/studies/${study.value.study_instance_uid}/series`, 
          {
            withCredentials: true,  // Important pour l'authentification de session
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            }
          }
        );
        
        console.log('Réponse des séries reçue:', seriesResponse);
        
        // S'assurer que la réponse est un tableau
        let seriesList = [];
        if (Array.isArray(seriesResponse.data)) {
          seriesList = seriesResponse.data;
        } else if (seriesResponse.data && typeof seriesResponse.data === 'object') {
          // Si la réponse est un objet, le convertir en tableau
          seriesList = Object.values(seriesResponse.data);
        }
        
        if (!seriesList || seriesList.length === 0) {
          console.error('Aucune série trouvée dans la réponse:', seriesResponse);
          throw new Error('Aucune série trouvée pour cette étude');
        }
        
        console.log(`Nombre de séries trouvées: ${seriesList.length}`);
        
        // 3. Pour chaque série, récupérer les instances via le proxy Django
        const instancesPromises = seriesList.map(series => {
          const seriesId = series.ID || series.id || series.SeriesInstanceUID || series.seriesInstanceUid;
          if (!seriesId) {
            console.warn('Série sans ID valide:', series);
            return Promise.resolve({ data: [] });
          }
          return axios.get(`${ORTHANC_URL}/series/${seriesId}/instances`, {
            withCredentials: true
          });
        });
        
        const instancesResponses = await Promise.all(instancesPromises);
        
        // 4. Aplatir la liste des instances
        instances.value = instancesResponses.flatMap(response => response.data);
        
        // 5. Charger la première instance de chaque série
        instances.value.forEach((instance, index) => {
          setTimeout(() => {
            loadDicomInstance(instance.ID, `dicom-canvas-${instance.ID}`);
          }, index * 500); // Délai pour éviter de surcharger le navigateur
        });
        
      } catch (err) {
        console.error('Erreur lors du chargement de l\'étude:', err);
        error.value = 'Impossible de charger les détails de l\'étude. ' + 
                     (err.response?.data?.message || err.message || '');
      } finally {
        loading.value = false;
      }
    };
    
    // Nettoyer les ressources lors du démontage
    onBeforeUnmount(() => {
      // Désactiver tous les éléments Cornerstone
      document.querySelectorAll('.cornerstone-enabled-image').forEach(element => {
        cornerstone.disable(element);
      });
    });
    
    // Initialiser au montage du composant
    onMounted(() => {
      loadStudy();
    });
    
    return {
      study,
      instances,
      loading,
      error,
      tools,
      activeTool,
      imageLoaded,
      zoomLevel,
      formatDate,
      goBack,
      getToolLabel,
      setActiveTool
    };
  }
};
</script>

<style>
/* Styles pour OHIF Viewer */
#ohif-viewer {
  width: 100%;
  height: 100%;
  min-height: 600px;
}

/* Personnalisation du thème OHIF */
:root {
  --primary-color: #3b82f6;
  --primary-dark: #2563eb;
  --primary-light: #93c5fd;
  --secondary-color: #6b7280;
  --background-color: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #4b5563;
}

/* Amélioration de l'accessibilité */
button:focus {
  outline: 2px solid var(--primary-color);
  outline-offset: 2px;
}

/* Animation de chargement */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>