from django.apps import AppConfig


class MiddleschoolConfig(AppConfig):
    name = 'middleschool'

    def ready(self):
        import middleschool.signals


