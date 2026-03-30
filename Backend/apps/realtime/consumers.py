"""Realtime App - WebSocket Consumer and Routing"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import logging

logger = logging.getLogger(__name__)


class NotificationConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time notifications."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.user = self.scope["user"]
        self.room_name = f"user_{self.user.id}"
        self.room_group_name = f"notifications_{self.room_name}"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"User {self.user.id} connected to notifications")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"User {self.user.id} disconnected from notifications")
    
    async def receive(self, text_data):
        """Receive message from WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            # Handle different message types
            if message_type == 'heartbeat':
                await self.send(text_data=json.dumps({
                    'type': 'heartbeat_response',
                    'status': 'alive'
                }))
            elif message_type == 'subscribe':
                # Subscribe to specific channels
                pass
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {str(e)}")
    
    # Receive message from room group
    async def notification_message(self, event):
        """Send notification to WebSocket."""
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))


class MatchLiveConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for live match updates."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f"match_{self.match_id}"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        logger.info(f"Client connected to match {self.match_id}")
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"Client disconnected from match {self.match_id}")
    
    async def receive(self, text_data):
        """Receive message from WebSocket."""
        try:
            data = json.loads(text_data)
            event_type = data.get('type')
            
            # Broadcast to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'match_update',
                    'event': data
                }
            )
        except Exception as e:
            logger.error(f"Error in match WebSocket: {str(e)}")
    
    async def match_update(self, event):
        """Send match update to WebSocket."""
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['event']))
