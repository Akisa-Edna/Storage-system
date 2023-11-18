from django.apps import AppConfig


class AuthenticationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentications'

 
#imports the signals.py file for creating profiles
    def ready(self):
        import authentications.signals   
