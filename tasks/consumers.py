import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


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
        data = json.loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            data
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

    def move_task(self, event):
        self.send(text_data=json.dumps({
            "type": "move_task",
            "task_id": event["task_id"],
            "new_column_id": event["new_column_id"],
        }))