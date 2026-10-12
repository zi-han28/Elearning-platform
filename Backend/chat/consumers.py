import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import ChatMessage
from django.utils import timezone
from courses.models import Course

# WebSocket chat consumer 
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['course_slug']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope.get('user', AnonymousUser())

        try:
            # Get course object
            self.course = await Course.objects.aget(slug=self.room_name)
            
            # Only allow authenticated users
            if isinstance(self.user, AnonymousUser):
                await self.close()
                return
                
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            
        except Course.DoesNotExist:
            await self.close()
        except Exception as e:
            print(f"Connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # save message data and broadcast 
        try:
            if not hasattr(self, 'user') or not hasattr(self, 'course'):
                return

            text_data_json = json.loads(text_data)
            message = text_data_json.get('message', '').strip()
            
            if not message:
                return

            # Save message to database
            await ChatMessage.objects.acreate(
                course=self.course,
                user=self.user,
                message=message,
                timestamp=timezone.now()
            )

            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username
                }
            )
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")

    # send message down 
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))