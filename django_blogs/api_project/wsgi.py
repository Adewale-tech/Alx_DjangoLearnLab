"""
<<<<<<< HEAD
WSGI config for api_project project.
=======
WSGI config for django_blog project.
>>>>>>> 23e1b6c04226f5007912c149b37799f2733dfcc2

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_blog.settings')
>>>>>>> 23e1b6c04226f5007912c149b37799f2733dfcc2

application = get_wsgi_application()
