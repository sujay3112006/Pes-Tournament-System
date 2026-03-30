"""Auctions App URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.auctions.views import AuctionViewSet, AuctionBidViewSet

router = DefaultRouter()
router.register(r'auctions', AuctionViewSet, basename='auction')
router.register(r'bids', AuctionBidViewSet, basename='auction-bid')

urlpatterns = [
    path('', include(router.urls)),
]
