# Chatbot Médical - Documentation de l'API

Ce document fournit une documentation complète pour l'API du chatbot médical intégrant le modèle Llama 3.3 70B Instruct via OpenRouter.

## Configuration requise

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- Clé API OpenRouter valide

## Installation

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

2. Configurer les variables d'environnement dans `.env` :
   ```
   OPENROUTER_API_KEY=votre_cle_api
   CHATBOT_MODEL=meta-llama/llama-3-70b-instruct
   CHATBOT_MAX_TOKENS=1000
   CHATBOT_TEMPERATURE=0.7
   ```

3. Appliquer les migrations :
   ```bash
   python manage.py migrate
   ```

## Points de terminaison de l'API

### 1. Envoyer un message au chatbot

**Endpoint** : `POST /api/chatbot/request/`

**Paramètres** :

| Paramètre  | Type   | Requis | Description                                   |
|------------|--------|--------|-----------------------------------------------|
| session_id | string | Non    | ID de session existant (optionnel)            |
| message    | string | Oui    | Message de l'utilisateur                      |


**Exemple de requête** :
```json
{
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "Bonjour, j'ai mal à la tête"
}
```

**Réponse réussie (200 OK)** :
```json
{
    "session_id": "123e4567-e89b-12d3-a456-426614174000",
    "message_id": 42,
    "response": "Bonjour ! Je suis désolé d'apprendre que vous avez mal à la tête..."
}
```

### 2. Soumettre un feedback sur une réponse

**Endpoint** : `POST /api/chatbot/feedback/`

**Paramètres** :

| Paramètre  | Type    | Requis | Description                                   |
|------------|---------|--------|-----------------------------------------------|
| message_id | integer | Oui    | ID du message auquel le feedback s'applique   |
| rating     | integer | Oui    | Note de 1 à 5 étoiles                        |
| comment    | string  | Non    | Commentaire optionnel                         |

**Exemple de requête** :
```json
{
    "message_id": 42,
    "rating": 5,
    "comment": "Réponse très utile, merci !"
}
```

## Gestion des erreurs

L'API renvoie les codes d'état HTTP suivants :

- **200 OK** : Requête traitée avec succès
- **400 Bad Request** : Données de requête invalides
- **401 Unauthorized** : Authentification requise
- **404 Not Found** : Ressource non trouvée
- **500 Internal Server Error** : Erreur serveur

## Journalisation

Les logs sont enregistrés dans `backend/logs/chatbot.log` avec les niveaux suivants :
- DEBUG : Informations détaillées pour le débogage
- INFO : Événements importants du système
- WARNING : Événements inattendus mais non critiques
- ERROR : Échecs d'opérations
- CRITICAL : Erreurs critiques nécessitant une intervention

## Sécurité

- Toutes les requêtes doivent être faites via HTTPS
- L'authentification est requise pour les opérations sensibles
- Les données sensibles (comme les clés API) ne sont jamais incluses dans les réponses

## Développement

Pour exécuter les tests :
```bash
python manage.py test chatbot.tests
```

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
