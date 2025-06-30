# Synchronisation Multi-Base Patients — MedLink

## Objectif
Permettre la gestion et la synchronisation automatique des dossiers patients entre une base régionale (locale) et une base centrale (nationale), pour garantir la cohérence et la disponibilité des données sur tout le territoire.

---

## 1. Architecture technique

- **Deux bases configurées dans `settings.py`** :
  - `default` (centrale)
  - `regionale` (locale)
- **Router Django personnalisé** (`patients/db_router.py`) :
  - Toutes les opérations du module `patients` (lecture, écriture, migration) sont faites sur la base régionale par défaut.
- **Synchronisation automatique** :
  - À chaque création, modification ou suppression d’un patient, l’opération est répliquée dans la base centrale (`default`) via le serializer ou la vue.

---

## 2. Fonctionnement du flux patient

- **Création** :
  - Un patient créé sur la régionale est automatiquement dupliqué dans la centrale (avec tous ses champs).
  - Un `medical_id` unique est généré automatiquement si non fourni.
- **Modification** :
  - Toute modification sur la régionale est répercutée dans la centrale (synchronisation champ à champ).
- **Suppression** :
  - La suppression d’un patient sur la régionale entraîne la suppression de la fiche correspondante dans la centrale.

---

## 3. Limites connues et points d’attention

- **Conflits** :
  - Si un patient est modifié simultanément sur deux bases, la dernière écriture l’emporte (pas de résolution automatique de conflit).
  - Pas d’alerte ou de verrouillage en cas de conflit détecté.
- **Synchronisation asynchrone** :
  - Si la centrale est indisponible, la synchronisation échouera silencieusement (à améliorer avec du logging ou une file d’attente).
- **Permissions** :
  - Les opérations sont soumises aux permissions DRF (rôles médecin, spécialiste, etc.).

---

## 4. Bonnes pratiques et recommandations

- **Toujours utiliser l’API MedLink** pour créer/modifier/supprimer les patients (ne pas manipuler directement les bases).
- **Vérifier la cohérence des données** régulièrement entre régionale et centrale (scripts d’audit ou vues d’admin).
- **Documenter les cas d’usage métier** (ex : patient transféré d’une région à une autre).
- **Prévoir une évolution** vers une gestion des conflits plus fine (timestamp, logs, alertes admin).

---

## 5. Exemple de configuration (settings.py)

```python
DATABASES = {
    'default': {  # Centrale
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'central_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'regionale': {  # Régionale
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'region_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
DATABASE_ROUTERS = ['patients.db_router.PatientsRouter']
```

---

## 6. Pour aller plus loin

- Ajouter du logging et des alertes en cas d’échec de synchronisation.
- Mettre en place une file d’attente (ex : Celery) pour les opérations hors-ligne.
- Étendre la synchronisation à d’autres modules (dossiers médicaux, prescriptions, etc.).
- Prévoir une interface d’audit et de résolution des conflits pour les administrateurs régionaux et nationaux.
