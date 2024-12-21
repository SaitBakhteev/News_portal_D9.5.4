"""
Django settings for djangoProject_News_Portal project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from dotenv import load_dotenv, find_dotenv  # импорт компонентов
# для защиты персональных данных и секртных ключей в файле .env
from pathlib import Path

load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # добавки
    'django.contrib.sites', 'django.contrib.flatpages',
    'django_filters',
    'news_portal.apps.NewsPortalConfig',
    'crispy_forms',
    'sign', 'protect',  # приложения для авторизации
    'django_apscheduler',  # планировщик заданий

    # добавки allauth
    'allauth', 'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.google',

]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # добавка
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # добавка allauth
    'allauth.account.middleware.AccountMiddleware',

    #ДОБАВКИ ПО КЭШУ
    # Они кэшируют абсолютно все страницы проекта, что в нашем случае не очень приемлемо, поскольку проект обновляются
    # постоянно обновляется новыми постами, сами посты тоже могут подвергаться редактированию и т.п. и т.п. Поэтому
    # здесь нижеприведенные добавки оставлены для демонсатрации, но закоментированы для дезактивации

    # 'django.middleware.cache.UpdateCacheMiddleware',  # Должно быть первым. Он записывает в кэш HTTP-ответ после обработки представления
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # Должно быть последним. При поступлении запроса, он сначала произваодит поиск
    # уже имеющегося кэша по отвенту на этот запрос. Если кэш найден, то пропускает обработку запроса

]

ROOT_URLCONF = 'djangoProject_News_Portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # это исходная настройка
        # 'DIRS': [],
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

# добавления AUTHENTICATION_BACKENDS после установки пакета allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

WSGI_APPLICATION = 'djangoProject_News_Portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        #настройки при использовании postgres
        # 'ENGINE': 'django.db.backends.postgresql', # при использовании postgres,
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT'),
        # 'USER': os.getenv('DB_USER'),
        # 'NAME': os.getenv('DB_NAME'),
        # 'PASSWORD': os.getenv('DB_PASSWORD')
        # #
            # Настройки при использовании sqlite
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'DB_django',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_DIRS = [BASE_DIR / 'static']

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# добавки для рассылки почты
EMAIL_HOST = 'smtp.yandex.ru'  # ажрес сервера яндекс почты
EMAIL_PORT = 465  # ПОРТ smtp серврера
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True  # ЯНДЕКС ИСПОЛЬЗУЕТ SSL, ПОЭТОМУ НУЖНО УСТАНАВЛИВАТЬ True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # установка отправки уведомлений на почтовый сервер
EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'  # установка отправки уведомлений на консоль


DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
# MANAGERS = ('test@example.ru,stepler@laxap.ru')

# добавки по авторизации
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # требуется верификация e-mail для первого входа в систему
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True

# настройки для того, чтобы при регистарции пользователь
# автоматически добавлялся в группу "common"
ACCOUNT_FORMS = {'signup': 'sign.models.CommonSignupForm'}
SOCIALACCOUNT_FORMS = {'signup': 'sign.models.SocialCommonSignupForm'}
SOCIALACCOUNT_AUTO_SIGNUP = False # эта настройка важна, чтобы
    #SOCIALACCOUNT_FORMS ссылался на ту форму, которую указали выше

# добавки по celery и redis
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#------- КЭШ ------------
CACHES = {'default':
              {'BACKEND':'django.core.cache.backends.filebased.FileBasedCache',
               'LOCATION': os.path.join(BASE_DIR, 'cache_files'),  # здесь указывается директория для кэшируемых файлов
               'OPTIONS': {'MAX_ENTRIES':1}}}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60  # здесь задается время жизни кэша
CACHE_MIDDLEWARE_KEY_PREFIX = 'news_portal'  # необязательный параметр, который определяет разделение ключей для указанного приложения

SOCIALACCOUNT_PROVIDERS = {'yandex':
                               {'APP':
                                    {'client_id':os.environ.get('YANDEX_CLIEND_ID'),
                                     'secret':os.environ.get('YANDEX_SECRET'),
                                     'key':'',}
                                },
                           }# токены для oauth яндекс

# добавки по FRONTEND
X_FRAME_OPTIONS='SAMEORIGIN'

# формат даты, которую будет воспринимать наш задачник (вспоминаем модуль по фильтрам)
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"

# # если задача не выполняется за 25 секунд, то она автоматически снимается, можете поставить время побольше, но как правило, это сильно бьёт по производительности сервера
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds