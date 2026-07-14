from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from conf.permissions import IsProjectOwnerOrReadOnly
from projects.models import Project
from tasks.models import Task , Column, ActivityLog
from .serializers import ColumnSerializer, TaskSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]
    serializer_class = ColumnSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)  # runs authentication first
        self.project = get_object_or_404(
            Project.objects.filter(
                Q(owner=request.user) | Q(projectmember__user=request.user)
            ).distinct(),
            pk=kwargs["projects_pk"],
        )

    def get_queryset(self):
        return Column.objects.filter(project=self.project)

    def perform_create(self, serializer):
        column = serializer.save(project=self.project)
        ActivityLog.objects.create(
            user=self.request.user,
            project=self.project,
            activity_type="create-column",
            description=f'Created column "{column.title}"',
        )


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]
    serializer_class = TaskSerializer

    def initial(self, request, *args, **kwargs):
        self.format_kwarg = self.get_format_suffix(**kwargs)
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        self.perform_authentication(request)

        self.project = get_object_or_404(
            Project.objects.filter(
                Q(owner=request.user) | Q(projectmember__user=request.user)
            ).distinct(),
            pk=kwargs["projects_pk"],
        )
        self.column = get_object_or_404(
            Column,
            pk=kwargs["columns_pk"],
            project=self.project,
        )

        self.check_permissions(request)
        self.check_throttles(request)

    def get_queryset(self):
        return Task.objects.filter(column=self.column)

    def perform_create(self, serializer):
        task = serializer.save(column=self.column)
        ActivityLog.objects.create(
            user=self.request.user,
            project=self.project,
            activity_type="create-task",
            description=f'Created task "{task.title}" in column "{self.column.title}"',
        )

    def perform_update(self, serializer):
        task = serializer.save()
        ActivityLog.objects.create(
            user=self.request.user,
            project=self.project,
            activity_type="update-task",
            description=f'Updated task "{task.title}" in column "{self.column.title}"',
        )

    def perform_destroy(self, instance):
        title = instance.title
        column_title = self.column.title
        instance.delete()
        ActivityLog.objects.create(
            user=self.request.user,
            project=self.project,
            activity_type="delete-task",
            description=f'Deleted task "{title}" from column "{column_title}"',
        )