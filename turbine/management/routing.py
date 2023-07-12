from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("turbine/", consumers.TurbineConsumer.as_asgi()),
]
