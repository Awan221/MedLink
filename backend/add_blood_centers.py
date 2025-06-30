import os
import django

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def create_blood_centers():
    from bloodbank.models import BloodDonationCenter
    from django.contrib.gis.geos import Point
    
    # Coordonnées de Dakar (approximatives)
    dakar_centers = [
        {
            'name': 'Centre National de Transfusion Sanguine',
            'address': 'Avenue Nelson Mandela, Dakar',
            'city': 'Dakar',
            'region': 'Dakar',
            'phone': '33 889 10 10',
            'email': 'cnts@cnts.sn',
            'location': Point(-17.4676861, 14.716677)
        },
        {
            'name': 'Hôpital Principal de Dakar',
            'address': 'Avenue Nelson Mandela, Dakar',
            'city': 'Dakar',
            'region': 'Dakar',
            'phone': '33 839 50 50',
            'email': 'contact@hopitalprincipal.sn',
            'location': Point(-17.4576861, 14.706677)
        },
        {
            'name': 'Centre Hospitalier Abass Ndao',
            'address': 'Rue 10, Abass Ndao',
            'city': 'Dakar',
            'region': 'Dakar',
            'phone': '33 849 30 30',
            'email': 'contact@chan.sn',
            'location': Point(-17.4476861, 14.696677)
        },
        {
            'name': 'Hôpital Aristide Le Dantec',
            'address': 'Avenue Pasteur, Dakar',
            'city': 'Dakar',
            'region': 'Dakar',
            'phone': '33 839 60 60',
            'email': 'contact@le-dantec.sn',
            'location': Point(-17.4776861, 14.686677)
        },
        {
            'name': 'Centre Hospitalier de Grand Yoff',
            'address': 'Grand Yoff, Dakar',
            'city': 'Dakar',
            'region': 'Dakar',
            'phone': '33 869 10 10',
            'email': 'contact@chgy.sn',
            'location': Point(-17.4676861, 14.726677)
        },
    ]
    
    for center_data in dakar_centers:
        # Vérifier si le centre existe déjà
        if not BloodDonationCenter.objects.filter(name=center_data['name']).exists():
            # Créer le centre
            center = BloodDonationCenter.objects.create(**center_data)
            print(f"Centre créé : {center.name}")
            
            # Créer des entrées d'inventaire pour chaque groupe sanguin
            blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            for blood_type in blood_types:
                from random import randint
                center.inventory.create(
                    blood_type=blood_type,
                    quantity_ml=randint(0, 5000),  # Quantité aléatoire entre 0 et 5000 ml
                    minimum_required_ml=2000  # 2L par défaut
                )
            print(f"  - Inventaire créé pour {center.name}")
        else:
            print(f"Le centre {center_data['name']} existe déjà")

if __name__ == "__main__":
    setup_django()
    create_blood_centers()
