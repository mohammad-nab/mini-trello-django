from projects.models import ProjectMember
from rest_framework import permissions


def is_project_member(user, project):
    return ProjectMember.objects.filter(user=user, project=project).exists()

def is_project_owner(user, project):
    return ProjectMember.objects.filter(user=user, project=project, role='owner').exists()

class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, project):
        return project.owner == request.user
