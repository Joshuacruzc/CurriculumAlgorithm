from django.conf import settings
from django.utils.module_loading import import_string
from rest_framework.permissions import BasePermission


def get_permission_class():
    return import_string(settings.REST_FRAMEWORK['REST_FRAMEWORK DEFAULT_PERMISSION_CLASSES'][0])


class ByPassAuthentication(BasePermission):

    def has_permission(self, request, view):
        return True
