// Fichier de routage spécifique pour le module d'imagerie
import { ROLES } from '@/constants/roles';

// Import des composants d'imagerie
import StudyList from '@/views/imaging/StudyList.vue';
import StudyDetail from '@/views/imaging/StudyDetail.vue';
import StudyViewer from '@/views/imaging/StudyViewer.vue';
import NewStudy from '@/views/imaging/NewStudy.vue';

const imagingRoutes = [
  // Liste des études d'imagerie
  {
    path: '/imaging/studies',
    name: 'StudyList',
    component: StudyList,
    meta: { 
      requiresAuth: true, 
      title: 'Études d\'imagerie',
      roles: [
        'doctor',
        ROLES.DOCTOR,
        ROLES.RADIOLOGIST, 
        ROLES.TECHNICIAN,
        ROLES.ADMIN
      ]
    }
  },
  
  // Création d'une nouvelle étude
  {
    path: '/imaging/studies/new',
    name: 'NewStudy',
    component: NewStudy,
    meta: { 
      requiresAuth: true, 
      title: 'Nouvel examen DICOM',
      roles: [
        'doctor',
        ROLES.DOCTOR,
        ROLES.RADIOLOGIST, 
        ROLES.TECHNICIAN,
        ROLES.ADMIN
      ]
    },
    props: (route) => ({ patientId: route.query.patient_id })
  },
  
  // Détails d'une étude
  {
    path: '/imaging/studies/:id',
    name: 'StudyDetail',
    component: StudyDetail,
    meta: { 
      requiresAuth: true,
      title: 'Détails de l\'étude',
      roles: [
        'doctor',
        ROLES.DOCTOR, 
        ROLES.RADIOLOGIST, 
        ROLES.TECHNICIAN,
        ROLES.ADMIN
      ]
    }
  },
  
  // Visualisation DICOM
  {
    path: '/imaging/studies/:id/view',
    name: 'StudyViewer',
    component: StudyViewer,
    meta: { 
      requiresAuth: true,
      title: 'Visualisation DICOM',
      roles: [
        'doctor',
        ROLES.DOCTOR, 
        ROLES.RADIOLOGIST, 
        ROLES.TECHNICIAN,
        ROLES.ADMIN
      ]
    }
  }
];

export default imagingRoutes;
