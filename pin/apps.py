from django.apps import AppConfig


class PinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pin'
    def ready(self):
      import pin.signals