"""
ASGI config for report_manager project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report_manager.settings')

application = get_asgi_application()


'''
[Unit]
Description=report_manager daemon
Requires=report_manager.socket
After=network.target

[Service]
User=rider
Group=www-data
WorkingDirectory=/home/rider/projects/report_manager
ExecStart=/home/rider/projects/oneklassenv/bin/gunicorn \
          --access-logfile - \
          -k uvicorn.workers.UvicornWorker \
          --workers 3 \
          --bind unix:/run/report_manager.sock \
          report_manager.asgi:application

[Install]
WantedBy=multi-user.target
'''