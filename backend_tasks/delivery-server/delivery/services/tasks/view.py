import logging

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from delivery.models import Task, TaskStatusEnum
from delivery.services.tasks.serializer import TaskSerializer


class TasksAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TaskSerializer
    model = Task

    def get_queryset(self):
        """
        This method is used to filter the tasks based on the status and sort_by query parameters. Default sorting is by updated_at.
        status: TaskStatusEnum
        sort_by: title, due_date, status
        """
        status = self.request.query_params.get('status')
        sort_by = self.request.query_params.get('sort_by')
        queryset = Task.objects.all().order_by("updated_at")
        if status and status in TaskStatusEnum.values:
            queryset = queryset.filter(status=status)
        if sort_by in ["title", "due_date", "status"]:
            queryset = queryset.order_by(sort_by)
        return queryset

