from django.apps import AppConfig
import sys


class TempleAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'temple_app'

    def ready(self):
        # Auto-run migrations on server startup so SQLite tables (like VisitorLog) always exist
        if any(cmd in sys.argv[0] for cmd in ['gunicorn', 'manage.py', 'wsgi']):
            try:
                from django.core.management import call_command
                call_command('migrate', interactive=False)
            except Exception:
                pass

