from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from conf.permissions import IsProjectOwnerOrReadOnly
from projects.models import Project
from tasks.models import Task , Column, ActivityLog
from .serializers import ColumnSerializer


class ColumnViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectOwnerOrReadOnly]
    serializer_class = ColumnSerializer

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project.objects.filter(
                Q(owner=request.user) | Q(projectmember__user=request.user)
            ).distinct(),
            pk=kwargs["project_pk"],
        )
        return super().dispatch(request, *args, **kwargs)

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