import os.path
from decouple import config

# form error message override
from django.forms import Field, EmailField
from django.utils.translation import ugettext_lazy
Field.default_error_messages = {
    'required': ugettext_lazy("To pole jest wymagane."),
}
EmailField.default_error_messages = {
	'invalid': ugettext_lazy("Wprowadź poprawny adres e-mail.")
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

DEBUG_PROPAGATE_EXCEPTIONS = True


ALLOWED_HOSTS = ['goldenscreen.pythonanywhere.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
	'repertoire.apps.RepertoireConfig',
	'library.apps.LibraryConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'social_django',
    'django_extensions',
    'django_google_maps',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'goldenscreen.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'goldenscreen.context_processors.cinema_list',
                'goldenscreen.context_processors.cinemas_geolocation'
            ],
			
			'libraries':{
                'admin_tags': 'repertoire.templatetags.admin_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'goldenscreen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files
STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = ( os.path.join('static'), )

# Media files 

MEDIA_ROOT = ''

MEDIA_URL = '/media/'

MEDIAFILES_DIRS = ( os.path.join('media'), )

# Redirect links

LOGIN_REDIRECT_URL = 'repertoire:mainPage'
LOGIN_URL = 'login'
LOGOUT_URL = 'logout'


# Authentication

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
	'account.authentication.EmailAuthBackend',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
]

SOCIAL_AUTH_FACEBOOK_KEY = config('FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = config('FACEBOOK_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('GOOGLE_SECRET')

GOOGLE_MAPS_API_KEY = 'AIzaSyBNoFllG6lCPzjxe02ySghBDEc90bxsAOo'