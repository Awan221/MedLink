# Documentation Fonctionnelle - MedLink

## Table des Matières
1. [Présentation du Projet](#présentation-du-projet)
2. [Cas d'Utilisation](#cas-dutilisation)
3. [Maquettes et Parcours Utilisateur](#maquettes-et-parcours-utilisateur)
4. [Règles Métier](#règles-métier)
5. [Glossaire](#glossaire)
6. [Annexes](#annexes)

## Présentation du Projet

### Contexte
MedLink est une plateforme de télémédecine complète qui vise à :
- Faciliter la gestion des dossiers patients
- Permettre la téléradiologie et le partage d'images médicales
- Optimiser la gestion des stocks de sang
- Offrir une assistance médicale via un chatbot intelligent

### Objectifs
- Améliorer l'accès aux soins médicaux
- Faciliter la collaboration entre professionnels de santé
- Digitaliser la gestion des données médicales
- Assurer la sécurité et la confidentialité des données

### Public Cible
- Médecins généralistes et spécialistes
- Personnel paramédical
- Administrateurs de santé
- Patients
- Donneurs de sang

## Cas d'Utilisation

### 1. Gestion des Utilisateurs
#### 1.1 Inscription d'un Professionnel de Santé
**Acteur** : Personnel médical  
**Description** : Un professionnel de santé s'inscrit sur la plateforme.  
**Préconditions** : Aucune  
**Scénario principal** :
1. L'utilisateur accède à la page d'inscription
2. Il remplit le formulaire avec ses informations
3. Le système envoie une demande de validation à l'administrateur
4. L'administrateur valide le compte
5. L'utilisateur reçoit un email de confirmation
**Post-conditions** : Le compte est créé mais inactif en attente de validation

#### 1.2 Connexion
**Acteur** : Utilisateur enregistré  
**Description** : Un utilisateur se connecte à son compte.  
**Scénario principal** :
1. L'utilisateur accède à la page de connexion
2. Il entre son email et son mot de passe
3. Le système vérifie les identifiants
4. L'utilisateur est redirigé vers son tableau de bord
**Extensions** :
- 3a. Identifiants incorrects → Message d'erreur
- 3b. Compte non validé → Message d'information

### 2. Gestion des Dossiers Patients
#### 2.1 Création d'un Dossier Patient
**Acteur** : Médecin  
**Description** : Création d'un nouveau dossier patient.  
**Scénario principal** :
1. Le médecin accède à la liste des patients
2. Il clique sur "Nouveau patient"
3. Il remplit les informations du patient
4. Le système enregistre le dossier
**Règles métier** :
- Numéro d'identification unique généré automatiquement
- Validation des champs obligatoires

### 3. Téléradiologie
#### 3.1 Téléversement d'Images DICOM
**Acteur** : Médecin  
**Description** : Téléversement d'images médicales.  
**Scénario principal** :
1. Le médecin sélectionne un patient
2. Il clique sur "Ajouter une imagerie"
3. Il sélectionne le fichier DICOM
4. Le système traite et stocke l'image
5. L'image est associée au dossier du patient

## Maquettes et Parcours Utilisateur

### 1. Page de Connexion
```
+----------------------------------+
|            MEDLINK              |
|  Email: [               ]       |
|  Mot de passe: [        ]       |
|  [ Se connecter ] [ S'inscrire ] |
|  Mot de passe oublié ?          |
+----------------------------------+
```

### 2. Tableau de Bord Médecin
```
+----------------------------------+
| Tableau de Bord - Dr. Dupont    |
+------------------+---------------+
| Rendez-vous     |  Patients     |
| [Liste RDV]     |  [Recherche]  |
|                 |  [Nouveau]    |
+------------------+---------------+
| Alertes         |  Statistiques |
| - 2 examens     |  - 10 patients|
|   en attente    |  - 5 RDV auj. |
+------------------+---------------+
```

## Règles Métiers

### 1. Gestion des Accès
- Seuls les médecins peuvent créer des dossiers patients
- Les radiologues ont un accès complet aux fonctionnalités d'imagerie
- Les administrateurs peuvent gérer les utilisateurs et les paramètres système

### 2. Validation des Données
- Numéro de sécurité sociale : format français valide
- Email : doit contenir @ et un domaine valide
- Téléphone : format international

### 3. Sécurité
- Mots de passe : 12 caractères minimum, majuscules, minuscules, chiffres
- Verrouillage du compte après 5 tentatives échouées
- Journalisation des accès sensibles

## Glossaire

### Termes Techniques
- **DICOM** : Standard pour les images médicales
- **PACS** : Système d'archivage et de communication d'images
- **HL7** : Standard d'échange de données de santé
- **FHIR** : Standard d'échange de données de santé moderne

### Termes Métier
- **CIS** : Code Identification de la Structure
- **RPPS** : Répertoire Partagé des Professionnels de Santé
- **NIR** : Numéro d'Inscription au Répertoire (Sécurité Sociale)

## Annexes

### 1. Codes d'Erreur
| Code | Description | Action Recommandée |
|------|-------------|-------------------|
| 400 | Requête invalide | Vérifier les données envoyées |
| 401 | Non autorisé | Vérifier les identifiants |
| 403 | Accès refusé | Vérifier les permissions |
| 404 | Ressource non trouvée | Vérifier l'URL |
| 500 | Erreur serveur | Contacter l'administrateur |

### 2. Références
- [Documentation Orthanc](https://book.orthanc-server.com/)
- [Guide HL7 FHIR](https://www.hl7.org/fhir/)
- [RGPD et santé](https://www.cnil.fr/)

### 3. Contacts Support
- Support technique : support@medlink.example.com
- Assistance 24/7 disponible pour les établissements de santé
