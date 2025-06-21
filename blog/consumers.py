import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class BlogConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('blog_updates', self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('blog_updates', self.channel_name)
    
    async def post_created(self, event):
        await self.send(text_data=json.dumps({
            'type': 'post_created',
            'data': event['message']
        }))

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.post_id = self.scope['url_route']['kwargs']['post_id']
        self.post_group_name = f'post_{self.post_id}'
        
        await self.channel_layer.group_add(self.post_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.post_group_name, self.channel_name)
    
    async def comment_added(self, event):
        await self.send(text_data=json.dumps({
            'type': 'comment_added',
            'data': event['message']
        }))
