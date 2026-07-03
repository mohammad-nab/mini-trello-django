import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer


class ProjectConsumer(WebsocketConsumer):
    def connect(self):
        project_id = self.scope["url_route"]["kwargs"]["project_id"]
        self.group_name = f"project_{project_id}"
        async_to_sync(self.channel_layer.group_add)(self.group_name,self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        event_type = text_data_json.get("type")

        if event_type == "task_created":
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                text_data_json
            )

    def create_task(self, event):
        self.send(text_data=json.dumps({
            "type": "task_created",
            "task_id": event["task_id"],
            "title": event["title"],
            "column_id": event["column_id"],
            "assigned_to": event["assigned_to"],
            "order": event["order"],
        }))
