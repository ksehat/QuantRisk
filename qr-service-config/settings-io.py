from pathlib import Path
from urllib.parse import urljoin

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
import os

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
    'apps.IOH',

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

ROOT_URLCONF = 'io_handler.urls'

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
WSGI_APPLICATION = 'io_handler.wsgi.application'

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

IOH_DB_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
# Settings for Proxy
IOH_HTTPS_PROXY = os.environ.get("IOH_HTTPS_PROXY", None)
IOH_HTTP_PROXY = os.environ.get("IOH_HTTP_PROXY", None)

IOH_PROXIES = {"http": IOH_HTTP_PROXY, "https": IOH_HTTPS_PROXY}

# API URL Settings
IOH_BASE_URL = os.environ.get("IOH_BASE_URL")

# Settings for SecurityCenter and Proxies
IOH_SC_URL = None
IOH_SC_METHOD = "post"
IOH_SC_USERNAME = None
IOH_SC_PASSWORD = None

IOH_SC_METHOD = None

IOH_VISUALIZATION_API_URL = urljoin(IOH_BASE_URL,
                                    "/etrm-rest-api/job-run-output/write")
IOH_VISUALIZATION_API_METHOD = "post"

IOH_RESULTS_API_URL = urljoin(IOH_BASE_URL, "/etrm-rest-api/base-data-curve/v-1/write/")
IOH_RESULTS_API_METHOD = "post"

IOH_STATUS_API_URL = urljoin(IOH_BASE_URL, "/etrm-rest-api/job-run-output/write")
IOH_STATUS_API_METHOD = "post"

IOH_OFFLINE_MODE = False

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
    service_name="IO Handler",
    validate=True,
)
# this call also sets opentracing.tracer
tracer = config.initialize_tracer()
OPENTRACING_TRACING = django_opentracing.DjangoTracing(tracer)
