from .base import *
import dj_database_url
from decouple import config

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = [config('RENDER_EXTERNAL_HOSTNAME', default='*')]

# Database
DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Cloudinary Media
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Security Headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
