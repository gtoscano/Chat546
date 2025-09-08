
# main/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import main.routing  # Replace 'main' with your project name if different

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

application = ProtocolTypeRouter({
    # Routes HTTP requests to Django's ASGI application
    "http": get_asgi_application(),
    # Routes WebSocket requests to the Channels routing
    "websocket": AuthMiddlewareStack(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})
