import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from .serializers import MessageSerializer
from asgiref.sync import sync_to_async



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Приєднуємося до групи
        self.room_name = "chat_room"  # Назва кімнати
        self.room_group_name = f'chat_{self.room_name}'

        # Приєднання до групи
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Вихід з групи
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Отримання повідомлення від WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Зберігаємо повідомлення в базі
        await self.save_message(message)

        # Відправляємо повідомлення до групи
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Відправка повідомлення до WebSocket
    async def chat_message(self, event):
        message = event['message']

        # Відправка повідомлення через WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @sync_to_async
    def save_message(self, message):
        # Створюємо нове повідомлення в базі
        Message.objects.create(text=message, user=None)  # Можна додати користувача за потреби
