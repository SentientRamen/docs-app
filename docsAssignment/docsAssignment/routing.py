from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import docs.routing

application = ProtocolTypeRouter({
    # websocket middleware
    'websocket': AuthMiddlewareStack(
        URLRouter(
            docs.routing.websocket_urlpatterns
        )
    ),
})
