from api import settings

# SHINA_URL = settings.dotenv_config.get('SHINA_URL')
# SHINA_PASSWORD = settings.dotenv_config.get('SHINA_PASSWORD')
# SHINA_USERNAME = settings.dotenv_config.get('SHINA_USERNAME')

SHINA_URL = 'http://10.0.10.250:25153/'
SHINA_PASSWORD = '1'
SHINA_USERNAME = 'bosh135'


SMS_URL = settings.dotenv_config.get('SMS_URL')
SMS_TOKEN = settings.dotenv_config.get('SMS_TOKEN')
MEANING_URL_FERNET_KEY = settings.dotenv_config.get('MEANING_URL_FERNET_KEY')

UZCARD_URL = settings.dotenv_config.get('UZCARD_URL')
UZCARD_TOKEN = settings.dotenv_config.get('UZCARD_TOKEN')

HUMO_URL = settings.dotenv_config.get('HUMO_URL')
HUMO_TOKEN = settings.dotenv_config.get('HUMO_TOKEN')

FIREBASE_URL = settings.dotenv_config.get('FIREBASE_URL')
FIREBASE_SCOPE = settings.dotenv_config.get('FIREBASE_SCOPE')
ADMIN_URL = settings.dotenv_config.get('DJANGO_ADMIN_URL', 'admin')

MY_ID_GRANT_TYPE = settings.dotenv_config.get('MY_ID_GRANT_TYPE')
MY_ID_CLIENT_ID = settings.dotenv_config.get('MY_ID_CLIENT_ID')
MY_ID_CLIENT_SECRET_KEY = settings.dotenv_config.get('MY_ID_CLIENT_SECRET_KEY')
MY_ID_URL = settings.dotenv_config.get('MY_ID_URL')

EGOV_BASE_URL = settings.dotenv_config.get('EGOV_BASE_URL')
EGOV_TOKEN = settings.dotenv_config.get('EGOV_TOKEN')

METIN_URL = settings.dotenv_config.get('METIN_URL')
CARD_NUMBER_FERNET_KEY = settings.dotenv_config.get('CARD_NUMBER_FERNET_KEY')
