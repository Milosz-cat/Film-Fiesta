from django.apps import AppConfig


class BaseConfig(AppConfig):
    """
    Configuration for the 'base' Django application. Additionally, it imports signals from the
    `list_management` module when the application is ready.

    Methods:
        ready(): Imports signals from the `list_management` module when the application is
        initialized.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "base"

    def ready(self):
        import list_management.signals
