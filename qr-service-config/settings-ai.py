import os
from pathlib import Path

from jaeger_client import Config
# OPENTRACING_TRACED_ATTRIBUTES = ['META']
import django_opentracing

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p!7lqn_38f8n*tav2jye@2l!y-h*n7ngy9q675zazm$dz2@q3='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # internal app:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # external apps:
    'apps.ai',

    # third party apps:
    'rest_framework',
    'django_opentracing'
]

MIDDLEWARE = [
    'django_opentracing.OpenTracingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'qr_utils.middlewares.ExceptionMiddleware',
]

ROOT_URLCONF = 'ai_machin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'qr_utils.CustomExceptionHandler.custom_exception_handler',
}
WSGI_APPLICATION = 'ai_machin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)

SC_URL = "https://qr-du-trading.aboitiz.net/security-service-1.0"

# AI_OFFLINE_MODE = True
AI_DEBUG_MODE = True
# AI_PROXY = "116.202.212.199:5902"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'django-error.log',
            'formatter': 'standard',
        }
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}

# OpenTracing settings

# if not included, defaults to True.
# has to come before OPENTRACING_TRACING setting because python...
OPENTRACING_TRACE_ALL = True
# Callable that returns an `opentracing.Tracer` implementation.
# OPENTRACING_TRACER_CALLABLE = 'django_opentracing.DjangoTracing()'

# OPENTRACING_TRACED_ATTRIBUTES = ['META']

config = Config(
    config={  # usually read from some yaml config
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'local_agent': {
            'reporting_host': '127.0.0.1',
            'reporting_port': '5775',
        },
        'logging': True
    },
    service_name='AI Machine',
    validate=True,
)
# this call also sets opentracing.tracer
tracer = config.initialize_tracer()
OPENTRACING_TRACING = django_opentracing.DjangoTracing(tracer)
