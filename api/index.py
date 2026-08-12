import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carrental.settings")

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

application = get_wsgi_application()

call_command("migrate", interactive=False, verbosity=0)