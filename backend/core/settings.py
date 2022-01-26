"""
Django version 4.0.1
"""

from pathlib import Path

from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

# Env.
ENV_PATH = BASE_DIR.joinpath('.env')
env = Env()
env.read_env(str(ENV_PATH))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG_MODE')

ALLOWED_HOSTS = ('127.0.0.1',)


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'src.accounts.apps.AccountsConfig',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates')
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
DATABASE_NAME = env.str('DATABASE_NAME')
DATABASE_USER = env.str('DATABASE_USER')
DATABASE_PASSWORD = env.str('DATABASE_PASSWORD')
DATABASE_HOST = env.str('DATABASE_HOST')
DATABASE_PORT = env.str('DATABASE_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': DATABASE_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

# Media files.
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentications.
AUTHENTICATION_BACKENDS = (
    'src.accounts.backends.EmailCaseInsensitiveAndPasswordBackendAuthentication',
    'src.accounts.backends.UsernameCaseInsensitiveAndPasswordBackendAuthentication',
)
AUTH_USER_MODEL = 'accounts.User'

USER_USERNAME_MINIMUM_LENGTH = 3
USER_USERNAME_MAXIMUM_LENGTH = 32
USER_USERNAME_VALID_FIRST_SYMBOL_REGEX = r'^[a-zA-Z_]$'
USER_USERNAME_VALID_CHARACTERS_REGEX = r'^[a-zA-Z_0-9]*$'
