from django.apps import AppConfig

class ListManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'list_management'

    def ready(self):
        import list_management.signals