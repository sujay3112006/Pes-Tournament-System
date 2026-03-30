"""Auctions App Serializers"""
from rest_framework import serializers
from apps.auctions.models import Auction, AuctionBid
from django.utils import timezone
from datetime import timedelta


class AuctionBidSerializer(serializers.Serializer):
    """Serializer for auction bids."""
    bid_id = serializers.CharField(read_only=True)
    auction_id = serializers.CharField(read_only=True)
    bidder_id = serializers.CharField(read_only=True)
    bidder_username = serializers.CharField(read_only=True)
    bid_amount = serializers.IntegerField(read_only=True)
    bid_time = serializers.DateTimeField(read_only=True)


class AuctionListSerializer(serializers.Serializer):
    """Serializer for listing auctions."""
    auction_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    player_username = serializers.CharField(read_only=True)
    player_image_url = serializers.URLField(read_only=True, allow_null=True)
    starting_bid = serializers.IntegerField(read_only=True)
    current_bid = serializers.IntegerField(read_only=True, allow_null=True)
    highest_bidder_username = serializers.CharField(read_only=True, allow_null=True)
    total_bids = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    time_remaining = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def get_time_remaining(self, obj):
        """Calculate time remaining in auction."""
        now = timezone.now()
        if now >= obj.end_time:
            return 0
        remaining = (obj.end_time - now).total_seconds()
        return max(0, int(remaining))


class AuctionDetailSerializer(serializers.Serializer):
    """Serializer for detailed auction view."""
    auction_id = serializers.CharField(read_only=True)
    tournament_id = serializers.CharField(read_only=True)
    player_id = serializers.CharField(read_only=True)
    player_username = serializers.CharField(read_only=True)
    player_rating = serializers.CharField(read_only=True, allow_null=True)
    player_image_url = serializers.URLField(read_only=True, allow_null=True)
    starting_bid = serializers.IntegerField(read_only=True)
    current_bid = serializers.IntegerField(read_only=True, allow_null=True)
    highest_bidder_id = serializers.CharField(read_only=True, allow_null=True)
    highest_bidder_username = serializers.CharField(read_only=True, allow_null=True)
    total_bids = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)
    time_remaining = serializers.SerializerMethodField(read_only=True)
    min_next_bid = serializers.SerializerMethodField(read_only=True)
    recent_bids = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def get_time_remaining(self, obj):
        """Calculate time remaining in auction."""
        now = timezone.now()
        if now >= obj.end_time:
            return 0
        remaining = (obj.end_time - now).total_seconds()
        return max(0, int(remaining))
    
    def get_min_next_bid(self, obj):
        """Calculate minimum next bid amount."""
        if obj.current_bid:
            # Minimum increment is 10% or 10 coins, whichever is higher
            increment = max(10, int(obj.current_bid * 0.1))
            return obj.current_bid + increment
        return obj.starting_bid
    
    def get_recent_bids(self, obj):
        """Get last 5 bids on this auction."""
        bids = AuctionBid.objects(auction_id=obj.auction_id).order_by('-bid_time')[:5]
        return AuctionBidSerializer(bids, many=True).data


class StartAuctionSerializer(serializers.Serializer):
    """Serializer for starting an auction."""
    player_id = serializers.CharField(required=True)
    player_username = serializers.CharField(required=True)
    starting_bid = serializers.IntegerField(min_value=1, required=True)
    duration_minutes = serializers.IntegerField(min_value=5, max_value=1440, default=60)
    player_rating = serializers.CharField(required=False, allow_blank=True)
    player_image_url = serializers.URLField(required=False, allow_blank=True)
    
    def validate_starting_bid(self, value):
        """Validate starting bid."""
        if value < 100:
            raise serializers.ValidationError("Starting bid must be at least 100 coins.")
        if value > 1000000:
            raise serializers.ValidationError("Starting bid cannot exceed 1,000,000 coins.")
        return value
    
    def validate_duration_minutes(self, value):
        """Validate auction duration."""
        if value < 5:
            raise serializers.ValidationError("Auction duration must be at least 5 minutes.")
        if value > 1440:  # 24 hours
            raise serializers.ValidationError("Auction duration cannot exceed 24 hours.")
        return value


class PlaceBidSerializer(serializers.Serializer):
    """Serializer for placing a bid."""
    bid_amount = serializers.IntegerField(required=True)
    
    def validate_bid_amount(self, value):
        """Validate bid amount."""
        if value < 1:
            raise serializers.ValidationError("Bid amount must be positive.")
        return value


class AuctionUpdateSerializer(serializers.Serializer):
    """Serializer for updating auction status."""
    status = serializers.ChoiceField(
        choices=['pending', 'live', 'sold', 'unsold', 'cancelled'],
        required=True
    )
    
    def validate_status(self, value):
        """Validate status transition."""
        # Add validation logic for status transitions if needed
        return value


class AuctionStatsSerializer(serializers.Serializer):
    """Serializer for user auction statistics."""
    total_auctions = serializers.IntegerField()
    active_auctions = serializers.IntegerField()
    completed_auctions = serializers.IntegerField()
    total_bids_placed = serializers.IntegerField()
    items_won = serializers.IntegerField()
    total_coins_spent = serializers.IntegerField()
