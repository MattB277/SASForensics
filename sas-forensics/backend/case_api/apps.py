from django.apps import AppConfig

class CaseApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'case_api'

    def ready(self):
        import case_api.signals
