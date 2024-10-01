"""
ASGI config for Chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter ##new
import chat_room.routing
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Chat_app.settings')

asgi_application = get_asgi_application()


application = ProtocolTypeRouter({
	'http': asgi_application,
	'websocket':
	AllowedHostsOriginValidator(
		AuthMiddlewareStack(
			URLRouter(chat_room.routing.websocket_urlpatterns)
		),
	)
})