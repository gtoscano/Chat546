# core/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class InterjectionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.interjection_id = self.scope['url_route']['kwargs']['interjection_id']
        self.group_name = f'interjection_{self.interjection_id}'

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    async def interjection_update(self, event):
        bot_response = event['bot_response']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'bot_response': bot_response
        }))

