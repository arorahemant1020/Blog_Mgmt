from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/blog/$', consumers.BlogConsumer.as_asgi()),
    re_path(r'ws/blog/post/(?P<post_id>\d+)/$', consumers.PostConsumer.as_asgi()),
]
