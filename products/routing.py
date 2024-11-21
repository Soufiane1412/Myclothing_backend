from django.urls import re_path
from . import consumers # Import the consumer that will handle websocket logic

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]