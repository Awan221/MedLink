// Utilitaire pour extraire les métadonnées d’un fichier DICOM côté frontend
// Nécessite dcmjs ou dicom-parser (préféré pour la légèreté)
// npm install dicom-parser

import * as dicomParser from 'dicom-parser';

export function extractDicomMetadata(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = function(e) {
      try {
        const byteArray = new Uint8Array(e.target.result);
        const dataSet = dicomParser.parseDicom(byteArray);
        const tags = {
          PatientName: dataSet.string('x00100010') || '',
          PatientID: dataSet.string('x00100020') || '',
          StudyDate: dataSet.string('x00080020') || '',
          Modality: dataSet.string('x00080060') || '',
          StudyDescription: dataSet.string('x00081030') || '',
          SeriesDescription: dataSet.string('x0008103e') || '',
          InstitutionName: dataSet.string('x00080080') || '',
        };
        resolve(tags);
      } catch (err) {
        reject('Ce fichier ne semble pas être un DICOM valide.');
      }
    };
    reader.onerror = function() {
      reject('Erreur de lecture du fichier.');
    };
    reader.readAsArrayBuffer(file);
  });
}
