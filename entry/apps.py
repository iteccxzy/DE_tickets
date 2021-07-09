from django.apps import AppConfig


class EntryConfig(AppConfig):
    name = 'entry'

    def ready(self):
        import entry.signals
