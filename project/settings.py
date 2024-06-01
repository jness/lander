"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-9_ias6c81ss99=if)c6*_l%##%pteu)(gv0bh*5vq*kr!trw&o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# application hosts multiple sites
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["http://django-tacos.com", "http://django-burgers.com"]

# Toggle to enable one time password
OTP_ENABLED = True

# Enable running schedules using cron
CRON_SCHEDULES = True
CRON_SCHEDULES_PATH = '/app'
CRON_SCHEDULES_RUN_AS = 'root'  # change me!
CRON_SCHEDULES_WITH_SUDO = False

# ChatGPT API Token for management/commands/create_ai_article.py
#OPENAI_API_KEY = 'sk-.........'

# Application definition

PRIMARY_SITE = 1
SITE_ID = int(PRIMARY_SITE)

INSTALLED_APPS = [
    # jazzmin admin ui theme
    "jazzmin",
    # base django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd party apps
    "colorfield",
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
    "rest_framework",
    "rest_framework.authtoken",
    "django_summernote",
    # our app
    "app",
]

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "lux",
    "button_classes": {
        "primary": "btn-dark btn-sm",
        "secondary": "btn-secondary btn-sm",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

JAZZMIN_SETTINGS = {
    "show_ui_builder": False,
    "site_brand": "Administrator",
    "custom_css": "/app/css/jazzmin.css",
    "custom_js": "/app/js/jazzmin.js",

    "show_sidebar": True,

    # sidebar ordering
    "order_with_respect_to": [
        "auth",
        "auth.user",
        "auth.group",
        "otp_totp",
        "authtoken",
        "django_summernote",
        "sites",
        "app",
        "app.template",
        "app.landing",
        "app.article",
        "app.tag",
        "app.articlebot",
        "app.contact",
        "app.schedule",
        "app.schedulelog",
    ],

    # sidebar icons
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "sites.site": "fas fa-sitemap",
        "app.landing": "fas fa-plane",
        "app.template": "fas fa-hashtag",
        "app.article": "fas fa-file",
        "app.tag": "fas fa-tag",
        "app.articlebot": "fas fa-robot",
        "app.contact": "fas fa-comment",
        "app.schedule": "fas fa-clock",
        "app.schedulelog": "fas fa-glasses",
        "authtoken.tokenproxy": "fas fa-key",
        "otp_totp.totpdevice": "fas fa-lock",
        "django_summernote.attachment": "fas fa-image"
    },
}

SUMMERNOTE_CONFIG = {
    'summernote': {
        'width': '100%',

        'attachment_require_authentication': True,

        # Toolbar customization
        # https://summernote.org/deep-dive/#custom-toolbar-popover
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture']],
            ['view', ['fullscreen', 'codeview']],
        ]
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissions'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication'
    ]
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # django otp middleware
    'django_otp.middleware.OTPMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # django site middleware
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    # our app middlewarer
    "app.middleware.SiteMiddleware"
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [ BASE_DIR / 'templates' ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "app.context_processors.otp_enabled",
                "app.context_processors.site_id",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Determine if we use postgres or sqlite.
# Make sure to install psycopg2 if you use postgres
if os.getenv('POSTGRES_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': os.getenv('POSTGRES_PORT'),
        }
    }
else:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = [
    "app.authentication_backends.TOTPModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'staticfiles'),
)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Logging

if not os.path.exists('logs'):
    try:
        os.makedirs('logs/')
    except:
        print('Failed to create logging directory')

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s.%(module)s] - %(message)s'
        }
    },
    "handlers": {
        "console": {
            "level": "WARN",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "WARN",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/debug.log",
            "maxBytes": 25 * 1024 * 1024,  # 25 MB
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "WARN",
            "propagate": True,
        },
    },
}

# load override settings
_dir = os.path.dirname(os.path.abspath(__file__))
_file = os.path.join(_dir, 'settings_local.py')
if os.path.exists(_file):
    from .settings_local import *
