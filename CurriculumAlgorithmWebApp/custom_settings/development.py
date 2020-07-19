from ..settings import *

DEBUG = True
REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = ()
REST_FRAMEWORK['REST_FRAMEWORK DEFAULT_PERMISSION_CLASSES'] = ('CurriculumAlgorithmWebApp.utils'
                                                               '.ByPassAuthentication',)
