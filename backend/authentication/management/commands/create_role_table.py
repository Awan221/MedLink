from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

class Command(BaseCommand):
    help = 'Crée la table des rôles et insère les rôles par défaut'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            # Créer la table authentication_role
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authentication_role (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Insérer les rôles par défaut
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

            current_time = timezone.now()
            for role_name, role_display in roles:
                cursor.execute("""
                    INSERT INTO authentication_role (name, description, created_at, updated_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING;
                """, [role_name, f'Rôle de {role_display}', current_time, current_time])
                self.stdout.write(self.style.SUCCESS(f'Rôle "{role_display}" créé avec succès')) 