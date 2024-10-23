from drf_spectacular.utils import extend_schema_field

from delivery.models import Task, TaskStatusEnum
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
