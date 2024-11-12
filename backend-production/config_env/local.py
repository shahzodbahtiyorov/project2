import os

from dotenv import dotenv_values

from config_env.base import BASE_DIR

config = dotenv_values('.env')
SECRET_KEY = config.get('Credentials', 'SECRET_KEY')
DEBUG = config.get('Credentials', 'DEBUG')

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': f'django.db.backends.{os.environ.get("DB_ENGINE")}',
            'NAME': os.environ.get("DB_NAME"),
            'USER': os.environ.get("DB_USER"),
            'PASSWORD': os.environ.get("DB_PASSWORD"),
            'HOST': os.environ.get("DB_HOST"),
            'PORT': os.environ.get("DB_PORT"),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

ALLOWED_HOSTS = ['*']
