from django.apps import AppConfig


class MprofilesConfig(AppConfig):
    name = 'mprofiles'

    def ready(self):
        import mprofiles.signals