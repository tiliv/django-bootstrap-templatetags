# -*- coding: utf-8 -*-

import warnings

from .settings import *


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Handle system warning as log messages
warnings.simplefilter("once")

for handler in LOGGING.get("handlers", []):
    LOGGING["handlers"][handler]["level"] = "CRITICAL"
for logger in LOGGING.get("loggers", []):
    LOGGING["loggers"][logger]["level"] = "CRITICAL"

DEFAULT_DB = DATABASES["default"]
if os.environ.get("DB_TYPE") == "sqlite":
    DEFAULT_DB = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}

DATABASES = {
    "default": DEFAULT_DB,
}

MEDIA_ROOT = "/tmp"

SILENCED_SYSTEM_CHECKS = ["django_mysql.E016"]

CELERY_TASK_ALWAYS_EAGER = CELERY_TASK_EAGER_PROPAGATES = True
CELERYD_HIJACK_ROOT_LOGGER = True

DJANGO_TEST_PROCESSES = 4
