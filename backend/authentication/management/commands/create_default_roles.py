from django.core.management.base import BaseCommand
from authentication.models import Role

class Command(BaseCommand):
    help = 'Crée les rôles par défaut dans la base de données'

    def handle(self, *args, **kwargs):
        roles = [
            ('admin', 'Administrateur'),
            ('doctor', 'Médecin Généraliste'),
            ('specialist', 'Médecin Spécialiste'),
            ('nurse', 'Infirmier'),
            ('patient', 'Patient'),
            ('lab_technician', 'Technicien de laboratoire'),
            ('radiologist', 'Radiologue'),
            ('blood_bank_manager', 'Responsable de banque de sang'),
        ]

        for role_name, role_display in roles:
            Role.objects.get_or_create(
                name=role_name,
                defaults={
                    'description': f'Rôle de {role_display}'
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Rôle "{role_display}" créé avec succès')) 