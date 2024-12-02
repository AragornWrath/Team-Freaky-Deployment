"""
ASGI config for Group_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# import home.routing
# home.routing.websocket_urlpatterns
from home import consumers
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Group_chat.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([re_path(r'all_trips/websocket', consumers.LikeConsumer.as_asgi()),
                   re_path(r'scheme', consumers.SchemeConsumer.as_asgi()),])
    )
})
