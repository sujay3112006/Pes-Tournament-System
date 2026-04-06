"""Auctions App URLs"""
from django.urls import path
from apps.auctions.views import (
    StartAuctionView,
    TournamentAuctionsView,
    ActiveAuctionsView,
    AuctionDetailView,
    PlaceBidView,
    AuctionBidHistoryView,
    UserAuctionStatsView,
)

urlpatterns = [
    # Auction CRUD
    path('tournament/<str:tournament_id>/start/', StartAuctionView.as_view(), name='start_auction'),
    path('tournament/<str:tournament_id>/', TournamentAuctionsView.as_view(), name='tournament_auctions'),
    path('active/', ActiveAuctionsView.as_view(), name='active_auctions'),
    path('<str:auction_id>/', AuctionDetailView.as_view(), name='auction_detail'),
    
    # Bidding
    path('<str:auction_id>/bid/', PlaceBidView.as_view(), name='place_bid'),
    path('<str:auction_id>/bids/', AuctionBidHistoryView.as_view(), name='bid_history'),
    
    # Stats
    path('stats/<str:user_id>/', UserAuctionStatsView.as_view(), name='user_auction_stats'),
]
