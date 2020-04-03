# docs/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import UserDocumentInfo, Document


class DocConsumer(WebsocketConsumer):

    # Initialize DocConsumer variables
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'doc_%s' % self.room_name

    # Connect to channel
    def connect(self):
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # Obtain updated viewing history
        message = self.get_viewing_history()

        # Broadcast viewing history
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'viewing_history'
            }
        )

        self.accept()

    # Disconnect from channel
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'message_type': 'ping'
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'message_type': event['message_type'],
        }))

    # Obtain viewing history for document
    def get_viewing_history(self):
        document = Document.objects.get(name=self.room_name)
        viewing_history = UserDocumentInfo.objects.filter(document=document)
        view_history_data = {}

        for i in viewing_history:
            view_history_data[i.user.username] = i.last_visited.strftime('%Y-%m-%d %H:%M')

        return view_history_data
