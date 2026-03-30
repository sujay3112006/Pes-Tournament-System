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
    path('tournaments/<str:tournament_id>/auctions/start/', StartAuctionView.as_view(), name='start_auction'),
    path('tournaments/<str:tournament_id>/auctions/', TournamentAuctionsView.as_view(), name='tournament_auctions'),
    path('auctions/active/', ActiveAuctionsView.as_view(), name='active_auctions'),
    path('auctions/<str:auction_id>/', AuctionDetailView.as_view(), name='auction_detail'),
    
    # Bidding
    path('auctions/<str:auction_id>/bid/', PlaceBidView.as_view(), name='place_bid'),
    path('auctions/<str:auction_id>/bids/', AuctionBidHistoryView.as_view(), name='bid_history'),
    
    # Stats
    path('auctions/stats/<str:user_id>/', UserAuctionStatsView.as_view(), name='user_auction_stats'),
]
