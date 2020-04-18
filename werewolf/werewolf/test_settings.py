import os

from werewolf.settings import *  # noqa
from werewolf.settings import BASE_DIR

SECRET_KEY = "TestSecretKey"


DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
        }
}
