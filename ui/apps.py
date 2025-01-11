#pylint: disable=C0114,W0612,C0115,C0116
from django.apps import AppConfig


class UiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ui'
