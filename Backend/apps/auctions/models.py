"""Auctions App Models"""
from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField, URLField
from datetime import datetime


class Auction(Document):
    """Player auction model."""
    auction_id = StringField(unique=True, required=True)
    player_id = StringField(required=True)
    player_name = StringField(required=True)
    tournament_id = StringField(required=True)
    starting_bid = IntField(required=True)
    current_bid = IntField()
    highest_bidder_id = StringField()
    highest_bidder_name = StringField()
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    status = StringField(choices=['pending', 'live', 'sold', 'unsold', 'cancelled'], default='pending')
    player_rating = StringField()
    player_image = URLField()
    created_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'auctions',
        'indexes': ['auction_id', 'player_id', 'tournament_id'],
    }
    
    def __str__(self):
        return f"Auction - {self.player_name}"


class AuctionBid(Document):
    """Bid on auction."""
    bid_id = StringField(unique=True, required=True)
    auction_id = StringField(required=True)
    bidder_id = StringField(required=True)
    bidder_name = StringField()
    bid_amount = IntField(required=True)
    bid_time = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'auction_bids',
        'indexes': ['auction_id', 'bidder_id'],
    }
    
    def __str__(self):
        return f"Bid - {self.bid_amount} by {self.bidder_name}"
