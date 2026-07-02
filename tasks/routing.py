from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/projects/<int:pk>/", consumers.ProjectConsumer.as_asgi()),
]