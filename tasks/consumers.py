import json
from channels.generic.websocket import WebsocketConsumer


class ProjectConsumer(WebsocketConsumer):
    def connect(self):
        print("WebSocket connected")
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        self.send(text_data=json.dumps({
            "message": "Hello from Django!"
        }))