from dotenv import dotenv_values
from io import StringIO

with open('/unired-business/.env', 'rt') as f:
    content = f.read()
    dotenv_config = dotenv_values(stream=StringIO(content))

ALLOWED_HOSTS = eval(dotenv_config.get('ALLOWED_HOSTS'))
DEBUG = dotenv_config.get('DEBUG')
SECRET_KEY = dotenv_config.get('SECRET_KEY')
GW_UNIPOS_TOKEN = dotenv_config.get('GW_UNIPOS_TOKEN')

CSRF_TRUSTED_ORIGINS = [
    'https://gw.cloudgate.uz',
    'https://unired-business-test.cloudgate.uz',
    'https://unired-msb.cloudgate.uz'

]

CORS_ORIGIN_WHITELIST = [
    'http://localhost:5173',
    'http://localhost:63342',
    'http://192.168.14.47:5173',
    'https://unired-msb.cloudgate.uz'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': dotenv_config.get('POSTGRES_MASTER_HOST'),
        'NAME': dotenv_config.get('POSTGRES_DATABASE'),
        'USER': dotenv_config.get('POSTGRES_USERNAME'),
        'PASSWORD': dotenv_config.get('POSTGRES_PASSWORD'),
        'PORT': dotenv_config.get('POSTGRES_MASTER_PORT'),
        'OPTIONS': {
            'application_name': 'unired-business-backend-django',
            'connect_timeout': 10,
        },
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': dotenv_config.get('POSTGRES_REPLICA_HOST'),
        'NAME': dotenv_config.get('POSTGRES_DATABASE'),
        'USER': dotenv_config.get('POSTGRES_USERNAME'),
        'PASSWORD': dotenv_config.get('POSTGRES_PASSWORD'),
        'PORT': dotenv_config.get('POSTGRES_REPLICA_PORT'),
        'OPTIONS': {
            'application_name': 'unired-business-backend-django',
            'connect_timeout': 10,
        },
    }
}
MINIO_ENDPOINT = dotenv_config.get('CDN_URL')
if MINIO_ENDPOINT is None:
    print("MINIO_ENDPOINT is not set. .env content:")
MINIO_REGION = dotenv_config.get('CDN_REGION')
MINIO_ACCESS_KEY = dotenv_config.get('CDN_ACCESS_KEY')
MINIO_SECRET_KEY = dotenv_config.get('CDN_SECRET_KEY')
MINIO_USE_HTTPS = True
MINIO_PUBLIC_BUCKETS = [
    'bucket-1',
]
DEFAULT_FILE_STORAGE = 'django_minio_backend.models.MinioBackend'
STATICFILES_STORAGE = 'django_minio_backend.models.MinioBackendStatic'
MINIO_MEDIA_FILES_BUCKET = 'bucket-1'
MINIO_STATIC_FILES_BUCKET = 'bucket-1'

EMAIL_BACKEND = dotenv_config.get('EMAIL_BACKEND')
EMAIL_HOST = dotenv_config.get('EMAIL_HOST')
EMAIL_PORT = dotenv_config.get('EMAIL_PORT')
EMAIL_HOST_USER = dotenv_config.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = dotenv_config.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = dotenv_config.get('DEFAULT_FROM_EMAIL')

ADMIN_URL = dotenv_config.get('DJANGO_ADMIN_URL', 'admin')

CELERY_TIMEZONE = 'UTC'
# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# This configures Redis as the datastore between Django + Celery
CELERY_BROKER_URL = dotenv_config.get('CELERY_BROKER_REDIS_URL')
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{dotenv_config.get('REDIS_HOST')}:{dotenv_config.get('REDIS_DB')}",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
