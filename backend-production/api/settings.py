import os
from pathlib import Path
from dotenv import dotenv_values
from config_env.base import *
import sentry_sdk

sentry_sdk.init(
    dsn="https://ae4ea8553bd235372e798cc4822dcc13@sentry.cloudgate.uz/6",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
)

DEBUG = False

PROJECT_CONFIG = config
APP_NAME = 'MSB'

if DEBUG:
    from config_env.local import *

else:
    from config_env.production import *

    INSTALLED_APPS.append('django_minio_backend.apps.DjangoMinioBackendConfig')
LOGS_DIR = BASE_DIR / 'logs'

if not LOGS_DIR.exists():
    LOGS_DIR.mkdir()

IDENTITY = 'UM'
RATE_MARGIN = 0.4

