from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter


from django.conf.urls import url

from mishipay.core import consumers

websocket_urlpatterns = [
    url(r'^chat/$', consumers.ChatConsumer),
]

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})