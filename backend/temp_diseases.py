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
            # 1. Maladies cardiologiques
            {
                'name': 'Hypertension artérielle',
                'scientific_name': 'Hypertensio arterialis',
                'category': 'Cardiologie',
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
                'prevention': (
                    "Surveillance régulière de la tension artérielle\n"
                    "Alimentation équilibrée (régime DASH riche en fruits, légumes et céréales complètes)\n"
                    "Réduction de la consommation de sel\n"
                    "Activité physique régulière\n"
                    "Maintien d'un poids santé\n"
                    "Gestion du stress"
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
                    "Premier diagnostic d'hypertension\n"
                    "Maux de tête sévères et persistants\n"
                    "Essoufflement inhabituel\n"
                    "Saignements de nez fréquents\n"
                    "Vision trouble\n"
                    "Douleur thoracique"
                ),
                'resources': [
                    {'title': 'Fédération Française de Cardiologie', 'description': 'Informations sur les maladies cardiovasculaires', 'url': 'https://fedecardio.org'},
                    {'title': 'Société Française d\'Hypertension Artérielle', 'description': 'Recommandations et actualités sur l\'HTA', 'url': 'http://www.sfhta.eu'},
                    {'title': 'Ameli.fr - Hypertension artérielle', 'description': 'Informations officielles de l\'Assurance Maladie', 'url': 'https://www.ameli.fr/assure/sante/themes/hypertension-arterelle-hta'}
                ]
            },
            # Autres maladies...
        ]

        # Création des maladies dans la base de données
        for disease_data in diseases_data:
            category_name = disease_data.pop('category').lower()
            category = created_categories.get(category_name)
            
            # Création du slug à partir du nom
            slug = slugify(disease_data['name'])
            
            # Création de la maladie
            disease, created = Disease.objects.get_or_create(
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
                    'prognosis': (disease_data.get('complications', '') + 
                                 '\n\nQuand consulter un médecin :\n' + 
                                 disease_data.get('when_to_see_doctor', '')),
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
                        description=resource['description']
                    )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Maladie créée : {disease.name}"))
            else:
                self.stdout.write(f"La maladie {disease.name} existe déjà")
        
        self.stdout.write(self.style.SUCCESS('Données de test détaillées créées avec succès!'))
