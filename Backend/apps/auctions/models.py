"""Auctions App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, URLField, DynamicField
from datetime import datetime
import uuid


class Auction(Document):
    """Player auction model."""
    auction_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    tournament_id = StringField(required=True)
    player_id = StringField(required=True)  # Reference to User.user_id
    player_username = StringField(required=True)
    starting_bid = IntField(required=True)
    current_bid = IntField()
    highest_bidder_id = StringField(blank=True, null=True)  # Reference to User.user_id
    highest_bidder_username = StringField(blank=True, null=True)
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    status = StringField(choices=['pending', 'live', 'sold', 'unsold', 'cancelled'], default='pending')
    player_rating = StringField(blank=True)
    player_image_url = URLField(blank=True)
    total_bids = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'auctions',
        'indexes': ['auction_id', 'tournament_id', 'player_id', 'status'],
    }
    
    def __str__(self):
        return f"Auction: {self.player_username} - {self.current_bid} coins ({self.status})"


class AuctionBid(Document):
    """Individual bid on auction."""
    bid_id = StringField(unique=True, required=True, default=lambda: str(uuid.uuid4()))
    auction_id = StringField(required=True)
    bidder_id = StringField(required=True)  # Reference to User.user_id
    bidder_username = StringField(required=True)
    bid_amount = IntField(required=True)
    bid_time = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'auction_bids',
        'indexes': ['auction_id', 'bidder_id', 'bid_time'],
    }
    
    def __str__(self):
        return f"{self.bidder_username} bid {self.bid_amount} coins"
