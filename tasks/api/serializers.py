from rest_framework import serializers
from tasks.models import Column


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["id", "title", "order"]