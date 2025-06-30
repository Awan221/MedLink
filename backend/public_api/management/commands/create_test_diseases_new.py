from django.core.management.base import BaseCommand
from django.utils.text import slugify
from public_api.models import DiseaseCategory, Disease, DiseaseResource

class Command(BaseCommand):
    help = 'Crée des exemples détaillés de catégories et de maladies pour les tests'

    def handle(self, *args, **options):
        self.stdout.write("Création des données de test détaillées...")
        
        # Création des catégories
        categories = [
            # Catégories existantes
            {'name': 'Cardiologie', 'description': 'Maladies du cœur et des vaisseaux sanguins'},
            {'name': 'Neurologie', 'description': 'Maladies du système nerveux'},
            {'name': 'Pneumologie', 'description': 'Maladies respiratoires'},
            {'name': 'Gastro-entérologie', 'description': 'Maladies du système digestif'},
            {'name': 'Dermatologie', 'description': 'Maladies de la peau'},
            
            # Nouvelles catégories
            {'name': 'Endocrinologie', 'description': 'Maladies des glandes endocrines et du métabolisme'},
            {'name': 'Rhumatologie', 'description': 'Maladies des articulations et des tissus conjonctifs'},
            {'name': 'Néphrologie', 'description': 'Maladies des reins'},
            {'name': 'Hématologie', 'description': 'Maladies du sang et des organes hématopoïétiques'},
            {'name': 'Oncologie', 'description': 'Cancers et tumeurs'},
            {'name': 'Infectiologie', 'description': 'Maladies infectieuses'},
            {'name': 'Allergologie', 'description': 'Allergies et hypersensibilités'},
            {'name': 'Psychiatrie', 'description': 'Troubles mentaux et du comportement'},
            {'name': 'Ophtalmologie', 'description': 'Maladies des yeux'},
            {'name': 'ORL', 'description': 'Maladies des oreilles, du nez et de la gorge'},
            {'name': 'Gynécologie', 'description': 'Maladies de l\'appareil génital féminin'},
            {'name': 'Urologie', 'description': 'Maladies de l\'appareil urinaire et génital masculin'}
        ]

        created_categories = {}
        for cat_data in categories:
            category, created = DiseaseCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            created_categories[cat_data['name'].lower()] = category
            self.stdout.write(f"Catégorie créée : {category.name}")

        # Dictionnaire des maladies avec leurs données détaillées
        diseases_data = [
            # 1. Maladies endocriniennes - Maladie de Cushing
            {
                'name': 'Maladie de Cushing',
                'scientific_name': 'Hypercorticisme ACTH-dépendant',
                'category': 'Endocrinologie',
                'prevalence': '1-2 cas par million d\'habitants par an',
                'age_group': 'Pic entre 20 et 50 ans, plus fréquent chez les femmes',
                'risk_factors': 'Adénome hypophysaire, tumeurs sécrétantes d\'ACTH, traitement prolongé par corticoïdes',
                'diagnosis': 'Cortisol libre urinaire sur 24h, test de freinage à la dexaméthasone, IRM hypophysaire',
                'differential_diagnosis': 'Syndrome de Cushing exogène, dépression, obésité, syndrome des ovaires polykystiques',
                'follow_up': 'Surveillance clinique et biologique après traitement, recherche de récidive',
                'references': 'Recommandations ESE 2015, SFEndo 2020',
                'short_description': 'Hypercorticisme lié à une sécrétion excessive d\'ACTH par un adénome hypophysaire',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Prise de poids, visage lunaire, bosse de bison, vergetures pourpres, hypertension',
                'description': (
                    "La maladie de Cushing est une affection endocrinienne rare caractérisée par un excès de production "
                    "de cortisol, secondaire à un adénome hypophysaire sécrétant de l'ACTH. Cette maladie entraîne de "
                    "nombreuses complications métaboliques, cardiovasculaires et osseuses. Le diagnostic est souvent "
                    "retardé en raison de la variabilité des symptômes et de leur progression lente."
                ),
                'causes': (
                    "Adénome hypophysaire sécrétant de l'ACTH (90% des cas)\n"
                    "Hyperplasie des cellules corticotropes\n"
                    "Exceptionnellement, tumeur maligne sécrétant de l'ACTH\n"
                    "Formes familiales rares (Néoplasie Endocrinienne Multiple de type 1)"
                ),
                'treatment': (
                    "Chirurgie d'exérèse de l'adénome hypophysaire par voie trans-sphénoïdale\n"
                    "Radiothérapie en cas d'échec ou de contre-indication chirurgicale\n"
                    "Médicaments inhibiteurs de la stéroïdogenèse (kétoconazole, métopirone)\n"
                    "Traitement des complications (antihypertenseurs, antidiabétiques, ostéoporose)\n"
                    "Substitution hormonale après chirurgie si nécessaire"
                ),
                'prevention': 'Aucune prévention primaire connue',
                'prevention_details': (
                    "- Pas de prévention primaire possible\n"
                    "- Dépistage des formes familiales dans le cadre des NEM1\n"
                    "- Surveillance des patients sous corticoïdes au long cours"
                ),
                'complications': (
                    "Hypertension artérielle sévère\n"
                    "Diabète sucré\n"
                    "Ostéoporose avec fractures pathologiques\n"
                    "Infections à répétition\n"
                    "Troubles psychiatriques (dépression, psychose)\n"
                    "Crise de sevrage en post-opératoire"
                ),
                'when_to_see_doctor': (
                    "Prise de poids rapide avec redistribution des graisses\n"
                    "Apparition de vergetures pourpres sur l'abdomen et les cuisses\n"
                    "Faiblesse musculaire progressive\n"
                    "Aménorrhée ou troubles des règles chez la femme\n"
                    "Hypertension artérielle résistante au traitement"
                ),
                'resources': [
                    {'title': 'Association Surrénales', 'description': 'Association de patients atteints de maladies surrénaliennes', 'url': 'https://www.surrenales.com'},
                    {'title': 'Société Française d\'Endocrinologie', 'description': 'Recommandations professionnelles', 'url': 'https://www.sfendocrino.org'},
                    {'title': 'Orphanet - Maladie de Cushing', 'description': 'Fiche d\'information sur la maladie rare', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=fr&Expert=96253'}
                ]
            },
            
            # 2. Maladies cardiologiques
            {
                'name': 'Hypertension artérielle',
                'scientific_name': 'Hypertensio arterialis',
                'category': 'Cardiologie',
                'prevalence': '30-45% des adultes',
                'age_group': 'Tous âges, plus fréquent après 50 ans',
                'risk_factors': 'Âge, obésité, sédentarité, alimentation riche en sel, tabagisme, alcool, stress',
                'diagnosis': 'Mesure de la pression artérielle à plusieurs reprises, bilan rénal, électrocardiogramme',
                'differential_diagnosis': 'Hypertension secondaire, phéochromocytome, hyperaldostéronisme primaire',
                'follow_up': 'Mesures régulières de la tension, surveillance rénale, évaluation du risque cardiovasculaire',
                'references': 'Recommandations ESC/ESH 2018, HAS 2020',
                'short_description': 'Pression artérielle trop élevée de manière chronique',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Maux de tête\nÉtourdissements\nSaignements de nez\nEssoufflement',
                'description': (
                    "L'hypertension artérielle (HTA) est une pathologie cardiovasculaire définie par une pression artérielle "
                    "trop élevée. Elle est dite 'silencieuse' car souvent asymptomatique sur de nombreuses années. "
                    "Non traitée, elle peut entraîner des complications graves comme les accidents vasculaires cérébraux, "
                    "les infarctus du myocarde, l'insuffisance cardiaque ou rénale."
                ),
                'causes': (
                    "Facteurs génétiques (antécédents familiaux)\n"
                    "Âge (risque accru après 50 ans)\n"
                    "Surpoids et obésité\n"
                    "Sédentarité\n"
                    "Consommation excessive de sel\n"
                    "Tabagisme\n"
                    "Consommation excessive d'alcool\n"
                    "Stress chronique"
                ),
                'treatment': (
                    "Médicaments antihypertenseurs (diurétiques, bêta-bloquants, inhibiteurs calciques, etc.)\n"
                    "Régime alimentaire pauvre en sel (moins de 5g/jour)\n"
                    "Activité physique régulière (30 min/jour minimum)\n"
                    "Perte de poids en cas de surcharge pondérale\n"
                    "Arrêt du tabac\n"
                    "Réduction de la consommation d'alcool"
                ),
                'prevention': "Mesures de prévention de l'hypertension artérielle",
                'prevention_details': (
                    "- Mesurer régulièrement sa tension artérielle, surtout en cas d'antécédents familiaux\n"
                    "- Adopter un régime alimentaire équilibré de type DASH (riche en fruits, légumes, céréales complètes, produits laitiers pauvres en matières grasses)\n"
                    "- Réduire la consommation de sel à moins de 5g par jour (équivalent à une cuillère à café)\n"
                    "- Pratiquer une activité physique régulière (au moins 30 minutes par jour, 5 fois par semaine)\n"
                    "- Maintenir un poids santé (IMC entre 18,5 et 25 kg/m²)\n"
                    "- Limiter la consommation d'alcool (maximum 2 verres standards par jour pour les femmes, 3 pour les hommes)\n"
                    "- Arrêter de fumer et éviter le tabagisme passif\n"
                    "- Gérer le stress par des techniques de relaxation (méditation, cohérence cardiaque, yoga)\n"
                    "- Dormir suffisamment (7 à 8 heures par nuit)"
                ),
                'complications': (
                    "Accident vasculaire cérébral (AVC)\n"
                    "Infarctus du myocarde\n"
                    "Insuffisance cardiaque\n"
                    "Insuffisance rénale chronique\n"
                    "Rétinopathie hypertensive pouvant mener à la cécité\n"
                    "Artériopathie oblitérante des membres inférieurs"
                ),
                'when_to_see_doctor': (
                    "- Premier diagnostic d'hypertension artérielle\n"
                    "- Maux de tête sévères et persistants, surtout s'ils s'accompagnent de vertiges ou de nausées\n"
                    "- Essoufflement inhabituel à l'effort ou au repos\n"
                    "- Saignements de nez fréquents et abondants\n"
                    "- Vision trouble ou apparition de mouches volantes\n"
                    "- Douleur thoracique ou sensation d'oppression\n"
                    "- Pouls irrégulier ou palpitations\n"
                    "- Difficultés d'élocution ou faiblesse d'un côté du corps (signe d'AVC)\n"
                    "- Valeurs tensionnelles très élevées (supérieures à 180/110 mmHg)"
                ),
                'useful_links': (
                    "Fédération Française de Cardiologie - https://fedecardio.org\n"
                    "Société Française d'Hypertension Artérielle - http://www.sfhta.eu\n"
                    "Ameli.fr - Hypertension artérielle - https://www.ameli.fr/assure/sante/themes/hypertension-arterelle-hta\n"
                    "Recommandations ESC/ESH 2018 - https://academic.oup.com/eurheartj/article/39/33/3021/4095038\n"
                    'Application mobile: "Tensiomètre" pour suivre sa tension artérielle'
                ),
                'resources': [
                    {'title': 'Fédération Française de Cardiologie', 'description': 'Informations sur les maladies cardiovasculaires', 'url': 'https://fedecardio.org'},
                    {'title': 'Société Française d\'Hypertension Artérielle', 'description': 'Recommandations et actualités sur l\'HTA', 'url': 'http://www.sfhta.eu'},
                    {'title': 'Ameli.fr - Hypertension artérielle', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/hypertension-arterelle-hta'}
                ]
            },
            # 4. Maladie endocrinienne
            {
                'name': 'Diabète de type 2',
                'scientific_name': 'Diabetes mellitus type 2',
                'category': 'Endocrinologie',
                'prevalence': '5-10% de la population adulte',
                'age_group': 'Principalement après 40 ans, mais de plus en plus fréquent chez les jeunes',
                'risk_factors': 'Obésité, sédentarité, antécédents familiaux, hypertension artérielle',
                'diagnosis': 'Glycémie à jeun ≥ 1.26 g/l (7.0 mmol/l) à deux reprises ou HbA1c ≥ 6.5%',
                'differential_diagnosis': 'Diabète de type 1, diabète MODY, diabète secondaire',
                'follow_up': 'Auto-surveillance glycémique, HbA1c trimestrielle, bilan annuel des complications',
                'references': 'Recommandations HAS 2019, ADA 2021',
                'short_description': 'Trouble métabolique caractérisé par une hyperglycémie chronique',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Soif intense, envie fréquente d\'uriner, fatigue, vision trouble',
                'description': (
                    "Le diabète de type 2 est une maladie métabolique chronique caractérisée par une résistance à l'insuline "
                    "et une défaillance progressive des cellules bêta pancréatiques. C'est la forme la plus courante de diabète, "
                    "représentant environ 90% des cas. La maladie évolue souvent silencieusement pendant des années avant d'être diagnostiquée."
                ),
                'causes': (
                    "Facteurs génétiques (antécédents familiaux)\n"
                    "Surpoids et obésité abdominale\n"
                    "Sédentarité\n"
                    "Alimentation déséquilibrée riche en graisses et sucres\n"
                    "Âge avancé\n"
                    "Origine ethnique à risque (afro-antillaise, maghrébine, asiatique)"
                ),
                'treatment': (
                    "Mesures hygiéno-diététiques (alimentation équilibrée, activité physique régulière, perte de poids)\n"
                    "Médicaments antidiabétiques oraux (metformine, sulfamides, gliptines, gliflozines)\n"
                    "Injection d'insuline si échec des autres traitements\n"
                    "Traitement des facteurs de risque associés (hypertension, dyslipidémie)\n"
                    "Éducation thérapeutique du patient"
                ),
                'prevention': (
                    "Maintien d'un poids santé (IMC < 25 kg/m²)\n"
                    "Activité physique régulière (30 minutes par jour)\n"
                    "Alimentation équilibrée (riche en fibres, pauvre en graisses saturées et sucres rapides)\n"
                    "Arrêt du tabac\n"
                    "Surveillance régulière de la glycémie en cas de facteurs de risque"
                ),
                'complications': (
                    "Complications microvasculaires : rétinopathie, néphropathie, neuropathie\n"
                    "Complications macrovasculaires : infarctus du myocarde, AVC, artériopathie des membres inférieurs\n"
                    "Pied diabétique (risque d'amputation)\n"
                    "Complications infectieuses\n"
                    "Troubles de l'érection"
                ),
                'when_to_see_doctor': (
                    "Symptômes évocateurs (soif intense, envie fréquente d'uriner, fatigue inexpliquée)\n"
                    "Glycémie à jeun > 1.26 g/l à deux reprises\n"
                    "Présence de facteurs de risque (surpoids, antécédents familiaux, hypertension)\n"
                    "Apparition de complications (troubles de la vision, douleurs des membres, plaies qui cicatrisent mal)"
                ),
                'resources': [
                    {'title': 'Fédération Française des Diabétiques', 'description': 'Association de patients et informations sur le diabète', 'url': 'https://www.federationdesdiabetiques.org'},
                    {'title': 'Ameli.fr - Diabète de type 2', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/diabete-comprendre'},
                    {'title': 'Société Francophone du Diabète', 'description': 'Recommandations professionnelles et actualités', 'url': 'https://www.sfdiabete.org'}
                ]
            },
            
            # 5. Maladie rhumatologique
            {
                'name': 'Polyarthrite rhumatoïde',
                'scientific_name': 'Polyarthritis rheumatoidea',
                'category': 'Rhumatologie',
                'prevalence': '0.3-1% de la population',
                'age_group': 'Tous âges, pic entre 40 et 60 ans',
                'risk_factors': 'Facteurs génétiques, tabagisme, obésité, parodontite',
                'diagnosis': 'Critères ACR/EULAR 2010, bilan inflammatoire, sérologie (facteur rhumatoïde, ACPA)',
                'differential_diagnosis': 'Rhumatisme psoriasique, connectivites, arthrose',
                'follow_up': 'Évaluation régulière de l\'activité de la maladie, imagerie articulaire, dépistage des complications',
                'references': 'Recommandations EULAR 2022, SFR 2020',
                'short_description': 'Maladie auto-immune inflammatoire chronique touchant principalement les articulations',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Douleurs articulaires, raideur matinale, gonflement des articulations, fatigue',
                'description': (
                    "La polyarthrite rhumatoïde est une maladie auto-immune chronique qui provoque une inflammation de la membrane "
                    "synoviale des articulations, entraînant des douleurs, des raideurs et une destruction articulaire progressive. "
                    "Elle peut également toucher d'autres organes (poumons, cœur, yeux). La maladie évolue par poussées et peut entraîner "
                    "des déformations articulaires et un handicap fonctionnel important si elle n'est pas traitée précocement."
                ),
                'causes': (
                    "Facteurs génétiques (HLA-DR4, PTPN22)\n"
                    "Facteurs environnementaux (tabagisme, infections, déséquilibre du microbiote intestinal)\n"
                    "Dérèglement du système immunitaire\n"
                    "Facteurs hormonaux (plus fréquent chez les femmes)"
                ),
                'treatment': (
                    "Traitement de fond (Méthotrexate en première intention, biothérapies, inhibiteurs de JAK)\n"
                    "Anti-inflammatoires non stéroïdiens (AINS) et corticoïdes pour les poussées\n"
                    "Traitements locaux (infiltrations, synovectomie)\n"
                    "Rééducation fonctionnelle et ergothérapie\n"
                    "Prise en charge de la douleur\n"
                    "Arrêt du tabac et activité physique adaptée"
                ),
                'prevention': (
                    "Arrêt du tabac (facteur de risque majeur)\n"
                    "Dépistage et traitement précoce des formes débutantes\n"
                    "Maintien d'une bonne hygiène bucco-dentaire (lien avec la parodontite)\n"
                    "Activité physique régulière pour préserver la mobilité articulaire"
                ),
                'complications': (
                    "Destruction articulaire et déformations (mains en col de cygne, en coup de vent)\n"
                    "Atteintes extra-articulaires (nodules rhumatoïdes, vascularite, syndrome de Gougerot-Sjögren)\n"
                    "Complications liées aux traitements (infections, effets secondaires des immunosuppresseurs)\n"
                    "Maladies cardiovasculaires (risque accru d'infarctus et d'AVC)\n"
                    "Syndrome sec oculaire et buccal"
                ),
                'when_to_see_doctor': (
                    "Douleurs articulaires persistantes avec raideur matinale prolongée (> 30 minutes)\n"
                    "Gonflement articulaire persistant\n"
                    "Fatigue inexpliquée avec symptômes articulaires\n"
                    "Apparition de nodules sous-cutanés\n"
                    "Signes généraux (fièvre, amaigrissement) associés à des douleurs articulaires"
                ),
                'resources': [
                    {'title': 'Association Française des Polyarthritiques', 'description': 'Association de patients et informations sur la PR', 'url': 'https://www.polyarthrite.org'},
                    {'title': 'Société Française de Rhumatologie', 'description': 'Recommandations professionnelles', 'url': 'https://sfr.larhumatologie.fr'},
                    {'title': 'Ameli.fr - Polyarthrite rhumatoïde', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/polyarthrite-rhumatoide'}
                ]
            },
            
            # 6. Maladie neurologique
            {
                'name': 'Maladie de Parkinson',
                'scientific_name': 'Morbus Parkinson',
                'category': 'Neurologie',
                'prevalence': '1-2% des plus de 60 ans',
                'age_group': 'Principalement après 60 ans, formes précoces possibles avant 50 ans',
                'risk_factors': 'Âge, facteurs génétiques, exposition aux pesticides, traumatismes crâniens',
                'diagnosis': 'Examen clinique, critères MDS-UPDRS, imagerie cérébrale (DATscan, IRM)',
                'differential_diagnosis': 'Tremblement essentiel, atrophie multi-systématisée, paralysie supranucléaire progressive',
                'follow_up': 'Consultations neurologiques régulières, évaluation des symptômes non moteurs, adaptation du traitement',
                'references': 'Recommandations HAS 2012, MDS 2021',
                'short_description': 'Maladie neurodégénérative caractérisée par la destruction des neurones à dopamine',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Tremblement de repos, rigidité musculaire, akinésie, troubles de la marche et de l\'équilibre',
                'description': (
                    "La maladie de Parkinson est une affection neurodégénérative chronique évolutive caractérisée par la dégénérescence "
                    "des neurones à dopamine de la substance noire. Elle se manifeste par des troubles moteurs (tremblement, rigidité, akinésie) "
                    "et non moteurs (troubles du sommeil, dépression, troubles cognitifs). La maladie évolue sur plusieurs décennies avec une "
                    "aggravation progressive des symptômes."
                ),
                'causes': (
                    "Facteurs génétiques (mutations des gènes PARK, LRRK2, GBA)\n"
                    "Facteurs environnementaux (exposition aux pesticides, solvants, métaux lourds)\n"
                    "Vieillissement cérébral accéléré\n"
                    "Dysfonctionnement du système immunitaire"
                ),
                'treatment': (
                    "Lévodopa (traitement de référence)\n"
                    "Agonistes dopaminergiques (ropinirole, pramipexole)\n"
                    "Inhibiteurs de la COMT et de la MAO-B\n"
                    "Kinésithérapie et orthophonie\n"
                    "Traitement des symptômes non moteurs (dépression, douleurs, troubles du sommeil)\n"
                    "Stimulation cérébrale profonde dans les formes avancées"
                ),
                'prevention': (
                    "Activité physique régulière (protection neuronale démontrée)\n"
                    "Alimentation méditerranéenne riche en antioxydants\n"
                    "Éviction des pesticides et toxines environnementales\n"
                    "Traitement précoce des troubles du sommeil paradoxal"
                ),
                'complications': (
                    "Fluctuations motrices et dyskinésies sous traitement\n"
                    "Troubles de la déglutition et fausses routes\n"
                    "Syndrome parkinsonien atypique (démence, chutes à répétition, dysautonomie)\n"
                    "Dépression et anxiété\n"
                    "Troubles cognitifs évoluant vers une démence"
                ),
                'when_to_see_doctor': (
                    "Apparition de tremblements au repos\n"
                    "Ralentissement des mouvements et difficultés à initier le pas\n"
                    "Raideur musculaire douloureuse\n"
                    "Troubles de l'équilibre et chutes inexpliquées\n"
                    "Modification de l'écriture (micrographie)"
                ),
                'resources': [
                    {'title': 'France Parkinson', 'description': 'Association de patients et d\'information sur la maladie de Parkinson', 'url': 'https://www.franceparkinson.fr'},
                    {'title': 'Ameli.fr - Maladie de Parkinson', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/maladie-parkinson'},
                    {'title': 'Société Française de Neurologie', 'description': 'Recommandations professionnelles', 'url': 'https://www.sf-neuro.org'}
                ]
            },
            
            # 7. Maladie infectieuse
            {
                'name': 'Maladie de Lyme',
                'scientific_name': 'Borreliosis',
                'category': 'Infectiologie',
                'prevalence': 'En augmentation en France, particulièrement dans l\'Est et le Centre',
                'age_group': 'Tous âges, plus fréquent chez les enfants et les personnes exposées aux tiques',
                'risk_factors': 'Activités en forêt ou en zone rurale, promenades dans les herbes hautes, absence de protection contre les tiques',
                'diagnosis': 'Sérologie (Elisa puis Western Blot en cas de doute), PCR dans certains cas, évaluation clinique',
                'differential_diagnosis': 'Syndrome grippal, méningite, sclérose en plaques, fibromyalgie',
                'follow_up': 'Surveillance clinique après morsure de tique, recherche de signes disséminés, contrôle sérologique si nécessaire',
                'references': 'Recommandations HAS 2018, SPILF 2019',
                'short_description': 'Infection bactérienne transmise par les tiques, due à Borrelia burgdorferi',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Érythème migrant, fièvre, fatigue, douleurs articulaires, paralysie faciale',
                'description': (
                    "La maladie de Lyme est une infection bactérienne transmise par la morsure de tiques infectées par des bactéries du genre Borrelia. "
                    "Elle évolue en trois phases : localisée (érythème migrant), disséminée (atteintes neurologiques, articulaires, cardiaques) et tardive "
                    "(arthrite chronique, manifestations neurologiques persistantes). Le diagnostic repose sur la clinique et la sérologie, avec des difficultés "
                    "dans les formes chroniques ou atypiques."
                ),
                'causes': (
                    "Morsure de tique infectée par Borrelia burgdorferi\n"
                    "Contact avec des zones d'endémie (forêts, prairies, parcs boisés)\n"
                    "Activités de plein air sans protection adaptée"
                ),
                'treatment': (
                    "Antibiothérapie adaptée selon le stade (doxycycline, amoxicilline, ceftriaxone)\n"
                    "Traitement symptomatique des douleurs articulaires et musculaires\n"
                    "Rééducation fonctionnelle en cas d'atteinte neurologique\n"
                    "Prise en charge multidisciplinaire pour les formes chroniques"
                ),
                'prevention': (
                    "Port de vêtements couvrants et clairs en zone à risque\n"
                    "Utilisation de répulsifs cutanés (DEET, IR3535, icaridine)\n"
                    "Inspection minutieuse du corps après exposition\n"
                    "Retrait rapide des tiques avec un tire-tique (sans application de produit)\n"
                    "Surveillance de la zone de piqûre pendant 1 mois"
                ),
                'complications': (
                    "Arthrite de Lyme (gonflement douloureux d'une grosse articulation, souvent le genou)\n"
                    "Neuroborréliose (méningite, paralysie faciale, radiculite douloureuse)\n"
                    "Troubles cardiaques (troubles de la conduction, myocardite)\n"
                    "Formes chroniques avec fatigue chronique et douleurs diffuses"
                ),
                'when_to_see_doctor': (
                    "Apparition d'un érythème migrant (plaque rouge s'étendant en cercle)\n"
                    "Fièvre inexpliquée après une morsure de tique\n"
                    "Douleurs articulaires ou musculaires diffuses\n"
                    "Paralysie faciale ou autres symptômes neurologiques\n"
                    "Palpitations ou douleurs thoraciques après exposition aux tiques"
                ),
                'resources': [
                    {'title': 'France Lyme', 'description': 'Association de patients et d\'information sur la maladie de Lyme', 'url': 'https://francelyme.fr'},
                    {'title': 'Ministère de la Santé - Maladie de Lyme', 'description': 'Informations officielles et recommandations', 'url': 'https://solidarites-sante.gouv.fr/soins-et-maladies/maladies/maladies-infectieuses/maladie-de-lyme'},
                    {'title': 'Société de Pathologie Infectieuse de Langue Française', 'description': 'Recommandations professionnelles', 'url': 'https://www.infectiologie.com'}
                ]
            },
            
            # 8. Maladie endocrinienne - Diabète de type 1
            {
                'name': 'Diabète de type 1',
                'scientific_name': 'Diabetes mellitus type 1',
                'category': 'Endocrinologie',
                'prevalence': '0.3-0.5% de la population générale',
                'age_group': 'Principalement chez les enfants et jeunes adultes, mais peut survenir à tout âge',
                'risk_factors': 'Prédisposition génétique, facteurs environnementaux, infections virales',
                'diagnosis': 'Glycémie à jeun ≥ 1.26 g/l, HbA1c ≥ 6.5%, présence d\'auto-anticorps (anti-GAD, anti-IA2)',
                'differential_diagnosis': 'Diabète de type 2, diabète MODY, diabète secondaire, diabète LADA',
                'follow_up': 'Auto-surveillance glycémique, HbA1c trimestrielle, bilan annuel des complications',
                'references': 'Recommandations HAS 2021, ISPAD 2022',
                'short_description': 'Maladie auto-immune entraînant une destruction des cellules bêta du pancréas productrices d\'insuline',
                'severity': 'H',
                'is_emergency': True,
                'main_symptoms': 'Soif intense, envie fréquente d\'uriner, perte de poids, fatigue, augmentation de l\'appétit',
                'description': (
                    "Le diabète de type 1 est une maladie auto-immune caractérisée par la destruction progressive "
                    "des cellules bêta des îlots de Langerhans du pancréas, entraînant une carence complète en insuline. "
                    "Cette maladie nécessite un traitement par insuline à vie. Le diabète de type 1 représente environ 10% "
                    "des cas de diabète et survient généralement chez les enfants et les jeunes adultes, bien qu'il puisse "
                    "apparaître à tout âge. La maladie évolue par une phase préclinique silencieuse suivie d'un début clinique "
                    "souvent brutal avec des symptômes marqués d'hyperglycémie."
                ),
                'causes': (
                    "Prédisposition génétique (gènes HLA-DR3, HLA-DR4, PTPN22, INS)\n"
                    "Facteurs environnementaux déclenchants (infections virales comme les entérovirus, virus Coxsackie B4)\n"
                    "Réaction auto-immune contre les cellules bêta pancréatiques\n"
                    "Facteurs alimentaires précoces (introduction précoce du lait de vache, carence en vitamine D)"
                ),
                'treatment': (
                    "Insulinothérapie intensifiée (injections multiples ou pompe à insuline)\n"
                    "Surveillance glycémique autorisée (6-8 contrôles par jour ou capteur de glycémie en continu)\n"
                    "Éducation thérapeutique du patient et de son entourage\n"
                    "Alimentation équilibrée avec calcul des glucides\n"
                    "Activité physique adaptée et sécurisée\n"
                    "Prise en charge des facteurs de risque cardiovasculaires\n"
                    "Suivi régulier par une équipe pluridisciplinaire (médecin, infirmier, diététicien)"
                ),
                'prevention': 'Pas de prévention primaire connue actuellement',
                'prevention_details': (
                    "- Pas de moyen de prévention primaire identifié à ce jour\n"
                    "- Essais en cours avec des immunomodulateurs en phase préclinique\n"
                    "- Dépistage des apparentés du premier degré (risque accru de 5 à 10%)\n"
                    "- Recherche d'auto-anticorps dans les familles à risque\n"
                    "- Éviter l'introduction précoce du lait de vache chez les nourrissons à risque"
                ),
                'complications': (
                    "Hypoglycémies sévères (urgence vitale)\n"
                    "Acidocétose diabétique (urgence médicale)\n"
                    "Rétinopathie diabétique pouvant mener à la cécité\n"
                    "Néphropathie diabétique évoluant vers l'insuffisance rénale\n"
                    "Neuropathie diabétique (douleurs, troubles de la sensibilité, pied diabétique)\n"
                    "Maladies cardiovasculaires (infarctus, AVC, artérite des membres inférieurs)\n"
                    "Complications de la grossesse (pré-éclampsie, macrosomie fœtale)"
                ),
                'when_to_see_doctor': (
                    "Apparition de symptômes évocateurs (soif intense, amaigrissement, fatigue, polyurie)\n"
                    "Glycémie capillaire > 2.5 g/l ou < 0.6 g/l malgré les corrections\n"
                    "Présence de corps cétoniques dans les urines ou le sang\n"
                    "Signes d'acidocétose (nausées, vomissements, douleurs abdominales, respiration rapide, haleine fruitée)\n"
                    "Hypoglycémies sévères ou fréquentes"
                ),
                'resources': [
                    {'title': 'Fédération Française des Diabétiques', 'description': 'Association de patients et informations sur le diabète', 'url': 'https://www.federationdesdiabetiques.org'},
                    {'title': 'Aide aux Jeunes Diabétiques', 'description': 'Association spécialisée dans le diabète de type 1 chez l\'enfant et l\'adolescent', 'url': 'https://www.ajd-diabete.fr'},
                    {'title': 'Ameli.fr - Diabète de type 1', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/diabete-type-1'},
                    {'title': 'Société Francophone du Diabète', 'description': 'Recommandations professionnelles', 'url': 'https://www.sfdiabete.org'}
                ]
            },
            
            # 9. Maladie neurologique - Maladie de Parkinson
            {
                'name': 'Maladie de Parkinson',
                'scientific_name': 'Morbus Parkinson',
                'category': 'Neurologie',
                'prevalence': '1-2% des plus de 60 ans, 2e maladie neurodégénérative après Alzheimer',
                'age_group': 'Principalement après 60 ans, formes précoces possibles avant 50 ans',
                'risk_factors': 'Âge, prédisposition génétique, exposition aux pesticides, traumatismes crâniens',
                'diagnosis': 'Examen clinique, critères MDS-UPDRS, DATscan, IRM cérébrale pour éliminer d\'autres causes',
                'differential_diagnosis': 'Tremblement essentiel, atrophie multi-systématisée, paralysie supranucléaire progressive',
                'follow_up': 'Consultations neurologiques régulières, évaluation des troubles moteurs et non moteurs, adaptation thérapeutique',
                'references': 'Recommandations HAS 2012, MDS 2015',
                'short_description': 'Maladie neurodégénérative caractérisée par la destruction des neurones à dopamine',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Tremblement de repos, rigidité musculaire, akinésie, instabilité posturale',
                'description': (
                    "La maladie de Parkinson est une affection neurodégénérative chronique évolutive caractérisée par la destruction "
                    "progressive des neurones à dopamine de la substance noire du cerveau. Elle se manifeste par des troubles "
                    "moteurs caractéristiques (tremblement, rigidité, akinésie) et des symptômes non moteurs (troubles du sommeil, "
                    "dépression, troubles cognitifs). La maladie évolue sur plusieurs années avec une aggravation progressive des symptômes."
                ),
                'causes': (
                    "Dégénérescence des neurones dopaminergiques de la substance noire\n"
                    "Facteurs génétiques (mutations des gènes LRRK2, PARK2, PINK1, etc.)\n"
                    "Facteurs environnementaux (exposition aux pesticides, solvants, métaux lourds)\n"
                    "Vieillissement cérébral accéléré"
                ),
                'treatment': (
                    "Lévodopa (traitement de référence)\n"
                    "Agonistes dopaminergiques (ropinirole, pramipexole, rotigotine)\n"
                    "Inhibiteurs de la MAO-B (sélégiline, rasagiline)\n"
                    "Inhibiteurs de la COMT (entacapone, opicapone)\n"
                    "Traitement des symptômes non moteurs (dépression, douleurs, troubles du sommeil)\n"
                    "Rééducation (kinésithérapie, orthophonie, ergothérapie)\n"
                    "Stimulation cérébrale profonde dans les formes avancées"
                ),
                'prevention': 'Aucune prévention primaire connue',
                'prevention_details': (
                    "- Caféine et thé vert pourraient avoir un effet protecteur\n"
                    "- Activité physique régulière\n"
                    "- Éviction des pesticides et produits toxiques\n"
                    "- Protection contre les traumatismes crâniens"
                ),
                'complications': (
                    "Troubles de la marche et chutes à répétition\n"
                    "Troubles de la déglutition avec fausses routes\n"
                    "Démence parkinsonienne (30-40% des cas)\n"
                    "Hallucinations et psychose induites par les traitements\n"
                    "Fluctuations motrices et dyskinésies liées à la Lévodopa\n"
                    "Syndrome d'épuisement dopaminergique"
                ),
                'when_to_see_doctor': (
                    "Apparition d'un tremblement de repos\n"
                    "Ralentissement des mouvements et difficulté à initier les gestes\n"
                    "Raidissement des membres et du tronc\n"
                    "Troubles de l'équilibre et chutes inexpliquées\n"
                    "Modification de l'écriture (devenue plus petite et serrée)"
                ),
                'resources': [
                    {'title': 'France Parkinson', 'description': 'Association de patients et d\'information sur la maladie de Parkinson', 'url': 'https://www.franceparkinson.fr'},
                    {'title': 'Orphanet - Maladie de Parkinson', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=2828'},
                    {'title': 'Société Française de Neurologie', 'description': 'Recommandations professionnelles', 'url': 'https://www.sf-neuro.org'}
                ]
            },
            
            # 10. Maladie neurologique - Sclérose en plaques
            {
                'name': 'Sclérose en plaques',
                'scientific_name': 'Sclerosis multiplex',
                'category': 'Neurologie',
                'prevalence': '1 cas pour 1000 habitants en France',
                'age_group': 'Jeune adulte (20-40 ans), plus fréquente chez la femme (3 femmes pour 1 homme)',
                'risk_factors': 'Prédisposition génétique, carence en vitamine D, tabagisme, obésité à l\'adolescence, infection par le virus EBV',
                'diagnosis': 'IRM cérébrale et médullaire, ponction lombaire (bandes oligoclonales), potentiels évoqués, critères de McDonald 2017',
                'differential_diagnosis': 'Névrite optique isolée, myélite transverse, maladie de Lyme, vascularites, maladies métaboliques',
                'follow_up': 'IRM annuelle, évaluation EDSS, suivi des traitements de fond, prise en charge des symptômes',
                'references': 'Recommandations HAS 2018, ECTRIMS 2020',
                'short_description': 'Maladie auto-immune du système nerveux central caractérisée par une démyélinisation et une neurodégénérescence',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Troubles visuels, faiblesse musculaire, troubles de l\'équilibre, troubles sensitifs, fatigue intense',
                'description': (
                    "La sclérose en plaques (SEP) est une maladie auto-immune chronique du système nerveux central caractérisée par une réaction inflammatoire "
                    "dirigée contre la myéline, gaine protectrice des fibres nerveuses. Elle évolue par poussées (formes rémittentes) ou de manière progressive "
                    "avec une accumulation du handicap. La maladie est imprévisible et très variable d'un patient à l'autre. Les lésions (ou plaques) de démyélinisation "
                    "peuvent toucher différentes zones du cerveau et de la moelle épinière, expliquant la diversité des symptômes. La recherche a fait d'importants "
                    "progrès ces dernières années, avec le développement de nombreux traitements modificateurs de la maladie."
                ),
                'causes': (
                    "Prédisposition génétique (gènes HLA-DRB1, IL2RA, IL7R, etc.)\n"
                    "Facteurs environnementaux (carence en vitamine D, tabagisme, obésité)\n"
                    "Infections virales (virus d'Epstein-Barr, herpès virus 6)\n"
                    "Altération du microbiote intestinal\n"
                    "Facteurs hormonaux (rôle protecteur de la grossesse)"
                ),
                'treatment': (
                    "Traitement des poussées (corticoïdes à fortes doses, échanges plasmatiques dans les formes sévères)\n"
                    "Traitements de fond de première ligne (interféron bêta, acétate de glatiramère, tériflunomide, diméthyl fumarate)\n"
                    "Traitements de fond de deuxième intention (natalizumab, fingolimod, ocrelizumab, cladribine, alentuzumab)\n"
                    "Traitements symptomatiques (fatigue, spasticité, douleurs, troubles vésicaux, troubles cognitifs)\n"
                    "Rééducation (kinésithérapie, orthophonie, ergothérapie, neuropsychologie)\n"
                    "Prise en charge globale (assistante sociale, soutien psychologique)"
                ),
                'prevention': 'Pas de prévention primaire connue',
                'prevention_details': (
                    "- Supplémentation en vitamine D chez les sujets à risque (carence avérée)\n"
                    "- Arrêt du tabac impératif\n"
                    "- Activité physique régulière adaptée\n"
                    "- Alimentation équilibrée (régime méditerranéen)\n"
                    "- Éviction des facteurs déclenchants (stress, infections, chaleur excessive)"
                ),
                'complications': (
                    "Handicap moteur progressif (marche difficile, fauteuil roulant)\n"
                    "Troubles sphinctériens (incontinence urinaire, constipation)\n"
                    "Troubles cognitifs (mémoire, attention, fonctions exécutives)\n"
                    "Dépression et troubles de l'humeur\n"
                    "Douleurs chroniques (neuropathiques, musculo-squelettiques)\n"
                    "Complications de décubitus (escarres, infections urinaires, rétractions tendineuses)"
                ),
                'when_to_see_doctor': (
                    "Apparition de symptômes neurologiques inexpliqués (baisse d'acuité visuelle, troubles de l'équilibre, faiblesse musculaire)\n"
                    "Aggravation brutale de symptômes existants (suspicion de poussée)\n"
                    "Effets secondaires des traitements\n"
                    "Signes d'infection urinaire ou pulmonaire\n"
                    "Apparition de troubles de la déglutition ou de troubles cognitifs"
                ),
                'resources': [
                    {'title': 'Ligue Française contre la Sclérose en Plaques', 'description': 'Association de patients et d\'information sur la SEP', 'url': 'https://www.lfsep.asso.fr'},
                    {'title': 'ARSEP - Fondation pour l\'Aide à la Recherche sur la Sclérose en Plaques', 'description': 'Informations scientifiques et recherches sur la SEP', 'url': 'https://www.arsep.org'},
                    {'title': 'Orphanet - Sclérose en plaques', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=802'},
                    {'title': 'Société Francophone de la Sclérose en Plaques', 'description': 'Recommandations professionnelles', 'url': 'https://www.sfsep.fr'}
                ]
            },
            
            # 11. Maladie rhumatologique - Polyarthrite rhumatoïde
            {
                'name': 'Polyarthrite rhumatoïde',
                'scientific_name': 'Polyarthritis rheumatoidea',
                'category': 'Rhumatologie',
                'prevalence': '0.3-0.8% de la population, 3 femmes pour 1 homme',
                'age_group': 'Pic entre 40 et 60 ans, mais peut survenir à tout âge',
                'risk_factors': 'Tabagisme, prédisposition génétique (HLA-DRB1), facteurs hormonaux, obésité, parodontopathies',
                'diagnosis': 'Critères ACR/EULAR 2010, facteur rhumatoïde, anticorps anti-CCP, VS/CRP, échographie articulaire, radiographies',
                'differential_diagnosis': 'Arthrose, spondylarthropathies, connectivites, hémochromatose, polyarthrite virale',
                'follow_up': 'DAS28, échographie articulaire, bilan biologique trimestriel, radiographies annuelles',
                'references': 'Recommandations EULAR 2022, SFR 2019',
                'short_description': 'Maladie auto-immune inflammatoire chronique touchant principalement les articulations périphériques',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Douleurs articulaires, gonflements, raideur matinale prolongée, fatigue, déformations articulaires',
                'description': (
                    "La polyarthrite rhumatoïde (PR) est une maladie auto-immune systémique caractérisée par une inflammation chronique des articulations "
                    "périphériques, évoluant par poussées. Elle entraîne une destruction progressive du cartilage et de l'os, avec un risque de déformations "
                    "et de handicap fonctionnel important. La PR peut également s'accompagner de manifestations extra-articulaires (poumon, cœur, œil, peau). "
                    "Le diagnostic et la mise en route rapide d'un traitement de fond sont essentiels pour prévenir les lésions articulaires irréversibles. "
                    "La prise en charge est multidisciplinaire, associant traitements médicamenteux, rééducation et parfois chirurgie."
                ),
                'causes': (
                    "Prédisposition génétique (gènes HLA-DRB1, PTPN22, STAT4, etc.)\n"
                    "Facteurs environnementaux (tabac, silice, infections)\n"
                    "Dérégulation du système immunitaire (activation des lymphocytes T et B, production d'auto-anticorps)\n"
                    "Altération de la barrière épithéliale (parodonte, poumon, intestin)\n"
                    "Déséquilibre du microbiote intestinal (dysbiose)"
                ),
                'treatment': (
                    "Traitements de fond conventionnels (méthotrexate, léflunomide, sulfasalazine)\n"
                    "Biothérapies (anti-TNF alpha, anti-IL6, anti-CD20, co-stimulation des lymphocytes T)\n"
                    "Petites molécules synthétiques (inhibiteurs de JAK-STAT)\n"
                    "Corticoïdes à la dose minimale efficace\n"
                    "Antalgiques et anti-inflammatoires non stéroïdiens en traitement d'appoint\n"
                    "Rééducation fonctionnelle et ergothérapie\n"
                    "Chirurgie orthopédique dans les formes sévères (prothèses, arthrodèses)"
                ),
                'prevention': 'Pas de prévention primaire connue',
                'prevention_details': (
                    "- Arrêt impératif du tabac (facteur de risque majeur)\n"
                    "- Hygiène bucco-dentaire rigoureuse (lien avec les parodontopathies)\n"
                    "- Activité physique régulière adaptée\n"
                    "- Maintien d'un poids santé (rôle délétère de l'obésité)\n"
                    "- Dépistage et traitement précoce des facteurs de risque cardiovasculaires"
                ),
                'complications': (
                    "Destruction articulaire avec déformations et handicap fonctionnel\n"
                    "Atteintes extra-articulaires (poumon, cœur, vaisseaux, œil, peau)\n"
                    "Risque cardiovasculaire accru (infarctus, AVC, artérite)\n"
                    "Syndrome sec secondaire (syndrome de Gougerot-Sjögren associé)\n"
                    "Infections (liées aux traitements immunosuppresseurs)\n"
                    "Douleurs chroniques et altération de la qualité de vie\n"
                    "Dépression et troubles anxieux"
                ),
                'when_to_see_doctor': (
                    "Douleurs articulaires inflammatoires (nocturnes, améliorées par le mouvement)\n"
                    "Gonflement articulaire persistant plus de 6 semaines\n"
                    "Raideur matinale prolongée (>30 minutes)\n"
                    "Fatigue inhabituelle et persistante\n"
                    "Apparition de nodules rhumatoïdes ou d'autres manifestations extra-articulaires"
                ),
                'resources': [
                    {'title': 'Association Française des Polyarthritiques', 'description': 'Association de patients et d\'information sur la PR', 'url': 'https://www.polyarthrite.org'},
                    {'title': 'Société Française de Rhumatologie', 'description': 'Recommandations professionnelles', 'url': 'https://sfr.larhumatologie.fr'},
                    {'title': 'Ameli.fr - Polyarthrite rhumatoïde', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/polyarthrite-rhumatoide'},
                    {'title': 'Orphanet - Polyarthrite rhumatoïde', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=28413'}
                ]
            },
            
            # 12. Maladie digestive - Maladie de Crohn
            {
                'name': 'Maladie de Crohn',
                'scientific_name': 'Morbus Crohn',
                'category': 'Gastro-entérologie',
                'prevalence': '1 cas pour 1000 habitants en Europe et Amérique du Nord',
                'age_group': 'Jeune adulte (20-30 ans), second pic vers 60 ans',
                'risk_factors': 'Prédisposition génétique (NOD2/CARD15), tabagisme, déséquilibre du microbiote, alimentation occidentale',
                'diagnosis': 'Coloscopie avec iléoscopie et biopsies, entéro-IRM/entéro-scanner, vidéocapsule, marqueurs biologiques (calprotectine fécale, CRP)',
                'differential_diagnosis': 'Rectocolite hémorragique, tuberculose intestinale, maladie cœliaque, syndrome de l\'intestin irritable, maladie de Behçet',
                'follow_up': 'Suivi clinique régulier, surveillance biologique, imagerie et endoscopie selon l\'évolution, dépistage des cancers colorectaux',
                'references': 'Recommandations ECCO 2019, GETAID 2021',
                'short_description': 'Maladie inflammatoire chronique pouvant toucher tout le tube digestif, avec une prédilection pour l\'iléon et le côlon',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Douleurs abdominales, diarrhée chronique, perte de poids, fatigue, fièvre, manifestations extra-intestinales',
                'description': (
                    "La maladie de Crohn est une maladie inflammatoire chronique du tube digestif, appartenant au groupe des maladies inflammatoires chroniques de l'intestin (MICI). "
                    "Elle peut toucher n'importe quelle partie du tube digestif, de la bouche à l'anus, avec une prédilection pour la fin de l'intestin grêle (iléon) et le côlon. "
                    "La maladie évolue par poussées entrecoupées de périodes de rémission. Elle est caractérisée par une inflammation chronique pouvant entraîner des complications "
                    "comme des sténoses, des fistules ou des abcès. La maladie de Crohn a un retentissement important sur la qualité de vie et nécessite une prise en charge "
                    "pluridisciplinaire et personnalisée."
                ),
                'causes': (
                    "Prédisposition génétique (mutations des gènes NOD2/CARD15, ATG16L1, IL23R, etc.)\n"
                    "Dérégulation du système immunitaire intestinal (réponse anormale à la flore bactérienne)\n"
                    "Altération de la barrière épithéliale intestinale\n"
                    "Déséquilibre du microbiote intestinal (dysbiose)\n"
                    "Facteurs environnementaux (tabagisme, alimentation occidentale, hygiène excessive)"
                ),
                'treatment': (
                    "Traitement des poussées (corticoïdes, anti-TNF, immunosuppresseurs, antibiotiques si abcès)\n"
                    "Traitement d'entretien (azathioprine, méthotrexate, anti-TNF, anti-intégrines, anti-IL12/23, JAK-inhibiteurs)\n"
                    "Traitement des complications (sténoses, fistules, abcès)\n"
                    "Support nutritionnel (régime spécifique, compléments, nutrition entérale ou parentérale si nécessaire)\n"
                    "Chirurgie en cas de complications (sténoses symptomatiques, abcès, fistules, perforations, cancers)\n"
                    "Arrêt impératif du tabac\n"
                    "Prise en charge psychologique et éducation thérapeutique"
                ),
                'prevention': 'Aucune prévention primaire connue',
                'prevention_details': (
                    "- Arrêt impératif du tabac (aggrave la maladie et réduit l'efficacité des traitements)\n"
                    "- Alimentation équilibrée et variée, sans régime d'éviction sauf intolérances avérées\n"
                    "- Activité physique régulière adaptée\n"
                    "- Gestion du stress (facteur déclenchant des poussées)\n"
                    "- Suivi régulier même en période de rémission"
                ),
                'complications': (
                    "Sténoses intestinales (rétrécissements)\n"
                    "Fistules (communications anormales entre organes)\n"
                    "Abcès intra-abdominaux\n"
                    "Malabsorption et carences nutritionnelles\n"
                    "Risque accru de cancer colorectal\n"
                    "Manifestations extra-intestinales (articulaires, cutanées, oculaires, hépatiques)\n"
                    "Retard de croissance et de puberté chez l'enfant"
                ),
                'when_to_see_doctor': (
                    "Douleurs abdominales persistantes ou intenses\n"
                    "Diarrhée chronique (plus de 4 semaines)\n"
                    "Sang dans les selles\n"
                    "Perte de poids inexpliquée\n"
                    "Fièvre prolongée\n"
                    "Signes de complications (vomissements, arrêt des matières et des gaz, douleur abdominale aiguë)"
                ),
                'resources': [
                    {'title': 'Association François Aupetit', 'description': 'Association de patients et d\'information sur les MICI', 'url': 'https://www.afa.asso.fr'},
                    {'title': 'GETAID', 'description': 'Groupe d\'Étude Thérapeutique des Affections Inflammatoires du Tube Digestif', 'url': 'https://www.getaid.org'},
                    {'title': 'Ameli.fr - Maladie de Crohn', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/maladie-crohn'},
                    {'title': 'Orphanet - Maladie de Crohn', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=104'}
                ]
            },
            
            # 13. Maladie auto-immune - Lupus érythémateux disséminé
            {
                'name': 'Lupus érythémateux disséminé',
                'scientific_name': 'Lupus erythematosus systemicus',
                'category': 'Médecine interne',
                'prevalence': '20-70 cas pour 100 000 habitants, 9 femmes pour 1 homme',
                'age_group': 'Jeune adulte (20-40 ans), mais peut survenir à tout âge',
                'risk_factors': 'Prédisposition génétique, facteurs hormonaux, exposition aux UV, médicaments, infections, tabagisme',
                'diagnosis': 'Critères SLICC 2012 ou ACR/EULAR 2019, anticorps antinucléaires, anti-ADN natif, anti-Sm, complément sérique, biopsie rénale si atteinte rénale',
                'differential_diagnosis': 'Syndrome des anticorps antiphospholipides, syndrome de Sjögren, polyarthrite rhumatoïde, vascularites, dermatomyosite, lymphome',
                'follow_up': 'Suivi clinique régulier, bilan biologique (NFS, créatinine, protéinurie, complément, anticorps), surveillance du risque cardiovasculaire',
                'references': 'Recommandations EULAR 2019, SNFMI 2020',
                'short_description': 'Maladie auto-immune systémique caractérisée par une atteinte multiviscérale et la présence d\'auto-anticorps',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Éruption malaire, photosensibilité, ulcérations buccales, arthralgies, fatigue, fièvre, atteinte rénale',
                'description': (
                    "Le lupus érythémateux disséminé (LED) est une maladie auto-immune chronique caractérisée par une activation incontrôlée du système immunitaire "
                    "entraînant une inflammation et des lésions tissulaires dans divers organes. La maladie évolue par poussées entrecoupées de périodes de rémission. "
                    "Le LED est une maladie extrêmement hétérogène dans ses manifestations cliniques et son pronostic, allant de formes bénignes à des formes sévères "
                    "engagant le pronostic vital. Les femmes en âge de procréer sont les plus touchées, avec un pic d'incidence entre 15 et 45 ans. La prise en charge "
                    "est multidisciplinaire et doit être adaptée à chaque patient en fonction de l'atteinte organique."
                ),
                'causes': (
                    "Prédisposition génétique (gènes HLA-DR2, HLA-DR3, IRF5, STAT4, etc.)\n"
                    "Facteurs hormonaux (rôle des œstrogènes, incidence accrue chez les femmes en âge de procréer)\n"
                    "Facteurs environnementaux (rayons UV, infections virales, médicaments, stress, tabac)\n"
                    "Dérégulation du système immunitaire (activation des lymphocytes B et T, production d'auto-anticorps, déficit d'apoptose)\n"
                    "Altération de la clairance des débris cellulaires et des complexes immuns"
                ),
                'treatment': (
                    "Hydroxychloroquine en traitement de fond pour tous les patients\n"
                    "Corticoïdes à la dose minimale efficace selon la sévérité des manifestations\n"
                    "Immunosuppresseurs (azathioprine, mycophénolate mofétil, cyclophosphamide, méthotrexate)\n"
                    "Biothérapies (bélimumab, rituximab dans certaines indications)\n"
                    "Anticoagulation en cas de syndrome des anticorps antiphospholipides associé\n"
                    "Traitements symptomatiques (antalgiques, anti-inflammatoires non stéroïdiens avec prudence)\n"
                    "Photoprotection stricte\n"
                    "Prise en charge des facteurs de risque cardiovasculaires"
                ),
                'prevention': 'Pas de prévention primaire connue',
                'prevention_details': (
                    "- Photoprotection stricte (vêtements couvrants, crème solaire indice 50+)\n"
                    "- Arrêt impératif du tabac\n"
                    "- Équilibre entre activité physique et repos\n"
                    "- Vaccinations (sauf vaccins vivants atténués sous immunosuppresseurs)\n"
                    "- Éviction des médicaments inducteurs de poussées (si possible)\n"
                    "- Suivi gynécologique régulier (contraception adaptée, dépistage du cancer du col)"
                ),
                'complications': (
                    "Atteinte rénale (néphropathie lupique) pouvant évoluer vers l'insuffisance rénale\n"
                    "Atteinte neurologique (accident vasculaire cérébral, épilepsie, neuropathie, psychose)\n"
                    "Atteinte cardiovasculaire (péricardite, endocardite de Libman-Sacks, coronaropathie précoce)\n"
                    "Atteinte pulmonaire (pleurésie, pneumopathie interstitielle, hypertension artérielle pulmonaire)\n"
                    "Infections opportunistes (liées aux traitements immunosuppresseurs)\n"
                    "Complications de la grossesse (pré-éclampsie, retard de croissance fœtale, mort fœtale in utero)\n"
                    "Syndrome des anticorps antiphospholipides associé (thromboses, fausses couches à répétition)"
                ),
                'when_to_see_doctor': (
                    "Apparition d'une éruption cutanée ou aggravation d'une éruption préexistante\n"
                    "Douleurs articulaires ou gonflements persistants\n"
                    "Fièvre inexpliquée ou fatigue importante\n"
                    "Œdèmes des membres inférieurs ou prise de poids rapide\n"
                    "Douleur thoracique ou essoufflement\n"
                    "Maux de tête sévères ou troubles neurologiques\n"
                    "Signes d'infection (fièvre, frissons, toux productive, brûlures mictionnelles)"
                ),
                'resources': [
                    {'title': 'Association Française du Lupus et autres maladies auto-immunes', 'description': 'Association de patients et d\'information sur le lupus', 'url': 'https://www.lupus-france.fr'},
                    {'title': 'Filière des maladies auto-immunes et auto-inflammatoires rares', 'description': 'Réseau de santé dédié aux maladies auto-immunes', 'url': 'https://www.fai2r.org'},
                    {'title': 'Orphanet - Lupus érythémateux disséminé', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=536'},
                    {'title': 'Société Nationale Française de Médecine Interne', 'description': 'Recommandations professionnelles', 'url': 'https://www.snfmi.org'}
                ]
            },
            
            # 14. Maladie auto-immune - Sclérodermie systémique
            {
                'name': 'Sclérodermie systémique',
                'scientific_name': 'Systemic sclerosis',
                'category': 'Médecine interne',
                'prevalence': '15-30 cas pour 100 000 habitants, 4 femmes pour 1 homme',
                'age_group': '30-50 ans, mais peut survenir à tout âge',
                'risk_factors': 'Prédisposition génétique, exposition à la silice, solvants organiques, infections, médicaments (bléomycine, taxanes)',
                'diagnosis': 'Critères ACR/EULAR 2013, capillaroscopie, anticorps spécifiques (anti-centromère, anti-topoisomérase I, anti-ARN polymérase III), épreuves fonctionnelles respiratoires, échocardiographie',
                'differential_diagnosis': 'Sclérodermie localisée, syndrome de Sharp, dermatomyosite, syndrome de chevauchement, scléromyxœdème, amylose',
                'follow_up': 'Suivi clinique régulier, épreuves fonctionnelles respiratoires, échocardiographie, bilan rénal, capillaroscopie, évaluation de l\'atteinte digestive',
                'references': 'Recommandations EULAR 2017, SNFMI 2019',
                'short_description': 'Maladie auto-immune rare caractérisée par une fibrose cutanée et viscérale, une atteinte microvasculaire et des anomalies immunitaires',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Phénomène de Raynaud, épaississement cutané, dyspnée, reflux gastro-œsophagien, douleurs articulaires, ulcérations digitales',
                'description': (
                    "La sclérodermie systémique est une maladie auto-immune rare et complexe caractérisée par trois mécanismes physiopathologiques principaux : "
                    "une dysfonction endothéliale avec atteinte microvasculaire, une activation immunitaire avec production d'auto-anticorps spécifiques, et une "
                    "activation des fibroblastes conduisant à une accumulation excessive de matrice extracellulaire et à une fibrose tissulaire. La maladie se présente "
                    "sous deux formes principales : la forme cutanée limitée (atteinte cutanée distale aux coudes et genoux) et la forme cutanée diffuse (atteinte cutanée "
                    "proximale et tronculaire). Le pronostic est principalement conditionné par l'atteinte viscérale, notamment pulmonaire, cardiaque et rénale."
                ),
                'causes': (
                    "Prédisposition génétique (gènes HLA, IRF5, STAT4, TNFAIP3, etc.)\n"
                    "Facteurs environnementaux (exposition professionnelle à la silice, solvants organiques, pesticides)\n"
                    "Microchimérisme fœtal (persistance de cellules fœtales chez la mère après grossesse)\n"
                    "Infections (cytomégalovirus, parvovirus B19, virus d'Epstein-Barr)\n"
                    "Médicaments (bléomycine, taxanes, amphétamines, ergotamine)"
                ),
                'treatment': (
                    "Traitement du phénomène de Raynaud (inhibiteurs calciques, inhibiteurs des récepteurs de l'endothéline, analogues des prostacyclines)\n"
                    "Traitement des ulcères digitaux (inhibiteurs des phosphodiestérases de type 5, analogues des prostacyclines, soins locaux)\n"
                    "Traitement de l'hypertension artérielle pulmonaire (antagonistes des récepteurs de l'endothéline, inhibiteurs des phosphodiestérases de type 5, analogues des prostacyclines)\n"
                    "Traitement de l'atteinte pulmonaire interstitielle (mycophénolate mofétil, cyclophosphamide, rituximab, nintedanib)\n"
                    "Traitement du reflux gastro-œsophagien (inhibiteurs de la pompe à protons, prokinétiques)\n"
                    "Traitement de la crise rénale sclérodermique (inhibiteurs de l'enzyme de conversion, antagonistes des récepteurs de l'angiotensine II, hémodialyse si nécessaire)\n"
                    "Rééducation fonctionnelle et ergothérapie"
                ),
                'prevention': 'Pas de prévention primaire connue',
                'prevention_details': (
                    "- Éviction des facteurs déclenchants du phénomène de Raynaud (froid, stress, tabac, médicaments vasoconstricteurs)\n"
                    "- Protection contre le froid (gants, vêtements chauds, chaufferettes)\n"
                    "- Arrêt impératif du tabac\n"
                    "- Éviction des expositions professionnelles à risque (silice, solvants organiques)\n"
                    "- Soins cutanés hydratants réguliers\n"
                    "- Surveillance régulière de la pression artérielle et de la fonction rénale"
                ),
                'complications': (
                    "Hypertension artérielle pulmonaire (complication grave engageant le pronostic vital)\n"
                    "Pneumopathie interstitielle diffuse pouvant évoluer vers l'insuffisance respiratoire chronique\n"
                    "Crise rénale sclérodermique (urgence médicale)\n"
                    "Troubles du rythme et insuffisance cardiaque\n"
                    "Malnutrition et dénutrition liées à l'atteinte digestive sévère\n"
                    "Ulcères digitaux et nécroses digitales\n"
                    "Syndrome sec et syndrome de Gougerot-Sjögren associé"
                ),
                'when_to_see_doctor': (
                    "Aggravation du phénomène de Raynaud ou apparition d'ulcérations digitales\n"
                    "Essoufflement à l'effort ou au repos\n"
                    "Douleur thoracique, palpitations ou syncopes\n"
                    "Œdèmes des membres inférieurs ou prise de poids rapide\n"
                    "Troubles de la déglutition ou perte de poids inexpliquée\n"
                    "Diarrhée chronique ou alternance diarrhée/constipation\n"
                    "Signes d'infection (fièvre, frissons, toux productive)"
                ),
                'resources': [
                    {'title': 'Association des Sclérodermiques de France', 'description': 'Association de patients et d\'information sur la sclérodermie', 'url': 'https://www.association-sclerodermie.fr'},
                    {'title': 'Filière des maladies auto-immunes et auto-inflammatoires rares', 'description': 'Réseau de santé dédié aux maladies auto-immunes', 'url': 'https://www.fai2r.org'},
                    {'title': 'Orphanet - Sclérodermie systémique', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=90291'},
                    {'title': 'Société Française de Médecine Vasculaire', 'description': 'Recommandations sur la prise en charge du phénomène de Raynaud', 'url': 'https://www.sfmv.org'}
                ]
            },
            
            # 15. Maladie auto-immune - Maladie de Behçet
            {
                'name': 'Maladie de Behçet',
                'scientific_name': 'Morbus Behçet',
                'category': 'Médecine interne',
                'prevalence': '1-10 cas pour 100 000 habitants en Europe, plus fréquent sur la route de la soie',
                'age_group': '20-40 ans, rare avant la puberté et après 50 ans',
                'risk_factors': 'Prédisposition génétique (HLA-B51), facteurs environnementaux (infections, stress), origine géographique (Méditerranée, Moyen-Orient, Asie)',
                'diagnosis': 'Critères de l\'ICBD 2014, pathergie, imagerie (IRM cérébrale, angio-TDM/angio-IRM, échographie doppler)',
                'differential_diagnosis': 'Syndrome de Reiter, maladie de Crohn, sarcoïdose, lupus érythémateux disséminé, syndrome de Sweet, infections (herpès, syphilis)',
                'follow_up': 'Suivi clinique régulier, bilan ophtalmologique, imagerie cérébrale si symptômes neurologiques, surveillance des traitements immunosuppresseurs',
                'references': 'Recommandations EULAR 2018, SNFMI 2020',
                'short_description': 'Vascularite systémique caractérisée par des aphtes buccaux récidivants, des ulcérations génitales et une atteinte oculaire, articulaire, cutanée ou neurologique',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Aphtes buccaux récidivants, ulcérations génitales, érythème noueux, uvéite, arthralgies, manifestations neurologiques',
                'description': (
                    "La maladie de Behçet est une vascularite systémique d'étiologie inconnue, caractérisée par une inflammation des vaisseaux sanguins de tous calbres. "
                    "Elle se manifeste par des poussées de symptômes variés, les plus caractéristiques étant des aphtes buccaux récidivants, des ulcérations génitales, "
                    "des lésions cutanées (érythème noueux, pseudofolliculite) et une atteinte oculaire (uvéite). La maladie peut également toucher les articulations, le système "
                    "nerveux central, le tube digestif et les vaisseaux de gros calbre. L'évolution est imprévisible, marquée par des poussées et des rémissions. "
                    "La maladie est plus fréquente et souvent plus sévère chez les hommes jeunes. Le pronostic est principalement conditionné par l'atteinte neurologique, "
                    "oculaire et vasculaire."
                ),
                'causes': (
                    "Prédisposition génétique (association avec HLA-B51, gènes IL10, IL23R-IL12RB2, ERAP1, etc.)\n"
                    "Facteurs environnementaux (infections bactériennes ou virales, stress, traumatismes)\n"
                    "Dysfonctionnement immunitaire avec activation des neutrophiles et des lymphocytes T\n"
                    "Altération de l'endothélium vasculaire\n"
                    "Facteurs géographiques (prévalence plus élevée le long de l'ancienne route de la soie)"
                ),
                'treatment': (
                    "Traitement local des lésions cutanéo-muqueuses (corticoïdes locaux, anesthésiques locaux, colchicine)\n"
                    "Traitement de l'uvéite (colchicine, corticoïdes locaux et généraux, immunosuppresseurs : azathioprine, ciclosporine, interféron-alpha)\n"
                    "Traitement des formes sévères (corticoïdes à fortes doses, cyclophosphamide, anti-TNF alpha, interféron-alpha, tocilizumab)\n"
                    "Traitement de la thrombose veineuse (anticoagulation après mise en place d'un traitement immunosuppresseur)\n"
                    "Traitement des manifestations articulaires (AINS, colchicine, sulfasalazine, anti-TNF alpha)\n"
                    "Prise en charge de la douleur et des symptômes"
                ),
                'prevention': 'Pas de prévention primaire connue',
                'prevention_details': (
                    "- Éviction des facteurs déclenchants des poussées (stress, traumatismes, infections)\n"
                    "- Hygiène bucco-dentaire rigoureuse\n"
                    "- Protection oculaire (lunettes de soleil, suivi ophtalmologique régulier)\n"
                    "- Éviction des aliments acides ou irritants en cas d'aphtes\n"
                    "- Arrêt du tabac (aggrave les lésions vasculaires et la maladie)\n"
                    "- Activité physique adaptée"
                ),
                'complications': (
                    "Cécité par uvéite ou vascularite rétinienne\n"
                    "Thromboses veineuses profondes et superficielles, thrombophlébite\n"
                    "Anévrismes artériels (risque de rupture)\n"
                    "Atteinte neurologique centrale (méningo-encéphalite, thrombophlébite cérébrale, atteinte du tronc cérébral)\n"
                    "Perforations et hémorragies digestives dans les formes intestinales\n"
                    "Amylose secondaire\n"
                    "Complications iatrogènes des traitements immunosuppresseurs"
                ),
                'when_to_see_doctor': (
                    "Apparition ou aggravation des aphtes buccaux ou génitaux\n"
                    "Baisse brutale de l'acuité visuelle ou douleur oculaire\n"
                    "Céphalées inhabituelles ou troubles neurologiques (troubles de l'équilibre, de la parole, faiblesse musculaire)\n"
                    "Douleur thoracique ou essoufflement\n"
                    "Œdème ou douleur d'un membre (suspicion de thrombose veineuse profonde)\n"
                    "Sang dans les selles ou douleurs abdominales intenses\n"
                    "Fièvre inexpliquée ou altération de l'état général"
                ),
                'resources': [
                    {'title': 'Association Française de la Maladie de Behçet', 'description': 'Association de patients et d\'information sur la maladie de Behçet', 'url': 'https://association-behcet.fr'},
                    {'title': 'Centre de Référence des Maladies Auto-immunes Systémiques Rares', 'description': 'Informations sur les centres experts', 'url': 'https://www.cri-net.com'},
                    {'title': 'Orphanet - Maladie de Behçet', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=117'},
                    {'title': 'Société Nationale Française de Médecine Interne', 'description': 'Recommandations professionnelles', 'url': 'https://www.snfmi.org'}
                ]
            },
            
            # 16. Trouble neurologique - Tremblement essentiel
            {
                'name': 'Tremblement essentiel',
                'scientific_name': 'Essential tremor',
                'category': 'Neurologie',
                'prevalence': '0.4-5% de la population, jusqu\'à 20% chez les plus de 65 ans',
                'age_group': 'Tous âges, avec deux pics de fréquence (jeune adulte et après 60 ans)',
                'risk_factors': 'Antécédents familiaux (transmission autosomique dominante dans 50% des cas), âge, exposition à certains toxiques',
                'diagnosis': 'Examen clinique, élimination des autres causes de tremblement, tests d\'écriture et de dessin, éventuellement EMG',
                'differential_diagnosis': 'Maladie de Parkinson, tremblement physiologique exagéré, tremblement cérébelleux, dystonie, hyperthyroïdie, effets secondaires médicamenteux',
                'follow_up': 'Consultations neurologiques régulières, évaluation de l\'impact sur la qualité de vie, adaptation du traitement',
                'references': 'Recommandations ANAES 2004, MDS Evidence-Based Review 2018',
                'short_description': 'Trouble neurologique fréquent caractérisé par des tremblements rythmiques des mains, de la tête ou de la voix, en l\'absence d\'autre cause identifiée',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Tremblements des mains lors du maintien des postures ou des mouvements, tremblement de la tête ou de la voix, amélioration au repos et sous alcool',
                'description': (
                    "Le tremblement essentiel est le trouble du mouvement le plus fréquent. Il se caractérise par des tremblements rythmiques involontaires qui surviennent principalement "
                    "lors du maintien d'une posture ou lors de mouvements volontaires. Contrairement à la maladie de Parkinson, le tremblement est généralement plus marqué à l'action "
                    "qu'au repos. L'évolution est lentement progressive et variable d'un individu à l'autre. Bien que souvent considéré comme bénin, le tremblement essentiel peut "
                    "avoir un impact considérable sur la qualité de vie, gênant les activités quotidiennes comme écrire, boire ou se maquiller. Dans environ 50% des cas, il existe "
                    "des antécédents familiaux, suggérant une composante génétique. Le diagnostic est clinique et repose sur l'exclusion des autres causes de tremblement."
                ),
                'causes': (
                    "Prédisposition génétique (mutations identifiées dans les gènes LINGO1, FUS, TENM4, etc. dans certaines formes familiales)\n"
                    "Altérations des voies cérébelleuses et des noyaux gris centraux\n"
                    "Dysfonctionnement des systèmes inhibiteurs GABAergiques\n"
                    "Facteurs environnementaux (certains toxiques, stress, fatigue, caféine peuvent aggraver les symptômes)\n"
                    "Âge (prévalence et sévérité augmentent avec l'âge)"
                ),
                'treatment': (
                    "Traitement médicamenteux en première intention : propranolol (bêta-bloquant) ou primidone (anti-épileptique)\n"
                    "Autres options médicamenteuses : topiramate, gabapentine, benzodiazépines (clonazépam), injections de toxine botulique pour les tremblements de la tête ou de la voix\n"
                    "Mesures non médicamenteuses : kinésithérapie, ergothérapie, aides techniques (ustensiles adaptés, poids pour les poignets)\n"
                    "Traitements chirurgicaux pour les formes sévères : stimulation cérébrale profonde (noyau ventral intermédiaire du thalamus)\n"
                    "Éviction des facteurs aggravants (caféine, stress, fatigue, certains médicaments)"
                ),
                'prevention': 'Aucune prévention connue',
                'prevention_details': (
                    "- Pas de prévention primaire connue\n"
                    "- Éviction des facteurs aggravants (caféine, stress, fatigue)\n"
                    "- Prise en charge précoce pour limiter l'impact sur la qualité de vie\n"
                    "- Éducation thérapeutique du patient et de son entourage\n"
                    "- Activité physique régulière pour maintenir la coordination et la force musculaire"
                ),
                'complications': (
                    "Handicap fonctionnel important dans les activités de la vie quotidienne\n"
                    "Isolement social et retrait des activités de loisirs\n"
                    "Anxiété et dépression réactionnelle\n"
                    "Difficultés professionnelles pouvant mener à un arrêt de travail ou une reconversion\n"
                    "Effets secondaires des traitements médicamenteux (fatigue, étourdissements, troubles de l'érection avec les bêta-bloquants)"
                ),
                'when_to_see_doctor': (
                    "Apparition de tremblements gênants dans la vie quotidienne\n"
                    "Aggravation brutale des symptômes\n"
                    "Apparition d'autres symptômes neurologiques (raideur, lenteur, troubles de l'équilibre, troubles cognitifs)\n"
                    "Inefficacité ou effets secondaires des traitements en cours\n"
                    "Retentissement psychologique important (anxiété, dépression, isolement)"
                ),
                'resources': [
                    {'title': 'France Parkinson - Fiche sur le tremblement essentiel', 'description': 'Informations détaillées sur le tremblement essentiel', 'url': 'https://www.franceparkinson.fr/maladie-de-parkinson-et-troubles-apparentes/tremblement-essentiel/'},
                    {'title': 'Orphanet - Tremblement essentiel', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=86809'},
                    {'title': 'Société Française de Neurologie', 'description': 'Recommandations professionnelles', 'url': 'https://www.sf-neuro.org'},
                    {'title': 'Association des Personnes Concernées par le Tremblement Essentiel', 'description': 'Association de patients', 'url': 'https://www.aptes.org'}
                ]
            },
            
            # 17. Maladie neurologique - Dystonie
            {
                'name': 'Dystonie',
                'scientific_name': 'Dystonia',
                'category': 'Neurologie',
                'prevalence': 'Varie selon le type (15-30/100 000 pour les formes généralisées, plus fréquent pour les formes focales)',
                'age_group': 'Tous âges, selon le type (formes précoces avant 26 ans, formes tardives après)',
                'risk_factors': 'Prédisposition génétique, antécédents familiaux, traumatisme, prise de neuroleptiques, accident vasculaire cérébral',
                'diagnosis': 'Examen clinique, tests génétiques pour certaines formes, IRM cérébrale, électromyographie, tests pharmacologiques',
                'differential_diagnosis': 'Troubles psychogènes, contractures musculaires, tics, maladie de Parkinson, spasticité, syndrome de Gilles de la Tourette',
                'follow_up': 'Consultations neurologiques régulières, évaluation de la réponse aux traitements, adaptation thérapeutique, prise en charge multidisciplinaire',
                'references': 'Recommandations EFNS 2011, MDS Evidence-Based Review 2018',
                'short_description': 'Trouble du mouvement caractérisé par des contractions musculaires involontaires, soutenues ou intermittentes, entraînant des postures anormales et/ou des mouvements répétitifs',
                'severity': 'M',
                'is_emergency': False,
                'main_symptoms': 'Contractions musculaires involontaires, postures anormales, mouvements répétitifs ou de torsion, douleurs musculaires, aggravation avec le stress et la fatigue',
                'description': (
                    "La dystonie est un trouble du mouvement complexe caractérisé par des contractions musculaires involontaires soutenues ou intermittentes, entraînant des mouvements "
                    "et/ou des postures anormales, souvent répétitifs. Ces contractions peuvent être douloureuses et entraver considérablement les activités quotidiennes. "
                    "La dystonie peut être classée selon sa distribution (focale, segmentaire, multifocale, généralisée ou hémidystonie) ou son étiologie (génétique, acquise ou idiopathique). "
                    "Les formes focales, comme le torticolis spasmodique ou le blépharospasme, sont les plus fréquentes chez l'adulte. La dystonie peut être isolée ou associée à d'autres "
                    "troubles neurologiques. Le diagnostic repose principalement sur l'examen clinique et l'élimination des causes secondaires."
                ),
                'causes': (
                    "Formes génétiques (mutations dans les gènes TOR1A, THAP1, GCH1, ATP1A3, etc. pour les dystonies monogéniques)\n"
                    "Causes acquises (traumatisme crânien, accident vasculaire cérébral, encéphalite, tumeur, exposition à des toxiques, médicaments neuroleptiques)\n"
                    "Formes idiopathiques (sans cause identifiée)\n"
                    "Troubles métaboliques (maladie de Wilson, maladie de Niemann-Pick type C)\n"
                    "Troubles neurodégénératifs (maladie de Parkinson, chorée de Huntington, ataxies cérébelleuses)"
                ),
                'treatment': (
                    "Injections de toxine botulique (traitement de première intention pour les formes focales et segmentaires)\n"
                    "Traitements médicamenteux : anticholinergiques (trihexyphénidyle), benzodiazépines, baclofène, tétrabénazine, L-dopa (pour les formes dopa-sensibles)\n"
                    "Traitements chirurgicaux : stimulation cérébrale profonde (globus pallidus interne) pour les formes sévères et généralisées\n"
                    "Rééducation fonctionnelle (kinésithérapie, ergothérapie, orthophonie selon la localisation)\n"
                    "Mesures complémentaires : gestion du stress, techniques de relaxation, soutien psychologique\n"
                    "Prise en charge de la douleur si nécessaire"
                ),
                'prevention': 'Limité aux formes secondaires',
                'prevention_details': (
                    "- Éviction des neuroleptiques en cas d'antécédent de dystonie aiguë\n"
                    "- Dépistage génétique et conseil génétique pour les formes héréditaires\n"
                    "- Prise en charge précoce des symptômes pour prévenir les rétractions et déformations\n"
                    "- Éviction des facteurs aggravants (stress, fatigue, certains médicaments)\n"
                    "- Activité physique adaptée pour maintenir la mobilité articulaire"
                ),
                'complications': (
                    "Rétractions tendineuses et déformations articulaires dans les formes sévères\n"
                    "Douleurs musculaires et articulaires chroniques\n"
                    "Difficultés fonctionnelles majeures (marche, écriture, parole, déglutition)\n"
                    "Isolement social et difficultés professionnelles\n"
                    "Troubles anxio-dépressifs réactionnels\n"
                    "Effets secondaires des traitements (sécheresse buccale, troubles de la mémoire avec les anticholinergiques, faiblesse musculaire avec la toxine botulique)"
                ),
                'when_to_see_doctor': (
                    "Apparition de postures ou mouvements anormaux involontaires\n"
                    "Aggravation brutale des symptômes\n"
                    "Apparition de difficultés à marcher, parler ou avaler\n"
                    "Douleurs importantes liées aux contractions musculaires\n"
                    "Inefficacité ou effets secondaires des traitements en cours\n"
                    "Signes de dépression ou d'isolement social"
                ),
                'resources': [
                    {'title': 'France Dystonie', 'description': 'Association de patients atteints de dystonie', 'url': 'https://www.france-dystonie.org'},
                    {'title': 'Orphanet - Dystonies', 'description': 'Fiches d\'information sur les différentes formes de dystonie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR'},
                    {'title': 'Société Française de Neurologie', 'description': 'Recommandations professionnelles', 'url': 'https://www.sf-neuro.org'},
                    {'title': 'Dystonia Medical Research Foundation', 'description': 'Informations scientifiques et recherche sur la dystonie (en anglais)', 'url': 'https://dystonia-foundation.org'}
                ]
            },
            
            # 18. Maladie neurologique - Maladie de Huntington
            {
                'name': 'Maladie de Huntington',
                'scientific_name': 'Chorea Huntington',
                'category': 'Neurologie',
                'prevalence': '5-10 cas pour 100 000 habitants en Europe occidentale',
                'age_group': 'Début généralement entre 30 et 50 ans (forme adulte), formes juvéniles et tardives possibles',
                'risk_factors': 'Antécédent familial, transmission autosomique dominante, expansion anormale de triplets CAG sur le gène HTT',
                'diagnosis': 'Test génétique (nombre de répétitions CAG), IRM cérébrale, évaluation neuropsychologique, examen clinique',
                'differential_diagnosis': 'Autres chorées (chorée de Sydenham, chorée gravidique, médicaments), maladie de Wilson, neuroacanthocytose, maladie de Fahr, démences sous-corticales',
                'follow_up': 'Prise en charge multidisciplinaire, consultations neurologiques régulières, évaluations neuropsychologiques, suivi psychiatrique, soutien social',
                'references': 'Recommandations EHDN 2019, HAS 2020',
                'short_description': 'Maladie neurodégénérative héréditaire caractérisée par des mouvements choréiques, des troubles psychiatriques et une détérioration cognitive progressive',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Mouvements choréiques involontaires, troubles de l\'humeur, troubles cognitifs, difficultés de déglutition et d\'élocution, perte de poids',
                'description': (
                    "La maladie de Huntington est une affection neurodégénérative héréditaire rare, transmise sur un mode autosomique dominant. Elle est causée par une expansion anormale "
                    "de triplets CAG dans le gène HTT, codant pour la huntingtine. La maladie se caractérise par une triade de symptômes : mouvements anormaux involontaires (chorée, dystonie), "
                    "troubles psychiatriques (dépression, anxiété, psychose, apathie) et déclin cognitif progressif. L'âge de début est généralement entre 30 et 50 ans, avec une évolution "
                    "progressive sur 15 à 20 ans. Les formes juvéniles (début avant 20 ans) sont plus rares et se manifestent différemment (rigidité, myoclonies, épilepsie). La maladie affecte "
                    "considérablement la qualité de vie des patients et de leurs proches, avec un impact majeur sur l'autonomie et les interactions sociales."
                ),
                'causes': (
                    "Mutation génétique : expansion anormale de triplets CAG (>36 répétitions) dans l'exon 1 du gène HTT sur le chromosome 4\n"
                    "Transmission autosomique dominante (50% de risque pour chaque enfant d'un parent atteint)\n"
                    "Corrélation inverse entre le nombre de répétitions CAG et l'âge de début\n"
                    "Phénomène d'anticipation (début plus précoce et parfois plus sévère dans les générations successives, surtout en transmission paternelle)"
                ),
                'treatment': (
                    "Traitement symptomatique des mouvements anormaux : tétrabénazine, deutétrabénazine, neuroleptiques atypiques (olanzapine, rispéridone, tiapride)\n"
                    "Prise en charge psychiatrique : antidépresseurs, anxiolytiques, antipsychotiques selon les symptômes\n"
                    "Prise en charge des troubles du comportement : approches non médicamenteuses, éducation des aidants\n"
                    "Rééducation : orthophonie, kinésithérapie, ergothérapie\n"
                    "Soutien nutritionnel (adaptation des textures, supplémentation, gastrostomie si nécessaire)\n"
                    "Suivi multidisciplinaire (neurologue, psychiatre, infirmier, assistant social, généticien)"
                ),
                'prevention': 'Conseil génétique et diagnostic présymptomatique',
                'prevention_details': (
                    "- Conseil génétique pour les personnes à risque\n"
                    "- Dépistage génétique présymptomatique avec accompagnement psychologique\n"
                    "- Diagnostic prénatal ou diagnostic préimplantatoire pour les couples à risque\n"
                    "- Éviction des facteurs aggravants (stress, fatigue, certains médicaments)\n"
                    "- Maintien d'une activité physique et intellectuelle"
                ),
                'complications': (
                    "Complications liées aux troubles de la déglutition (fausses routes, pneumopathies d'inhalation)\n"
                    "Dénutrition et perte de poids\n"
                    "Complications de décubitus (escarres, infections urinaires, thromboses veineuses profondes)\n"
                    "Troubles du comportement avec mise en danger (conduite automobile, comportements inappropriés)\n"
                    "Dépression avec risque suicidaire (particulièrement en phase présymptomatique et au début de la maladie)\n"
                    "Aggravation progressive vers un état grabataire nécessitant une assistance complète"
                ),
                'when_to_see_doctor': (
                    "Apparition de mouvements anormaux involontaires\n"
                    "Troubles de l'humeur ou du comportement inexpliqués\n"
                    "Difficultés cognitives ou de concentration inhabituelles\n"
                    "Problèmes d'équilibre ou de coordination\n"
                    "Difficultés à parler ou à avaler\n"
                    "Perte de poids inexpliquée\n"
                    "Idées suicidaires ou dépression"
                ),
                'resources': [
                    {'title': 'Association Huntington France', 'description': 'Association de patients et familles concernées par la maladie de Huntington', 'url': 'https://www.huntington.fr'},
                    {'title': 'Orphanet - Maladie de Huntington', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=399'},
                    {'title': 'European Huntington\'s Disease Network', 'description': 'Réseau européen sur la maladie de Huntington (en anglais)', 'url': 'https://www.ehdn.org'},
                    {'title': 'HAS - Maladie de Huntington', 'description': 'Recommandations de la Haute Autorité de Santé', 'url': 'https://www.has-sante.fr'}
                ]
            },
            
            # 19. Maladie neurologique - Sclérose latérale amyotrophique (SLA)
            {
                'name': 'Sclérose latérale amyotrophique',
                'scientific_name': 'Amyotrophic lateral sclerosis (ALS)',
                'category': 'Neurologie',
                'prevalence': '5-7 cas pour 100 000 habitants',
                'age_group': 'Principalement 50-70 ans, avec un pic vers 65 ans',
                'risk_factors': 'Âge, sexe masculin (ratio 1.5:1), tabagisme, exposition aux pesticides, antécédents familiaux (dans 10% des cas)',
                'diagnosis': "Critères d'El Escorial révisés, EMG, IRM médullaire et cérébrale, ponction lombaire, bilan biologique exhaustif, tests génétiques si forme familiale suspectée",
                'differential_diagnosis': 'Myélopathie cervicale, neuropathies motrices multifocales, sclérose en plaques, myasthénie, syndrome post-poliomyélitique, maladies du motoneurone héréditaires',
                'follow_up': 'Prise en charge multidisciplinaire dans des centres de référence, consultations régulières, évaluation des fonctions respiratoires et nutritionnelles, adaptation des aides techniques',
                'references': 'Recommandations HAS 2017, EFNS 2012, AAN 2009',
                'short_description': 'Maladie neurodégénérative fatale caractérisée par une atteinte progressive des motoneurones centraux et périphériques, entraînant une paralysie musculaire progressive',
                'severity': 'H',
                'is_emergency': False,
                'main_symptoms': 'Faiblesse musculaire progressive, atrophie musculaire, crampes, fasciculations, troubles de l\'élocution et de la déglutition, difficultés respiratoires',
                'description': (
                    "La sclérose latérale amyotrophique (SLA), également connue sous le nom de maladie de Charcot, est une maladie neurodégénérative rare mais grave qui affecte "
                    "sélectivement les motoneurones, cellules nerveuses qui contrôlent les muscles volontaires. La maladie se caractérise par une dégénérescence progressive "
                    "des motoneurones centraux (dans le cerveau) et périphériques (dans la moelle épinière), entraînant une faiblesse musculaire, une atrophie et finalement "
                    "une paralysie complète. Les fonctions cognitives et sensorielles sont généralement épargnées, bien qu'une atteinte frontotemporale soit observée chez "
                    "certains patients. L'évolution est variable mais généralement rapide, avec une médiane de survie de 3 à 5 ans après le diagnostic. La maladie reste "
                    "incurable à ce jour, mais des traitements peuvent en ralentir la progression et améliorer la qualité de vie des patients."
                ),
                'causes': (
                    "Dans 90% des cas, la cause est inconnue (formes sporadiques)\n"
                    "Dans 10% des cas, forme familiale avec transmission autosomique dominante (mutations identifiées dans les gènes C9ORF72, SOD1, TARDBP, FUS, etc.)\n"
                    "Facteurs environnementaux suspectés (tabagisme, exposition aux pesticides, métaux lourds, activité physique intense, traumatismes crâniens répétés)\n"
                    "Mécanismes physiopathologiques impliqués : stress oxydatif, excitotoxicité glutamatergique, agrégation protéique anormale, inflammation, dysfonction mitochondriale"
                ),
                'treatment': (
                    "Riluzole (Rilutek®) : seul traitement ayant démontré un allongement modeste de la survie\n"
                    "Édavarone (Radicava®) : antioxydant ayant montré un ralentissement du déclin fonctionnel\n"
                    "Traitement symptomatique : antispastiques, antalgiques, antidépresseurs, anticholinergiques pour l'hypersialorrhée\n"
                    "Ventilation non invasive pour l'insuffisance respiratoire\n"
                    "Nutrition entérale par gastrostomie en cas de troubles sévères de la déglutition\n"
                    "Rééducation fonctionnelle (kinésithérapie, orthophonie, ergothérapie)\n"
                    "Soins de support et accompagnement psychologique\n"
                    "Suivi multidisciplinaire dans des centres spécialisés"
                ),
                'prevention': 'Aucune prévention connue',
                'prevention_details': (
                    "- Pas de prévention primaire connue pour les formes sporadiques\n"
                    "- Éviction des facteurs de risque potentiels (tabac, exposition aux toxiques)\n"
                    "- Conseil génétique pour les formes familiales\n"
                    "- Diagnostic présymptomatique discuté au cas par cas dans les formes familiales\n"
                    "- Recherche active de facteurs de risque modifiables dans les études en cours"
                ),
                'complications': (
                    "Insuffisance respiratoire restrictive (cause principale de décès)\n"
                    "Dénutrition et déshydratation liées aux troubles de la déglutition\n"
                    "Escarres et infections cutanées\n"
                    "Thrombose veineuse profonde et embolie pulmonaire\n"
                    "Syndrome pseudobulbaire (rire et pleurer spasmodiques)\n"
                    "Détresse psychologique, dépression, troubles anxieux\n"
                    "Syndrome d'épuisement de l'aidant"
                ),
                'when_to_see_doctor': (
                    "Faiblesse musculaire progressive inexpliquée\n"
                    "Difficultés à marcher, à monter les escaliers ou à effectuer des gestes fins\n"
                    "Troubles de l'élocution ou de la déglutition\n"
                    "Crampes musculaires fréquentes et fasciculations\n"
                    "Essoufflement à l'effort ou en position couchée\n"
                    "Perte de poids inexpliquée\n"
                    "Signes de dépression ou d'anxiété"
                ),
                'resources': [
                    {'title': 'Association pour la Recherche sur la SLA (ARSLA)', 'description': 'Association de patients et de soutien à la recherche sur la SLA', 'url': 'https://www.arsla.org'},
                    {'title': 'Orphanet - Sclérose latérale amyotrophique', 'description': 'Fiche d\'information sur la maladie', 'url': 'https://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=FR&Expert=803'},
                    {'title': 'Filière de Santé des Maladies du Motoneurone', 'description': 'Réseau de soins pour les maladies du motoneurone', 'url': 'https://www.filieres-maladies-rares.fr/filieres/filmn/'},
                    {'title': 'Haute Autorité de Santé - SLA', 'description': 'Recommandations de bonnes pratiques', 'url': 'https://www.has-sante.fr'}
                ]
            }
        ]

        # Création des maladies dans la base de données
        for disease_data in diseases_data:
            category_name = disease_data.pop('category').lower()
            category = created_categories.get(category_name)
            
            # Création du slug à partir du nom
            slug = slugify(disease_data['name'])
            
            # Création de la maladie avec les nouveaux champs
            disease, created = Disease.objects.update_or_create(
                name=disease_data['name'],
                defaults={
                    'slug': slug,
                    'category': category,
                    'scientific_name': disease_data.get('scientific_name', ''),
                    'short_description': disease_data.get('short_description', ''),
                    'description': disease_data.get('description', ''),
                    'main_symptoms': disease_data.get('main_symptoms', ''),
                    'causes': disease_data.get('causes', ''),
                    'treatment': disease_data.get('treatment', ''),
                    'prevention': disease_data.get('prevention', ''),
                    'prevention_details': disease_data.get('prevention_details', ''),
                    'when_to_see_doctor': disease_data.get('when_to_see_doctor', ''),
                    'useful_links': disease_data.get('useful_links', ''),
                    'prognosis': disease_data.get('prognosis', '') or (disease_data.get('complications', '') + '\n\n' + disease_data.get('additional_notes', '')),
                    'severity': disease_data.get('severity', 'M'),
                    'is_emergency': disease_data.get('is_emergency', False),
                    'is_published': True
                }
            )
            
            # Ajout des ressources si la maladie est nouvelle
            if created and 'resources' in disease_data:
                for resource in disease_data['resources']:
                    DiseaseResource.objects.create(
                        disease=disease,
                        title=resource['title'],
                        url=resource['url'],
                        description=resource.get('description', '')
                    )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Maladie créée : {disease.name}"))
            else:
                self.stdout.write(f"La maladie {disease.name} a été mise à jour")
        
        self.stdout.write(self.style.SUCCESS('Données de test détaillées créées avec succès!'))
