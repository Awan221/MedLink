import os
import django
import random

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

def create_blood_stocks():
    from bloodbank.models import BloodInventory, BloodDonationCenter
    
    # Tous les groupes sanguins possibles
    BLOOD_TYPES = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    
    # Niveaux de stock possibles (en ml)
    STOCK_LEVELS = {
        'critical': (0, 300),     # Stock critique : 0-300ml
        'low': (300, 1000),      # Stock bas : 300-1000ml
        'warning': (1000, 2000),  # Stock d'avertissement : 1000-2000ml
        'good': (2000, 5000)      # Bon stock : 2000-5000ml
    }
    
    # Pour chaque centre de don
    centers = BloodDonationCenter.objects.all()
    
    for center in centers:
        print(f"\nAjout de stocks pour le centre: {center.name}")
        
        # Pour chaque groupe sanguin
        for blood_type in BLOOD_TYPES:
            # Choisir un niveau de stock aléatoire (plus de chances d'avoir des stocks moyens/élevés)
            level = random.choices(
                ['critical', 'low', 'warning', 'good'],
                weights=[0.1, 0.2, 0.3, 0.4]  # Probabilités pour chaque niveau
            )[0]
            
            # Générer une quantité aléatoire dans la plage du niveau sélectionné
            min_qty, max_qty = STOCK_LEVELS[level]
            quantity = random.randint(min_qty, max_qty)
            
            # Créer ou mettre à jour l'entrée d'inventaire
            inventory, created = BloodInventory.objects.update_or_create(
                center=center,
                blood_type=blood_type,
                defaults={
                    'quantity_ml': quantity,
                    'minimum_required_ml': 2000  # 2L par défaut
                }
            )
            
            status = "créé" if created else "mis à jour"
            print(f"  - Stock {status} pour {blood_type}: {quantity}ml (niveau: {level})")

if __name__ == "__main__":
    print("Début de l'ajout des stocks de sang...")
    setup_django()
    create_blood_stocks()
    print("\nOpération terminée avec succès !")
