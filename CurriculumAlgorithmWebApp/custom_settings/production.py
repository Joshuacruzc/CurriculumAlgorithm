import django_heroku

from ..settings import *

STATIC_ROOT = 'staticfiles'
DEBUG = DEBUG
DEBUG = False
django_heroku.settings(locals())
