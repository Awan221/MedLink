import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
from dotenv import load_dotenv
import os

GDAL_LIBRARY_PATH = r"E:\OSGeo4W\bin\gdal310.dll"  # Mets ici le chemin exact vers ta DLL GDAL
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production

# --- Configuration email (Mailtrap) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'sandbox.smtp.mailtrap.io')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 2525))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ['true', '1', 'yes']
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Configuration OpenRouter
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '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')
CHATBOT_MODEL = os.getenv('CHATBOT_MODEL', 'meta-llama/llama-3-70b-instruct')
CHATBOT_MAX_TOKENS = int(os.getenv('CHATBOT_MAX_TOKENS', '1000'))
CHATBOT_TEMPERATURE = float(os.getenv('CHATBOT_TEMPERATURE', '0.7'))

# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',  # Nécessaire pour les champs géographiques
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_yasg',
    'debug_toolbar',
    'django_extensions',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Local apps
    'authentication',
    'patients',
    'dicom',              # Application DICOM pour la téléradiologie
    'bloodbank',          # Application pour la gestion de la banque de sang
    'chatbot',
    'public_api',
    'notifications',
    'imaging',
    'blood_donation',
    'ai_diagnostic',
    'blood_bank',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'chatbot.chatbot_auth_middleware.ChatbotAuthMiddleware',
]

# Configuration CORS
CORS_ALLOW_ALL_ORIGINS = False  # Désactiver pour une meilleure sécurité
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Autoriser les credentials (cookies, en-têtes d'autorisation)
CORS_ALLOW_CREDENTIALS = True

# Configuration CSRF
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()
CSRF_COOKIE_HTTPONLY = False  # Nécessaire pour que le frontend puisse lire le cookie CSRF
CSRF_COOKIE_SECURE = False    # Mettre à True en production avec HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'  # ou 'None' si vous utilisez HTTPS
CSRF_USE_SESSIONS = False     # Utiliser des cookies CSRF au lieu des sessions
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_NAME = 'csrftoken'

# Autoriser les méthodes HTTP
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Autoriser les en-têtes
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Configuration pour les requêtes avec credentials
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()
CSRF_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
CSRF_COOKIE_HTTPONLY = False  # Nécessaire pour les requêtes AJAX
SESSION_COOKIE_SECURE = False  # Mettre à True en production avec HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'  # ou 'None' si vous utilisez HTTPS

# Configuration des fichiers statiques et médias
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, '..', 'frontend', 'dist'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'orthanc_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/chatbot.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'chatbot': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuration Orthanc
ORTHANC_URL = "http://localhost:8042"
ORTHANC_USERNAME = "admin"  # Remplacez par vos identifiants Orthanc
ORTHANC_PASSWORD = "admin"  # Remplacez par votre mot de passe Orthanc

# Créer les dossiers nécessaires s'ils n'existent pas
os.makedirs(MEDIA_ROOT, exist_ok=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Par défaut, l'authentification est requise
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT settings

# URL du frontend pour les liens dans les emails
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8080')

# Multi-DB router pour les patients

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_EXPIRATION_DELTA', 7))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY', SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_COOKIE': 'access_token',  # Nom du cookie pour stocker le token
    'AUTH_COOKIE_SECURE': False,    # En production, mettre à True pour HTTPS
    'AUTH_COOKIE_HTTP_ONLY': True,  # Empêche l'accès au cookie via JavaScript
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Protection contre les attaques CSRF
}

# CORS settings
# Configuration CORS pour le développement
# En production, définir CORS_ALLOW_ALL_ORIGINS = False et spécifier les origines autorisées
CORS_ALLOW_ALL_ORIGINS = True  # À désactiver en production
CORS_ALLOW_CREDENTIALS = True

# Liste des origines autorisées (utilisée si CORS_ALLOW_ALL_ORIGINS = False)
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:8081',
    'http://127.0.0.1:8081',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Méthodes HTTP autorisées
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# En-têtes HTTP autorisés
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-csrftoken',
    'x-xsrf-token',
]

# Cookies autorisés dans les requêtes cross-origin
CORS_ALLOW_CREDENTIALS = True

# Durée de mise en cache des pré-vérifications CORS (en secondes)
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 heures

# Custom user model
AUTH_USER_MODEL = 'authentication.User'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Celery settings
CELERY_BROKER_URL = f"redis://{os.getenv('REDIS_HOST')}:{os.getenv('REDIS_PORT')}/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# Configuration Orthanc (Téléradiologie)
ORTHANC_URL = os.getenv('ORTHANC_URL', 'http://localhost:8042')
ORTHANC_USERNAME = os.getenv('ORTHANC_USERNAME', 'orthanc')
ORTHANC_PASSWORD = os.getenv('ORTHANC_PASSWORD', 'orthanc')

# Configuration de la banque de sang
MIN_BLOOD_QUANTITY_ALERT = int(os.getenv('MIN_BLOOD_QUANTITY_ALERT', '1000'))  # 1L par défaut

# Configuration du chatbot
CHATBOT_DEFAULT_MODEL = 'meta-llama/llama-3-70b-instruct'
CHATBOT_MAX_TOKENS = 1000
CHATBOT_TEMPERATURE = 0.7

# Configuration des permissions par défaut
DEFAULT_PERMISSIONS = {
    'bloodbank': {
        'view_bloodbank': ['medecin', 'infirmier', 'admin'],
        'manage_bloodbank': ['admin', 'responsable_banque_sang'],
    },
    'dicom': {
        'view_dicom': ['medecin', 'radiologue', 'admin'],
        'upload_dicom': ['medecin', 'radiologue', 'admin'],
    },
}

# Configuration de la géolocalisation
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
DEFAULT_COUNTRY = 'SN'  # Code pays par défaut (Sénégal)

# Configuration du frontend
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8080')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@medlink.sn')

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'imaging': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'urllib3': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# AllAuth settings
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Configuration Allauth
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = ['email']