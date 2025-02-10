import os
from django.core.wsgi import get_wsgi_application

# Point to settings.py inside 'financialweb' app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financialweb.settings')

application = get_wsgi_application()
