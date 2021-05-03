from django.apps import AppConfig


class CprofilesConfig(AppConfig):
    name = 'cprofiles'

    def ready(self):
        import cprofiles.signals