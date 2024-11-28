import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join notifications gorup
        await self.channel_layer.group_add(
            'notifications', # Group name
            self.order_updates # Unique channel name
        )
        await self.accept() # Accept websocket connection

    async def disconnect(self, close_code):
        # Leave notifications group
        await self.channel_layer.group_discard(
            'notifications',
            self.order_updates
        )
    async def send_notifications(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))