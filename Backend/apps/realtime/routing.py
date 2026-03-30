"""Realtime App - WebSocket URL Routing"""
from django.urls import re_path
from apps.realtime.consumers import NotificationConsumer, MatchLiveConsumer

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/matches/(?P<match_id>\w+)/$', MatchLiveConsumer.as_asgi()),
]
