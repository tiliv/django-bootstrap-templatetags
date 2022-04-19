# -*- coding: utf-8 -*-

import warnings

from .settings import *  # noqa: F403,F401

# Handle system warning as log messages
warnings.simplefilter("once")

for handler in LOGGING.get("handlers", []):
    LOGGING["handlers"][handler]["level"] = "CRITICAL"
for logger in LOGGING.get("loggers", []):
    LOGGING["loggers"][logger]["level"] = "CRITICAL"

mysql_db = DATABASES["default"]
DEFAULT_DB = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
    "TEST": {"MIGRATE": False},
}
if os.environ.get("DB_TYPE") == "mysql":
    print("Using MySQL Backend!")
    DEFAULT_DB = mysql_db

DATABASES = {
    "default": DEFAULT_DB,
}

MEDIA_ROOT = "/tmp"

SILENCED_SYSTEM_CHECKS = ["django_mysql.E016"]

CELERY_TASK_ALWAYS_EAGER = CELERY_TASK_EAGER_PROPAGATES = True
CELERYD_HIJACK_ROOT_LOGGER = True

DJANGO_TEST_PROCESSES = 4
