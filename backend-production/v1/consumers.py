import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.user_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.channel_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data is None:
            return

        try:
            text_data_json = json.loads(text_data)
            receiver_id = text_data_json.get('receiver_id')
            content = text_data_json.get('content')
            timestamp = text_data_json.get('timestamp')

            # Check if all necessary fields are present
            if receiver_id is None or content is None or timestamp is None:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid message format'
                }))
                return

            # Save message to the database
            sender = self.scope['user']  # Make sure to use the right attribute for user
            receiver = User.objects.get(id=receiver_id)
            message = Message(sender=sender, receiver=receiver, content=content, timestamp=timestamp)
            message.save()

            # Send message to the receiver's WebSocket
            await self.channel_layer.group_send(
                self.channel_name,
                {
                    'type': 'chat_message',
                    'sender': sender.username,
                    'content': content,
                    'timestamp': str(timestamp),
                }
            )
        except json.JSONDecodeError as e:
            await self.send(text_data=json.dumps({
                'error': 'Malformed JSON',
                'details': str(e)
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            }))

    async def chat_message(self, event):
        sender = event['sender']
        content = event['content']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'content': content,
            'timestamp': timestamp,
        }))
