<template>
  <div class="dicom-viewer">
    <div class="viewer-container">
      <div class="sidebar">
        <div class="study-list">
          <h3>Études DICOM</h3>
          <v-text-field
            v-model="searchQuery"
            label="Rechercher..."
            prepend-inner-icon="mdi-magnify"
            dense
            outlined
            hide-details
            class="mb-4"
          />
          
          <v-list dense>
            <v-list-item-group v-model="selectedStudy" color="primary">
              <v-list-item
                v-for="study in filteredStudies"
                :key="study.id"
                @click="selectStudy(study)"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ formatStudyDate(study.study_date) }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ study.modality }} - {{ study.study_description || 'Sans description' }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-action>
                  <v-icon>mdi-chevron-right</v-icon>
                </v-list-item-action>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </div>
        
        <div v-if="selectedStudy" class="series-list">
          <h3>Séries</h3>
          <v-list dense>
            <v-list-item-group v-model="selectedSeries" color="primary">
              <v-list-item
                v-for="series in selectedStudy.series"
                :key="series.id"
                @click="selectSeries(series)"
              >
                <v-list-item-icon>
                  <v-icon>mdi-database</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>Série {{ series.series_number }}</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ series.modality }} - {{ series.series_description || 'Sans description' }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
          </v-list>
        </div>
      </div>
      
      <div class="viewer-main">
        <div v-if="!selectedStudy" class="empty-state">
          <v-icon x-large>mdi-radiology-box</v-icon>
          <p>Sélectionnez une étude pour commencer</p>
        </div>
        
        <div v-else class="viewer-content">
          <div class="viewer-toolbar">
            <v-toolbar dense>
              <v-toolbar-title>
                {{ selectedStudy.patient_name }} - {{ formatStudyDate(selectedStudy.study_date) }}
              </v-toolbar-title>
              <v-spacer></v-spacer>
              <v-btn icon @click="downloadStudy">
                <v-icon>mdi-download</v-icon>
              </v-btn>
              <v-btn icon @click="printStudy">
                <v-icon>mdi-printer</v-icon>
              </v-btn>
            </v-toolbar>
          </div>
          
          <div v-if="selectedSeries" class="image-viewer">
            <div class="viewer-controls">
              <v-slider
                v-model="currentImageIndex"
                :max="selectedSeries.instances.length - 1"
                :tick-labels="imageTicks"
                ticks="always"
                tick-size="4"
                class="slider"
              ></v-slider>
              
              <div class="viewer-actions">
                <v-btn icon @click="zoomIn">
                  <v-icon>mdi-magnify-plus</v-icon>
                </v-btn>
                <v-btn icon @click="zoomOut">
                  <v-icon>mdi-magnify-minus</v-icon>
                </v-btn>
                <v-btn icon @click="resetView">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
                <v-btn icon @click="toggleFullscreen">
                  <v-icon>mdi-fullscreen</v-icon>
                </v-btn>
              </div>
            </div>
            
            <div ref="viewerElement" class="cornerstone-viewer">
              <!-- Le visualiseur DICOM sera rendu ici -->
            </div>
            
            <div class="image-metadata">
              <v-expansion-panels flat>
                <v-expansion-panel>
                  <v-expansion-panel-header>
                    Métadonnées DICOM
                  </v-expansion-panel-header>
                  <v-expansion-panel-content>
                    <v-simple-table dense>
                      <template v-slot:default>
                        <tbody>
                          <tr v-for="(value, key) in currentInstance.metadata" :key="key">
                            <td class="font-weight-bold">{{ key }}</td>
                            <td>{{ value }}</td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-expansion-panels>
            </div>
          </div>
          
          <div v-else class="no-series">
            <p>Sélectionnez une série pour afficher les images</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Chargement -->
    <v-overlay :value="loading">
      <v-progress-circular indeterminate size="64"></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import {
  getEnabledElement,
  enable as enableCornerstone,
  disable as disableCornerstone,
  setViewport,
  getDefaultViewport,
  resize,
  getEnabledElements,
} from 'cornerstone-core';
import cornerstoneMath from 'cornerstone-math';
import cornerstoneTools from 'cornerstone-tools';
import cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';
import dicomParser from 'dicom-parser';
import { useToast } from 'vue-toastification';

export default {
  name: 'DicomViewer',
  
  setup() {
    const toast = useToast();
    
    // Références
    const viewerElement = ref(null);
    const loading = ref(false);
    const searchQuery = ref('');
    const selectedStudy = ref(null);
    const selectedSeries = ref(null);
    const currentImageIndex = ref(0);
    const isFullscreen = ref(false);
    
    // Données factices pour la démonstration
    const studies = ref([
      {
        id: 1,
        study_uid: '1.2.840.113619.2.5.1763500119.1601.1446000000.1',
        study_date: '2023-05-15T10:30:00Z',
        study_description: 'CT ABDOMEN PELVIS',
        patient_name: 'DUPONT Jean',
        patient_id: '12345',
        modality: 'CT',
        series: [
          {
            id: 1,
            series_uid: '1.2.840.113619.2.5.1763500119.1601.1446000000.2',
            series_number: 1,
            series_description: 'ABDOMEN',
            modality: 'CT',
            instances: Array(50).fill(0).map((_, i) => ({
              id: i + 1,
              sop_instance_uid: `1.2.840.113619.2.5.1763500119.1601.1446000000.2.${i + 1}`,
              instance_number: i + 1,
              metadata: {
                'Patient Name': 'DUPONT Jean',
                'Patient ID': '12345',
                'Study Date': '20230515',
                'Modality': 'CT',
                'Body Part': 'ABDOMEN',
                'Slice Thickness': '5.0 mm',
                'KVP': '120 kVp',
                'Exposure': '200 mAs',
              }
            }))
          }
        ]
      },
      // Ajoutez d'autres études factices si nécessaire
    ]);
    
    // Filtrage des études
    const filteredStudies = computed(() => {
      if (!searchQuery.value) return studies.value;
      const query = searchQuery.value.toLowerCase();
      return studies.value.filter(study => 
        study.patient_name.toLowerCase().includes(query) ||
        study.study_description?.toLowerCase().includes(query) ||
        study.modality.toLowerCase().includes(query)
      );
    });
    
    // Ticks pour le slider
    const imageTicks = computed(() => {
      if (!selectedSeries.value) return [];
      return selectedSeries.value.instances.map((_, i) => i % 10 === 0 ? i : '');
    });
    
    // Instance DICOM courante
    const currentInstance = computed(() => {
      if (!selectedSeries.value) return null;
      return selectedSeries.value.instances[currentImageIndex.value];
    });
    
    // Formater la date d'étude
    const formatStudyDate = (dateString) => {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
      return new Date(dateString).toLocaleDateString('fr-FR', options);
    };
    
    // Sélectionner une étude
    const selectStudy = (study) => {
      selectedStudy.value = study;
      selectedSeries.value = null;
      currentImageIndex.value = 0;
    };
    
    // Sélectionner une série
    const selectSeries = (series) => {
      selectedSeries.value = series;
      currentImageIndex.value = 0;
      // Ici, vous chargeriez les images DICOM réelles
      // loadDicomImages(series);
    };
    
    // Télécharger l'étude
    const downloadStudy = () => {
      toast.info('Téléchargement de l\'étude...');
      // Implémentez la logique de téléchargement
    };
    
    // Imprimer l'étude
    const printStudy = () => {
      window.print();
    };
    
    // Contrôles du visualiseur
    const zoomIn = () => {
      // Implémentez le zoom avant
    };
    
    const zoomOut = () => {
      // Implémentez le zoom arrière
    };
    
    const resetView = () => {
      // Réinitialisez la vue
    };
    
    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        viewerElement.value?.requestFullscreen?.();
      } else {
        document.exitFullscreen?.();
      }
      isFullscreen.value = !isFullscreen.value;
    };
    
    // Initialiser Cornerstone
    const initCornerstone = () => {
      // Configuration de cornerstone-tools
      const { MouseWheelTool, ZoomTool, PanTool, StackScrollTool, ToolGroupManager } = cornerstoneTools;
      
      // Configuration du chargeur d'images DICOM
      const config = {
        webWorkerPath: '/static/cornerstoneWADOImageLoaderWebWorker.min.js',
        taskConfiguration: {
          decodeTask: {
            codecsPath: '/static/cornerstoneWADOImageLoaderCodecs.js'
          }
        }
      };
      
      cornerstoneWADOImageLoader.webWorkerManager.initialize(config);
      
      // Enregistrer les outils
      cornerstoneTools.external.cornerstone = cornerstone;
      cornerstoneTools.external.cornerstoneMath = cornerstoneMath;
      cornerstoneTools.external.Hammer = Hammer;
      
      // Initialiser les outils
      const toolGroupId = 'default';
      const toolGroup = ToolGroupManager.createToolGroup(toolGroupId);
      
      // Ajouter les outils
      toolGroup.addTool(PanTool.toolName);
      toolGroup.addTool(ZoomTool.toolName);
      toolGroup.addTool(StackScrollTool.toolName);
      toolGroup.addTool(MouseWheelTool.toolName);
      
      // Activer les outils
      toolGroup.setToolActive(PanTool.toolName, { mouseButtonMask: 1 });
      toolGroup.setToolActive(ZoomTool.toolName, { mouseButtonMask: 2 });
      toolGroup.setToolActive(StackScrollTool.toolName, { mouseButtonMask: 4 });
      toolGroup.setToolActive(MouseWheelTool.toolName);
      
      // Activer l'élément Cornerstone
      enableCornerstone(viewerElement.value);
    };
    
    // Nettoyer Cornerstone lors de la destruction du composant
    const cleanupCornerstone = () => {
      if (viewerElement.value) {
        disableCornerstone(viewerElement.value);
      }
    };
    
    // Cycle de vie du composant
    onMounted(() => {
      try {
        initCornerstone();
      } catch (error) {
        console.error('Erreur lors de l\'initialisation de Cornerstone:', error);
        toast.error('Erreur lors de l\'initialisation du visualiseur DICOM');
      }
    });
    
    onBeforeUnmount(() => {
      cleanupCornerstone();
    });
    
    return {
      // Références
      viewerElement,
      loading,
      searchQuery,
      selectedStudy,
      selectedSeries,
      currentImageIndex,
      
      // Données
      studies: filteredStudies,
      
      // Computed
      imageTicks,
      currentInstance,
      
      // Méthodes
      formatStudyDate,
      selectStudy,
      selectSeries,
      downloadStudy,
      printStudy,
      zoomIn,
      zoomOut,
      resetView,
      toggleFullscreen,
    };
  },
};
</script>

<style scoped>
.dicom-viewer {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.viewer-container {
  display: flex;
  flex: 1;
  height: calc(100vh - 64px);
  overflow: hidden;
}

.sidebar {
  width: 300px;
  border-right: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.study-list, .series-list {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.study-list {
  flex: 1;
  overflow-y: auto;
}

.viewer-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.viewer-toolbar {
  border-bottom: 1px solid #e0e0e0;
}

.image-viewer {
  display: flex;
  flex-direction: column;
  flex: 1;
  overflow: hidden;
}

.viewer-controls {
  padding: 8px 16px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #e0e0e0;
}

.slider {
  margin: 0 16px;
}

.viewer-actions {
  display: flex;
  justify-content: center;
  gap: 8px;
  margin-top: 8px;
}

.cornerstone-viewer {
  flex: 1;
  background-color: #000;
  position: relative;
  overflow: hidden;
}

.image-metadata {
  max-height: 200px;
  overflow-y: auto;
  border-top: 1px solid #e0e0e0;
}

.empty-state, .no-series {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #757575;
  text-align: center;
  padding: 24px;
}

.empty-state i, .no-series i {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.5;
}
</style>
