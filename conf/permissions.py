from projects.models import ProjectMember
from rest_framework.permissions import SAFE_METHODS, BasePermission


def is_project_member(user, project):
    return ProjectMember.objects.filter(user=user, project=project).exists()

def is_project_owner(user, project):
    return ProjectMember.objects.filter(user=user, project=project, role='owner').exists()

class IsProjectOwner(BasePermission):
    def has_object_permission(self, request, view, project):
        return project.owner == request.user


class IsProjectOwnerOrReadOnly(BasePermission):
    """
    Any project member can read (list/retrieve).
    Only the project owner can create/update/delete.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # view.project is set in dispatch() before permission checks run
        return view.project.owner_id == request.user.id