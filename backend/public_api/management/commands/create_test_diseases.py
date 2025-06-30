from django.core.management.base import BaseCommand
from public_api.models import DiseaseCategory, Disease
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crée des exemples de catégories et de maladies pour les tests'

    def handle(self, *args, **options):
        self.stdout.write("Création des données de test...")
        
        # Création des catégories
        categories = [
            {'name': 'Cardiologie', 'description': 'Maladies du cœur et des vaisseaux sanguins'},
            {'name': 'Neurologie', 'description': 'Maladies du système nerveux'},
            {'name': 'Pneumologie', 'description': 'Maladies respiratoires'},
            {'name': 'Gastro-entérologie', 'description': 'Maladies du système digestif'},
            {'name': 'Dermatologie', 'description': 'Maladies de la peau'},
            {'name': 'Endocrinologie', 'description': 'Maladies des glandes endocrines et du métabolisme'},
            {'name': 'Psychiatrie', 'description': 'Troubles mentaux et du comportement'}
        ]
        
        created_categories = {}
        for cat_data in categories:
            category, created = DiseaseCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            created_categories[cat_data['name'].lower()] = category
            self.stdout.write(f"Catégorie créée : {category.name}")
        
        # Exemples de maladies
        diseases = [
            # Maladies cardiologiques
            {
                'name': 'Hypertension artérielle',
                'category': 'Cardiologie',
                'short_description': 'Pression artérielle trop élevée de manière chronique',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Maux de tête\nÉtourdissements\nSaignements de nez',
                'description': "L'hypertension artérielle est une pathologie cardiovasculaire définie par une pression artérielle trop élevée. Elle peut entraîner des complications graves si elle n'est pas traitée.",
                'causes': 'Facteurs génétiques\nObésité\nSédentarité\nConsommation excessive de sel',
                'treatment': 'Médicaments antihypertenseurs\nRégime alimentaire adapté\nActivié physique régulière',
                'prevention': 'Réduire la consommation de sel\nMaintenir un poids santé\nÉviter le tabac et l\'alcool',
            },
            {
                'name': 'Migraine',
                'category': 'Neurologie',
                'short_description': 'Maux de tête intenses et récurrents',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Douleur pulsatile d\'un côté de la tête\nNausées\nSensibilité à la lumière et au bruit',
                'description': 'La migraine est un type de mal de tête qui peut causer une douleur intense ou une sensation de battement, généralement d\'un seul côté de la tête.',
                'causes': 'Facteurs génétiques\nChangements hormonaux\nCertains aliments\nStress',
                'treatment': 'Antalgiques\nTriptans\nRepos dans un endroit calme et sombre',
                'prevention': 'Identifier et éviter les déclencheurs\nGérer le stress\nDormir suffisamment',
            },
            {
                'name': 'Asthme',
                'category': 'Pneumologie',
                'short_description': 'Maladie inflammatoire chronique des voies respiratoires',
                'severity': 'M',
                'is_emergency': True,
                'main_symptoms': 'Essoufflement\nSifflements respiratoires\nToux sèche\nOppression thoracique',
                'description': "L'asthme est une maladie chronique des voies respiratoires qui provoque leur inflammation et leur rétrécissement, rendant la respiration difficile.",
                'causes': 'Allergies\nFacteurs environnementaux\nPrédisposition génétique',
                'treatment': 'Corticoïdes inhalés\nBronchodilatateurs\nÉviction des facteurs déclenchants',
                'prevention': 'Éviter les allergènes connus\nNe pas fumer\nVaccination contre la grippe',
            },
            {
                'name': 'Reflux gastro-œsophagien (RGO)',
                'category': 'Gastro-entérologie',
                'short_description': 'Remontées acides de l\'estomac vers l\'œsophage',
                'severity': 'L',
                'is_emergency': False,
                'main_symptoms': 'Brûlures d\'estomac\nRégurgitations acides\nDouleur thoracique',
                'description': 'Le RGO est une affection digestive dans laquelle les acides de l\'estomac remontent dans l\'œsophage, provoquant une irritation.',
                'causes': 'Dysfonctionnement du sphincter œsophagien inférieur\nHernie hiatale\nObésité',
                'treatment': 'Anti-acides\nInhibiteurs de la pompe à protons\nModifications du mode de vie',
                'prevention': 'Éviter les repas copieux\nNe pas s\'allonger après les repas\nSurélever la tête du lit',
            },
            {
                'name': 'Eczéma',
                'category': 'Dermatologie',
                'short_description': 'Affection cutanée inflammatoire chronique',
                'severity': 'L',
                'is_emergency': False,
                'main_symptoms': 'Démangeaisons intenses\nRougeurs\nPeau sèche et squameuse',
                'description': "L'eczéma est une affection cutanée non contagieuse caractérisée par des démangeaisons, des rougeurs et des lésions cutanées.",
                'causes': 'Facteurs génétiques\nAllergènes environnementaux\nStress',
                'treatment': 'Crèmes hydratantes\nCorticoïdes topiques\nAntihistaminiques',
                'prevention': 'Hydrater régulièrement la peau\nÉviter les savons agressifs\nGérer le stress',
            },
            {
                'name': 'Tremblement essentiel',
                'category': 'Neurologie',
                'short_description': 'Trouble du mouvement caractérisé par des tremblements incontrôlables',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Tremblements rythmiques des mains et des bras\nTremblements de la tête\nVoix tremblotante\nAggravation avec le stress et la fatigue',
                'description': 'Le tremblement essentiel est un trouble neurologique fréquent qui provoque des secousses rythmiques incontrôlables. Contrairement à la maladie de Parkinson, il survient généralement lors de mouvements volontaires et s\'aggrave avec l\'âge.',
                'causes': 'Facteurs génétiques (dans 50% des cas)\nAltérations dans certaines zones cérébrales\nFacteurs environnementaux non identifiés',
                'treatment': 'Bêta-bloquants (propranolol)\nAntiépileptiques (primidone)\nThérapie par ultrasons focalisés\nStimulation cérébrale profonde pour les cas sévères',
                'prevention': 'Éviter la caféine et autres stimulants\nGérer le stress (relaxation, méditation)\nLimiter la consommation d\'alcool',
                'prognosis': 'Le tremblement essentiel est une affection chronique qui peut s\'aggraver avec le temps mais ne met généralement pas en jeu le pronostic vital. La qualité de vie peut être affectée dans les cas sévères.'
            },
            {
                'name': 'Diabète de type 2',
                'category': 'Endocrinologie',
                'short_description': 'Trouble métabolique caractérisé par une hyperglycémie chronique nécessitant une prise en charge à vie',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Soif intense (polydipsie)\nMictions fréquentes (polyurie)\nFatigue inhabituelle\nVision trouble\nCicatrisation lente des plaies\nInfections fréquentes\nPicotements ou engourdissement des extrémités',
                'description': 'Le diabète de type 2 est une maladie métabolique chronique caractérisée par une résistance à l\'insuline et une carence relative en insuline. Il représente environ 90% des cas de diabète. Cette pathologie évolue silencieusement pendant des années avant d\'être diagnostiquée. Elle peut entraîner des complications microvasculaires (rétinopathie, néphropathie, neuropathie) et macrovasculaires (maladies cardiovasculaires). Le diagnostic repose sur la mesure de la glycémie à jeun, l\'hémoglobine glyquée (HbA1c) ou une hyperglycémie provoquée par voie orale.',
                'causes': 'Surpoids et obésité (notamment graisse abdominale)\nSédentarité et manque d\'activité physique\nAntécédents familiaux de diabète de type 2\nÂge supérieur à 45 ans\nHypertension artérielle\nDyslipidémie\nSyndrome des ovaires polykystiques\nAntécédent de diabète gestationnel',
                'treatment': 'Modifications du mode de vie (alimentation équilibrée pauvre en sucres rapides, riche en fibres)\nActivité physique régulière (150 min/semaine d\'activité modérée)\nMédicaments antidiabétiques oraux (metformine, sulfamides, glinides, glitazones, inhibiteurs de la DPP-4, inhibiteurs des SGLT2)\nTraitements injectables (analogues du GLP-1, insuline basale ou prandiale si échec des autres traitements)\nSurveillance glycémique régulière et éducation thérapeutique\nPrise en charge des facteurs de risque cardiovasculaires associés',
                'prevention': 'Maintenir un indice de masse corporelle (IMC) entre 18,5 et 25 kg/m²\nPratiquer au moins 30 minutes d\'activité physique modérée par jour\nAdopter une alimentation équilibrée riche en fibres (fruits, légumes, céréales complètes)\nLimiter la consommation de sucres rapides et de graisses saturées\nÉviter le tabac et limiter la consommation d\'alcool\nSurveiller régulièrement sa glycémie après 45 ans ou en cas de facteurs de risque\nDépistage systématique chez les personnes à risque',
                'prognosis': 'Avec une prise en charge précoce et adaptée, les personnes atteintes de diabète de type 2 peuvent mener une vie quasi-normale. Un contrôle glycémique strict (HbA1c < 7%) réduit considérablement le risque de complications. Cependant, l\'évolution naturelle de la maladie conduit souvent à une aggravation progressive de l\'insulinorésistance et de la défaillance des cellules bêta pancréatiques, nécessitant une escalade thérapeutique. Les complications à long terme incluent la rétinopathie diabétique (première cause de cécité avant 65 ans), la néphropathie (première cause de dialyse), la neuropathie, les maladies cardiovasculaires (infarctus, AVC) et les atteintes artérielles périphériques. L\'espérance de vie est réduite en moyenne de 5 à 10 ans par rapport à la population non diabétique, principalement en raison des complications cardiovasculaires.'
            },
            {
                'name': 'Dépression majeure récurrente',
                'category': 'Psychiatrie',
                'short_description': 'Trouble de l\'humeur sévère caractérisé par des épisodes dépressifs récurrents avec impact fonctionnel majeur',
                'severity': 'S',
                'is_emergency': True,
                'main_symptoms': 'Humeur dépressive quasi-permanente\nPerte d\'intérêt ou de plaisir pour presque toutes les activités (anhédonie)\nTroubles du sommeil (insomnie ou hypersomnie)\nFatigue ou perte d\'énergie\nSentiment excessif de culpabilité ou de dévalorisation\nDifficultés de concentration et indécision\nRalentissement ou agitation psychomotrice\nPensées de mort récurrentes ou idées suicidaires\nPerte ou prise de poids significative\nDiminution de la libido',
                'description': 'La dépression majeure est un trouble mental sévère caractérisé par la survenue d\'épisodes dépressifs majeurs récurrents. Elle se distingue des simples variations d\'humeur par son intensité, sa durée (au moins 2 semaines) et son retentissement sur le fonctionnement global de l\'individu. Le diagnostic repose sur des critères cliniques précis (DSM-5 ou CIM-11) nécessitant la présence d\'au moins 5 symptômes caractéristiques pendant une période minimale de 2 semaines. La dépression majeure est une cause majeure d\'incapacité dans le monde et représente un facteur de risque important de suicide. Elle peut survenir à tout âge mais débute le plus souvent entre 20 et 40 ans, avec une prévalence deux fois plus élevée chez les femmes.',
                'causes': 'Facteurs biologiques : déséquilibres des neurotransmetteurs (sérotonine, noradrénaline, dopamine), anomalies structurelles cérébrales, facteurs génétiques (héritabilité estimée à 40%)\nFacteurs psychologiques : traumatismes précoces, personnalité à risque (névrosisme élevé, perfectionnisme), schémas cognitifs dysfonctionnels\nFacteurs environnementaux : événements de vie stressants (deuil, séparation, perte d\'emploi), isolement social, conditions socio-économiques défavorables\nFacteurs médicaux : maladies chroniques, douleurs chroniques, troubles hormonaux, certains médicaments (corticoïdes, interféron, etc.)',
                'treatment': 'Psychothérapies : TCC (thérapie cognitive et comportementale), thérapie interpersonnelle, thérapie d\'acceptation et d\'engagement (ACT), psychothérapie psychodynamique\nTraitements médicamenteux : antidépresseurs (ISRS, IRSNA, tricycliques, IMAO) pendant au moins 6 à 12 mois après rémission\nTraitements biologiques : sismothérapie (électroconvulsivothérapie) pour les dépressions résistantes ou sévères, stimulation magnétique transcrânienne (rTMS), stimulation du nerf vague\nHospitalisation en cas de risque suicidaire élevé ou d\'incapacité à s\'alimenter\nMesures non médicamenteuses : luminothérapie (pour la dépression saisonnière), activité physique régulière, techniques de relaxation, rétablissement du rythme veille-sommeil\nApproches complémentaires : méditation pleine conscience, acupuncture, oméga-3 (à haute dose)',
                'prevention': 'Dépistage précoce des symptômes dépressifs, notamment dans les populations à risque\nDéveloppement des compétences psychosociales et de la résilience\nMaintien d\'un réseau social de qualité\nGestion du stress et des émotions\nHygiène de vie équilibrée (sommeil, alimentation, activité physique)\nPrévention de la rechute après un premier épisode dépressif (traitement d\'entretien, psychothérapie de prévention des rechutes)\nÉducation du patient et de son entourage à la reconnaissance des signes précoces de rechute\nPrise en charge des comorbidités (troubles anxieux, addictions, maladies somatiques)',
                'prognosis': 'Sous traitement adapté, environ 70% des patients répondent favorablement avec une rémission complète des symptômes. Cependant, le risque de récidive est élevé : 50% après un premier épisode, 70% après deux épisodes, et 90% après trois épisodes. Les facteurs de mauvais pronostic incluent : début précoce, antécédents familiaux, comorbidités psychiatriques, personnalité pathologique, soutien social faible, événements de vie stressants persistants. La dépression majeure est associée à une surmortalité importante, principalement par suicide (15% des cas graves non traités) et par comorbidités somatiques (maladies cardiovasculaires, diabète). Un suivi prolongé (au moins 2 ans après la rémission) est recommandé pour prévenir les rechutes.'
            },
            {
                'name': 'Asthme sévère non contrôlé',
                'category': 'Pneumologie',
                'short_description': 'Forme grave et réfractaire d\'asthme persistant malgré un traitement optimal à fortes doses',
                'severity': 'S',
                'is_emergency': True,
                'main_symptoms': 'Essoufflement sévère au moindre effort ou au repos\nSifflements respiratoires constants et audibles\nToux nocturne récurrente perturbant le sommeil\nLimitation sévère des activités quotidiennes\nSensation d\'oppression thoracique invalidante\nNécessité d\'utiliser quotidiennement des bronchodilatateurs de courte durée d\'action\nExacerbations fréquentes nécessitant des cures de corticoïdes oraux',
                'description': 'L\'asthme sévère est une forme d\'asthme qui ne répond pas bien aux traitements standards. Il peut entraîner des exacerbations fréquentes et potentiellement mortelles.',
                'causes': 'Inflammation chronique des voies respiratoires\nFacteurs génétiques\nExposition à des déclencheurs environnementaux\nInfections respiratoires',
                'treatment': 'Corticoïdes inhalés à fortes doses\nBiothérapies ciblées (anti-IgE, anti-IL5)\nBronchodilatateurs à longue durée d\'action\nOxygénothérapie si nécessaire',
                'prevention': 'Éviter les allergènes connus\nVaccination contre la grippe et la pneumonie\nPlan d\'action contre l\'asthme personnalisé',
                'prognosis': 'L\'asthme sévère nécessite une prise en charge spécialisée. Avec un traitement approprié, la qualité de vie peut être améliorée, mais la maladie reste chronique.'
            }
        ]
        
        for disease_data in diseases:
            category_name = disease_data.pop('category').lower()
            category = created_categories.get(category_name)
            
            disease, created = Disease.objects.get_or_create(
                name=disease_data['name'],
                defaults={
                    'category': category,
                    'scientific_name': disease_data.get('scientific_name', ''),
                    'short_description': disease_data['short_description'],
                    'description': disease_data['description'],
                    'main_symptoms': disease_data['main_symptoms'],
                    'causes': disease_data.get('causes', ''),
                    'treatment': disease_data.get('treatment', ''),
                    'prevention': disease_data.get('prevention', ''),
                    'severity': disease_data['severity'],
                    'is_emergency': disease_data['is_emergency'],
                    'is_published': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Maladie créée : {disease.name}"))
            else:
                self.stdout.write(f"La maladie {disease.name} existe déjà")
        
        self.stdout.write(self.style.SUCCESS('Données de test créées avec succès!'))
