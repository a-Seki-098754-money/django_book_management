from django.apps import AppConfig


class BookManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_management'
    
    def ready(self):
        import book_management.signals
