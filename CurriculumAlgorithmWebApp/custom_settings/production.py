import dj_database_url
import django_heroku

from ..settings import *

DEBUG = DEBUG
DEBUG = False
django_heroku.settings(locals())
DATABASES['default'] = dj_database_url.config()
