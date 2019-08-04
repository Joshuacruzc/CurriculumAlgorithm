import dj_database_url
import django_heroku

from ..settings import *

DEBUG = False

ALLOWED_HOSTS = ['curriculum-algorithm.herokuapp.com', ]

django_heroku.settings(locals())

DATABASES['default'] = dj_database_url.config()
