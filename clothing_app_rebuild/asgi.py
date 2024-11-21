"""
ASGI config for clothing_app_rebuild project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
# Channels imports
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# django imports
from django.core.asgi import get_asgi_application
import products.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_app_rebuild.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(), # Handle HTTP requests
    'websocket': AuthMiddlewareStack( # Add websocket support
        URLRouter(
            products.routing.websocket_urlpatterns
        ),
    ),
})

