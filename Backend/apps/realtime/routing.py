"""Realtime App - WebSocket URL Routing"""
from django.urls import re_path
from apps.realtime.consumers import (
    NotificationConsumer,
    MatchLiveConsumer,
    AuctionLiveConsumer
)

# WebSocket URL patterns for real-time features
websocket_urlpatterns = [
    # Notifications - user-specific channel
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi(), name='ws_notifications'),
    
    # Match live updates - match-specific channel
    re_path(r'ws/matches/(?P<match_id>[\w-]+)/$', MatchLiveConsumer.as_asgi(), name='ws_match_live'),
    
    # Auction live bidding - auction-specific channel
    re_path(r'ws/auctions/(?P<auction_id>[\w-]+)/$', AuctionLiveConsumer.as_asgi(), name='ws_auction_live'),
]
