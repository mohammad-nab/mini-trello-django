from rest_framework import serializers
from tasks.models import Column
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "column",
            "title",
            "description",
            "assigned_to",
            "order",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "column", "order", "created_at", "updated_at"]


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["id", "title", "order"]