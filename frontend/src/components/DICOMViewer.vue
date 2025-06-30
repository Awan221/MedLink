<template>
  <div class="dicom-viewer">
    <div class="toolbar">
      <button :class="{active: tool==='wwwc'}" @click="setTool('wwwc')">Window</button>
      <button :class="{active: tool==='zoom'}" @click="setTool('zoom')">Zoom</button>
      <button :class="{active: tool==='pan'}" @click="setTool('pan')">Déplacer</button>
      <button :class="{active: tool==='length'}" @click="setTool('length')">Mesure</button>
      <button :class="{active: tool==='annotate'}" @click="setTool('annotate')">Annotation</button>
      <button :class="{active: tool==='reset'}" @click="resetView">Réinitialiser</button>
    </div>
    <div ref="dicomViewport" class="dicom-viewport"></div>
    <div class="dicom-controls">
      <button @click="prevImage" :disabled="currentIndex <= 0">Précédent</button>
      <button @click="nextImage" :disabled="currentIndex >= imageUrls.length - 1">Suivant</button>
      <span>{{ currentIndex + 1 }} / {{ imageUrls.length }}</span>
    </div>
  </div>
</template>

<script>
import * as cornerstone from 'cornerstone-core';
import * as cornerstoneWADOImageLoader from 'cornerstone-wado-image-loader';
import * as cornerstoneTools from 'cornerstone-tools';

export default {
  name: 'DICOMViewer',
  props: {
    imageUrls: {
      type: Array,
      required: true,
      // Example: ["/api/dicom/instances/123/file", ...]
    }
  },
  data() {
    return {
      currentIndex: 0,
      tool: 'wwwc', // outil courant (window/width par défaut)
    };
  },
  mounted() {
    this.loadCornerstone();
    this.displayImage();
  },
  watch: {
    currentIndex() {
      this.displayImage();
    },
    imageUrls() {
      this.currentIndex = 0;
      this.displayImage();
    }
  },
  methods: {
    loadCornerstone() {
      cornerstoneWADOImageLoader.external.cornerstone = cornerstone;
      cornerstoneWADOImageLoader.configure({
        beforeSend: function(xhr) {
          // Optionally add auth headers here
        }
      });
      cornerstoneTools.external.cornerstone = cornerstone;
      cornerstoneTools.init();
    },
    displayImage() {
      const element = this.$refs.dicomViewport;
      const imageId = `wadouri:${window.location.origin}${this.imageUrls[this.currentIndex]}`;
      cornerstone.enable(element);
      cornerstone.loadAndCacheImage(imageId).then(image => {
        cornerstone.displayImage(element, image);
        this.setTool(this.tool);
      });
    },
    setTool(tool) {
      this.tool = tool;
      const element = this.$refs.dicomViewport;
      cornerstoneTools.setToolActive('Pan', { mouseButtonMask: 4 }); // désactive tout
      cornerstoneTools.setToolActive('Zoom', { mouseButtonMask: 4 });
      cornerstoneTools.setToolActive('Wwwc', { mouseButtonMask: 4 });
      cornerstoneTools.setToolActive('Length', { mouseButtonMask: 4 });
      cornerstoneTools.setToolActive('FreehandRoi', { mouseButtonMask: 4 });
      if (tool === 'pan') {
        cornerstoneTools.setToolActive('Pan', { mouseButtonMask: 1 });
      } else if (tool === 'zoom') {
        cornerstoneTools.setToolActive('Zoom', { mouseButtonMask: 1 });
      } else if (tool === 'wwwc') {
        cornerstoneTools.setToolActive('Wwwc', { mouseButtonMask: 1 });
      } else if (tool === 'length') {
        cornerstoneTools.setToolActive('Length', { mouseButtonMask: 1 });
      } else if (tool === 'annotate') {
        cornerstoneTools.setToolActive('FreehandRoi', { mouseButtonMask: 1 });
      }
    },
    resetView() {
      const element = this.$refs.dicomViewport;
      cornerstone.reset(element);
    },
    prevImage() {
      if (this.currentIndex > 0) this.currentIndex--;

    },
    nextImage() {
      if (this.currentIndex < this.imageUrls.length - 1) this.currentIndex++;
    }
  }
};
</script>

<style scoped>
.dicom-viewer {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.dicom-viewport {
  width: 512px;
  height: 512px;
  background: #222;
  margin-bottom: 1em;
}
.dicom-controls {
  display: flex;
  gap: 1em;
  align-items: center;
}
</style>
