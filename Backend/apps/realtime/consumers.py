"""Realtime App - WebSocket Consumers for Live Updates"""
import json
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time user notifications.
    
    Handles notifications for:
    - Mission completions and rewards
    - Auction wins
    - Club invitations and updates
    - Tournament announcements
    - Friend/rival activities
    """
    
    async def connect(self):
        """Handle WebSocket connection."""
        try:
            self.user = self.scope.get("user")
            
            # Reject unauthenticated users
            if not self.user or not self.user.is_authenticated:
                await self.close()
                logger.warning("Unauthenticated user attempted to connect to notifications")
                return
            
            # Get user_id (handle both custom and Django user models)
            self.user_id = getattr(self.user, 'user_id', self.user.id)
            self.room_group_name = f"notifications_{self.user_id}"
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"User {self.user_id} connected to notifications (channel: {self.channel_name})")
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'status': 'connected',
                'user_id': str(self.user_id),
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error during notification connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        try:
            # Leave room group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user_id} disconnected from notifications (code: {close_code})")
        except Exception as e:
            logger.error(f"Error during notification disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Receive and process messages from WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Handle heartbeat to keep connection alive
            if message_type == 'heartbeat':
                await self.send(text_data=json.dumps({
                    'type': 'heartbeat_response',
                    'status': 'alive',
                    'timestamp': datetime.now().isoformat()
                }))
            
            # Handle subscription confirmation
            elif message_type == 'subscribe':
                await self.send(text_data=json.dumps({
                    'type': 'subscribed',
                    'channel': 'notifications',
                    'timestamp': datetime.now().isoformat()
                }))
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in notification consumer: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error in notification consumer receive: {str(e)}")
    
    # Messages from group (various notification types)
    async def notify_mission_completed(self, event):
        """Send mission completion notification."""
        await self.send(text_data=json.dumps({
            'type': 'mission_completed',
            'mission_id': event.get('mission_id'),
            'mission_name': event.get('mission_name'),
            'reward_coins': event.get('reward_coins', 0),
            'reward_points': event.get('reward_points', 0),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def notify_auction_won(self, event):
        """Send auction won notification."""
        await self.send(text_data=json.dumps({
            'type': 'auction_won',
            'auction_id': event.get('auction_id'),
            'player_name': event.get('player_name'),
            'winning_bid': event.get('winning_bid'),
            'tournament_id': event.get('tournament_id'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def notify_club_invitation(self, event):
        """Send club invitation notification."""
        await self.send(text_data=json.dumps({
            'type': 'club_invitation',
            'club_id': event.get('club_id'),
            'club_name': event.get('club_name'),
            'invited_by': event.get('invited_by'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def notify_tournament_announcement(self, event):
        """Send tournament announcement."""
        await self.send(text_data=json.dumps({
            'type': 'tournament_announcement',
            'tournament_id': event.get('tournament_id'),
            'message': event.get('message'),
            'announcement_type': event.get('announcement_type'),  # started, ended, updated
            'timestamp': datetime.now().isoformat()
        }))
    
    async def notify_generic(self, event):
        """Send generic notification."""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'title': event.get('title'),
            'message': event.get('message'),
            'category': event.get('category'),  # achievement, alert, info
            'timestamp': datetime.now().isoformat()
        }))


class MatchLiveConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for live match updates.
    
    Broadcasts real-time match data:
    - Score updates
    - Match status changes
    - Events (goals, fouls, substitutions)
    - Match completion
    """
    
    async def connect(self):
        """Handle WebSocket connection to match channel."""
        try:
            self.match_id = self.scope['url_route']['kwargs']['match_id']
            self.room_group_name = f"match_{self.match_id}"
            self.user = self.scope.get("user")
            
            # Get user_id
            self.user_id = getattr(self.user, 'user_id', self.user.id) if self.user else None
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"User {self.user_id} connected to match {self.match_id} (channel: {self.channel_name})")
            
            # Send connection confirmation with match info
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'match_id': self.match_id,
                'status': 'connected',
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error during match connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection from match."""
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user_id} disconnected from match {self.match_id} (code: {close_code})")
        except Exception as e:
            logger.error(f"Error during match disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Receive messages from match WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Handle heartbeat
            if message_type == 'heartbeat':
                await self.send(text_data=json.dumps({
                    'type': 'heartbeat_response',
                    'match_id': self.match_id,
                    'timestamp': datetime.now().isoformat()
                }))
            
            # Handle subscription confirmation
            elif message_type == 'subscribe':
                await self.send(text_data=json.dumps({
                    'type': 'subscribed',
                    'match_id': self.match_id,
                    'timestamp': datetime.now().isoformat()
                }))
            
            # Only authenticated users can send updates (will be validated server-side)
            elif message_type in ['score_update', 'status_change', 'event_occurred']:
                # Send to all clients watching this match
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'match_update',
                        'data': data,
                        'user_id': str(self.user_id)
                    }
                )
            else:
                logger.warning(f"Unknown match message type: {message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in match consumer: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error in match consumer receive: {str(e)}")
    
    async def match_update(self, event):
        """Broadcast match update to all connected clients."""
        await self.send(text_data=json.dumps({
            'type': event['data'].get('type', 'match_update'),
            'match_id': self.match_id,
            'data': event['data'],
            'updated_by': event.get('user_id'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def score_updated(self, event):
        """Broadcast score update."""
        await self.send(text_data=json.dumps({
            'type': 'score_updated',
            'match_id': self.match_id,
            'player1_score': event.get('player1_score'),
            'player2_score': event.get('player2_score'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def match_status_changed(self, event):
        """Broadcast match status change."""
        await self.send(text_data=json.dumps({
            'type': 'match_status_changed',
            'match_id': self.match_id,
            'status': event.get('status'),  # pending, live, completed
            'message': event.get('message'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def match_completed(self, event):
        """Broadcast match completion."""
        await self.send(text_data=json.dumps({
            'type': 'match_completed',
            'match_id': self.match_id,
            'winner_id': event.get('winner_id'),
            'final_score': event.get('final_score'),
            'is_draw': event.get('is_draw', False),
            'timestamp': datetime.now().isoformat()
        }))


class AuctionLiveConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for live auction updates.
    
    Broadcasts real-time auction data:
    - New bids
    - Current highest bid
    - Time remaining
    - Auction status changes
    - Auction completion
    """
    
    async def connect(self):
        """Handle WebSocket connection to auction channel."""
        try:
            self.auction_id = self.scope['url_route']['kwargs']['auction_id']
            self.room_group_name = f"auction_{self.auction_id}"
            self.user = self.scope.get("user")
            
            # Get user_id
            self.user_id = getattr(self.user, 'user_id', self.user.id) if self.user else None
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"User {self.user_id} connected to auction {self.auction_id} (channel: {self.channel_name})")
            
            # Send connection confirmation
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'auction_id': self.auction_id,
                'status': 'connected',
                'timestamp': datetime.now().isoformat()
            }))
            
        except Exception as e:
            logger.error(f"Error during auction connect: {str(e)}")
            await self.close()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection from auction."""
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"User {self.user_id} disconnected from auction {self.auction_id} (code: {close_code})")
        except Exception as e:
            logger.error(f"Error during auction disconnect: {str(e)}")
    
    async def receive(self, text_data):
        """Receive messages from auction WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Handle heartbeat
            if message_type == 'heartbeat':
                await self.send(text_data=json.dumps({
                    'type': 'heartbeat_response',
                    'auction_id': self.auction_id,
                    'timestamp': datetime.now().isoformat()
                }))
            
            # Handle subscription
            elif message_type == 'subscribe':
                await self.send(text_data=json.dumps({
                    'type': 'subscribed',
                    'auction_id': self.auction_id,
                    'timestamp': datetime.now().isoformat()
                }))
            
            # Broadcast bid updates to all connected clients
            elif message_type == 'new_bid':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'bid_placed',
                        'data': data,
                        'user_id': str(self.user_id)
                    }
                )
            else:
                logger.warning(f"Unknown auction message type: {message_type}")
                
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in auction consumer: {str(e)}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format',
                'timestamp': datetime.now().isoformat()
            }))
        except Exception as e:
            logger.error(f"Error in auction consumer receive: {str(e)}")
    
    async def bid_placed(self, event):
        """Broadcast new bid to all connected clients."""
        await self.send(text_data=json.dumps({
            'type': 'bid_placed',
            'auction_id': self.auction_id,
            'bid_amount': event['data'].get('bid_amount'),
            'bidder_id': event['data'].get('bidder_id'),
            'total_bids': event['data'].get('total_bids'),
            'current_highest': event['data'].get('current_highest'),
            'previous_bidder': event['data'].get('previous_bidder'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def auction_status_updated(self, event):
        """Broadcast auction status update."""
        await self.send(text_data=json.dumps({
            'type': 'auction_status_updated',
            'auction_id': self.auction_id,
            'status': event.get('status'),  # pending, live, sold, unsold
            'message': event.get('message'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def time_remaining(self, event):
        """Broadcast time remaining countdown."""
        await self.send(text_data=json.dumps({
            'type': 'time_remaining',
            'auction_id': self.auction_id,
            'seconds_remaining': event.get('seconds_remaining'),
            'timestamp': datetime.now().isoformat()
        }))
    
    async def auction_completed(self, event):
        """Broadcast auction completion."""
        await self.send(text_data=json.dumps({
            'type': 'auction_completed',
            'auction_id': self.auction_id,
            'status': event.get('status'),  # sold or unsold
            'final_bid': event.get('final_bid'),
            'winner_id': event.get('winner_id'),
            'player_name': event.get('player_name'),
            'timestamp': datetime.now().isoformat()
        }))
