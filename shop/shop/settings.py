from decouple import Config, Csv, RepositoryEnv
from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_FILEPATH = BASE_DIR.parent / '.env'


try:
    config_env = Config(RepositoryEnv(DOTENV_FILEPATH))
except FileNotFoundError:
    from decouple import config
    config_env = config


SECRET_KEY = config_env('SECRET_KEY')
DEBUG = config_env('DEBUG', cast=bool)
ALLOWED_HOSTS = config_env('ALLOWED_HOSTS', cast=Csv())
CSRF_TRUSTED_ORIGINS = config_env('CSRF_TRUSTED_ORIGINS', cast=Csv(), default='')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # дополнительные приложения

    'mptt',
    'django_bootstrap5',

    # свои приложения

    'accounts.apps.AccountsConfig',
    'product.apps.ProductConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'wishlist.apps.WishlistConfig',


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Свой middleware

    'accounts.middleware.ActiveUserMiddleware',

]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        'debug': DEBUG, # Удалить эту стрчоку
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config_env('DB_NAME'),
        'USER': config_env('DB_USER'),
        'PASSWORD': config_env('DB_PASSWORD'),
        'HOST': config_env('DB_HOST'),
        'PORT': config_env('DB_PORT'),

    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Свои дополнительные настройки



MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
CART_SESSION_ID = 'cart'
BROKER_URL = config_env('BROKER_URL')


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login'
AUTH_USER_MODEL = 'accounts.CustomUser'


#Мэйл данные

EMAIL_HOST = config_env('EMAIL_HOST')
EMAIL_HOST_USER = config_env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config_env('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config_env('EMAIL_PORT')
EMAIL_USE_TLS = config_env('EMAIL_USE_TLS')