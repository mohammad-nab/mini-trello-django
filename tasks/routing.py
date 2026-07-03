from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(r"ws/projects/<int:project_id>/", consumers.ProjectConsumer.as_asgi()),
]