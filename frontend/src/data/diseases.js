export const diseasesData = {
  1: {
    id: 1,
    name: 'COVID-19',
    category: 'Maladie infectieuse',
    description: 'Le COVID-19 est une maladie infectieuse causée par le coronavirus SARS-CoV-2. Elle peut provoquer des symptômes respiratoires et, dans les cas graves, une pneumonie.',
    symptoms: [
      'Fièvre',
      'Toux sèche',
      'Fatigue',
      'Perte du goût et de l\'odorat',
      'Difficultés respiratoires',
      'Douleurs musculaires',
      'Maux de gorge',
      'Congestion nasale'
    ],
    causes: [
      'Infection par le virus SARS-CoV-2',
      'Contact avec une personne infectée',
      'Transmission par gouttelettes respiratoires',
      'Contact avec des surfaces contaminées'
    ],
    treatments: [
      {
        title: 'Traitement symptomatique',
        description: 'Repos, hydratation et médicaments pour soulager les symptômes (paracétamol pour la fièvre, etc.)'
      },
      {
        title: 'Traitement hospitalier',
        description: 'Pour les cas graves : oxygénothérapie, ventilation mécanique, médicaments antiviraux'
      }
    ],
    prevention: [
      'Vaccination',
      'Port du masque',
      'Distanciation sociale',
      'Lavage régulier des mains',
      'Aération des espaces clos'
    ],
    complications: [
      'Pneumonie',
      'Syndrome de détresse respiratoire aiguë',
      'Problèmes cardiaques',
      'Fatigue chronique',
      'Problèmes neurologiques'
    ],
    whenToSeeDoctor: [
      'Difficultés respiratoires',
      'Douleur ou pression persistante dans la poitrine',
      'Confusion ou difficulté à se réveiller',
      'Lèvres ou visage bleutés'
    ],
    resources: [
      {
        title: 'Organisation Mondiale de la Santé',
        description: 'Informations officielles sur le COVID-19',
        url: 'https://www.who.int/fr/emergencies/diseases/novel-coronavirus-2019'
      },
      {
        title: 'Ministère de la Santé',
        description: 'Recommandations nationales',
        url: 'https://solidarites-sante.gouv.fr/'
      }
    ]
  },
  2: {
    id: 2,
    name: 'Diabète',
    category: 'Maladie endocrinienne',
    description: 'Le diabète est une maladie chronique qui affecte la façon dont votre corps traite le glucose (sucre) dans le sang. Il existe deux types principaux : le diabète de type 1 et le diabète de type 2.',
    symptoms: [
      'Soif excessive',
      'Mictions fréquentes',
      'Faim excessive',
      'Perte de poids inexpliquée',
      'Fatigue',
      'Vision floue',
      'Cicatrisation lente des plaies',
      'Infections fréquentes'
    ],
    causes: [
      'Type 1 : Réaction auto-immune détruisant les cellules productrices d\'insuline',
      'Type 2 : Résistance à l\'insuline et production insuffisante d\'insuline',
      'Facteurs génétiques',
      'Mode de vie sédentaire',
      'Alimentation déséquilibrée',
      'Surpoids et obésité'
    ],
    treatments: [
      {
        title: 'Insulinothérapie',
        description: 'Injections d\'insuline pour le diabète de type 1 et parfois pour le type 2'
      },
      {
        title: 'Médicaments antidiabétiques',
        description: 'Médicaments oraux pour améliorer la sensibilité à l\'insuline ou stimuler sa production'
      },
      {
        title: 'Modifications du mode de vie',
        description: 'Alimentation équilibrée, activité physique régulière, maintien d\'un poids santé'
      }
    ],
    prevention: [
      'Maintenir un poids santé',
      'Alimentation équilibrée',
      'Activité physique régulière',
      'Surveillance régulière de la glycémie',
      'Éviter le tabac et l\'alcool excessif'
    ],
    complications: [
      'Maladies cardiovasculaires',
      'Problèmes rénaux',
      'Problèmes oculaires',
      'Lésions nerveuses',
      'Problèmes de cicatrisation'
    ],
    whenToSeeDoctor: [
      'Symptômes de diabète non diagnostiqué',
      'Glycémie très élevée ou très basse',
      'Apparition de complications',
      'Difficulté à contrôler la glycémie'
    ],
    resources: [
      {
        title: 'Association Française des Diabétiques',
        description: 'Informations et soutien pour les personnes diabétiques',
        url: 'https://www.federationdesdiabetiques.org/'
      },
      {
        title: 'Organisation Mondiale de la Santé',
        description: 'Informations sur le diabète',
        url: 'https://www.who.int/fr/news-room/fact-sheets/detail/diabetes'
      }
    ]
  },
  3: {
    id: 3,
    name: 'Hypertension',
    category: 'Maladie cardiovasculaire',
    description: 'L\'hypertension artérielle est une pression anormalement élevée du sang dans les artères. Elle est souvent asymptomatique mais peut causer de graves complications si elle n\'est pas traitée.',
    symptoms: [
      'Souvent asymptomatique',
      'Maux de tête',
      'Vertiges',
      'Saignements de nez',
      'Essoufflement',
      'Douleurs thoraciques'
    ],
    causes: [
      'Âge avancé',
      'Antécédents familiaux',
      'Surpoids et obésité',
      'Sédentarité',
      'Alimentation riche en sel',
      'Consommation excessive d\'alcool',
      'Stress chronique'
    ],
    treatments: [
      {
        title: 'Médicaments antihypertenseurs',
        description: 'Plusieurs classes de médicaments disponibles selon le cas'
      },
      {
        title: 'Modifications du mode de vie',
        description: 'Réduction de la consommation de sel, activité physique, alimentation équilibrée'
      }
    ],
    prevention: [
      'Alimentation pauvre en sel',
      'Activité physique régulière',
      'Maintien d\'un poids santé',
      'Limitation de l\'alcool',
      'Gestion du stress'
    ],
    complications: [
      'Maladies cardiaques',
      'Accidents vasculaires cérébraux',
      'Insuffisance rénale',
      'Problèmes oculaires',
      'Démence vasculaire'
    ],
    whenToSeeDoctor: [
      'Pression artérielle élevée lors de mesures régulières',
      'Symptômes d\'hypertension',
      'Antécédents familiaux d\'hypertension',
      'Facteurs de risque multiples'
    ],
    resources: [
      {
        title: 'Fédération Française de Cardiologie',
        description: 'Informations sur l\'hypertension artérielle',
        url: 'https://www.fedecardio.org/'
      },
      {
        title: 'Société Française d\'Hypertension Artérielle',
        description: 'Ressources pour les professionnels et les patients',
        url: 'https://www.sfhta.eu/'
      }
    ]
  },
  4: {
    id: 4,
    name: 'Asthme',
    category: 'Maladie respiratoire',
    description: 'L\'asthme est une maladie inflammatoire chronique des voies respiratoires qui provoque des difficultés respiratoires récurrentes.',
    symptoms: [
      'Essoufflement',
      'Sifflements respiratoires',
      'Toux sèche',
      'Oppression thoracique',
      'Difficulté à respirer pendant l\'effort',
      'Crises nocturnes'
    ],
    causes: [
      'Facteurs génétiques',
      'Allergies',
      'Pollution atmosphérique',
      'Infections respiratoires',
      'Exercice physique',
      'Stress émotionnel'
    ],
    treatments: [
      {
        title: 'Bronchodilatateurs',
        description: 'Médicaments pour soulager rapidement les symptômes'
      },
      {
        title: 'Corticoïdes inhalés',
        description: 'Traitement de fond pour réduire l\'inflammation'
      },
      {
        title: 'Éviction des déclencheurs',
        description: 'Identifier et éviter les facteurs déclenchant les crises'
      }
    ],
    prevention: [
      'Éviter les allergènes connus',
      'Maintenir un environnement propre',
      'Suivre le traitement prescrit',
      'Avoir un plan d\'action en cas de crise',
      'Vaccination contre la grippe'
    ],
    complications: [
      'Crises d\'asthme sévères',
      'Fatigue chronique',
      'Problèmes de sommeil',
      'Limitation des activités physiques',
      'Anxiété et dépression'
    ],
    whenToSeeDoctor: [
      'Premiers symptômes d\'asthme',
      'Aggravation des symptômes',
      'Crises fréquentes',
      'Difficulté à contrôler l\'asthme'
    ],
    resources: [
      {
        title: 'Association Asthme & Allergies',
        description: 'Informations et soutien pour les personnes asthmatiques',
        url: 'https://asthme-allergies.org/'
      },
      {
        title: 'Fondation du Souffle',
        description: 'Ressources sur les maladies respiratoires',
        url: 'https://www.lesouffle.org/'
      }
    ]
  },
  5: {
    id: 5,
    name: 'Maladie de Parkinson',
    category: 'Maladie neurologique',
    description: 'La maladie de Parkinson est un trouble dégénératif du système nerveux central qui affecte principalement les mouvements.',
    symptoms: [
      'Tremblements au repos',
      'Rigidité musculaire',
      'Lenteur des mouvements',
      'Troubles de l\'équilibre',
      'Problèmes de posture',
      'Troubles de la marche'
    ],
    causes: [
      'Dégénérescence des neurones producteurs de dopamine',
      'Facteurs génétiques',
      'Exposition à certaines toxines',
      'Âge avancé',
      'Facteurs environnementaux'
    ],
    treatments: [
      {
        title: 'Lévodopa',
        description: 'Médicament principal pour compenser le manque de dopamine'
      },
      {
        title: 'Thérapie physique',
        description: 'Exercices pour maintenir la mobilité et l\'équilibre'
      },
      {
        title: 'Stimulation cérébrale profonde',
        description: 'Pour les cas avancés ne répondant pas aux médicaments'
      }
    ],
    prevention: [
      'Activité physique régulière',
      'Alimentation équilibrée',
      'Protection contre les toxines',
      'Suivi médical régulier'
    ],
    complications: [
      'Dépression',
      'Troubles du sommeil',
      'Problèmes de déglutition',
      'Démence',
      'Chutes fréquentes'
    ],
    whenToSeeDoctor: [
      'Apparition de tremblements',
      'Ralentissement des mouvements',
      'Problèmes d\'équilibre',
      'Changements dans l\'écriture'
    ],
    resources: [
      {
        title: 'France Parkinson',
        description: 'Association de patients et d\'aidants',
        url: 'https://www.franceparkinson.fr/'
      },
      {
        title: 'Institut du Cerveau',
        description: 'Recherche et information sur les maladies neurologiques',
        url: 'https://institutducerveau-icm.org/'
      }
    ]
  },
  6: {
    id: 6,
    name: 'Maladie de Crohn',
    category: 'Maladie digestive',
    description: 'La maladie de Crohn est une maladie inflammatoire chronique du tube digestif qui peut affecter n\'importe quelle partie du système digestif.',
    symptoms: [
      'Douleurs abdominales',
      'Diarrhée chronique',
      'Perte de poids',
      'Fatigue',
      'Fièvre',
      'Saignements rectaux'
    ],
    causes: [
      'Facteurs génétiques',
      'Dysfonctionnement du système immunitaire',
      'Facteurs environnementaux',
      'Tabagisme',
      'Alimentation'
    ],
    treatments: [
      {
        title: 'Anti-inflammatoires',
        description: 'Pour réduire l\'inflammation'
      },
      {
        title: 'Immunosuppresseurs',
        description: 'Pour moduler la réponse immunitaire'
      },
      {
        title: 'Chirurgie',
        description: 'Pour les cas sévères ou les complications'
      }
    ],
    prevention: [
      'Arrêt du tabac',
      'Alimentation adaptée',
      'Gestion du stress',
      'Suivi médical régulier'
    ],
    complications: [
      'Sténoses intestinales',
      'Fistules',
      'Abcès',
      'Malnutrition',
      'Cancer colorectal'
    ],
    whenToSeeDoctor: [
      'Douleurs abdominales persistantes',
      'Diarrhée chronique',
      'Perte de poids inexpliquée',
      'Saignements rectaux'
    ],
    resources: [
      {
        title: 'Association François Aupetit',
        description: 'Association de patients atteints de MICI',
        url: 'https://www.afa.asso.fr/'
      },
      {
        title: 'Société Nationale Française de Gastro-Entérologie',
        description: 'Informations pour les professionnels et les patients',
        url: 'https://www.snfge.org/'
      }
    ]
  },
  7: {
    id: 7,
    name: 'Lupus',
    category: 'Maladie auto-immune',
    description: 'Le lupus est une maladie auto-immune chronique qui peut affecter plusieurs organes et systèmes du corps.',
    symptoms: [
      'Éruption cutanée en forme de papillon',
      'Douleurs articulaires',
      'Fatigue extrême',
      'Fièvre',
      'Sensibilité au soleil',
      'Problèmes rénaux'
    ],
    causes: [
      'Facteurs génétiques',
      'Facteurs hormonaux',
      'Facteurs environnementaux',
      'Certains médicaments',
      'Infections'
    ],
    treatments: [
      {
        title: 'Anti-inflammatoires',
        description: 'Pour soulager les douleurs et l\'inflammation'
      },
      {
        title: 'Antipaludéens',
        description: 'Pour traiter les symptômes cutanés et articulaires'
      },
      {
        title: 'Immunosuppresseurs',
        description: 'Pour les cas sévères'
      }
    ],
    prevention: [
      'Protection solaire',
      'Éviter le stress',
      'Repos suffisant',
      'Suivi médical régulier'
    ],
    complications: [
      'Problèmes rénaux',
      'Problèmes cardiaques',
      'Problèmes pulmonaires',
      'Problèmes neurologiques',
      'Problèmes de grossesse'
    ],
    whenToSeeDoctor: [
      'Apparition d\'une éruption cutanée',
      'Douleurs articulaires persistantes',
      'Fatigue extrême',
      'Fièvre inexpliquée'
    ],
    resources: [
      {
        title: 'Association Lupus France',
        description: 'Soutien et information pour les patients',
        url: 'https://www.lupusfrance.com/'
      },
      {
        title: 'Fondation Arthritis',
        description: 'Recherche sur les maladies auto-immunes',
        url: 'https://www.arthritis.org/'
      }
    ]
  },
  8: {
    id: 8,
    name: 'Cancer du sein',
    category: 'Cancer',
    description: 'Le cancer du sein est une tumeur maligne qui se développe dans les tissus du sein. C\'est le cancer le plus fréquent chez la femme.',
    symptoms: [
      'Masse dans le sein',
      'Modification de la forme du sein',
      'Écoulement du mamelon',
      'Modification de la peau',
      'Ganglions axillaires',
      'Douleur mammaire'
    ],
    causes: [
      'Facteurs génétiques',
      'Âge',
      'Antécédents familiaux',
      'Facteurs hormonaux',
      'Mode de vie',
      'Exposition aux radiations'
    ],
    treatments: [
      {
        title: 'Chirurgie',
        description: 'Ablation de la tumeur ou du sein'
      },
      {
        title: 'Radiothérapie',
        description: 'Utilisation de rayons pour détruire les cellules cancéreuses'
      },
      {
        title: 'Chimiothérapie',
        description: 'Médicaments pour détruire les cellules cancéreuses'
      },
      {
        title: 'Hormonothérapie',
        description: 'Pour les cancers hormonodépendants'
      }
    ],
    prevention: [
      'Auto-examen régulier',
      'Mammographie de dépistage',
      'Mode de vie sain',
      'Allaitement',
      'Limitation de l\'alcool'
    ],
    complications: [
      'Métastases',
      'Effets secondaires des traitements',
      'Problèmes psychologiques',
      'Lymphœdème',
      'Problèmes de fertilité'
    ],
    whenToSeeDoctor: [
      'Découverte d\'une masse',
      'Modification de la forme du sein',
      'Écoulement du mamelon',
      'Douleur persistante'
    ],
    resources: [
      {
        title: 'Institut Curie',
        description: 'Centre de recherche et de traitement du cancer',
        url: 'https://curie.fr/'
      },
      {
        title: 'Ligue contre le Cancer',
        description: 'Information et soutien aux patients',
        url: 'https://www.ligue-cancer.net/'
      }
    ]
  },
  9: {
    id: 9,
    name: 'Grippe',
    category: 'Maladie infectieuse',
    description: 'La grippe est une infection virale respiratoire aiguë causée par le virus influenza. Elle peut être saisonnière ou pandémique.',
    symptoms: [
      'Fièvre élevée',
      'Courbatures',
      'Fatigue intense',
      'Toux sèche',
      'Maux de gorge',
      'Congestion nasale'
    ],
    causes: [
      'Virus influenza',
      'Transmission par gouttelettes',
      'Contact avec des surfaces contaminées',
      'Contact avec une personne infectée'
    ],
    treatments: [
      {
        title: 'Traitement symptomatique',
        description: 'Repos, hydratation, paracétamol pour la fièvre'
      },
      {
        title: 'Antiviraux',
        description: 'Dans certains cas, sur prescription médicale'
      }
    ],
    prevention: [
      'Vaccination annuelle',
      'Lavage régulier des mains',
      'Port du masque en période épidémique',
      'Éviter les contacts avec les personnes malades'
    ],
    complications: [
      'Pneumonie',
      'Bronchite',
      'Sinusite',
      'Otite',
      'Aggravation des maladies chroniques'
    ],
    whenToSeeDoctor: [
      'Fièvre très élevée',
      'Difficultés respiratoires',
      'Douleurs thoraciques',
      'Aggravation des symptômes'
    ],
    resources: [
      {
        title: 'Santé Publique France',
        description: 'Surveillance et information sur la grippe',
        url: 'https://www.santepubliquefrance.fr/'
      },
      {
        title: 'Organisation Mondiale de la Santé',
        description: 'Informations sur la grippe',
        url: 'https://www.who.int/fr/news-room/fact-sheets/detail/influenza-(seasonal)'
      }
    ]
  },
  10: {
    id: 10,
    name: 'Tremblement essentiel',
    category: 'Maladie neurologique',
    description: 'Le tremblement essentiel est un trouble neurologique caractérisé par des tremblements involontaires et rythmiques, généralement des mains et de la tête. C\'est le trouble du mouvement le plus courant.',
    symptoms: [
      'Tremblements des mains lors des mouvements',
      'Tremblements de la tête (mouvement de "oui-non")',
      'Tremblements de la voix',
      'Tremblements des jambes',
      'Aggravation des tremblements avec le stress',
      'Difficulté à effectuer des tâches précises'
    ],
    causes: [
      'Facteurs génétiques (dans 50% des cas)',
      'Altérations dans certaines zones du cerveau',
      'Dysfonctionnement du cervelet',
      'Âge (plus fréquent après 40 ans)',
      'Facteurs environnementaux'
    ],
    treatments: [
      {
        title: 'Médicaments bêta-bloquants',
        description: 'Propranolol et autres bêta-bloquants pour réduire les tremblements'
      },
      {
        title: 'Antiépileptiques',
        description: 'Primidone et autres médicaments antiépileptiques'
      },
      {
        title: 'Toxine botulique',
        description: 'Injections pour les tremblements de la tête et de la voix'
      },
      {
        title: 'Stimulation cérébrale profonde',
        description: 'Pour les cas sévères ne répondant pas aux médicaments'
      }
    ],
    prevention: [
      'Éviter les facteurs aggravants (caféine, stress)',
      'Techniques de relaxation',
      'Exercices de contrôle moteur',
      'Suivi médical régulier'
    ],
    complications: [
      'Difficultés dans les activités quotidiennes',
      'Problèmes d\'écriture',
      'Difficultés à manger et boire',
      'Anxiété sociale',
      'Dépression'
    ],
    whenToSeeDoctor: [
      'Apparition de tremblements persistants',
      'Aggravation des symptômes',
      'Impact sur les activités quotidiennes',
      'Apparition de nouveaux symptômes'
    ],
    resources: [
      {
        title: 'Association des Personnes Concernées par le Tremblement Essentiel',
        description: 'Soutien et information pour les patients',
        url: 'https://www.aptes.org/'
      },
      {
        title: 'Fondation pour la Recherche Médicale',
        description: 'Informations sur les recherches en cours',
        url: 'https://www.frm.org/'
      }
    ]
  }
} 