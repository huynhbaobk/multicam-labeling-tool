"""
Django settings for gtmarker project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%z1g%^3%nf-k3sf$i^qra_d*0m4745c57f&(su(2=&nuwt#=z1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# ALLOWED_HOSTS = ['pedestriantag.epfl.ch']

# Application definition

INSTALLED_APPS = [
    'marker.apps.MarkerConfig',
    'gtm_hit.apps.Gtm_hitConfig',
    'home',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrapform',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'marker.middleware.RequireLoginMiddleware',
]
LOGIN_REQUIRED_URLS = (
    r'/marker/(.*)$',
)
LOGIN_REQUIRED_URLS_EXCEPTIONS = (
    r'/marker/login(.*)$',
    r'/marker/logout(.*)$',
)

LOGIN_URL = '/login/'

ROOT_URLCONF = 'gtmarker.urls'

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

WSGI_APPLICATION = 'gtmarker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'gtmarker',
#         'USER': 'admin',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'pedestriantag',
#         'USER': 'pedestriantag',
#         'PASSWORD': 'lAzyLift96',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
# STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static/'), )
# #STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_ROOT = os.path.join(BASE_DIR, "STATICROOT")
STATIC_URL = '/static/'

SAVES = '/labels/'

# Constants
#
# f_rect = open('./marker/static/marker/cst.txt', 'r')
# lines = f_rect.readlines()
# f_rect.close()
# NB_WIDTH = int(lines[2].split()[1])
# NB_HEIGHT = int(lines[3].split()[1])
# NB_RECT = NB_WIDTH * NB_HEIGHT
# MAN_RAY = float(lines[4].split()[1])
# MAN_HEIGHT = float(lines[5].split()[1])
# REDUCTION = float(lines[6].split()[1])
# NB_CAMS = int(lines[9].split()[1])

DELTA_SEARCH = 5

#TEMPLATES[0]['OPTIONS']['context_processors'].append("marker.context_processors.rectangles_processor")

try:
    rectangles_file = './marker/static/marker/rectangles.pom'#480x1440.pom'
    f_rect = open(rectangles_file, 'r')
    LINES = f_rect.readlines()
    f_rect.close()
    if LINES[0].split()[0] != "WIDTH":
        messagebox.showerror("Error","Incorrect file header")
    else:
        NB_WIDTH = int(LINES[2].split()[1])
        NB_HEIGHT = int(LINES[3].split()[1])
        NB_RECT = NB_WIDTH * NB_HEIGHT
        MAN_RAY = float(LINES[4].split()[1])
        MAN_HEIGHT = float(LINES[5].split()[1])
        REDUCTION = float(LINES[6].split()[1])
        NB_CAMS = int(LINES[9].split()[1])
        # NB_CAMS = 2

        incr = 0
        test = []
        FIND_RECT = [[{} for _ in range(2913)] for _ in range(NB_CAMS)]
        RECT = [{} for _ in range(NB_CAMS)]
        for line in LINES[10:]:
            l = line.split()
            cam = int(l[1])
            id_rect = int(l[2])
            if l[3] != "notvisible":
                a, b, c, d = l[3:]
                a = int(a)
                b = int(b)
                c = int(c)
                d = int(d)
                ratio = 180/(d-b)
                if d < 5000:
                    if abs(c - a) < abs(d - b):
                        if cam < NB_CAMS:
                            RECT[cam][id_rect] = (a, b, c, d,ratio)
                            FIND_RECT[cam][d][(a + c) // 2] = id_rect
except FileNotFoundError:
        print("Error: Rectangle file not found")

VALIDATIONCODES = []
STARTFRAME = 0
NBFRAMES = 18000
UNLABELED = list(range(0,NBFRAMES,10))
LASTLOADED = 0

SERVER_PATH = "/home/baohuynh/baohuynh/multicam/dataset/Wildtrack/Image_subsets/"
CAMS = []
for i in range(NB_CAMS):
    CAMS.append("C" + str(i+1) + "/")

