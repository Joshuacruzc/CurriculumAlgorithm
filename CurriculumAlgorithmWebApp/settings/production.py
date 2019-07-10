import django_heroku

from .settings import *

DEBUG = DEBUG
DEBUG = False
django_heroku.settings(locals())
