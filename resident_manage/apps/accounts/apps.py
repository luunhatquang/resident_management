from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resident_manage.apps.accounts'

    def ready(self):
        import resident_manage.apps.accounts.signals