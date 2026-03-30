"""Auctions App Serializers"""
from rest_framework import serializers


class AuctionSerializer(serializers.Serializer):
    """Auction serializer."""
    auction_id = serializers.CharField(read_only=True)
    player_id = serializers.CharField()
    player_name = serializers.CharField()
    tournament_id = serializers.CharField()
    starting_bid = serializers.IntegerField()
    current_bid = serializers.IntegerField(read_only=True)
    highest_bidder_id = serializers.CharField(read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=['pending', 'live', 'sold', 'unsold', 'cancelled'])


class AuctionBidSerializer(serializers.Serializer):
    """Auction bid serializer."""
    bid_id = serializers.CharField(read_only=True)
    auction_id = serializers.CharField()
    bidder_id = serializers.CharField()
    bid_amount = serializers.IntegerField()
    bid_time = serializers.DateTimeField(read_only=True)
