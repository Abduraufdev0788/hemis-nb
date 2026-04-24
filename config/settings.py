import os
from pathlib import Path

# Loyihaning asosiy papkasi
BASE_DIR = Path(__file__).resolve().parent.parent

# Xavfsizlik kaliti (Production'da almashtiriladi)
SECRET_KEY = 'django-insecure-maxfiy-kalit-shu-yerda-boladi'

DEBUG = True

ALLOWED_HOSTS = ['*']

# O'rnatilgan ilovalar
INSTALLED_APPS =[
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Uchinchi tomon kutubxonalari
    'rest_framework',

    # O'zimiz yaratgan app'lar
    'users',
    'attendance',
]

# Oraliq dasturlar (Login, xavfsizlik va sessiyalar uchun majburiy)
MIDDLEWARE =[
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# HTML qoliplar sozlamalari
TEMPLATES =[
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':[os.path.join(BASE_DIR, 'templates')], # Templatelar shu papkadan olinadi
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':[
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Ma'lumotlar bazasi
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Parol xavfsizligi
AUTH_PASSWORD_VALIDATORS =[
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Til va Vaqt sozlamalari
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Statik fayllar (CSS, JS, Rasmlar)
STATIC_URL = 'static/'
STATICFILES_DIRS =[os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ================= MAXSUS SOZLAMALAR =================

# Custom User Modelimizni tizimga tanitamiz
AUTH_USER_MODEL = 'users.CustomUser'

# Login marshrutlari
LOGIN_REDIRECT_URL = 'dashboard_redirect'
LOGIN_URL = 'login'

# Telegram Bot Token (O'zingiznikiga almashtiring)
TELEGRAM_BOT_TOKEN = '8729937214:AAFHODgB4MOh15DSI0mnPydsxTA_NsB3f-A'