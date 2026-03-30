"""Auctions App Admin"""
from django.contrib import admin


@admin.register()
class AuctionAdmin(admin.ModelAdmin):
    """Auction admin configuration."""
    list_display = ('auction_id', 'player_name', 'current_bid', 'status')
    list_filter = ('status',)
    search_fields = ('auction_id', 'player_name')
